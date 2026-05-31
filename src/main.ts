import { parsePdf } from "./pdf_reading";
import { chunkByTokens } from "./chunking";
import { generateQuiz } from "./quiz_generation";
import "dotenv/config";
import { writeFile, mkdir } from "fs/promises";
import { v4 as uuidv4 } from "uuid";

const fixQuiz = (quiz: any) => {
  return {
    ...quiz,
    questions: quiz.questions.map((q: any, i: number) => ({
      ...q,
      id: uuidv4(),
      order: i + 1,
      answers: q.answers.map((a: any, j: number) => ({
        ...a,
        id: uuidv4(),
        order: j + 1,
      })),
    })),
  };
};

async function run() {
  const text = await parsePdf("./src/files/test2.pdf");

  const blocks = text
    .replace(/\r/g, "")
    .split(/\n\n+/)
    .map((b) => b.trim())
    .filter(Boolean);

  const chunks = chunkByTokens(blocks);

  const fullContent = chunks.map((c) => c.text).join("\n\n");

  const quiz = await generateQuiz(fullContent, 20, "impossible");

  const finalQuiz = fixQuiz(quiz.object);

  const dir = "./src/files";
  const path = `${dir}/generated_quiz.json`;

  await mkdir(dir, { recursive: true });

  await writeFile(path, JSON.stringify(finalQuiz, null, 2), "utf-8");
}

run();
