import os
import yaml

docs_dir = "docs"
nav = []

for root, dirs, files in os.walk(docs_dir):
    md_files = [f for f in files if f.endswith(".md")]
    if md_files:
        folder_name = os.path.relpath(root, docs_dir)
        pages = [{os.path.splitext(f)[0].capitalize(): os.path.join(folder_name, f).replace("\\", "/")} for f in md_files]
        if folder_name != ".":
            nav.append({folder_name.capitalize(): pages})
        else:
            nav.extend(pages)

with open("mkdocs.yml", "r") as f:
    cfg = yaml.safe_load(f)

cfg["nav"] = nav

with open("mkdocs.yml", "w") as f:
    yaml.dump(cfg, f, sort_keys=False)
