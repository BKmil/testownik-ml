export async function chunkPdf(text: string) {
  const normalize = (
    t: string, // normalizacja
  ) =>
    t
      .replace(/\r/g, "")
      .replace(/[ \t]+/g, " ")
      .replace(/\n{3,}/g, "\n\n")
      .trim();

  const splitBlocks = (t: string) =>
    t
      .split(/\n\n+/)
      .map((b) => b.trim())
      .filter(Boolean);

  const semanticChunking = (blocks: string[], maxChars = 1500) => {
    const chunks: { text: string }[] = [];

    let current = "";

    for (const block of blocks) {
      const candidate = current ? current + "\n\n" + block : block;

      if (candidate.length > maxChars && current) {
        chunks.push({
          text: current.trim(),
        });

        current = block;
      } else {
        current = candidate;
      }
    }

    if (current.trim()) {
      chunks.push({
        text: current.trim(),
      });
    }

    return chunks;
  };

  const clean = normalize(text);
  const blocks = splitBlocks(clean);
  const chunks = semanticChunking(blocks);

  return chunks;
}
