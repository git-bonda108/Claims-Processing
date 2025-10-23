import streamlit as st
import os
import tempfile
import pandas as pd
from typing import List, Dict, Any
import time
from document_processor import DocumentProcessor
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Document Intelligence & AI Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful, professional UI
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.8rem;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .document-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .document-card:hover {
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }
    
    .chat-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .chat-message {
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left-color: #3b82f6;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
        border-left-color: #8b5cf6;
        margin-right: 2rem;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #86efac;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .error-banner {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        color: #dc2626;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #fca5a5;
        margin: 1rem 0;
    }
    
    .info-banner {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #93c5fd;
        margin: 1rem 0;
    }
    
    .extracted-fields {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .field-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .field-row:last-child {
        border-bottom: none;
    }
    
    .field-label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
    }
    
    .field-value {
        color: #1f2937;
        font-size: 0.9rem;
        text-align: right;
        max-width: 60%;
        word-wrap: break-word;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f8fafc;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
    
    .upload-area {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #3b82f6;
        background: #eff6ff;
    }
    
    .processing-spinner {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    if 'processor' not in st.session_state:
        st.session_state.processor = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_model' not in st.session_state:
        st.session_state.chat_model = None
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = []

def save_uploaded_files(uploaded_files) -> List[str]:
    """Save uploaded files to temporary directory and return file paths."""
    file_paths = []
    temp_dir = tempfile.mkdtemp()
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
    
    return file_paths

def extract_document_fields(text: str, filename: str) -> Dict[str, Any]:
    """Extract meaningful fields from document text."""
    fields = {
        "Document Name": filename,
        "Total Words": len(text.split()),
        "Total Characters": len(text),
        "Estimated Pages": max(1, len(text.split()) // 250),
        "Language": "English",  # Could be enhanced with language detection
        "Document Type": "PDF Document",
        "Processing Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Extract common business document fields
    if any(keyword in text.lower() for keyword in ['invoice', 'bill', 'receipt']):
        fields["Document Category"] = "Financial Document"
    elif any(keyword in text.lower() for keyword in ['contract', 'agreement', 'terms']):
        fields["Document Category"] = "Legal Document"
    elif any(keyword in text.lower() for keyword in ['report', 'analysis', 'summary']):
        fields["Document Category"] = "Report Document"
    elif any(keyword in text.lower() for keyword in ['email', 'message', 'communication']):
        fields["Document Category"] = "Communication Document"
    else:
        fields["Document Category"] = "General Document"
    
    # Extract potential key topics (simple keyword extraction)
    words = text.lower().split()
    word_freq = {}
    for word in words:
        if len(word) > 4 and word.isalpha():
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    fields["Key Topics"] = ", ".join([word for word, freq in top_words])
    
    return fields

def display_document_summary(results: Dict[str, Any]):
    """Display a beautiful, comprehensive summary of processed documents."""
    st.markdown('<div class="section-header">📊 Document Processing Results</div>', unsafe_allow_html=True)
    
    # Key metrics in beautiful cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results["total_files"]}</div>
            <div class="metric-label">Total Files</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(results["successful"])}</div>
            <div class="metric-label">Successfully Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results["total_chunks"]}</div>
            <div class="metric-label">Text Chunks Created</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results["total_words"]:,}</div>
            <div class="metric-label">Words Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display successful files with beautiful formatting
    if results["successful"]:
        st.markdown("### 📋 Processed Documents")
        
        for i, doc in enumerate(results["successful"], 1):
            # Extract fields for this document
            extracted_fields = extract_document_fields(doc["text"], doc["file_name"])
            
            with st.expander(f"📄 Document {i}: {doc['file_name']}", expanded=True):
                # Document metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Chunks", doc["chunk_count"])
                
                with col2:
                    st.metric("Words", f"{doc['word_count']:,}")
                
                with col3:
                    st.metric("Characters", f"{len(doc['text']):,}")
                
                with col4:
                    st.metric("Pages", f"~{max(1, doc['word_count'] // 250)}")
                
                # Extracted fields in a beautiful, well-formatted table
                st.markdown("**📋 Extracted Document Information:**")
                
                # Create a proper data table for better visibility
                field_data = []
                for field, value in extracted_fields.items():
                    field_data.append({
                        "Field": field,
                        "Value": str(value)
                    })
                
                df_fields = pd.DataFrame(field_data)
                st.dataframe(
                    df_fields, 
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Field": st.column_config.TextColumn(
                            "Field",
                            width="medium",
                            help="Document field name"
                        ),
                        "Value": st.column_config.TextColumn(
                            "Value", 
                            width="large",
                            help="Extracted field value"
                        )
                    }
                )
                
                # Content preview - make it properly visible
                if doc["text"]:
                    preview_text = doc["text"][:1000] + "..." if len(doc["text"]) > 1000 else doc["text"]
                    st.markdown("**📖 Content Preview:**")
                    
                    # Create a beautiful content preview box
                    st.markdown(f"""
                    <div style="
                        background: #f8fafc;
                        border: 1px solid #e2e8f0;
                        border-radius: 8px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                        line-height: 1.5;
                        max-height: 200px;
                        overflow-y: auto;
                        white-space: pre-wrap;
                    ">
                    {preview_text}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Display failed files
    if results["failed"]:
        st.markdown("### ❌ Failed Documents")
        for doc in results["failed"]:
            st.markdown(f"""
            <div class="error-banner">
                <strong>{doc['file_name']}</strong><br>
                Error: {doc['error']}
            </div>
            """, unsafe_allow_html=True)
    
    # Success message
    if results["successful"]:
        st.markdown(f"""
        <div class="success-banner">
            🎉 Processing Complete! Successfully processed {len(results['successful'])} documents with {results['total_chunks']} total chunks containing {results['total_words']:,} words.
            <br><br>
            💬 <strong>Ready for AI Chat!</strong> You can now ask questions about your documents using the AI Chat tab.
        </div>
        """, unsafe_allow_html=True)

def display_chat_interface():
    """Display a beautiful, professional chat interface."""
    st.markdown('<div class="section-header">💬 AI Document Assistant</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-banner">
        🤖 <strong>Chat with your documents!</strong> Ask questions about the content, request summaries, 
        or search for specific information. The AI will provide intelligent responses based on your uploaded documents.
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input area
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_area(
        "💭 Ask a question about your documents:",
        placeholder="e.g., What are the main topics in these documents? Summarize the key points. What specific information is mentioned about [topic]?",
        height=100,
        key=f"chat_input_{len(st.session_state.chat_history)}"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("🚀 Send", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process chat input
    if send_button and user_input:
        if st.session_state.chat_model and st.session_state.processor:
            with st.spinner("🤔 AI is thinking..."):
                try:
                    # Get context from documents
                    context = st.session_state.processor.get_context_for_query(user_input, k=5)
                    
                    # Create enhanced prompt with context
                    prompt = f"""You are an intelligent document assistant. Based on the following document context, please provide a helpful and accurate response to the user's question.

Document Context:
{context}

User Question: {user_input}

Instructions:
- Provide a comprehensive and well-structured response
- If the context contains relevant information, use it to answer the question
- If the context doesn't contain enough information, clearly state this
- Be specific and cite relevant parts of the documents when possible
- Format your response in a clear, easy-to-read manner
- If applicable, suggest follow-up questions the user might want to ask

Response:"""
                    
                    # Get AI response
                    response = st.session_state.chat_model.invoke(prompt)
                    
                    # Get source documents for display
                    source_docs = st.session_state.processor.search_documents(user_input, k=3)
                    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_input,
                        "ai": response.content,
                        "sources": sources,
                        "timestamp": pd.Timestamp.now().strftime("%H:%M:%S")
                    })
                    
                    # Clear input by rerunning
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing chat: {str(e)}")
        else:
            st.error("❌ Please process documents first to enable chat functionality.")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        
        for i, chat in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You ({chat['timestamp']}):</strong><br>
                {chat["user"]}
            </div>
            """, unsafe_allow_html=True)
            
            # AI response
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI Assistant:</strong><br>
                {chat["ai"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Sources
            if chat["sources"]:
                unique_sources = list(set(chat["sources"]))
                st.markdown(f"**📚 Sources:** {', '.join(unique_sources)}")
            
            st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Document Intelligence & AI Chat</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your PDF documents into intelligent, searchable knowledge with AI-powered insights</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # OpenAI API Key input
        openai_api_key = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to enable AI features",
            value=os.getenv("OPENAI_API_KEY", "")
        )
        
        if not openai_api_key:
            st.warning("⚠️ Please enter your OpenAI API key to use AI features")
            st.markdown("Get your API key from [OpenAI](https://platform.openai.com/api-keys)")
        
        # Document processing options
        st.markdown("## 📋 Processing Options")
        max_files = st.slider("Maximum files to process", 1, 10, 5)
        chunk_size = st.slider("Chunk size", 500, 2000, 1000)
        chunk_overlap = st.slider("Chunk overlap", 100, 500, 200)
        
        # App info
        st.markdown("## ℹ️ About")
        st.info("""
        This application processes PDF documents and creates an intelligent, searchable knowledge base.
        
        **Features:**
        - Batch PDF processing
        - AI-powered document chat
        - Semantic search
        - Field extraction
        - Beautiful UI
        """)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📁 Upload & Process", "💬 AI Chat", "🔍 Document Explorer"])
    
    with tab1:
        st.markdown('<div class="section-header">📁 Upload PDF Documents</div>', unsafe_allow_html=True)
        
        # File upload area
        uploaded_files = st.file_uploader(
            "Choose PDF files to process",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload up to 10 PDF documents for intelligent processing and analysis"
        )
        
        if uploaded_files:
            if len(uploaded_files) > max_files:
                st.warning(f"⚠️ You can only process up to {max_files} files at once. Please select fewer files.")
            else:
                st.success(f"✅ {len(uploaded_files)} file(s) selected for processing")
                
                # Process documents button
                if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                    if not openai_api_key:
                        st.error("❌ Please enter your OpenAI API key in the sidebar")
                    else:
                        with st.spinner("🔄 Processing documents..."):
                            try:
                                # Save uploaded files
                                file_paths = save_uploaded_files(uploaded_files)
                                
                                # Initialize processor
                                processor = DocumentProcessor(openai_api_key)
                                
                                # Process documents
                                results = processor.process_multiple_documents(file_paths)
                                
                                # Update session state
                                st.session_state.processor = processor
                                st.session_state.documents_processed = True
                                st.session_state.chat_model = processor.get_chat_model()
                                
                                # Display results
                                display_document_summary(results)
                                
                            except Exception as e:
                                st.error(f"❌ Error processing documents: {str(e)}")
    
    with tab2:
        if st.session_state.documents_processed and st.session_state.chat_model:
            display_chat_interface()
        else:
            st.markdown("""
            <div class="info-banner">
                ℹ️ <strong>No documents processed yet.</strong> Please upload and process documents first to enable chat functionality.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### 🚀 How to get started:
            1. Go to the "Upload & Process" tab
            2. Enter your OpenAI API key in the sidebar
            3. Upload PDF documents
            4. Click "Process Documents"
            5. Return to this tab to start chatting!
            """)
    
    with tab3:
        st.markdown('<div class="section-header">🔍 Document Explorer</div>', unsafe_allow_html=True)
        
        if st.session_state.documents_processed and st.session_state.processor:
            # Document summary
            summary = st.session_state.processor.get_document_summary()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Total Documents", summary["total_documents"])
            with col2:
                st.metric("📝 Total Chunks", summary["total_chunks"])
            with col3:
                st.metric("📚 Document Sources", len(summary["document_sources"]))
            
            # Search functionality
            st.markdown("### 🔍 Search Documents")
            search_query = st.text_input("Search for specific content:", placeholder="Enter search terms...")
            
            if search_query:
                with st.spinner("🔍 Searching..."):
                    search_results = st.session_state.processor.search_documents(search_query, k=5)
                    
                    if search_results:
                        st.markdown(f"### Found {len(search_results)} relevant chunks:")
                        for i, doc in enumerate(search_results):
                            with st.expander(f"📄 Chunk {i+1} from {doc.metadata.get('source', 'Unknown')}"):
                                st.text(doc.page_content)
                    else:
                        st.info("No relevant content found for your search query.")
            
            # Document sources
            st.markdown("### 📚 Document Sources")
            for source in summary["document_sources"]:
                st.write(f"• {source}")
        else:
            st.markdown("""
            <div class="info-banner">
                ℹ️ <strong>No documents processed yet.</strong> Please upload and process documents first to explore them.
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
