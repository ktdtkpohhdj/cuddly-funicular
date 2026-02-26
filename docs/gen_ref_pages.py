from pathlib import Path
import ast
import mkdocs_gen_files

SRC_PATH = Path("src")
DOCS_PATH = Path("")  # генерируем прямо в docs/ (корень)

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    # Модуль относительно src
    module_path = path.relative_to(SRC_PATH).with_suffix("")
    module_name = ".".join(module_path.parts)

    # Генерируем путь к md без reference
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

    # Создаём md для модуля
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {module_path.name}\n\n")
        f.write(f"::: {module_name}\n")

    # Создаём _index.md для всех родительских папок
    for i in range(1, len(module_path.parts)):
        parent = DOCS_PATH / Path(*module_path.parts[:i])
        parent_index = parent / "_index.md"
        if not mkdocs_gen_files.exists(parent_index):
            with mkdocs_gen_files.open(parent_index, "w") as f:
                f.write(f"# {module_path.parts[i-1]}\n")
