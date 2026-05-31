from pathlib import Path


def get_prompt() -> str:
    file_path = Path.cwd() / "prompt" / "prompt.txt"

    return file_path.read_text(encoding="utf-8")
