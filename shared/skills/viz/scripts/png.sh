#!/bin/sh
# Render a viz HTML file to a 2x PNG on the house black background.
# usage: png.sh <file.html> <out.png>
set -eu
html=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
playwright screenshot --full-page --color-scheme=dark --viewport-size=1616,400 \
  --wait-for-timeout=300 "file://$html#png" "$2"
