#!/usr/bin/env python3
"""Setup Manager Module - Setup and configuration management."""

from .constants import MODEL_NAME
from .config import save_search_api_key, save_search_engine_id
from .ollama_client import check_ollama_connection


def setup_ollama() -> bool:
    """Interactive setup for Ollama configuration.
    
    Returns:
        True if setup successful, False otherwise.
    """
    print("Mistral CLI Setup")
    print("=" * 50)
    print("This CLI uses Ollama for model inference.")
    print("Please ensure:")
    print("1. Ollama is installed and running")
    print(f"2. The {MODEL_NAME} model is pulled: ollama pull {MODEL_NAME}")
    print()
    
    # Check if Ollama is accessible
    if not check_ollama_connection():
        print("❌ Ollama setup failed. Please:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama serve")
        print(f"3. Run: ollama pull {MODEL_NAME}")
        return False
    
    # Optional: Setup search API for research mode
    print("\n📚 Research Mode Setup (Optional)")
    print("=" * 40)
    print("To enable research mode, you need Google Custom Search API credentials.")
    print("You can skip this and set it up later if needed.")
    print()
    
    setup_search = input("Would you like to set up search API credentials now? (y/n): ").strip().lower()
    
    if setup_search in ['y', 'yes']:
        print("\nTo get Google Custom Search API credentials:")
        print("1. Go to: https://console.cloud.google.com/apis/")
        print("2. Create a new project or select existing one")
        print("3. Enable 'Custom Search API'")
        print("4. Create credentials (API key)")
        print("5. Create a Custom Search Engine at: https://cse.google.com/cse/")
        print("6. Get the Search Engine ID from the CSE control panel")
        print()
        
        api_key = input("Enter your Google Custom Search API key (or press Enter to skip): ").strip()
        if api_key:
            engine_id = input("Enter your Custom Search Engine ID: ").strip()
            if engine_id:
                if save_search_api_key(api_key) and save_search_engine_id(engine_id):
                    print("✅ Search API credentials saved successfully!")
                else:
                    print("❌ Failed to save search API credentials.")
            else:
                print("⚠️  Skipping search API setup - missing Search Engine ID")
        else:
            print("⚠️  Skipping search API setup - you can set it up later")
    
    print("\n✅ Setup completed successfully!")
    print("You can now use the Mistral CLI.")
    return True 