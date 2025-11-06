"""
Utility functions for Kelly chatbot
"""
import re


def extract_topics(text: str, max_keep: int = 6) -> list:
    """
    Extract key topics from user query for context
    
    Args:
        text: User input text
        max_keep: Maximum number of topics to keep
        
    Returns:
        List of extracted topic keywords
    """
    # Clean text
    t = re.sub(r"http[s]?://\S+", "", text.lower())
    t = re.sub(r"[^a-z0-9\s\-\_\+\.]", " ", t)
    words = [w for w in re.split(r"\s+", t) if w]
    
    # Stop words
    stop = set("""
        a an the and or but if is are was were be been to of in on for with from at by as into over under
        about across within without not no yes true false can could should would may might will do does did
        this that these those you your yours me my mine their our ours they them we us i it its
    """.split())
    
    # Filter candidates
    cands = [w for w in words if w not in stop and len(w) > 2]
    
    # Count frequency
    freq = {}
    for w in cands:
        freq[w] = freq.get(w, 0) + 1
    
    # Rank by frequency and length
    ranked = sorted(freq.items(), key=lambda x: (-x[1], -len(x[0]), x[0]))
    keep = [w for w, _ in ranked[:max_keep]]
    
    return keep
