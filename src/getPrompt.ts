import { readFile } from "fs/promises";
import path from "path";

export async function getPrompt() {
  const filePath = path.join(process.cwd(), "prompt", "prompt.txt");
  return await readFile(filePath, "utf-8");
}
