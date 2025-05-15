#!/usr/bin/env python3
"""
Rename all image files in the `assets/images` directory from uppercase .JPG to lowercase .jpg.
"""
import os

def rename_uppercase_jpgs(images_dir='assets/images'):
    # Walk through the images directory
    for root, dirs, files in os.walk(images_dir):
        for fname in files:
            # Check for files ending in .JPG (uppercase)
            if fname.endswith('.JPG'):
                old_path = os.path.join(root, fname)
                # Construct new filename with lowercase extension
                base, _ = os.path.splitext(fname)
                new_fname = base + '.jpg'
                new_path = os.path.join(root, new_fname)
                # Rename the file
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} → {new_path}")

if __name__ == '__main__':
    rename_uppercase_jpgs()
    print('All .JPG files have been renamed to .jpg.')
