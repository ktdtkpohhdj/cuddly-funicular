from pdoc import pdoc, render
import pathlib

# Список приватных плагинов
private_plugins = [
    "private_plugin_temp/src",
]

for plugin_path in private_plugins:
    plugin_path = pathlib.Path(plugin_path)
    plugin_name = plugin_path.parent.name
    output_dir = pathlib.Path(f"docs/private/{plugin_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Создаём объект документации для всего пакета
    module_doc = pdoc(str(plugin_path))  # pdoc возвращает объект Module

    # Генерация Markdown
    md_content = render.markdown(module_doc)

    # Сохраняем как один .md файл на плагин
    output_file = output_dir / f"{plugin_name}.md"
    output_file.write_text(md_content, encoding="utf-8")
