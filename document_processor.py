import os
import tempfile
import logging
from typing import List, Dict, Any, Optional
import PyPDF2
import pandas as pd
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
# Note: ConversationalRetrievalChain is not available in the current LangChain version
# We'll implement a simpler chat interface
from langchain_openai import ChatOpenAI
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Main class for processing PDF documents and creating vector stores."""
    
    def __init__(self, openai_api_key: str):
        """Initialize the document processor with OpenAI API key."""
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None
        self.documents = []
        self.processed_files = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def process_single_document(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Process a single PDF document and return metadata."""
        try:
            # Extract text
            text = self.extract_text_from_pdf(file_path)
            if not text.strip():
                return {
                    "file_name": file_name,
                    "status": "failed",
                    "error": "No text extracted from PDF",
                    "text": "",
                    "chunks": []
                }
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create document objects
            doc_chunks = [Document(page_content=chunk, metadata={"source": file_name, "chunk_id": i}) 
                         for i, chunk in enumerate(chunks)]
            
            return {
                "file_name": file_name,
                "status": "success",
                "text": text,
                "chunks": doc_chunks,
                "chunk_count": len(chunks),
                "word_count": len(text.split())
            }
            
        except Exception as e:
            logger.error(f"Error processing {file_name}: {str(e)}")
            return {
                "file_name": file_name,
                "status": "failed",
                "error": str(e),
                "text": "",
                "chunks": []
            }
    
    def process_multiple_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process multiple PDF documents."""
        results = {
            "successful": [],
            "failed": [],
            "total_files": len(file_paths),
            "total_chunks": 0,
            "total_words": 0
        }
        
        all_chunks = []
        
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            result = self.process_single_document(file_path, file_name)
            
            if result["status"] == "success":
                results["successful"].append(result)
                all_chunks.extend(result["chunks"])
                results["total_chunks"] += result["chunk_count"]
                results["total_words"] += result["word_count"]
            else:
                results["failed"].append(result)
        
        # Create vector store if we have successful documents
        if all_chunks:
            try:
                self.vector_store = FAISS.from_documents(all_chunks, self.embeddings)
                self.documents = all_chunks
                logger.info(f"Created vector store with {len(all_chunks)} chunks")
            except Exception as e:
                logger.error(f"Error creating vector store: {str(e)}")
                results["vector_store_error"] = str(e)
        
        return results
    
    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """Search for relevant documents using vector similarity."""
        if self.vector_store is None:
            return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return docs
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def get_chat_model(self) -> ChatOpenAI:
        """Create a chat model for AI responses."""
        try:
            llm = ChatOpenAI(
                openai_api_key=self.openai_api_key,
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
            return llm
        except Exception as e:
            logger.error(f"Error creating chat model: {str(e)}")
            return None
    
    def get_context_for_query(self, query: str, k: int = 5) -> str:
        """Get relevant context for a query from the vector store."""
        if self.vector_store is None:
            return ""
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            context = "\n\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
            return ""
    
    def get_document_summary(self) -> Dict[str, Any]:
        """Get a summary of all processed documents."""
        if not self.documents:
            return {"message": "No documents processed"}
        
        summary = {
            "total_documents": len(set(doc.metadata.get("source", "unknown") for doc in self.documents)),
            "total_chunks": len(self.documents),
            "document_sources": list(set(doc.metadata.get("source", "unknown") for doc in self.documents))
        }
        
        return summary
