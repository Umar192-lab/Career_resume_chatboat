
import json

def load_career_data():
    with open("data/career_data.json", "r") as file:
        data = json.load(file)
    return data

def get_career_advice(interests):
    if not interests:
        return ["Please enter your interests to get suggestions."]

    user_keywords = [i.strip().lower() for i in interests.split(",")]
    career_data = load_career_data()
    suggestions = []

    for career, skills in career_data.items():
        score = sum(skill.lower() in user_keywords for skill in skills)
        if score > 0:
            suggestions.append((career, score))

    suggestions.sort(key=lambda x: x[1], reverse=True)
    top_careers = [career for career, _ in suggestions[:5]]  # top 5 matches

    return top_careers if top_careers else ["No matching careers found. Try different keywords."]
