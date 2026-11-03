#!/bin/bash
# Rebuild everything, in order. Run from the project root.
# Usage: bash scripts/rebuild_all.sh
set -e
cd "$(dirname "$0")/.."
python3 scripts/download_data.py
python3 scripts/process_data.py
python3 scripts/make_charts.py
python3 scripts/build_notebooks.py
echo "Notebooks built. Execute them with:"
echo "  jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb"
echo "Then copy charts to docs with: cp charts/*.png docs/charts/"
