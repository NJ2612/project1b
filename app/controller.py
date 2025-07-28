import os
import json
import time
from datetime import datetime
from document_reader import extract_text_from_pdfs
from relevance_model import RelevanceModel
from ranker import rank_sections
from summarizer import summarize_section

# Use relative paths that work in Docker
INPUT_DIR = "/code/input_pdfs"
OUTPUT_PATH = "/code/output/results.json"


MAX_CHUNKS = 1000  # increased cap for performance


def run_pipeline(persona, job_to_be_done):
    start = time.time()
    
    print(f"[INFO] Starting pipeline for persona: {persona}")
    print(f"[INFO] Job to be done: {job_to_be_done}")
    print(f"[INFO] Looking for PDFs in: {INPUT_DIR}")
    
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"[ERROR] Input directory '{INPUT_DIR}' not found!")
        return
    
    # Get PDF files
    documents = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    if not documents:
        print(f"[ERROR] No PDF files found in '{INPUT_DIR}'!")
        return
    
    print(f"[INFO] Found {len(documents)} PDF documents: {documents}")
    print(f"[DEBUG] Documents list: {documents}")
    
    # Extract text chunks
    try:
        full_text_chunks = extract_text_from_pdfs(documents, INPUT_DIR, max_pages=10)
        if not full_text_chunks:
            print("[ERROR] No text chunks extracted from PDFs!")
            return
            
        print(f"[DEBUG] Number of chunks before capping: {len(full_text_chunks)}")
        full_text_chunks = full_text_chunks[:MAX_CHUNKS]
        print(f"[INFO] Loaded {len(full_text_chunks)} chunks from {len(documents)} documents")
        
    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDFs: {e}")
        return

    # Initialize relevance model
    try:
        model = RelevanceModel()
        print("[INFO] Relevance model initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize relevance model: {e}")
        return

    # Rank sections
    try:
        ranked = rank_sections(full_text_chunks, model, persona, job_to_be_done)
        print(f"[INFO] Ranked {len(ranked)} sections")
    except Exception as e:
        print(f"[ERROR] Failed to rank sections: {e}")
        return

    # Extract top sections
    extracted_sections = []
    subsection_analysis = []
    
    for i, sec in enumerate(ranked[:10]):
        try:
            summary = summarize_section(sec["text"])
            extracted_sections.append({
                "document": sec["document"],
                "section_title": sec.get("title", "Untitled Section"),
                "importance_rank": i + 1,
                "page_number": sec["page"]
            })
            subsection_analysis.append({
                "document": sec["document"],
                "refined_text": summary,
                "page_number": sec["page"]
            })
        except Exception as e:
            print(f"[WARNING] Failed to process section {i}: {e}")
            continue

    # Create result
    result = {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    # Write output
    try:
        os.makedirs("output", exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("[✓] Extraction complete. Output written to", OUTPUT_PATH)
        print("Total Time:", round(time.time() - start, 2), "s")
    except Exception as e:
        print(f"[ERROR] Failed to write output: {e}")
