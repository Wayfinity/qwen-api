#!/bin/bash
# Quick Start Script for QWEN API

echo "======================================"
echo "QWEN API - Quick Start Setup"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Python: $python_version"

# Check CUDA
echo ""
echo "✓ Checking CUDA..."
python -c "import torch; print('  CUDA Available:', torch.cuda.is_available()); print('  Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" 2>/dev/null || echo "  CUDA: Not properly configured"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo ""
    echo "✓ Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    echo "  Virtual environment created and activated"
else
    echo ""
    echo "✓ Using existing virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "  Dependencies installed"

# Verify installation
echo ""
echo "✓ Verifying installation..."
python -c "import torch; import transformers; import fastapi; print('  All packages OK')" && echo "" || echo "  ERROR: Some packages missing"

# Show next steps
echo "======================================"
echo "✓ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the API server:"
echo "   python run.py"
echo ""
echo "2. In another terminal, test the API:"
echo "   python examples.py"
echo ""
echo "3. Access API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "For more information, see:"
echo "  - README.md - Project overview"
echo "  - API_DOCUMENTATION.md - Complete API reference"
echo "  - CONFIGURATION.md - Configuration options"
echo ""
