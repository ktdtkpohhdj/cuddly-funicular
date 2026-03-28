from pathlib import Path
import yaml

CONFIG_PATH = Path("plugins.yml")
DOCS_DIR = Path("docs/plugins")


def build_api_blocks(modules: list[str]) -> str:
    blocks = []

    for m in modules:
        blocks.append(
            f"""### `{m}`

::: {m}
    options:
      show_source: false
"""
        )

    return "\n\n".join(blocks)


def build_markdown_blocks(plugin_root: Path, docs_list: list[str]) -> str:
    parts = []

    for doc in docs_list:
        doc_path = plugin_root / doc

        if doc_path.exists():
            content = doc_path.read_text()
            parts.append(content)
        else:
            print(f"[WARN] Missing doc: {doc_path}")

    return "\n\n".join(parts)


def main():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for plugin in config["plugins"]:
        name = plugin["name"]
        plugin_root = Path("plugins") / name
        md_file = DOCS_DIR / f"{name}.md"

        sections = []

        # --- TITLE ---
        sections.append(f"# {name}\n")

        # --- DOCS (README etc) ---
        if "docs" in plugin:
            md_content = build_markdown_blocks(plugin_root, plugin["docs"])
            if md_content:
                sections.append(md_content)

        # --- API ---
        if "modules" in plugin:
            api_blocks = build_api_blocks(plugin["modules"])
            if api_blocks:
                sections.append("## API Reference\n")
                sections.append(api_blocks)

        final_content = "\n\n".join(sections).strip() + "\n"

        md_file.write_text(final_content)
        print(f"[GENERATED] {md_file}")


if __name__ == "__main__":
    main()
