from pathlib import Path
import ast
import mkdocs_gen_files

SRC_PATH = Path("src")
DOCS_REF_PATH = Path("reference")

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue

    module_path = path.relative_to(SRC_PATH).with_suffix("")
    module_name = ".".join(module_path.parts)

    doc_path = DOCS_REF_PATH / module_path.with_suffix(".md")

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
