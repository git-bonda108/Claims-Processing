#!/usr/bin/env python3
"""
Launcher script for the Document Processing & AI Chat application
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import streamlit
        import langchain
        import faiss
        import PyPDF2
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def launch_app():
    """Launch the Streamlit application."""
    if not check_dependencies():
        return False
    
    print("🚀 Launching Document Processing & AI Chat Application...")
    print("📄 Features:")
    print("   - Upload and process up to 10 PDF documents")
    print("   - AI-powered document search and chat")
    print("   - Vector-based semantic search using FAISS")
    print("   - Modern, responsive UI")
    print()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set in environment variables")
        print("   You can set it in the app's sidebar or create a .env file")
        print()
    
    try:
        # Launch Streamlit
        print("🌐 Starting Streamlit server...")
        print("   The app will open in your default browser")
        print("   If it doesn't open automatically, go to: http://localhost:8501")
        print()
        print("   Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Use the memory about Streamlit execution
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = launch_app()
    sys.exit(0 if success else 1)
