#!/usr/bin/env python3
"""
Test script for the DocumentProcessor class
"""

import os
import sys
from document_processor import DocumentProcessor

def test_document_processor():
    """Test the document processor with sample PDFs from Downloads."""
    
    # Check if Downloads folder exists and has PDFs
    downloads_path = "/Users/macbook/Downloads"
    if not os.path.exists(downloads_path):
        print("❌ Downloads folder not found")
        return False
    
    # Find PDF files
    pdf_files = [f for f in os.listdir(downloads_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in Downloads folder")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files in Downloads")
    
    # Test with first 2 PDF files
    test_files = pdf_files[:2]
    test_paths = [os.path.join(downloads_path, f) for f in test_files]
    
    print(f"🧪 Testing with: {', '.join(test_files)}")
    
    # Check if OpenAI API key is available
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️  No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        print("   Testing without AI features...")
        
        # Test basic PDF processing without AI
        try:
            processor = DocumentProcessor("dummy_key")
            for file_path in test_paths:
                result = processor.process_single_document(file_path, os.path.basename(file_path))
                if result["status"] == "success":
                    print(f"✅ Successfully processed: {result['file_name']}")
                    print(f"   - Chunks: {result['chunk_count']}")
                    print(f"   - Words: {result['word_count']}")
                else:
                    print(f"❌ Failed to process: {result['file_name']}")
                    print(f"   - Error: {result['error']}")
        except Exception as e:
            print(f"❌ Error during testing: {str(e)}")
            return False
    else:
        print("✅ OpenAI API key found. Testing with full AI features...")
        
        try:
            processor = DocumentProcessor(openai_key)
            results = processor.process_multiple_documents(test_paths)
            
            print(f"\n📊 Processing Results:")
            print(f"   - Total files: {results['total_files']}")
            print(f"   - Successful: {len(results['successful'])}")
            print(f"   - Failed: {len(results['failed'])}")
            print(f"   - Total chunks: {results['total_chunks']}")
            print(f"   - Total words: {results['total_words']}")
            
            if results['successful']:
                print(f"\n✅ Successfully processed files:")
                for doc in results['successful']:
                    print(f"   - {doc['file_name']}: {doc['chunk_count']} chunks, {doc['word_count']} words")
            
            if results['failed']:
                print(f"\n❌ Failed files:")
                for doc in results['failed']:
                    print(f"   - {doc['file_name']}: {doc['error']}")
            
            # Test search functionality
            if processor.vector_store:
                print(f"\n🔍 Testing search functionality...")
                search_results = processor.search_documents("test query", k=2)
                print(f"   - Search returned {len(search_results)} results")
                
                # Test conversation chain
                print(f"\n💬 Testing conversation chain...")
                conversation_chain = processor.get_conversation_chain()
                if conversation_chain:
                    print("   - Conversation chain created successfully")
                else:
                    print("   - Failed to create conversation chain")
            
        except Exception as e:
            print(f"❌ Error during AI testing: {str(e)}")
            return False
    
    print("\n🎉 Test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_document_processor()
    sys.exit(0 if success else 1)
