import os
import json
from uuid import uuid4

from pdf_reading import read_pdf, check_file_size
from chunking import chunk_by_tokens
from quiz_generation import generate_quiz


def fix_quiz(quiz: dict) -> dict:
    return {
        **quiz,
        "questions": [
            {
                **q,
                "id": str(uuid4()),
                "order": i+1,
                "answers": [
                    {
                        **a,
                        "id": str(uuid4()),
                        "order": j+1,
                    }
                    for j, a in enumerate(q["answers"])
                ],
            }
            for i, q in enumerate(quiz["questions"])
        ],
    }


def run():
    file_path = "./src/files/test2.pdf"

    # pdf size check
    check_file_size(file_path)

    # PDF -> text
    text = read_pdf(file_path)

    # cleanup + split
    blocks = [
        b.strip()
        for b in text.replace("\r", "").split("\n\n")
        if b.strip()
        ]

    # chunking
    chunks = chunk_by_tokens(blocks)

    TARGET_QUESTIONS = 10
    DIFFICULTY = "hard"
    total_chunks = len(chunks)

    if total_chunks == 0:
        print("Brak treści do przetworzenia.")
        return

    all_questions = []

    base_questions_per_chunk = TARGET_QUESTIONS // total_chunks
    leftovers = TARGET_QUESTIONS % total_chunks

    for i, chunk in enumerate(chunks):
        questions_to_generate = base_questions_per_chunk

        if leftovers > 0:
            questions_to_generate += 1
            leftovers -= 1

        if questions_to_generate == 0:
            continue

        quiz = generate_quiz(chunk["text"], questions_to_generate, DIFFICULTY)

        quiz_dict = quiz.model_dump() if hasattr(quiz, "model_dump") else quiz
        questions = quiz_dict.get("questions", [])
        all_questions.extend(questions)

    raw_quiz = {
        "title": "Generated Quiz",
        "description": "Quiz generated from PDF content.",
        "version": "1.0",
        "questions": all_questions,
    }

    final_quiz = fix_quiz(raw_quiz)

    dir_path = "./src/files"
    output_path = os.path.join(dir_path, "generated_quiz.json")

    os.makedirs(dir_path, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_quiz, f, ensure_ascii=False, indent=2)

    print(f"Quiz generated and saved to {output_path}")


if __name__ == "__main__":
    run()
