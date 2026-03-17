from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

async def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт по логистике КИТАЙСКИЙ ПАРТНЕР"},
                {"role": "user", "content": question}
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except:
        return False