from pathlib import Path
import yaml

CONFIG_PATH = Path("plugins.yml")
DOCS_DIR = Path("docs/plugins")


def get_modules(src_path, base_module):
    modules = []

    for py_file in src_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        rel = py_file.relative_to(src_path).with_suffix("")
        module_path = ".".join(rel.parts)

        modules.append(f"{base_module}.{module_path}")

    return modules


def read_markdown_files(plugin_root: Path, docs: list[str]) -> str:
    contents = []

    for doc in docs:
        doc_path = plugin_root / doc
        if doc_path.exists():
            contents.append(doc_path.read_text())
        else:
            print(f"[WARN] Missing doc file: {doc_path}")

    return "\n\n".join(contents)


def update_md_file(md_path: Path, modules: list[str], extra_md: str = ""):
    content = md_path.read_text() if md_path.exists() else ""

    # --- API блоки (как было) ---
    blocks = "\n\n".join(
        f"""::: {m}
    options:
      show_source: false
    """
        for m in modules
    )

    # --- Собираем итог ---
    parts = [content.strip()] if content else []

    if extra_md:
        parts.append(extra_md.strip())

    if blocks:
        parts.append(blocks)

    new_content = "\n\n".join(parts).strip() + "\n"

    md_path.write_text(new_content)
    print(f"[UPDATE] {md_path}")


def main():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    for plugin in config["plugins"]:
        name = plugin["name"]
        plugin_root = Path("plugins") / name

        all_modules = []

        # --- Поддержка нескольких модулей ---
        for module_entry in plugin.get("modules", []):
            module_name = module_entry.split(".")[0]
            src_path = plugin_root / module_entry.replace(".", "/")

            if src_path.exists():
                modules = get_modules(src_path, module_name)
                all_modules.extend(modules)
            else:
                print(f"[WARN] Missing module path: {src_path}")

        # --- Чтение md файлов ---
        extra_md = ""
        if "docs" in plugin:
            extra_md = read_markdown_files(plugin_root, plugin["docs"])

        md_file = DOCS_DIR / f"{name}.md"
        update_md_file(md_file, all_modules, extra_md)


if __name__ == "__main__":
    main()
