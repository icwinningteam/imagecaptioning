const switch1 = document.getElementById("switch1");
const slider1 = document.getElementById("slider1");
const switch2 = document.getElementById("switch2");
const switch3 = document.getElementById("switch3");
const button1 = document.getElementById("button1");
const switch4 = document.getElementById("switch4");


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

chrome.storage.local.get(['audioToText']).then(
    (result) => {
        switch4.checked = result.audioToText;
        switch4.disabled = false;
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

button1.addEventListener('click', async function () {
    // Add function
    // var checkBox = document.getElementById('button1');
    // open reader .mode page
    let queryOptions = { active: true, currentWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let turl = (await chrome.tabs.query(queryOptions))[0].url

    let resp = await fetch('http://localhost:5000/api/easyread', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "data": turl })
    });

    let text = await resp.text()

    chrome.tabs.create({ url: "data:text/html;charset=utf8," + encodeURIComponent(text) })

})


switch4.addEventListener('change', function () {
    // Add function
    chrome.storage.local.set({ 'audioToText': switch4.checked });
});

window.onload = function () {
    // Check if localStorage is available (IE8+) and make sure that the visited flag is not already set.
    if (typeof window.localStorage !== 'undefined') {
        var checkBox = document.getElementById('switch1');
        checkBox.checked = localStorage.getItem('textToSpeech');
    }
};
