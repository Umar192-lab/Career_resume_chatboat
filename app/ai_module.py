### ai_module.py (Online GPT-based Q&A)
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career and resume advisor."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"
