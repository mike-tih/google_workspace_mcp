#!/bin/bash
set -e

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found"
    echo ""
    echo "Please create .env file:"
    echo "  1. Copy .env.example to .env"
    echo "  2. Fill in your Google OAuth credentials"
    echo ""
    echo "Example:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your credentials"
    exit 1
fi

# Load environment variables from .env
echo "Loading environment variables from .env..."
export $(grep -v '^#' .env | xargs)

# Check if credentials are set
if [ -z "$GOOGLE_CLIENT_ID" ] || [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env"
    exit 1
fi

echo "✓ Credentials loaded"
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

source venv/bin/activate

# Run the script
echo "=========================================="
echo "Starting Google OAuth Token Generator"
echo "=========================================="
echo ""
python get_refresh_token.py
