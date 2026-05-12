export async function chunkPdf(text: string) {
  const normalize = (
    t: string, // normalizacja
  ) =>
    t
      .replace(/\r/g, "")
      .replace(/[ \t]+/g, " ")
      .replace(/\n{3,}/g, "\n\n")
      .trim();

  const splitBlocks = (
    t: string, // podział na bloki (akapit, tytuł, lista, definicja)
  ) =>
    t
      .split(/\n\n+/)
      .map((b) => b.trim())
      .filter(Boolean);

  type BlockType = "title" | "paragraph" | "list" | "definition";

  const detectType = (block: string): BlockType => {
    // heurystyka do wykrywania typu bloku
    if (
      /^(definicja|definition)\b/i.test(block) ||
      /^oznacza/i.test(block) ||
      /jest to/i.test(block)
    )
      if (/^\d+[\.\)]\s/.test(block)) return "list";
    if (block.length < 80) return "title";
    return "paragraph";
  };

  const semanticChunking = (blocks: string[], maxChars = 1500) => {
    // łączenie bloków w chunk'i semantyczne
    const chunks: { text: string; type: BlockType }[] = [];

    let current = "";
    let currentType: BlockType = "paragraph";

    for (const block of blocks) {
      const type = detectType(block);

      const candidate = current ? current + "\n\n" + block : block;

      if (candidate.length > maxChars && current) {
        chunks.push({
          text: current.trim(),
          type: currentType,
        });

        current = block;
        currentType = type;
      } else {
        current = candidate;
        if (currentType === "paragraph") currentType = type;
      }
    }

    if (current.trim()) {
      chunks.push({
        text: current.trim(),
        type: currentType,
      });
    }

    return chunks;
  };

  const clean = normalize(text);
  const blocks = splitBlocks(clean);
  const chunks = semanticChunking(blocks);

  return chunks;
}
