from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class RelevanceModel:
    def __init__(self):
        print("[INFO] Initializing TF-IDF relevance model...")
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.9
        )
        self.is_fitted = False
        print("[INFO] TF-IDF model initialized successfully")

    def _preprocess_text(self, text):
        """Clean and preprocess text for better matching."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def score(self, query, chunks):
        try:
            if not chunks:
                print("[WARNING] No chunks provided for scoring")
                return np.zeros(0)
            
            # Preprocess query
            query = self._preprocess_text(query)
            if not query:
                print("[WARNING] Empty query after preprocessing")
                return np.zeros(len(chunks))
            
            # Preprocess chunk texts
            chunk_texts = []
            for chunk in chunks:
                text = chunk.get("text", "").strip()
                processed_text = self._preprocess_text(text)
                chunk_texts.append(processed_text)
            
            # Remove empty texts
            valid_texts = [text for text in chunk_texts if text]
            if not valid_texts:
                print("[WARNING] No valid texts found after preprocessing")
                return np.zeros(len(chunks))
            
            # Fit vectorizer if not already fitted
            if not self.is_fitted:
                self.vectorizer.fit(valid_texts)
                self.is_fitted = True
            
            # Transform texts to TF-IDF vectors
            chunk_vectors = self.vectorizer.transform(chunk_texts)
            query_vector = self.vectorizer.transform([query])
            
            # Calculate cosine similarity
            scores = cosine_similarity(query_vector, chunk_vectors)[0]
            
            print(f"[INFO] Calculated relevance scores for {len(chunks)} chunks")
            return scores
            
        except Exception as e:
            print(f"[ERROR] Failed to calculate relevance scores: {e}")
            return np.zeros(len(chunks))
