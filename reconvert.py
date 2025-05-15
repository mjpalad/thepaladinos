import os
import re
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote, quote, urlunparse, parse_qs

# === Configuration ===
file_path        = 'BlogML.xml'                   # Your BlogML export file
output_dir       = './output_markdown'            # Directory for Markdown output
local_image_dir  = './output_images'              # Local directory to download images
web_image_prefix = '/thepaladinos/assets/images'  # URL prefix for images in Markdown

# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(local_image_dir, exist_ok=True)

# BlogML namespace definition
namespace = {'blogml': 'http://www.blogml.com/2006/09/BlogML'}

# Regex to convert old Flash YouTube embeds to iframe
yt_object_re = re.compile(
    r'<object.*?<param\s+name="movie"\s+value="https?://www\.youtube\.com/v/([^"&]+)[^>]*>.*?</object>',
    re.IGNORECASE | re.DOTALL
)

def convert_youtube(match):
    vid = match.group(1)
    return (
        f'<iframe height="315" width="560" '
        f'src="https://www.youtube.com/embed/{vid}" '
        f'frameborder="0" allowfullscreen></iframe>'
    )

# Extract comments for a post
def extract_comments(post):
    comments = []
    cmts = post.find('blogml:comments', namespace)
    if cmts is not None:
        for c in cmts.findall('blogml:comment', namespace):
            dt_str = c.get('date-created')
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
                date_only = dt.strftime("%Y-%m-%d")
            except:
                date_only = dt_str
            author = c.get('user-name') or (
                c.find('blogml:authors/blogml:author', namespace).get('ref')
                if c.find('blogml:authors/blogml:author', namespace) is not None else "Anonymous"
            )
            text = c.find('blogml:content', namespace).text or ""
            comments.append((date_only, author, text))
    return comments

# Convert and process post HTML content
def convert_post_content(post, prefix_date):
    raw_html = post.find('blogml:content', namespace).text or ''
    # Convert YouTube embeds
    html = yt_object_re.sub(convert_youtube, raw_html)
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    def process_url(raw_url):
        trimmed = raw_url.strip()
        full = trimmed if trimmed.startswith('http') else f"http://www.thepaladinos.com{trimmed}"
        p = urlparse(full)
        raw_path = unquote(p.path)
        encoded_path = quote(raw_path)
        url_fixed = urlunparse((p.scheme, p.netloc, encoded_path, p.params, p.query, p.fragment))
        params = parse_qs(p.query)
        if 'picture' in params:
            raw_name = params['picture'][0]
        else:
            raw_name = os.path.basename(raw_path)
        # Use basename, strip whitespace, and remove any spaces in filename
        clean_name = os.path.basename(raw_name).strip().replace(' ', '')
        new_filename = f"{prefix_date}-{clean_name}"
        local_path = os.path.join(local_image_dir, new_filename)
        web_path = f"{web_image_prefix}/{new_filename}"
        if not os.path.exists(local_path):
            try:
                resp = requests.get(url_fixed, stream=True)
                resp.raise_for_status()
                with open(local_path, 'wb') as f_img:
                    for chunk in resp.iter_content(1024):
                        f_img.write(chunk)
                print(f"Downloaded {url_fixed} -> {local_path}")
            except Exception as e:
                print(f"Error downloading {url_fixed}: {e}")
        return web_path

    # Update <img> tags
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and ('image.axd' in src or '/Portals/' in src):
            img['src'] = process_url(src)

    # Update <a> tags linking to images
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'image.axd' in href or '/Portals/' in href:
            a['href'] = process_url(href)

    return str(soup)

# Process posts older than 2009
def process_old_posts(root):
    processed = []
    posts_elem = root.find('blogml:posts', namespace)
    if posts_elem is None:
        print("No <posts> element found.")
        return processed
    for post in posts_elem.findall('blogml:post', namespace):
        dt_str = post.get('date-created')
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
        if dt.year >= 2009:
            continue
        prefix = dt.strftime("%Y-%m-%d")
        new_html = convert_post_content(post, prefix)
        post.find('blogml:content', namespace).text = new_html
        comments = extract_comments(post)
        title = post.find('blogml:title', namespace).text or 'untitled'
        processed.append((title, dt, new_html, comments))
    return processed

# Main execution
def main():
    tree = ET.parse(file_path)
    root = tree.getroot()
    posts = process_old_posts(root)
    for title, dt, content, comments in posts:
        slug = title.replace(' ', '-').lower()
        fname = f"{dt.strftime('%Y-%m-%d')}-{slug}.md"
        path = os.path.join(output_dir, fname)
        with open(path, 'w') as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write(f'title: "{title}"\n')
            f.write(f'date: {dt.strftime("%Y-%m-%d")}\n')
            f.write('---\n\n')
            f.write(content)
            if comments:
                f.write('\n---\n\n')
                f.write('## Archived Comments\n\n')
                for date_only, author, text in comments:
                    f.write(f'**{author}** on {date_only} wrote:\n\n')
                    for line in text.splitlines():
                        f.write(f'> {line}\n')
                    f.write('\n')
    print(f"✔ Processed {len(posts)} posts. Markdown in '{output_dir}', images in '{local_image_dir}'.")

if __name__ == '__main__':
    main()