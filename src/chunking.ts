import { encoding_for_model } from "tiktoken";

// tokenizer
const enc = encoding_for_model("gpt-4o-mini");

// liczenie tokenow
const countTokens = (t: string) => enc.encode(t).length;

// ograniczenia i parametry chunkowania
const MAX_TOKENS = 1250; //
const SLICE_TOKENS = 1000; //
const TOKEN_OVERLAP = 150; //
const OVERLAP_BLOCKS = 1; //

export function chunkByTokens(blocks: string[]) {
  const chunks: { text: string }[] = [];

  // obecny chunk
  let current: string[] = [];
  let currentTokens = 0;

  for (const block of blocks) {
    const tokens = countTokens(block);

    // jeśli blok za duży, podzial na mniejsze kawalki
    if (tokens > MAX_TOKENS) {
      const encoded = enc.encode(block);


      for (let i = 0; i < encoded.length; i += (SLICE_TOKENS - TOKEN_OVERLAP)) {
        const slice = encoded.slice(i, i + SLICE_TOKENS);

        const text = enc.decode(slice);

        chunks.push({ text: new TextDecoder().decode(text) });
      }

      continue;
    }

    // jesli limit przekroczony, przechodzimy do nowego chunku
    if (currentTokens + tokens > MAX_TOKENS) {
      chunks.push({
        text: current.join("\n\n"), // laczenie blokow w chunku
      });

      // ostatni blok dalej dla kontekstu
      const overlap = current.slice(-OVERLAP_BLOCKS);

      current = [...overlap, block];
      currentTokens =
        overlap.reduce((sum, b) => sum + countTokens(b), 0) + tokens;
    } else {
      // dodajemy blok do obecnego chunku
      current.push(block);
      currentTokens += tokens;
    }
  }

  // dodajemy ostatni chunk
  if (current.length) {
    chunks.push({
      text: current.join("\n\n"),
    });
  }

  return chunks;
}

// cleanup
process.on("exit", () => {
  enc.free();
});
