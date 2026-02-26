from pathlib import Path
import ast
import mkdocs_gen_files
import importlib.util
import sys

SRC_PATH = Path("src")
DOCS_PATH = Path("")  # генерируем прямо в docs/

# Добавляем src в sys.path, чтобы пакеты, которые есть, можно было импортировать
sys.path.insert(0, str(SRC_PATH.resolve()))

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    module_path = path.relative_to(SRC_PATH).with_suffix("")
    module_name = ".".join(module_path.parts)
    doc_path = DOCS_PATH / module_path.with_suffix(".md")
    full_doc_path = Path("docs") / doc_path

    # Сохраняем существующие ручные md
    if full_doc_path.exists():
        continue

    # Проверяем наличие docstring через AST
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    if not ast.get_docstring(tree):
        continue

    # Создаём md
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {module_path.name}\n\n")

        # Пытаемся вставить ::: module_name только если модуль реально импортируется
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                f.write(f"::: {module_name}\n")
            else:
                f.write("_Module could not be imported_\n")
        except ModuleNotFoundError:
            f.write("_Module could not be imported_\n")
