import os
import re
from datetime import datetime

# --- Config ---
posts_dir = "_posts"  # Adjust if needed
cutoff_year = 2013

# --- Patterns ---
digit_img_pattern = re.compile(r'["\']([^"\']*/\d{1,2}\.jpg)["\']', re.IGNORECASE)
youtube_embed_pattern = re.compile(r'<object[^>]*>.*youtube\.com/v/.*?</object>', re.IGNORECASE | re.DOTALL)

# --- Track Results ---
digit_img_hits = []
youtube_hits = []

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

    # Read file content
    path = os.path.join(posts_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Run checks
    if digit_img_pattern.search(content):
        digit_img_hits.append(filename)
    if youtube_embed_pattern.search(content):
        youtube_hits.append(filename)

# --- Output Summary ---
print("✅ Scan Complete.\n")

print("1️⃣ Images with 1–2 digit filenames:")
print("\n".join(digit_img_hits) or "None found")

print("\n3️⃣ Posts with old YouTube embed code:")
print("\n".join(youtube_hits) or "None found")
