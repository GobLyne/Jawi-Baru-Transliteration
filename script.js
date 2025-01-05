// Link to backend translation functionality (dummy translation example included)
// async function translateText(rumiText) {
//   // Simulate a backend translation API call
//   return new Promise((resolve) => {
//       setTimeout(() => {
//           const translatedText = rumiText
//               ? `Jawi translation of: ${rumiText}`
//               : "";
//           resolve(translatedText);
//       }, 1000); // Simulate a delay
//   });
// }

async function translateText(rumiText) {
  try {
      const response = await fetch('https://jawi-baru-transliteration.onrender.com/translate', { // Replace with your FastAPI server URL
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: rumiText }),
      });

      if (!response.ok) {
          throw new Error('Failed to fetch translation');
      }

      const data = await response.json();
      return data.translated_text; // Assuming the FastAPI response includes "translated_text"
  } catch (error) {
      console.error('Error:', error);
      return 'Error: Unable to fetch translation';
  }
}

// DOM Elements
const rumiTextArea = document.getElementById("rumi-text");
const jawiTextArea = document.getElementById("jawi-text");
const clearButton = document.querySelector(".btn.clear");
const translateButton = document.querySelector(".btn.translate");
const copyButton = document.querySelector(".btn.copy");

// Character limit counter
const charLimit = 120;
const charCounter = document.createElement("div");
charCounter.style.marginTop = "10px";
charCounter.style.color = "#838383";
charCounter.textContent = `Characters: 0/${charLimit}`;
rumiTextArea.parentElement.appendChild(charCounter);

// Event Listeners
rumiTextArea.addEventListener("input", () => {
  const inputText = rumiTextArea.value;
  const charCount = inputText.length;

  if (charCount > charLimit) {
      rumiTextArea.value = inputText.slice(0, charLimit);
  }

  charCounter.textContent = `Characters: ${Math.min(charCount, charLimit)}/${charLimit}`;
});

clearButton.addEventListener("click", () => {
  rumiTextArea.value = "";
  jawiTextArea.value = "";
  charCounter.textContent = `Characters: 0/${charLimit}`;
});

translateButton.addEventListener("click", async () => {
  const rumiText = rumiTextArea.value.trim();

  if (!rumiText) {
      alert("Sila masukkan teks Rumi untuk diterjemahkan.");
      return;
  }

  jawiTextArea.value = "Translating...";

  try {
      const translatedText = await translateText(rumiText);
      jawiTextArea.value = translatedText;
  } catch (error) {
      jawiTextArea.value = "Error: Unable to translate the text. Please try again later.";
      console.error("Translation error:", error);
  }
});

copyButton.addEventListener("click", () => {
  if (jawiTextArea.value) {
      jawiTextArea.select();
      document.execCommand("copy");

      // Display text pop-up inside the website
      const popup = document.createElement("div");
      popup.textContent = "Teks telah disalin!";
      popup.style.position = "fixed";
      popup.style.bottom = "20px";
      popup.style.right = "20px";
      popup.style.backgroundColor = "#4CAF50";
      popup.style.color = "white";
      popup.style.padding = "10px";
      popup.style.borderRadius = "5px";
      popup.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
      popup.style.zIndex = "1000";
      document.body.appendChild(popup);

      setTimeout(() => {
          document.body.removeChild(popup);
      }, 2000);
  } else {
      alert("Tiada teks untuk disalin.");
  }
});
