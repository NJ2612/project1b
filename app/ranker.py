def rank_sections(chunks, model, persona, job):
    try:
        if not chunks:
            print("[WARNING] No chunks provided for ranking")
            return []
        
        # Create query from persona and job
        query = f"{persona}: {job}"
        print(f"[INFO] Ranking with query: {query}")
        
        # Get relevance scores
        scores = model.score(query, chunks)
        
        if len(scores) != len(chunks):
            print(f"[ERROR] Score count ({len(scores)}) doesn't match chunk count ({len(chunks)})")
            return []
        
        # Rank by score (highest first)
        ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
        
        # Convert to list of dictionaries with scores
        result = []
        for i, (chunk, score) in enumerate(ranked):
            result.append({
                **chunk,
                "score": float(score),
                "rank": i + 1
            })
        
        print(f"[INFO] Successfully ranked {len(result)} sections")
        return result
        
    except Exception as e:
        print(f"[ERROR] Failed to rank sections: {e}")
        return []
