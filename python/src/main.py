import json
import os
from uuid import uuid4

from chunking import chunk_by_tokens
from pdf_reading import read_pdf
from quiz_generation import generate_quiz


def fix_quiz(quiz: dict) -> dict:
    return {
        **quiz,
        "questions": [
            {
                **q,
                "id": str(uuid4()),
                "order": i + 1,
                "answers": [
                    {
                        **a,
                        "id": str(uuid4()),
                        "order": j + 1,
                    }
                    for j, a in enumerate(q["answers"])
                ],
            }
            for i, q in enumerate(quiz["questions"])
        ],
    }


def run():
    text = read_pdf("./src/files/test2.pdf")

    blocks = [
        b.strip() for b in text.replace("\r", "").split("\n\n") if b.strip()
    ]

    chunks = chunk_by_tokens(blocks)

    TARGET_QUESTIONS = 5
    DIFFICULTY = "hard"
    total_chunks = len(chunks)

    all_questions = []

    base_per_chunk = TARGET_QUESTIONS // total_chunks
    leftovers = TARGET_QUESTIONS % total_chunks

    print(
        f"Rozpoczynam generowanie. Znaleziono chunków: {total_chunks}. Łączna liczba pytań: {TARGET_QUESTIONS}."
    )

    for i, chunk in enumerate(chunks):
        questions_to_generate = base_per_chunk

        if leftovers > 0:
            questions_to_generate += 1
            leftovers -= 1

        if questions_to_generate == 0:
            continue

        print(
            f"-> Generuję {questions_to_generate} pytań dla chunku {i+1}/{total_chunks}..."
        )

        chunk_quiz = generate_quiz(chunk["text"], questions_to_generate, DIFFICULTY)

        for q in chunk_quiz.questions:
            all_questions.append(q.model_dump())

    quiz_dict = {
        "title": "Wygenerowany Quiz",
        "description": "Quiz wygenerowany automatycznie z podziałem na chunki.",
        "version": 1,
        "questions": all_questions,
    }

    fixed_quiz = fix_quiz(quiz_dict)

    dir_path = "src/files"
    file_path = os.path.join(dir_path, "generated_quiz.json")

    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(fixed_quiz, f, ensure_ascii=False, indent=2)

    print(f"Sukces! Quiz został zapisany w: {file_path}")


if __name__ == "__main__":
    run()
