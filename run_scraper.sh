#!/bin/bash
# Bolitha - Booli.se Scraper Runner
# This script activates the virtual environment and runs the booli.se scraper

set -e  # Exit on error

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./init_toolchain.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run scraper with provided town name
if [ -z "$1" ]; then
    echo "Usage: ./run_scraper.sh <town_name> [output_file]"
    echo ""
    echo "Examples:"
    echo "  ./run_scraper.sh Uppsala"
    echo "  ./run_scraper.sh Stockholm listings.md"
    echo "  ./run_scraper.sh \"Göteborg\""
    exit 1
fi

python booli_scraper.py "$@"
