#!/usr/bin/env python3
"""
Debug script for LiteLLM proxy
This script can be used to debug specific parts of the LiteLLM proxy
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set timezone to avoid conflicts
os.environ["TZ"] = "Asia/Shanghai"

def debug_config_loading():
    """Debug configuration loading"""
    print("=== Debugging Config Loading ===")
    
    try:
        from litellm.proxy.proxy_server import ProxyConfig
        
        config = ProxyConfig()
        config_path = "zenx/admin.yaml"
        
        print(f"Loading config from: {config_path}")
        config_data = asyncio.run(config.get_config(config_file_path=config_path))
        
        print("Config loaded successfully!")
        print(f"Model list: {config_data.get('model_list', [])}")
        print(f"General settings: {config_data.get('general_settings', {})}")
        
    except Exception as e:
        print(f"Error loading config: {e}")
        import traceback
        traceback.print_exc()

def debug_database_connection():
    """Debug database connection"""
    print("\n=== Debugging Database Connection ===")
    
    try:
        from litellm.proxy.db.prisma_client import PrismaManager
        
        print("Testing database connection...")
        PrismaManager.setup_database()
        print("Database connection successful!")
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()

def debug_model_loading():
    """Debug model loading"""
    print("\n=== Debugging Model Loading ===")
    
    try:
        from litellm.proxy.proxy_server import save_worker_config
        
        print("Testing model configuration...")
        save_worker_config(
            model="cd-st-4-20250514-conf",
            config="zenx/admin.yaml",
            debug=True,
            detailed_debug=True
        )
        print("Model configuration successful!")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main debug function"""
    print("LiteLLM Proxy Debug Script")
    print("=" * 50)
    
    # Test config loading
    debug_config_loading()
    
    # Test database connection
    debug_database_connection()
    
    # Test model loading
    debug_model_loading()
    
    print("\n" + "=" * 50)
    print("Debug script completed!")

if __name__ == "__main__":
    main() 