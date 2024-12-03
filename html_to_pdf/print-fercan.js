// Function to map characters and diacritics to precomposed characters
function mapToPrecomposed(text) {
  const replacements = {
    // Uppercase with circumflex
    Â: "Â",
    B̂: "B̂",
    Ĉ: "Ĉ",
    D̂: "D̂",
    Ê: "Ê",
    F̂: "F̂",
    Ĝ: "Ĝ",
    Ĥ: "Ĥ",
    Î: "Î",
    Ĵ: "Ĵ",
    K̂: "K̂",
    L̂: "L̂",
    M̂: "M̂",
    N̂: "N̂",
    Ô: "Ô",
    P̂: "P̂",
    Q̂: "Q̂",
    R̂: "R̂",
    Ŝ: "Ŝ",
    T̂: "T̂",
    Û: "Û",
    V̂: "V̂",
    Ŵ: "Ŵ",
    X̂: "X̂",
    Ŷ: "Ŷ",
    Ẑ: "Ẑ",

    // Lowercase with circumflex
    â: "â",
    b̂: "b̂",
    ĉ: "ĉ",
    d̂: "d̂",
    ê: "ê",
    f̂: "f̂",
    ĝ: "ĝ",
    ĥ: "ĥ",
    î: "î",
    ĵ: "ĵ",
    k̂: "k̂",
    l̂: "l̂",
    m̂: "m̂",
    n̂: "n̂",
    ô: "ô",
    p̂: "p̂",
    q̂: "q̂",
    r̂: "r̂",
    ŝ: "ŝ",
    t̂: "t̂",
    û: "û",
    v̂: "v̂",
    ŵ: "ŵ",
    x̂: "x̂",
    ŷ: "ŷ",
    ẑ: "ẑ",
  };

  // Replace each instance found in the text
  Object.keys(replacements).forEach((key) => {
    const re = new RegExp(key, "g");
    text = text.replace(re, replacements[key]);
  });

  return text;
}

function generatePDF() {
  // Default export is a4 paper, portrait, using millimeters for units
  const doc = new jspdf.jsPDF();

  // Add the custom font
  doc.addFileToVFS("LeedsUni10-12-13.ttf", base64Font);
  doc.addFont("LeedsUni10-12-13.ttf", "LeedsUni", "normal");

  const img = new Image();
  img.crossOrigin = "anonymous";
  img.src = "ex.jpg";
  img.onload = function () {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0, img.width, img.height);
    const imgData = canvas.toDataURL("image/jpeg");

    doc.addImage(imgData, "JPEG", 10, 10, img.width / 600, img.height / 600); // scaling image down

    // load and add the second image
    const img2 = new Image();
    img2.crossOrigin = "anonymous";
    img2.src = "ex2.jpg";
    img2.onload = function () {
      const canvas2 = document.createElement("canvas");
      const ctx2 = canvas2.getContext("2d");
      canvas2.width = img2.width;
      canvas2.height = img2.height;
      ctx2.drawImage(img2, 0, 0, img2.width, img2.height);
      const imgData2 = canvas2.toDataURL("image/jpeg");

      doc.addImage(
        imgData2,
        "JPEG",
        10,
        100,
        img2.width / 600,
        img2.height / 600
      ); // scaling image down

      // Get the text to print
      let textToPrint = document.getElementById("textToPrint").innerText;
      textToPrint = mapToPrecomposed(textToPrint); // Apply the mapping function

      doc.setFont("LeedsUni"); // set font
      doc.text(textToPrint, 10, 200); // add some text, adjust coordinates to prevent overlap

      doc.save("fercan.pdf");
    };
  };
}
