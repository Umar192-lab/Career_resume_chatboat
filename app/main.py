import streamlit as st
from app.career_module import get_career_advice
from app.resume_review import review_resume
from app.ai_module import ai_chat_response
from app.utils.connectivity import is_connected
from app.utils.doc_parser import parse_resume

def main():
    st.set_page_config(page_title="Career & Resume Chatbot", layout="centered")
    st.title("💬 Career & Resume Assistant")

    menu = ["Career Guidance", "Resume Review", "Ask a Question"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    if choice == "Career Guidance":
        st.header("🧭 Career Guidance")
        interests = st.text_input("Enter your interests or skills (comma-separated):")
        if st.button("Suggest Careers"):
            suggestions = get_career_advice(interests)
            st.success("Recommended Careers:")
            for job in suggestions:
                st.write(f"✅ {job}")

    elif choice == "Resume Review":
        st.header("📄 Resume Review")
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file and st.button("Analyze Resume"):
            text = parse_resume(uploaded_file)
            feedback = review_resume(text)
            st.write("📝 Feedback:")
            st.write(feedback)

    elif choice == "Ask a Question":
        st.header("💡 Ask Me Anything")
        query = st.text_input("What's your question?")
        if query and st.button("Get Answer"):
            if is_connected():
                answer = ai_chat_response(query)
                st.success(answer)
            else:
                st.warning("⚠️ No internet connection. GPT support is offline.")

if __name__ == "__main__":
    main()

