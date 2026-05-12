import { parsePdf } from "./pdf_reading";

async function run() {
  const text = await parsePdf("./src/files/test.pdf");

  console.log("===== PDF TEXT =====");
  console.log(text);
}

run();
