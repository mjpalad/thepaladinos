import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# === Configuration ===
file_path = 'BlogML.xml'  
target_post_url = '/post/2007/02/18/Shes-Here!.aspx'  # Change to the post-url of the post you care about
output_dir = './downloaded_images'
#/2007/02/18/she's-here

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Namespace for BlogML
namespace = {'blogml': 'http://www.blogml.com/2006/09/BlogML'}

# Attempt to parse the BlogML file
try:
    tree = ET.parse(file_path)
except Exception as e:
    print("Failed to parse XML:", e)
    exit(1)

root = tree.getroot()

# Locate the specific post by its post-url attribute
post = root.find(
    f"blogml:posts/blogml:post[@post-url='{target_post_url}']",
    namespace
)
if post is None:
    print(f"No post found with post-url '{target_post_url}'")
    exit(1)

# Prepare date prefix for filenames
date_str = post.get('date-created')
date_created = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
date_prefix = date_created.strftime('%Y-%m-%d')

# Extract the HTML content
content = post.find('blogml:content', namespace).text or ''

# Regex to match both absolute and relative image URLs
image_pattern = re.compile(r'(?:https?://www\.thepaladinos\.com)?/image\.axd\?picture=[^"]+')

# Download each image
for img_url in image_pattern.findall(content):
    # Normalize to full URL
    full_url = img_url if img_url.startswith('http') else f"http://www.thepaladinos.com{img_url}"
    
    # Build new filename
    img_name = img_url.split('/')[-1]
    new_name = f"{date_prefix}-{img_name}"
    save_path = os.path.join(output_dir, new_name)
    
    # Download and save
    try:
        response = requests.get(full_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        print(f"Downloaded {full_url} → {save_path}")
    except Exception as e:
        print(f"Error downloading {full_url}: {e}")

print("All images downloaded.")