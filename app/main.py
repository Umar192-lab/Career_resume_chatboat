import streamlit as st
from app import career_module, resume_review, ai_module
from app.utils import connectivity

def main():
    st.set_page_config(page_title="Career & Resume Assistant", layout="centered")
    st.title("🤖 Career and Resume Chatbot")

    options = ["Career Guidance", "Resume Review", "Ask AI"]
    choice = st.sidebar.selectbox("Choose an option", options)

    online = connectivity.check_internet()

    if choice == "Career Guidance":
        interests = st.text_input("Enter your interests (comma separated):")
        if st.button("Suggest Careers") and interests:
            suggestions = career_module.suggest_careers(interests)
            st.write("### Suggested Careers:")
            for career in suggestions:
                st.success(career)

    elif choice == "Resume Review":
        uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file and st.button("Review Resume"):
            feedback = resume_review.review_resume(uploaded_file)
            st.write("### Resume Feedback:")
            st.info(feedback)

    elif choice == "Ask AI":
        if online:
            query = st.text_area("Ask any career or resume related question:")
            if st.button("Get Answer") and query:
                response = ai_module.ask_ai(query)
                st.write("### AI Response:")
                st.write(response)
        else:
            st.error("Internet is required for this feature.")

if __name__ == '__main__':
    main()
