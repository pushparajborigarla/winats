import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_keywords(text):
    return list(set(re.findall(r'\b[a-zA-Z]+\b', text.lower())))

def classify_keywords(jd):
    must, optional = [], []
    for line in jd.lower().split("\n"):
        if "must" in line or "required" in line:
            must += extract_keywords(line)
        else:
            optional += extract_keywords(line)
    return list(set(must)), list(set(optional))

def semantic_score(resume, jd):
    emb1 = model.encode([resume])
    emb2 = model.encode([jd])
    return cosine_similarity(emb1, emb2)[0][0] * 100

def calculate_ats(resume, jd):
    must, optional = classify_keywords(jd)
    must_matched = [k for k in must if k in resume.lower()]
    optional_matched = [k for k in optional if k in resume.lower()]

    keyword_score = (len(optional_matched)/(len(optional)+1))*100
    must_score = (len(must_matched)/(len(must)+1))*100
    similarity = semantic_score(resume, jd)

    final_score = (
        0.25 * keyword_score +
        0.25 * similarity +
        0.20 * must_score +
        0.15 * 80 +
        0.10 * min(len(optional_matched)*5,100) +
        0.05 * 80
    )

    if len(must) > 0 and len(must_matched) < len(must)/2:
        final_score -= 15

    return {
        "score": round(min(final_score,100),2),
        "must_missing": list(set(must)-set(must_matched)),
        "matched": optional_matched
    }
