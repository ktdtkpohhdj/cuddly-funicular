from pathlib import Path
import ast
import mkdocs_gen_files

SRC_PATH = Path("src")
DOCS_PATH = Path("")  # генерируем прямо в docs/

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    module_path = path.relative_to(SRC_PATH).with_suffix("")
    module_name = ".".join(module_path.parts)
    doc_path = DOCS_PATH / module_path.with_suffix(".md")
    full_doc_path = Path("docs") / doc_path

    # Не перезаписываем существующие ручные md
    if full_doc_path.exists():
        continue

    # Проверяем наличие docstring
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    if not ast.get_docstring(tree):
        continue

    # Создаём md
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {module_path.name}\n\n")

        # Пытаемся вставить импорт через ::: только если модуль реально импортируется
        try:
            __import__(module_name)
            f.write(f"::: {module_name}\n")
        except ModuleNotFoundError:
            f.write(f"_Module could not be imported_\n")
