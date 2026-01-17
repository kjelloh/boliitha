#!/bin/bash
# Bolitha - Boli.se Web Scraper Setup Script
# This script sets up the Python virtual environment and installs dependencies

set -e  # Exit on error

echo "========================================="
echo "Bolitha Toolchain Initialization"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Note about Python 3.14
if [[ "$PYTHON_VERSION" == *"3.14"* ]]; then
    echo "Note: Python 3.14 detected. Using latest compatible package versions."
fi
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install Python dependencies
echo "Installing Python packages from requirements.txt..."
echo "(This may take a minute...)"
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Python packages installed successfully"
else
    echo ""
    echo "✗ Error installing packages. Check the output above."
    exit 1
fi
echo ""

# Install Playwright browsers
echo "Installing Playwright browsers (this may take a few minutes)..."
playwright install chromium
echo "✓ Playwright browsers installed"
echo ""

echo "========================================="
echo "Verifying Installation"
echo "========================================="
echo ""
echo "Running quick verification test..."
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright import successful')"
echo "✓ Python environment verified"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "IMPORTANT: To use the scraper, you must first activate the virtual environment:"
echo ""
echo "  source venv/bin/activate"
echo ""
echo "Then run:"
echo "  python test_scraper.py          # Test booli.se access"
echo "  python booli_scraper.py         # Run main scraper"
echo ""
echo "Alternatively, use the run script (auto-activates venv):"
echo "  ./run_test.sh                   # Run test scraper"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo ""
