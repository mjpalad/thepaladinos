#!/usr/bin/env python3
"""
Script to scan all Jekyll posts in the _posts directory, report Photobucket flash embeds,
and replace them with YouTube <iframe> embeds based on mappings in yt_map.py.
"""
import os
import re
from yt_map import yt_map
from urllib.parse import unquote

# Regex patterns to identify legacy embeds
embed_re = re.compile(
    r'<embed[^>]*?player\.swf\?file=[^"\']*/(?P<file>[^"&]+)[^>]*>',
    re.IGNORECASE
)
param_re = re.compile(
    r'<param\s+name="movie"\s+value="(?P<url>https?://i\d+\.photobucket\.com/[^"]+)"',
    re.IGNORECASE
)
swfobject_re = re.compile(
    r'var\s+so\s*=\s*new\s+SWFObject\([^;]+?so\.write\("[^"]+"\);',
    re.IGNORECASE | re.DOTALL
)

# Replacement function

def replace_embeds(text: str, path: str) -> str:
    # Debug: find raw Photobucket references
    print(f"[DEBUG] Scanning {path}")
    if 'photobucket' in text.lower():
        embeds = embed_re.findall(text)
        params = [m.group('url') for m in param_re.finditer(text)]
        print(f"  Found embed tags: {embeds}")
        print(f"  Found param URLs: {params}")

    def repl_embed(m):
        raw_fn = m.group('file')
        fn = unquote(raw_fn).strip()
        fn = fn.split('?')[0]
        print(f"[DEBUG] embed filename: '{fn}' in {path}")
        yt_id = yt_map.get(fn)
        if yt_id:
            print(f"[UPDATE] Replacing embed for {fn} in {path}")
            return (
                f'<iframe width="560" height="315" '
                f'src="https://www.youtube.com/embed/{yt_id}" '
                f'frameborder="0" allowfullscreen></iframe>'
            )
        return m.group(0)

    text = embed_re.sub(repl_embed, text)

    def repl_param(m):
        url = m.group('url')
        raw_fn = url.split('/')[-1]
        fn = unquote(raw_fn).strip().split('?')[0]
        print(f"[DEBUG] param filename: '{fn}' in {path}")
        yt_id = yt_map.get(fn)
        if yt_id:
            print(f"[UPDATE] Replacing <param> for {fn} in {path}")
            return (
                f'<iframe width="560" height="315" '
                f'src="https://www.youtube.com/embed/{yt_id}" '
                f'frameborder="0" allowfullscreen></iframe>'
            )
        return m.group(0)

    text = param_re.sub(repl_param, text)

    if swfobject_re.search(text):
        print(f"[UPDATE] Removing SWFObject script in {path}")
    text = swfobject_re.sub('', text)

    return text

# Process all Markdown files under _posts
def process_posts(posts_dir='_posts'):
    for root_dir, dirs, files in os.walk(posts_dir):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            full_path = os.path.join(root_dir, fname)
            with open(full_path, 'r', encoding='utf-8') as fp:
                original = fp.read()

            if 'photobucket' not in original.lower():
                continue

            updated = replace_embeds(original, full_path)
            if updated != original:
                with open(full_path, 'w', encoding='utf-8') as fp:
                    fp.write(updated)
                print(f"[SAVED] Updated embeds in: {full_path}")
            else:
                print(f"[SKIP] No replacement needed in: {full_path}")

# Entry point
if __name__ == '__main__':
    process_posts()
    print('YouTube embed update complete.')