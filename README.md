# PDF Information Extractor

An AI-based PDF information extractor that processes collections of PDF documents to extract the most relevant sections based on a given persona and job-to-be-done. The system operates entirely offline using CPU-only processing.

## 🏗️ Project Structure

```
project1b/
├── app/                      # Core application code
│   ├── main.py              # Entry point (run this file only)
│   ├── controller.py        # Pipeline orchestration
│   ├── document_reader.py   # PDF text extraction
│   ├── relevance_model.py   # TF-IDF relevance scoring
│   ├── ranker.py           # Section ranking
│   └── summarizer.py       # Text summarization
├── input/                   # Place your PDF files here
├── output/                  # Results will be saved here
├── docs/                    # Documentation
│   └── approach_explanation.md  # Methodology explanation
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Prepare Your PDFs

Place your PDF files in the `input/` directory:

```bash
# Copy your PDF files to the input folder
cp your_documents/*.pdf input/
```

### 2. Run the Application

#### Option A: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main pipeline (this is the ONLY entrypoint)
python app/main.py "<persona>" "<job-to-be-done>"
# Example:
python app/main.py "Student" "Summarize key concepts from chemistry notes"
```

#### Option B: Docker (Recommended for deployment/submission)

```bash
# Build the Docker image
docker build -t pdf-extractor .

# Run with volume mounting
docker run -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output pdf-extractor "<persona>" "<job-to-be-done>"
# Example:
docker run -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output pdf-extractor "Student" "Summarize key concepts from chemistry notes"
```

### 3. View Results

Results are automatically saved to `output/results.json`:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "Student",
    "job_to_be_done": "Summarize key concepts",
    "processing_timestamp": "2025-07-26T10:40:31.913735"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Introduction to Chemistry",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Chemistry is the study of matter...",
      "page_number": 1
    }
  ]
}
```

## 📋 Usage Notes

- **Only run `app/main.py`**. Do not run any other scripts.
- **Input PDFs**: Place all your dataset PDFs in the `input/` folder before running.
- **Output**: Results will always be in `output/results.json`.
- **No test scenarios or test scripts are included**—the pipeline will process whatever PDFs you provide.

## 🏛️ Architecture

The system consists of modular components:

- **`document_reader.py`**: PDF text extraction and chunking
- **`relevance_model.py`**: TF-IDF based semantic similarity scoring
- **`ranker.py`**: Section ranking based on relevance scores
- **`summarizer.py`**: Text summarization for extracted sections
- **`controller.py`**: Main pipeline orchestration

## ⚡ Technical Specifications

- **Offline Operation**: No internet connection required
- **CPU-Only**: No GPU dependencies
- **Model Size**: ~50MB total (well under 1GB limit)
- **Processing Time**: ~4-5 seconds (well under 60s limit)
- **Memory Usage**: Optimized for CPU-only operation

## 🔧 Troubleshooting

### Common Issues

1. **No PDFs Found**
   ```
   [ERROR] No PDF files found in 'input'!
   ```
   - Ensure PDF files are in the `input/` directory
   - Check file extensions are `.pdf` (lowercase)

2. **PDF Reading Errors**
   ```
   [ERROR] Failed to open PDF file.pdf
   ```
   - Verify PDF is not corrupted
   - Ensure PDF contains extractable text (not just images)

3. **Empty Results**
   ```
   [ERROR] No text chunks extracted from PDFs!
   ```
   - Check if PDFs have sufficient text content
   - Verify PDFs are not password-protected

### Performance Tips

- **Large PDFs**: System processes first 10 pages only
- **Many PDFs**: Maximum 50 chunks processed for performance
- **Complex Layouts**: System works best with text-heavy documents

## 📚 Documentation

- **`docs/approach_explanation.md`**: Detailed methodology and technical approach

## 🎯 Hackathon Submission

Your solution is ready for submission! The project includes:

1. ✅ **Complete Implementation**: All required functionality
2. ✅ **Docker Support**: Containerized deployment
3. ✅ **Documentation**: Detailed approach explanation
4. ✅ **Performance Compliance**: Meets all constraints

## 📄 License

This project is developed for hackathon purposes. See individual component licenses for dependencies. 