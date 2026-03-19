import yaml
from pathlib import Path
import re

CONFIG_PATH = Path("plugins.yml")
DOCS_DIR = Path("docs/plugins")

MKDOCS_BLOCK_PATTERN = re.compile(r":::.*")


def update_md_file(md_path: Path, module: str):
    """
    Обновляет или добавляет mkdocstrings блок в .md файл
    """

    if not md_path.exists():
        print(f"[WARN] File not found: {md_path}")
        return

    content = md_path.read_text()

    new_block = f"::: {module}"

    if "::: " in content:
        # заменяем существующий блок
        content = MKDOCS_BLOCK_PATTERN.sub(new_block, content)
        print(f"[UPDATE] {md_path}")
    else:
        # добавляем в конец
        content = content.strip() + f"\n\n{new_block}\n"
        print(f"[ADD] {md_path}")

    md_path.write_text(content)


def main():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    for plugin in config["plugins"]:
        name = plugin["name"]
        module = plugin["module"]

        md_file = DOCS_DIR / f"{name}.md"

        update_md_file(md_file, module)


if __name__ == "__main__":
    main()
