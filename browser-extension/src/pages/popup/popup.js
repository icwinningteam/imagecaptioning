const switch1 = document.getElementById("switch1");
const slider1 = document.getElementById("slider1");
const switch2 = document.getElementById("switch2");
const switch3 = document.getElementById("switch3");
const switch4 = document.getElementById("switch4");
const switch5 = document.getElementById("switch5");


chrome.storage.local.get(['textToSpeech']).then(
    (result) => {
        switch1.checked = result.textToSpeech;
        switch1.disabled = false;
    }
);

chrome.storage.local.get(['speed']).then(
    (result) => {
        slider1.checked = result.speed;
        slider1.disabled = false;
    }
);

chrome.storage.local.get(["imageCaptioning"]).then(
    (result) => {
        switch2.checked = result.imageCaptioning;
        switch2.disabled = false;
    }
);

chrome.storage.local.get(['readSummary']).then(
    (result) => {
        switch3.checked = result.readSummary;
        switch3.disabled = false;
    }
);

chrome.storage.local.get(['easyReader']).then(
    (result) => {
        switch4.checked = result.textToSpeech;
        switch4.disabled = false;
    }
);

chrome.storage.local.get(['audioToText']).then(
    (result) => {
        switch5.checked = result.audioToText;
        switch5.disabled = false;
    }
);

switch1.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'textToSpeech': switch1.checked });
});

slider1.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'speed': slider1.checked });
});

switch2.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'imageCaptioning': switch2.checked });
});

switch3.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'readSummary': switch3.checked });
});

switch4.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'easyReader': switch4.checked });
});

switch5.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'audioToText': switch5.checked });
});
