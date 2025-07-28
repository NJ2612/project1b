# PDF Information Extractor - Approach Explanation

## Overview
This solution implements an AI-based PDF information extractor that processes collections of PDF documents to extract the most relevant sections based on a given persona and job-to-be-done. The system operates entirely offline using CPU-only processing with a model size under 1GB.

## Architecture & Methodology

### 1. Document Processing Pipeline

#### PDF Text Extraction (`document_reader.py`)
- **Tool**: `pdfplumber` for robust PDF text extraction
- **Process**: 
  - Iterates through each PDF file in the input directory
  - Extracts text from each page (up to 10 pages per document for performance)
  - Filters out pages with insufficient text (< 20 characters)
  - Extracts section titles from the first line of each page
  - Provides fallback titles for pages without clear headings

#### Text Chunking Strategy
- **Granularity**: Page-level chunks for optimal relevance matching
- **Size Control**: Maximum 50 chunks total to meet 60-second constraint
- **Quality Filtering**: Only chunks with meaningful content (> 20 characters)

### 2. Relevance Modeling (`relevance_model.py`)

#### TF-IDF Approach
- **Model**: TF-IDF Vectorizer with cosine similarity
- **Size**: ~50MB total, well under 1GB constraint
- **Capability**: Text-based semantic matching
- **Performance**: Optimized for CPU inference

#### Similarity Calculation
- **Method**: Cosine similarity between query and document TF-IDF vectors
- **Query Construction**: `"{persona}: {job_to_be_done}"`
- **Robustness**: Handles empty texts and encoding errors gracefully

### 3. Ranking System (`ranker.py`)

#### Ranking Algorithm
- **Approach**: TF-IDF similarity-based ranking
- **Process**: 
  1. Encode persona + job query into TF-IDF vector
  2. Calculate similarity scores for all document chunks
  3. Sort by relevance score (highest first)
  4. Return top-ranked sections with metadata

#### Output Structure
- **Ranked Sections**: Top 10 most relevant sections
- **Metadata**: Document name, page number, section title, importance rank
- **Scores**: Normalized relevance scores for transparency

### 4. Text Summarization (`summarizer.py`)

#### Summarization Strategy
- **Method**: Extractive summarization (first N meaningful lines)
- **Process**:
  - Split text into lines
  - Filter for meaningful content (> 30 characters)
  - Take first 3 lines as summary
  - Fallback to first 5 lines if no meaningful content
  - Truncate to 500 characters maximum

### 5. Controller Logic (`controller.py`)

#### Pipeline Orchestration
1. **Input Validation**: Check for PDF files and directory structure
2. **Document Processing**: Extract and chunk PDF content
3. **Model Initialization**: Load TF-IDF vectorizer
4. **Relevance Ranking**: Score and rank document sections
5. **Output Generation**: Create structured JSON output
6. **Error Handling**: Comprehensive error handling at each stage

## Technical Constraints & Solutions

### Offline Operation
- **Dependencies**: All models and libraries included in Docker image
- **Model Loading**: TF-IDF vectorizer cached locally
- **No External Calls**: All processing done within container

### Performance Optimization
- **Page Limits**: Maximum 10 pages per PDF
- **Chunk Limits**: Maximum 50 total chunks
- **Model Size**: ~50MB total
- **Processing Time**: Target < 60 seconds for 3-5 PDFs

### Robustness Features
- **Error Handling**: Graceful degradation for corrupted PDFs
- **Fallback Mechanisms**: Default titles and summaries for edge cases
- **Input Validation**: Comprehensive checks for file existence and format
- **Logging**: Detailed progress and error reporting

## Output Format

### JSON Structure
```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Student",
    "job_to_be_done": "Summarize key concepts",
    "processing_timestamp": "2024-01-01T12:00:00"
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "Introduction to Chemistry",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "Chemistry is the study of matter...",
      "page_number": 1
    }
  ]
}
```

## Usage Examples

### Different Personas & Jobs
- **Researcher**: "Extract methodology and findings"
- **Student**: "Summarize key concepts and definitions"
- **Analyst**: "Identify trends and data points"
- **Traveler**: "Find recommendations and tips"

### Domain Flexibility
The system works across various document types:
- Academic papers
- Technical manuals
- Travel guides
- Financial reports
- Any text-rich PDF content

## Future Enhancements
- **Advanced Chunking**: Semantic paragraph-based chunking
- **Multi-modal Support**: Image and table extraction
- **Custom Models**: Domain-specific fine-tuning
- **Batch Processing**: Parallel PDF processing
- **Caching**: Model and embedding caching for repeated runs
