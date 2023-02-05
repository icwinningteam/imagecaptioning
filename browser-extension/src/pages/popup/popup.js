document.getElementById('switch1').addEventListener('click', function () {
    // Add function
    var checkBox = document.getElementById('switch1');

    localStorage.setItem('textToSpeech', checkBox.checked);
    // chrome.tabs.create({
    //     url:
    //         'data:text/html;charset=utf-8,' + encodeURIComponent('Hello world'),
    // });
    console.log(localStorage.getItem('textToSpeech'));
});

document.getElementById('slider1').addEventListener('change', function () {
    // Add function
    var checkBox = document.getElementById('slider1');

    localStorage.setItem('speed', checkBox.checked);
});

document.getElementById('switch2').addEventListener('change', function () {
    // Add function
    var checkBox = document.getElementById('switch2');

    localStorage.setItem('imageCaptioning', checkBox.checked);
});

document.getElementById('switch3').addEventListener('change', function () {
    // Add function
    var checkBox = document.getElementById('switch3');

    localStorage.setItem('readSummary', checkBox.checked);
});

document.getElementById('button1').addEventListener('click', function () {
    // Add function
    var checkBox = document.getElementById('button1');
});

document.getElementById('switch4').addEventListener('change', function () {
    // Add function
    var checkBox = document.getElementById('switch4');

    localStorage.setItem('audioToText', checkBox.checked);
});
