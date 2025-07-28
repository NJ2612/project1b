import re

def summarize_section(text, max_lines=3):
    try:
        if not text or not text.strip():
            return "No content available"
        
        # Clean and split text into lines
        lines = re.split(r'[\n\r]+', text.strip())
        lines = [line.strip() for line in lines if line.strip()]
        
        # Filter lines by minimum length and remove very short lines
        meaningful_lines = [line for line in lines if len(line) > 30]
        
        if not meaningful_lines:
            # Fallback: take first few lines regardless of length
            meaningful_lines = lines[:5]
        
        # Take first max_lines and join
        summary_lines = meaningful_lines[:max_lines]
        summary = " ".join(summary_lines)
        
        # Truncate if too long
        if len(summary) > 500:
            summary = summary[:497] + "..."
        
        return summary
        
    except Exception as e:
        print(f"[WARNING] Failed to summarize text: {e}")
        return "Summary unavailable"
