from pathlib import Path
import yaml

CONFIG_PATH = Path("plugins.yml")
DOCS_DIR = Path("docs/plugins")


def get_modules(src_path: Path, base_module: str) -> list[str]:
    modules = []

    if not src_path.exists():
        print(f"[WARN] Source path not found: {src_path}")
        return modules

    for py_file in src_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        rel = py_file.relative_to(src_path).with_suffix("")
        module_path = ".".join(rel.parts)

        modules.append(f"{base_module}.{module_path}")

    return modules


def build_api_blocks(modules: list[str]) -> str:
    return "\n\n".join(
        f"""## API: {m}

::: {m}
    options:
      show_source: false
"""
        for m in modules
    )


def build_markdown_blocks(plugin_root: Path, docs_list: list[str]) -> str:
    blocks = []

    for doc in docs_list:
        doc_path = plugin_root / doc

        if doc_path.exists():
            content = doc_path.read_text()
            blocks.append(f"## Docs: {doc}\n\n{content}")
        else:
            print(f"[WARN] Missing doc: {doc_path}")

    return "\n\n".join(blocks)


def main():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for plugin in config["plugins"]:
        name = plugin["name"]
        plugin_root = Path("plugins") / name
        md_file = DOCS_DIR / f"{name}.md"

        sections = []

        # --- API (modules) ---
        if "modules" in plugin:
            all_modules = []

            for module in plugin["modules"]:
                base_module = module.split(".")[0]
                src_path = plugin_root / plugin.get("src_path", "") / base_module

                modules = get_modules(src_path, base_module)
                all_modules.extend(modules)

            if all_modules:
                sections.append(build_api_blocks(all_modules))

        # --- Markdown docs ---
        if "docs" in plugin:
            md_blocks = build_markdown_blocks(plugin_root, plugin["docs"])
            if md_blocks:
                sections.append(md_blocks)

        # --- Write file ---
        final_content = "\n\n".join(sections).strip() + "\n"

        md_file.write_text(final_content)
        print(f"[GENERATED] {md_file}")


if __name__ == "__main__":
    main()
