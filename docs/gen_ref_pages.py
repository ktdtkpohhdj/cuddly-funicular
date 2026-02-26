from pathlib import Path
import ast
import mkdocs_gen_files
import sys
import importlib.util
import os

SRC_PATH = Path("src")
DOCS_PATH = Path("")

# Добавляем абсолютный путь в sys.path
src_absolute = str(SRC_PATH.resolve())
if src_absolute not in sys.path:
    sys.path.insert(0, src_absolute)

# Также добавляем родительскую папку src
parent_path = str(SRC_PATH.parent.resolve())
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

def can_import_module(module_name):
    """Проверяет, можно ли импортировать модуль без реального импорта"""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ModuleNotFoundError, ValueError):
        return False

def get_module_from_path(path):
    """Получает имя модуля из пути к файлу"""
    # Получаем путь относительно src
    try:
        rel_path = path.relative_to(SRC_PATH)
    except ValueError:
        return None
    
    # Убираем .py расширение
    module_path = rel_path.with_suffix("")
    
    # Преобразуем путь в имя модуля
    return ".".join(module_path.parts)

# Собираем все валидные модули
valid_modules = set()

for path in SRC_PATH.rglob("*.py"):
    if path.name == "__init__.py":
        continue
    
    module_name = get_module_from_path(path)
    if not module_name:
        continue
    
    # Проверяем, можем ли мы импортировать модуль
    if can_import_module(module_name):
        valid_modules.add((path, module_name))
    else:
        print(f"⚠ Skipping {module_name} - cannot import")

# Генерируем документацию только для валидных модулей
for path, module_name in valid_modules:
    module_path = path.relative_to(SRC_PATH).with_suffix("")
    doc_path = DOCS_PATH / module_path.with_suffix(".md")
    full_doc_path = Path("docs") / doc_path
    
    # Проверяем существующие ручные md
    if full_doc_path.exists():
        continue
    
    # Проверяем наличие docstring
    try:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        if not ast.get_docstring(tree):
            continue
    except Exception:
        continue
    
    # Создаём md
    try:
        with mkdocs_gen_files.open(doc_path, "w") as f:
            f.write(f"# {path.stem}\n\n")
            
            # Пробуем импортировать для проверки
            try:
                __import__(module_name)
                f.write(f"::: {module_name}\n")
            except ImportError as e:
                print(f"⚠ Warning: {module_name} import failed: {e}")
                f.write(f"::: {module_name}\n")
                f.write(f"    options:\n")
                f.write(f"      show_source: true\n")
                f.write(f"      show_root_heading: true\n")
    except Exception as e:
        print(f"❌ Error generating {module_name}: {e}")
        continue

print(f"✅ Generated docs for {len(valid_modules)} modules")
