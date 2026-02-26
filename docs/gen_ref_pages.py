from pathlib import Path
import ast
import mkdocs_gen_files
import sys

SRC_PATH = Path("src")
DOCS_PATH = Path("")

sys.path.insert(0, str(SRC_PATH.resolve()))

def is_importable(module_name):
    """Проверяет, можно ли импортировать модуль"""
    try:
        __import__(module_name)
        return True
    except (ImportError, ModuleNotFoundError):
        return False

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    module_path = path.relative_to(SRC_PATH).with_suffix("")
    module_name = ".".join(module_path.parts)
    
    # Пропускаем если модуль не импортируется
    if not is_importable(module_name):
        continue

    doc_path = DOCS_PATH / module_path.with_suffix(".md")
    full_doc_path = Path("docs") / doc_path

    if full_doc_path.exists():
        continue

    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    if not ast.get_docstring(tree):
        continue

    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {module_path.name}\n\n")
        f.write(f"::: {module_name}\n")
