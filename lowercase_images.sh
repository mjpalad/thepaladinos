#!/usr/bin/env bash
# Rename uppercase .JPG → .jpg under assets/images using git mv

set -e

# Ensure clean working tree
if ! git diff-index --quiet HEAD --; then
  echo "Please commit or stash changes first."
  exit 1
fi

echo "Renaming .JPG files to .jpg under assets/images..."

git ls-files -z assets/images | while IFS= read -r -d '' file; do
  if [[ "$file" == *.JPG ]]; then
    lower="${file%.*}.jpg"
    git mv -k -- "$file" "$lower"
    echo "  $file → $lower"
  fi
done

echo "Done. Review with ‘git status’, then commit+push."
