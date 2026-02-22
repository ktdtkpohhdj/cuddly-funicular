from pdoc import pdoc, render
import pathlib

# Путь к приватному модулю, который мы клонировали в CI
module_path = pathlib.Path("private_plugin_temp/src")

# Генерируем документацию для всех модулей внутри src
modules = pdoc(module_path, template_directory=None)

# Папка, куда сохраняем Markdown
output_dir = pathlib.Path("docs/private")
output_dir.mkdir(parents=True, exist_ok=True)

for module in modules.values():
    md_content = render.markdown(module)
    # Сохраняем каждый модуль как отдельный md файл
    output_file = output_dir / f"{module.name}.md"
    output_file.write_text(md_content, encoding="utf-8")
