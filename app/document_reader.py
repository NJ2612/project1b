import os
import pdfplumber
import logging

def extract_text_from_pdfs(filenames, folder, max_pages=10):
    chunks = []
    
    for file in filenames:
        path = os.path.join(folder, file)
        print(f"[INFO] Processing PDF: {file}")
        
        try:
            with pdfplumber.open(path) as pdf:
                total_pages = len(pdf.pages)
                print(f"[INFO] PDF has {total_pages} pages, processing up to {max_pages}")
                
                for i, page in enumerate(pdf.pages[:max_pages]):
                    try:
                        text = page.extract_text()
                        if text and len(text.strip()) > 20:
                            # Extract title from first line or use fallback
                            lines = text.split("\n")
                            title = lines[0].strip() if lines and lines[0].strip() else f"Page {i+1}"
                            
                            # Clean up title if it's too long
                            if len(title) > 100:
                                title = title[:97] + "..."
                            
                            chunks.append({
                                "document": file,
                                "page": i + 1,
                                "title": title,
                                "text": text.strip()
                            })
                            print(f"[INFO] Extracted chunk from {file} page {i+1}")
                        else:
                            print(f"[WARNING] Page {i+1} in {file} has insufficient text")
                            
                    except Exception as e:
                        print(f"[WARNING] Failed to extract text from page {i+1} in {file}: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] Failed to open PDF {file}: {e}")
            continue
    
    print(f"[INFO] Successfully extracted {len(chunks)} text chunks from {len(filenames)} PDFs")
    return chunks