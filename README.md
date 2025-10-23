# Document Processing & AI Chat Application

A comprehensive Streamlit application for processing PDF documents, extracting information using LangChain and FAISS vector store, and providing conversational AI chat capabilities.

## Features

- 📄 **Batch PDF Processing**: Process up to 10 PDF documents simultaneously
- 🔍 **Vector Search**: Use FAISS vector store for semantic document search
- 💬 **AI Chat Interface**: Chat with an AI assistant about document content
- 📊 **Document Explorer**: Browse and search through processed documents
- 🎨 **Modern UI**: Clean, responsive interface with real-time feedback
- ⚡ **Fast Processing**: Optimized for quick document processing and retrieval

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- PDF documents to process

## Installation

1. **Clone or download this repository**
   ```bash
   cd /Users/macbook/Documents/RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage

1. **Start the application**
   ```bash
   python -m streamlit run app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8501`

3. **Process documents**
   - Enter your OpenAI API key in the sidebar
   - Upload PDF documents or use sample documents from Downloads
   - Click "Process Documents"

4. **Chat with AI**
   - Switch to the "AI Chat" tab
   - Ask questions about your documents
   - Get intelligent responses based on document content

5. **Explore documents**
   - Use the "Document Explorer" tab to search and browse content

## Application Structure

```
RAG/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document processing and vector store logic
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables template
└── README.md             # This file
```

## Key Components

### DocumentProcessor Class
- Handles PDF text extraction
- Creates vector embeddings using OpenAI
- Manages FAISS vector store
- Provides search and retrieval functionality

### Streamlit UI
- **Upload & Process Tab**: File upload and batch processing
- **AI Chat Tab**: Conversational interface with document context
- **Document Explorer Tab**: Search and browse functionality

## Configuration Options

- **Maximum files**: Process 1-10 documents at once
- **Chunk size**: Control text chunking (500-2000 characters)
- **Chunk overlap**: Set overlap between chunks (100-500 characters)

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure you have a valid OpenAI API key
   - Check that the key is correctly set in the environment

2. **PDF Processing Errors**
   - Ensure PDF files are not password-protected
   - Check that PDFs contain extractable text (not just images)

3. **Memory Issues**
   - Reduce chunk size or number of documents for large files
   - Process documents in smaller batches

### Performance Tips

- Use smaller chunk sizes for faster processing
- Process documents in batches of 3-5 for optimal performance
- Clear chat history periodically to free up memory

## Sample Documents

The application can automatically test with sample PDF documents from your Downloads folder. This is useful for:
- Testing the application without uploading files
- Demonstrating functionality
- Quick validation of the setup

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your OpenAI API key is valid
3. Ensure all dependencies are installed correctly

## License

This project is open source and available under the MIT License.
