import os
import re
from datetime import datetime

# --- Config ---
posts_dir = "_posts"  # Adjust if needed
cutoff_year = 2013  # Only edit posts before this year

# --- Patterns ---
youtube_embed_pattern = re.compile(
    r'<object[^>]*>.*?youtube\.com/v/([a-zA-Z0-9_-]+).*?</object>',
    re.IGNORECASE | re.DOTALL
)

# --- Logging ---
updated_files = []

# --- Process ---
for filename in os.listdir(posts_dir):
    if not filename.endswith(".md"):
        continue

    # Extract date from filename
    try:
        date_str = filename[:10]
        post_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        continue

    if post_date.year >= cutoff_year:
        continue

    path = os.path.join(posts_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace YouTube embeds
    matches = youtube_embed_pattern.findall(content)
    if not matches:
        continue

#    for video_id in matches:
#        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
#        content = re.sub(r'<object[^>]*>.*?youtube\.com/v/' + re.escape(video_id) + r'.*?</object>', iframe, content, flags=re.IGNORECASE | re.DOTALL)

#    with open(path, "w", encoding="utf-8") as f:
#        f.write(content)
    updated_files.append(filename)

# --- Summary ---
print("✅ YouTube embed updates complete.")
if updated_files:
    print("Updated files:\n" + "\n".join(updated_files))
else:
    print("No updates needed.")
