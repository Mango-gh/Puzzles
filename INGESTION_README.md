# Document Data Collection System

A simple document ingestion system for collecting and processing data from PDFs, Markdown files, and web pages. This system focuses on data collection and text extraction without generating embeddings.

## Features

- **PDF Processing**: Extract text from PDF documents using PyPDF2
- **Markdown Processing**: Parse Markdown files and extract clean text
- **Web Scraping**: Scrape content from web pages with BeautifulSoup
- **Text Chunking**: Split documents into overlapping chunks for better processing
- **Data Collection**: Collect and organize text data without embeddings
- **JSONL Output**: Save collected document chunks in JSONL format for easy loading

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Note: No API keys required for data collection - this system only extracts and processes text data.

## Usage

### Basic Usage

```python
from ingestion import DocumentIngester

# Initialize the ingester
ingester = DocumentIngester()

# Process a single document
results = ingester.process_document("path/to/document.pdf", "pdf")

# Process multiple documents
sources = [
    "document.pdf",
    "README.md", 
    "https://example.com"
]
results = ingester.process_multiple_sources(sources)

# Save results
ingester.save_to_jsonl(results, "collected_data.jsonl")
```

### Supported Source Types

- **PDF**: `"pdf"` - Processes PDF files
- **Markdown**: `"markdown"` - Processes .md and .markdown files  
- **Web**: `"web"` - Scrapes web pages
- **Auto**: `"auto"` - Automatically detects source type based on file extension or URL

### Example Output

Each collected chunk includes:
```json
{
    "source": "path/to/document.pdf",
    "source_type": "pdf",
    "chunk_id": 0,
    "text": "Extracted text content...",
    "chunk_size": 856
}
```

## Configuration

No special configuration required - the system works out of the box for data collection.

## Running Examples

```bash
# Run the main ingestion script
python ingestion.py

# Run the example script
python example_ingestion.py
```

## Customization

You can customize the chunking behavior by modifying the `chunk_text` method:
- `chunk_size`: Maximum characters per chunk (default: 1000)
- `overlap`: Character overlap between chunks (default: 200)

## Error Handling

The system includes robust error handling for:
- File not found errors
- Network timeouts for web scraping
- PDF parsing errors
- Markdown parsing errors

All errors are logged to console and processing continues with other documents.
