from variables import GEMENI_KEY
import google.generativeai as genai

genai.configure(api_key=GEMENI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def generate_answer(text):
    response = model.generate_content(text)
    return response.text