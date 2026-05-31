import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from quiz_schema import Quiz
from get_prompt import get_prompt

current_dir = Path(__file__).parent
root_dir = current_dir.parent
load_dotenv(dotenv_path=root_dir / ".env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        f"Nie znaleziono klucza OPENAI_API_KEY w pliku .env w lokalizacji: {root_dir / '.env'}"
    )

client = OpenAI(api_key=api_key)


def generate_quiz(
    chunk: str, question_count: int = 3, difficulty: str = "medium"
) -> Quiz:
    base_prompt = get_prompt()

    prompt = f"""
Generate quiz strictly from this content:
QUESTION_COUNT: {question_count}
DIFFICULTY: {difficulty}

CONTENT:
{chunk}
"""

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": prompt},
        ],
        response_format=Quiz, 
    )

    return response.choices[0].message.parsed