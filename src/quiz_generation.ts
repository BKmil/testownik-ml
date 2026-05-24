import { generateObject } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";
import { getPrompt } from "./getPrompt";

const QuizSchema = z.object({
  questions: z.array(
    z.object({
      id: z.string(),
      order: z.number(),
      text: z.string(),
      explanation: z.string(),
      multiple: z.boolean(),
      answers: z.array(
        z.object({
          id: z.string(),
          order: z.number(),
          text: z.string(),
          is_correct: z.boolean(),
        }),
      ),
    }),
  ),
});

export async function generateQuiz(
  chunk: string,
  questionCount = 3,
  difficulty = "medium",
) {
  const basePrompt = await getPrompt();

  return await generateObject({
    model: openai("gpt-4o-mini"),

    schema: QuizSchema,

    system: basePrompt,

    prompt: `
Generate quiz strictly from this content:

QUESTION_COUNT: ${questionCount}
DIFFICULTY: ${difficulty}

CONTENT:
${chunk}
`,
  });
}
