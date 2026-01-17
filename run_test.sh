#!/bin/bash
# Bolitha - Test Scraper Runner
# This script activates the virtual environment and runs the test scraper

set -e  # Exit on error

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./init_toolchain.sh first."
    exit 1
fi

# Activate virtual environment and run test
echo "Activating virtual environment..."
source venv/bin/activate

echo "Running test scraper..."
echo ""
python test_scraper.py

# Deactivate is automatic when script exits
