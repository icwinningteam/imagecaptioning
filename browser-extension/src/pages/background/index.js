console.log("Service Worker 👋");


// for tts
// Check if the browser supports the speechSynthesis API
if ('speechSynthesis' in window) {
    // Function to handle the text to speech
    function readJSON(jsonData) {
      // Use the text to speech API to read the JSON data
      const utterance = new SpeechSynthesisUtterance(jsonData);
      window.speechSynthesis.speak(utterance);
    }

    // Get the JSON data from the content script
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'readJSON') {
        readJSON(request.jsonData);
      }
    });
  }
