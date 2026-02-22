from pdoc import pdoc, render
import pathlib

# Список приватных плагинов
private_plugins = [
    "private_plugin_temp/src",
]

for plugin_path in private_plugins:
    plugin_name = pathlib.Path(plugin_path).parent.name
    output_dir = pathlib.Path(f"docs/private/{plugin_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # pdoc принимает только путь к модулю
    modules = pdoc(plugin_path)

    # Для каждого модуля создаём отдельный md-файл
    for module in modules.values():
        md_content = render.markdown(module)
        output_file = output_dir / f"{module.name}.md"
        output_file.write_text(md_content, encoding="utf-8")
