import os
import re

# --- Config ---
post_dir = "_posts"
map_file = "paladino_images_with_filenames.txt"
image_path_prefix = "/assets/images/"

# --- Load URL → filename map ---
url_to_filename = {}
with open(map_file, "r", encoding="utf-8") as f:
    for line in f:
        if "\t" in line:
            url, filename = line.strip().split("\t")
            url_to_filename[url] = filename

# --- Rewrite image paths in all blog posts ---
for root, _, files in os.walk(post_dir):
    for filename in files:
        if not filename.endswith(".md"):
            continue

        post_path = os.path.join(root, filename)
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()

        updated = content
        for url, fname in url_to_filename.items():
            if url in updated:
                updated = updated.replace(url, image_path_prefix + fname)

        if updated != content:
            with open(post_path, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"✅ Updated: {filename}")
        else:
            print(f"— No changes: {filename}")
