#!/usr/bin/env python3
"""
QWEN API Startup Script
Handles environment setup and starts the FastAPI server
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_environment():
    """Check system environment and dependencies."""
    logger.info("🔍 Checking environment...")
    
    # Check CUDA
    try:
        import torch
        if torch.cuda.is_available():
            logger.info(f"✅ CUDA Available: {torch.cuda.get_device_name(0)}")
            logger.info(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}GB")
        else:
            logger.warning("⚠️  CUDA not available - will use CPU (SLOW!)")
    except ImportError:
        logger.error("❌ PyTorch not installed")
        return False
    
    # Check required packages (package_name: import_name)
    required = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn', 
        'transformers': 'transformers',
        'pillow': 'PIL'
    }
    missing = []
    
    for package, import_name in required.items():
        try:
            __import__(import_name)
            logger.info(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            logger.error(f"❌ {package} not installed")
    
    if missing:
        logger.error(f"Missing packages: {', '.join(missing)}")
        logger.info(f"Install with: pip install {' '.join(missing)}")
        return False
    
    logger.info("✅ All checks passed!")
    return True


def main():
    """Main startup function."""
    parser = argparse.ArgumentParser(description="QWEN API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers")
    parser.add_argument("--no-check", action="store_true", help="Skip environment check")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🚀 QWEN VLM API Starting...")
    logger.info("=" * 60)
    
    # Check environment
    if not args.no_check:
        if not check_environment():
            logger.error("Environment check failed!")
            sys.exit(1)
    
    # Start server
    try:
        import uvicorn
        
        logger.info(f"\n📡 Starting server on {args.host}:{args.port}")
        logger.info(f"   Reload: {args.reload}")
        logger.info(f"   Workers: {args.workers}")
        logger.info(f"   API Docs: http://{args.host}:{args.port}/docs\n")
        
        uvicorn.run(
            "app.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Error starting server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
