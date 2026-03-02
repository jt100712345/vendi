#!/bin/bash
# Cleanup script for OpenClaw workspace

# Remove temporary files
find . -name "*.bak" -o -name "*.tmp" -o -name "*.swp" -o -name "*.DS_Store" | xargs rm -f

# Cleanup git cache
git add .
git status

echo "Cleanup complete!"
