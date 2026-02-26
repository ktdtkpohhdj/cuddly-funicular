from pathlib import Path
import ast
import mkdocs_gen_files
import sys

SRC_PATH = Path("src")
DOCS_PATH = Path("")

sys.path.insert(0, str(SRC_PATH.resolve()))

# Проверяем наличие __init__.py во всех папках
def ensure_init_files():
    """Создаёт недостающие __init__.py файлы"""
    created = []
    for path in SRC_PATH.rglob("*"):
        if path.is_dir() and path != SRC_PATH:
            init_file = path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                created.append(path)
    if created:
        print(f"Created __init__.py in: {[str(p) for p in created]}")

# Создаём недостающие __init__.py
ensure_init_files()

# Теперь генерируем документацию для всех модулей с docstring
for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue
    
    # Получаем имя модуля
    rel_path = path.relative_to(SRC_PATH)
    module_name = ".".join(rel_path.with_suffix("").parts)
    
    # Проверяем docstring
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    if not ast.get_docstring(tree):
        continue
    
    # Генерируем документацию
    doc_path = DOCS_PATH / rel_path.with_suffix(".md")
    full_doc_path = Path("docs") / doc_path
    
    if full_doc_path.exists():
        continue
    
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {path.stem}\n\n")
        f.write(f"::: {module_name}\n")
