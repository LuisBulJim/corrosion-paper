import nbformat
import re
import concurrent.futures
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# --- Configuración ---
ROOT_DIR = "." 
OUTPUT_DIR = "translated_repo_full"
MAX_WORKERS = 5

# --- Compilación de Regex ---
# Detecta print("texto") o print('texto')
# Grupo 1: print("
# Grupo 2: el texto a traducir
# Grupo 3: ")
REGEX_PRINT = re.compile(r'(print\s*\(\s*["\'])(.*?)(["\']\s*\))')

# Detecta comentarios: busca un # y captura todo lo que sigue
# Nota: Esto es simplista. Si tienes una URL en un string "http://..." podría fallar.
# Para scripts de análisis de datos suele ser seguro.
REGEX_COMMENT = re.compile(r'(\#\s*)(.*)')

def translate_text_safe(text, translator):
    """Wrapper para manejar errores de red o textos vacíos"""
    if not text or not text.strip():
        return text
    try:
        # Evitamos traducir si parece código o rutas
        if text.startswith("http") or "/" in text: 
            return text
        return translator.translate(text)
    except:
        return text # Si falla, devuelve original (Fail-safe)

def process_code_source(source_code, translator):
    """
    Procesa el bloque de código línea por línea buscando prints y comentarios.
    """
    translated_lines = []
    lines = source_code.split('\n')
    
    for line in lines:
        new_line = line
        
        # 1. Intentar traducir comentarios
        comment_match = REGEX_COMMENT.search(new_line)
        if comment_match:
            # Separamos la parte de código del comentario
            # Ojo: esto asume que el # no está dentro de un string.
            # Un parser real (tokenize) sería más seguro pero mucho más lento/complejo.
            prefix = comment_match.group(1) # El "# "
            content = comment_match.group(2) # El texto del comentario
            
            # Solo traducimos si tiene letras (evitamos traducir "#####")
            if any(c.isalpha() for c in content):
                trans_content = translate_text_safe(content, translator)
                # Reconstruimos la línea reemplazando solo la parte del match
                # Usamos replace con count=1 para asegurar
                original_comment = prefix + content
                translated_comment = prefix + trans_content
                new_line = new_line.replace(original_comment, translated_comment, 1)

        # 2. Intentar traducir prints simples
        # Solo aplicamos si encontramos un print literal
        print_match = REGEX_PRINT.search(new_line)
        if print_match:
            prefix = print_match.group(1)   # print("
            content = print_match.group(2)  # contenido
            suffix = print_match.group(3)   # ")
            
            # Evitamos f-strings o variables interpoladas si se colaron
            if "{" not in content and "}" not in content:
                trans_content = translate_text_safe(content, translator)
                new_line = new_line.replace(
                    f"{prefix}{content}{suffix}", 
                    f"{prefix}{trans_content}{suffix}", 
                    1
                )
        
        translated_lines.append(new_line)
        
    return '\n'.join(translated_lines)

def translate_single_notebook(file_path, output_root):
    try:
        relative_path = file_path.relative_to(ROOT_DIR)
        output_path = Path(output_root) / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        nb = nbformat.read(file_path, as_version=4)
        translator = GoogleTranslator(source='auto', target='en')
        
        mod_count = 0
        
        for cell in nb.cells:
            # --- Celdas Markdown ---
            if cell.cell_type == 'markdown':
                if cell.source.strip():
                    cell.source = translate_text_safe(cell.source, translator)
                    mod_count += 1
            
            # --- Celdas de Código ---
            elif cell.cell_type == 'code':
                if cell.source.strip():
                    # Aquí entra la lógica quirúrgica
                    new_source = process_code_source(cell.source, translator)
                    if new_source != cell.source:
                        cell.source = new_source
                        mod_count += 1

        nbformat.write(nb, output_path)
        return f"✅ {file_path.name}: {mod_count} celdas tocadas."
        
    except Exception as e:
        return f"❌ Error en {file_path.name}: {e}"

def process_repository():
    root_path = Path(ROOT_DIR)
    all_notebooks = list(root_path.rglob("*.ipynb"))
    
    notebooks_to_process = [
        p for p in all_notebooks 
        if ".ipynb_checkpoints" not in p.parts 
        and OUTPUT_DIR not in p.parts
        and ".venv" not in p.parts
        and ".git" not in p.parts
    ]

    print(f"🚀 Procesando {len(notebooks_to_process)} notebooks (Markdown + Code Prints/Comments)...")

    # Bajamos un poco los workers porque ahora hacemos MAS peticiones por archivo
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_file = {
            executor.submit(translate_single_notebook, nb_path, OUTPUT_DIR): nb_path 
            for nb_path in notebooks_to_process
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            print(future.result())

if __name__ == "__main__":
    start = time.time()
    process_repository()
    print(f"🏁 Terminado en {time.time() - start:.2f}s")