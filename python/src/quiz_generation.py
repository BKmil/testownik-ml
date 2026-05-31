from openai import OpenAI
from quiz_schema import Quiz
from get_prompt import get_prompt

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_quiz(
        chunk: str,
        question_count: int = 3,
        difficulty: str = "medium"
        ) -> Quiz:
    base_prompt = get_prompt()

    prompt = f"""
Generate quiz strictly from this content:
QUESTION_COUNT: {question_count}
DIFFICULTY: {difficulty}

CONTENT:
{chunk}
"""

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[{"role": "system", "content": base_prompt},
               {"role": "user", "content": prompt}],
        text_format=Quiz
    )

    return response.output_parsed
