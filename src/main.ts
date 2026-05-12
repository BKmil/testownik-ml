import { parsePdf } from "./pdf_reading";
import { chunkPdf } from "./chunking";

async function run() {
  const text = await parsePdf("./src/files/test2.pdf");
  const chunks = await chunkPdf(text);

  console.log("===== PDF TEXT =====");
  console.log(text);
  console.log("=== CHUNKS ===");
  console.log(JSON.stringify(chunks, null, 2));

  console.log("Ilość chunków:", chunks.length);
}

run();
