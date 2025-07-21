#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting Playwright cache directory..."
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/playwright

echo "Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium

echo "Build completed successfully!"