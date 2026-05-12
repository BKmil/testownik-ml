import PDFParser from "pdf2json";

/**
 * Parsuje PDF do czystego tekstu przy użyciu pdf2json
 */
export async function parsePdf(path: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const pdfParser = new PDFParser(null, true);

    // Obsługa błędów
    pdfParser.on("pdfParser_dataError", (errData: any) =>
      reject(errData.parserError),
    );

    // Obsługa sukcesu
    pdfParser.on("pdfParser_dataReady", () => {
      // Wyciąganie surowego tekstu z pól PDF
      const text = pdfParser.getRawTextContent();
      resolve(text);
    });

    // Wczytanie pliku
    pdfParser.loadPDF(path);
  });
}
