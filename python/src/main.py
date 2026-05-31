import os
import json
from uuid import uuid4

from pdf_reading import read_pdf
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
    # PDF -> text
    text = read_pdf("./src/files/test2.pdf")

    # cleanup + split
    blocks = [
        b.strip()
        for b in text.replace("\r", "").split("\n\n")
        if b.strip()
        ]

    # chunking
    chunks = chunk_by_tokens(blocks)

    full_content = "\n\n".join(c["text"] for c in chunks)

    # quiz generation
    quiz = generate_quiz(full_content, 5, "hard")

    # pydantic -> dict
    quiz_dict = quiz.model_dump()

    # fix quiz
    fixed_quiz = fix_quiz(quiz_dict)

    # save quiz
    dir_path = "files"
    file_path = os.path.join(dir_path, "generated_quiz.json")

    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(fixed_quiz, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run()
