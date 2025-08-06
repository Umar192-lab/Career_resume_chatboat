import streamlit as st
import json
import os
from datetime import datetime
from career_module import CareerGuidance
from resume_review import ResumeReviewer
from utils.connectivity import check_internet_connection
from utils.doc_parser import DocumentParser

# Configure Streamlit page
st.set_page_config(
    page_title="Career & Resume Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'career_guidance' not in st.session_state:
    st.session_state.career_guidance = CareerGuidance()
if 'resume_reviewer' not in st.session_state:
    st.session_state.resume_reviewer = ResumeReviewer()

def add_to_chat(role, message):
    """Add message to chat history"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "role": role,
        "message": message,
        "timestamp": timestamp
    })

def display_chat_history():
    """Display chat history"""
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.chat_message("user").write(f"**You ({chat['timestamp']}):** {chat['message']}")
        else:
            st.chat_message("assistant").write(f"**Bot ({chat['timestamp']}):** {chat['message']}")

def main():
    st.title("🤖 Career & Resume Bot")
    st.markdown("Your AI-powered career guidance and resume review assistant")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Features")
        feature = st.radio(
            "Choose a feature:",
            ["💬 Chat with Bot", "🎯 Career Guidance", "📄 Resume Review", "📊 Skills Assessment"]
        )
        
        # Connection status
        is_connected = check_internet_connection()
        if is_connected:
            st.success("🌐 Online - Enhanced features available")
        else:
            st.warning("📴 Offline - Basic features only")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    if feature == "💬 Chat with Bot":
        st.header("💬 Chat with Career Bot")
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("Chat History")
            display_chat_history()
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("Ask me anything about careers, resumes, or job search:", 
                                    placeholder="e.g., What skills do I need for data science?", 
                                    height=100)
            submitted = st.form_submit_button("Send 📤")
            
            if submitted and user_input.strip():
                add_to_chat("user", user_input)
                
                # Generate response based on query type
                response = generate_bot_response(user_input)
                add_to_chat("assistant", response)
                st.rerun()
    
    elif feature == "🎯 Career Guidance":
        st.header("🎯 Career Guidance")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Find Your Career Path")
            skills_input = st.text_area("Enter your skills (comma-separated):", 
                                      placeholder="Python, Data Analysis, Machine Learning")
            interests_input = st.text_area("Enter your interests:", 
                                         placeholder="Technology, Problem Solving, Analytics")
            
            if st.button("Get Career Suggestions 🚀"):
                if skills_input:
                    skills = [skill.strip() for skill in skills_input.split(',')]
                    suggestions = st.session_state.career_guidance.suggest_careers(skills, interests_input)
                    
                    with col2:
                        st.subheader("Career Recommendations")
                        for i, career in enumerate(suggestions, 1):
                            with st.expander(f"{i}. {career['title']} (Match: {career['match_score']:.0%})"):
                                st.write(f"**Description:** {career['description']}")
                                st.write(f"**Required Skills:** {', '.join(career['required_skills'])}")
                                st.write(f"**Average Salary:** {career['salary_range']}")
                                st.write(f"**Growth Outlook:** {career['growth_outlook']}")
    
    elif feature == "📄 Resume Review":
        st.header("📄 Resume Review")
        
        uploaded_file = st.file_uploader("Upload your resume", 
                                       type=['pdf', 'docx'],
                                       help="Supported formats: PDF, DOCX")
        
        if uploaded_file:
            try:
                # Parse document
                doc_parser = DocumentParser()
                resume_text = doc_parser.extract_text(uploaded_file)
                
                if resume_text:
                    st.success("Resume uploaded successfully!")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("Resume Content Preview")
                        st.text_area("Extracted Text:", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text, height=200)
                        
                        if st.button("Analyze Resume 🔍"):
                            analysis = st.session_state.resume_reviewer.analyze_resume(resume_text)
                            
                            with col2:
                                st.subheader("Resume Analysis")
                                
                                # Overall score
                                score = analysis.get('overall_score', 0)
                                st.metric("Overall Score", f"{score}/100")
                                
                                # Strengths
                                if analysis.get('strengths'):
                                    st.write("**✅ Strengths:**")
                                    for strength in analysis['strengths']:
                                        st.write(f"• {strength}")
                                
                                # Improvements
                                if analysis.get('improvements'):
                                    st.write("**⚠️ Areas for Improvement:**")
                                    for improvement in analysis['improvements']:
                                        st.write(f"• {improvement}")
                                
                                # Missing sections
                                if analysis.get('missing_sections'):
                                    st.write("**❌ Missing Sections:**")
                                    for section in analysis['missing_sections']:
                                        st.write(f"• {section}")
                else:
                    st.error("Could not extract text from the uploaded file.")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    elif feature == "📊 Skills Assessment":
        st.header("📊 Skills Assessment")
        
        st.write("Take a quick assessment to identify your skill gaps and career readiness.")
        
        # Technical Skills
        st.subheader("Technical Skills")
        tech_skills = {}
        common_tech_skills = ["Python", "JavaScript", "SQL", "Data Analysis", "Machine Learning", 
                            "Web Development", "Cloud Computing", "Cybersecurity"]
        
        for skill in common_tech_skills:
            tech_skills[skill] = st.select_slider(
                f"{skill}",
                options=["Beginner", "Intermediate", "Advanced", "Expert"],
                value="Beginner"
            )
        
        # Soft Skills
        st.subheader("Soft Skills")
        soft_skills = {}
        common_soft_skills = ["Communication", "Leadership", "Problem Solving", "Teamwork", 
                            "Time Management", "Adaptability"]
        
        for skill in common_soft_skills:
            soft_skills[skill] = st.select_slider(
                f"{skill}",
                options=["Poor", "Fair", "Good", "Excellent"],
                value="Fair"
            )
        
        if st.button("Generate Skills Report 📊"):
            # Generate skills assessment report
            assessment_result = generate_skills_assessment(tech_skills, soft_skills)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Your Skills Profile")
                st.json(assessment_result['profile'])
            
            with col2:
                st.subheader("Recommendations")
                for rec in assessment_result['recommendations']:
                    st.write(f"• {rec}")

def generate_bot_response(user_input):
    """Generate contextual bot response"""
    user_input_lower = user_input.lower()
    
    # Career guidance queries
    if any(word in user_input_lower for word in ['career', 'job', 'profession', 'work']):
        if 'data' in user_input_lower:
            return "Data-related careers are in high demand! Consider roles like Data Scientist, Data Analyst, or Machine Learning Engineer. Key skills include Python, SQL, statistics, and domain expertise. Would you like specific guidance on any of these paths?"
        elif 'software' in user_input_lower or 'programming' in user_input_lower:
            return "Software development offers diverse opportunities! Popular paths include Frontend Development (React, Vue.js), Backend Development (Python, Java, Node.js), or Full-Stack Development. What type of applications interest you most?"
        else:
            return "I can help you explore various career paths! To provide better guidance, could you tell me about your skills, interests, or the industry you're curious about?"
    
    # Resume queries
    elif any(word in user_input_lower for word in ['resume', 'cv', 'application']):
        return "Great resume tips: 1) Use action verbs and quantify achievements, 2) Tailor it to each job, 3) Keep it concise (1-2 pages), 4) Include relevant keywords, 5) Proofread carefully. Would you like me to review your resume or help with a specific section?"
    
    # Skills queries
    elif any(word in user_input_lower for word in ['skill', 'learn', 'training']):
        return "Skill development is key to career growth! Popular in-demand skills include: Programming (Python, JavaScript), Data Analysis, Cloud Computing (AWS, Azure), and Soft Skills (Communication, Leadership). What area interests you most?"
    
    # Interview queries
    elif any(word in user_input_lower for word in ['interview', 'preparation']):
        return "Interview preparation tips: 1) Research the company thoroughly, 2) Practice common questions, 3) Prepare STAR method examples, 4) Ask thoughtful questions, 5) Follow up professionally. Need help with specific interview scenarios?"
    
    # Salary/compensation queries
    elif any(word in user_input_lower for word in ['salary', 'pay', 'compensation', 'money']):
        return "Salary research is important! Use sites like Glassdoor, PayScale, or LinkedIn Salary Insights. Consider factors like location, experience, company size, and industry. Remember to negotiate based on your value and market rates. What role are you researching?"
    
    # General greeting
    elif any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'start']):
        return "Hello! I'm your Career & Resume Bot. I can help with career guidance, resume reviews, skill assessments, interview preparation, and job search strategies. What would you like to explore today?"
    
    # Default response
    else:
        return "I'd be happy to help! I specialize in career guidance, resume reviews, skill development, and job search strategies. Could you provide more details about what you're looking for assistance with?"

def generate_skills_assessment(tech_skills, soft_skills):
    """Generate skills assessment report"""
    # Calculate skill levels
    tech_score = sum([["Beginner", "Intermediate", "Advanced", "Expert"].index(level) + 1 for level in tech_skills.values()])
    soft_score = sum([["Poor", "Fair", "Good", "Excellent"].index(level) + 1 for level in soft_skills.values()])
    
    # Generate recommendations
    recommendations = []
    
    if tech_score < len(tech_skills) * 2:
        recommendations.append("Focus on building foundational technical skills through online courses")
    if soft_score < len(soft_skills) * 2:
        recommendations.append("Develop soft skills through practice and feedback")
    
    recommendations.extend([
        "Consider building a portfolio to showcase your skills",
        "Join professional networks and communities in your field",
        "Seek mentorship or coaching for career development"
    ])
    
    return {
        'profile': {
            'technical_skills': tech_skills,
            'soft_skills': soft_skills,
            'tech_score': f"{tech_score}/{len(tech_skills) * 4}",
            'soft_score': f"{soft_score}/{len(soft_skills) * 4}"
        },
        'recommendations': recommendations
    }

if __name__ == "__main__":
    main()

