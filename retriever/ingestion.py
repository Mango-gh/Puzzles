"""
Simple RAG Ingestion System
Handles PDFs, Markdown files, and web scraping for document processing
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import glob

# Document processing imports
import PyPDF2
from bs4 import BeautifulSoup
import markdown

from openai import OpenAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, EMBEDDING_MODEL

import faiss
import numpy as np


class DocumentIngester:
    """Simple document ingester for RAG systems"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.embedding_model = EMBEDDING_MODEL
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        text += page.extract_text() + "\n"
                    except Exception as e:
                        print(f"Error extracting text from page {i+1}: {e}")
                        continue
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_markdown(self, md_path: str) -> str:
        """Extract text from a Markdown file"""
        try:
            with open(md_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Convert markdown to HTML then extract text
                html = markdown.markdown(content)
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text().strip()
        except Exception as e:
            print(f"Error reading Markdown {md_path}: {e}")
            return ""
    
    def scrape_webpage(self, url: str) -> str:
        """Scrape text content from a webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error scraping webpage {url}: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for better embedding"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size - 100:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def process_document(self, source: str, source_type: str = "auto") -> List[Dict[str, Any]]:
        """Process a document and return text chunks for data collection"""
        # Determine source type if auto
        if source_type == "auto":
            if source.startswith("http"):
                source_type = "web"
            elif source.endswith(".pdf"):
                source_type = "pdf"
            elif source.endswith((".md", ".markdown")):
                source_type = "markdown"
            else:
                raise ValueError(f"Could not determine source type for: {source}")
        
        # Extract text based on source type
        if source_type == "pdf":
            text = self.extract_text_from_pdf(source)
        elif source_type == "markdown":
            text = self.extract_text_from_markdown(source)
        elif source_type == "web":
            text = self.scrape_webpage(source)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        if not text:
            print(f"No text extracted from {source}")
            return []
        
        # Chunk the text
        chunks = self.chunk_text(text)
        
        # Process each chunk
        results = []
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            results.append({
                "source": source,
                "source_type": source_type,
                "chunk_id": i,
                "text": chunk,
                "embedding": embedding
            })
        
        return results
    
    def process_multiple_sources(self, sources: List[str], source_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Process multiple documents"""
        if source_types is None:
            source_types = ["auto"] * len(sources)
        
        all_results = []
        for source, source_type in zip(sources, source_types):
            print(f"Processing {source}...")
            results = self.process_document(source, source_type)
            all_results.extend(results)
        
        return all_results
    
    def process_pdf_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all PDF files in a directory"""
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return []
        
        print(f"Found {len(pdf_files)} PDF files in {directory_path}")
        
        all_results = []
        for pdf_file in pdf_files:
            print(f"Processing: {os.path.basename(pdf_file)}")
            results = self.process_document(pdf_file, "pdf")
            all_results.extend(results)
        
        return all_results
    
    def process_markdown_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all markdown files in a directory"""
        md_files = glob.glob(os.path.join(directory_path, "*.md")) + glob.glob(os.path.join(directory_path, "*.markdown"))
        
        if not md_files:
            print(f"No markdown files found in {directory_path}")
            return []
        
        print(f"Found {len(md_files)} markdown files in {directory_path}")
        
        all_results = []
        for md_file in md_files:
            print(f"Processing: {os.path.basename(md_file)}")
            results = self.process_document(md_file, "markdown")
            all_results.extend(results)
        
        return all_results
    
    def save_to_jsonl(self, results: List[Dict[str, Any]], output_file: str = "collected_documents.jsonl"):
        """Save collected document chunks to JSONL format"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
        print(f"Saved {len(results)} document chunks to {output_file}")
    
    def save_to_faiss(self, results: List[Dict[str, Any]], index_file: str = "embeddings.index"):
        """Save embeddings to FAISS index"""
        if not results:
            return
        
        embeddings = [result["embedding"] for result in results]
        dimension = len(embeddings[0])
        
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        faiss.write_index(index, index_file)
        print(f"Saved {len(embeddings)} embeddings to {index_file}")


def main():
    """Process all PDFs in the pdfs/ folder and websites"""
    ingester = DocumentIngester()
    
    # Process PDFs
    pdf_results = ingester.process_pdf_directory("retriever/pdfs/")
    
    # Process websites
    websites = [
"https://nicoletalkslove.com/how-to-attract-real-love-without-playing-games-or-losing-yourself/"
    ]
    web_results = ingester.process_multiple_sources(websites)
    
    # Process markdown files
    md_results = ingester.process_markdown_directory("retriever/markdowns/")
    
    # Combine all results
    all_results = pdf_results + web_results + md_results
    ingester.save_to_jsonl(all_results)
    ingester.save_to_faiss(all_results)
    
    # Print results
    print(f"\nTotal chunks: {len(all_results)}")
    for i, result in enumerate(all_results[:3]):  # Print first 3
        print(f"\nChunk {i+1}:")
        print(f"Source: {result['source']}")
        print(f"Type: {result['source_type']}")
        print(f"Text: {result['text'][:100]}...")
        print(f"Embedding: {result['embedding'][:5]}...")  # First 5 values


if __name__ == "__main__":
    main()
