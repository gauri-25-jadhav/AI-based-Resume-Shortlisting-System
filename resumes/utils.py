import re
import pdfplumber
import spacy
import re
from collections import Counter
import pdfplumber

STOP_WORDS = {
    "and", "or", "the", "with", "to", "of", "for", "in", "on",
    "a", "an", "is", "are", "as", "by", "from", "this", "that",
    "will", "be", "we", "you", "your", "our", "at","experience", "knowledge", "skills", "required",
    "responsibilities", "years", "ability"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()



# ---------- JD SKILLS ----------
nlp = spacy.load("en_core_web_sm")
def extract_jd_skills(jd_text):
    jd_text = clean_text(jd_text)
    words = jd_text.split()

    # Remove stop words & short words
    keywords = [
        w for w in words
        if w not in STOP_WORDS and len(w) > 2
    ]

    # Count frequency
    freq = Counter(keywords)

    # Take top keywords as "skills"
    skills = [word for word, _ in freq.most_common(15)]

    return skills

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Cleanup
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    return text


# ---------- SCORE ----------
def calculate_score(jd_skills, resume_text):
    resume_text = clean_text(resume_text)
    matched = []
    missing_penalty = 0

    for skill in jd_skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing_penalty += 2
    if not jd_skills:
        return 0, []
    
    # Core score
    skill_match_ratio = len(matched) / max(len(jd_skills), 1)
    score = skill_match_ratio * 70
    # Frequency boost
    freq_bonus = sum(resume_text.count(skill) for skill in matched)
    score += min(freq_bonus * 2, 20)

    # Resume length sanity
    word_count = len(resume_text.split())
    if 300 <= word_count <= 1200:
        score += 10
    # Penalty
    score -= missing_penalty

    return round(min(score, 100), 2), matched

