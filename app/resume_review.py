### resume_review.py (Resume checker)
from app.utils import doc_parser

def review_resume(uploaded_file):
    text = doc_parser.extract_text(uploaded_file)

    feedback = []
    if "python" not in text.lower():
        feedback.append("❗ Mention Python if you have experience.")
    if len(text.split()) < 200:
        feedback.append("❗ Your resume seems too short. Add more detail.")
    if "intern" not in text.lower():
        feedback.append("❗ Add internship experience if applicable.")

    return "\n".join(feedback) if feedback else "✅ Your resume looks good!"

