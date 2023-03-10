import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import json
from newspaper import Article
from urlextract import URLExtract
import random

# getNPhotos setup
exts = [".png", ".jpg", ".gif", ".mp3", ".mp4"]


def easy_read(url):
    n = 10
    n_images = get_n_photos(url, n)
    pre_parsed_text = trim_article(url)
    random.shuffle(n_images)
    text = intersperse_image(pre_parsed_text, n_images)
    return make_html(text, n_images, url)


def get_n_photos(url, n):
    article = Article(url)
    article.download()
    article.parse()
    photos = list(article.imgs)
    photo_size = []
    for i in range(len(photos)):
        size = int(requests.get(photos[i], stream=True).headers["Content-length"])
        if size >= 4000:
            photo_size.append((size, photos[i]))
    photo_size.sort(key=lambda x: x[0])
    return [tup[1] for tup in photo_size][-n:]


def intersperse_image(trim_text, urls):
    trim_text += "\n"
    interspersed = []
    delims = ["\n"]
    n = len(urls) + 1
    gap = len(trim_text.split("\n")) // n
    k = 1
    for i in range(len(trim_text)):
        interspersed.append(trim_text[i])
        if trim_text[i] in delims:
            k += 1
        if k % gap == 0 and n > 0:
            interspersed.append("%i")
            n -= 1
            k = 1
    ret = ""
    for r in interspersed:
        ret += r
    return ret


def trim_article(url):
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    content = ""
    if "wiki" in url:

        inLink = False

        for i in range(len(text)):
            if text[i] == "[":
                inLink = True
            elif text[i] == "]":
                inLink = False
            elif not inLink:
                content += text[i]
    else:
        return text
    return content


def replace_images(text, images):
    t = text.split("%i")
    for i in range(len(t)):
        try:
            t[i] += f'<br><br><image src="{images[i]}"><br><br>'
        except IndexError:
            pass
    ret = ""
    for i in t:
        ret += i
    return ret


def make_html(text, images, url):
    p_text = replace_images(text, images).replace("\n", "<br>")
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")
    titleElem = soup.find("title")
    if titleElem != None:
        title = [titleElem.get_text(), "AccessIc Easy Reader"]
    else:
        title = ["", "AccessIc Easy Reader"]
    div_style = 'style="display: flex;justify-content: center;font-size:2em"'
    body_font = "<style>body{font-family: 'Roboto Slab', sans-serif;background-color:#FFF0C1; padding-left: 10%; padding-right: 10%; font-size: 1.8rem;}</style>"
    form_html = """<form action='#'>
        <div class="row">
          <label>Select Voice</label>
          <div class="outer">
            <select></select>
          </div>
        </div>
        <button>Read Article</button></form>"""

    js_text = (
        text.replace("\n\n", "\n")
        .replace("\n", ". ")
        .replace("%i", " ")
        .replace('"', "'")
    )
    css = """
::selection{
  color: #fff;
  background: #5256AD;
}
form .row{
  display: flex;
  margin-bottom: 10px;
  flex-direction: column;
}
form .row label{
  font-size: 18px;
  margin-bottom: 5px;
}
form .row:nth-child(2) label{
  font-size: 17px;
}
form :where(textarea, select, button){
  outline: none;
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 5px;
}
form .row textarea{
  resize: none;
  height: 110px;
  font-size: 15px;
  padding: 8px 10px;
  border: 1px solid #999;
}
form .row textarea::-webkit-scrollbar{
  width: 0px;
}
form .row .outer{
  height: 47px;
  display: flex;
  padding: 0 10px;
  align-items: center;
  border-radius: 5px;
  justify-content: center;
  border: 1px solid #999;
}
form .row select{
  font-size: 14px;
  background: none;
}
form .row select::-webkit-scrollbar{
  width: 8px;
}
form .row select::-webkit-scrollbar-track{
  background: #fff;
}
form .row select::-webkit-scrollbar-thumb{
  background: #888;
  border-radius: 8px;
  border-right: 2px solid #ffffff;
}
form button{
  height: 52px;
  color: #fff;
  font-size: 17px;
  cursor: pointer;
  margin-top: 10px;
  background: #FFB900;
  transition: 0.3s ease;
}
form button:hover{
  background: #FFA726;
}
img {
    max-width: 80%;
}
"""
    java_script = f"""
voiceList = document.querySelector("select"),
speechBtn = document.querySelector("button");

let synth = speechSynthesis,
isSpeaking = true;

voices();

function voices(){{
    for(let voice of synth.getVoices()){{
        let selected = voice.name === "Microsoft US English" ? "selected" : "";
        let option = `<option value="${{voice.name}}" ${{selected}}>${{voice.name}} (${{voice.lang}})</option>`;
        voiceList.insertAdjacentHTML("beforeend", option);
    }}
}}

synth.addEventListener("voiceschanged", voices);

function textToSpeech(text){{
    let utterance = new SpeechSynthesisUtterance(text);
    for(let voice of synth.getVoices()){{
        if(voice.name === voiceList.value){{
            utterance.voice = voice;
        }}
    }}
    synth.speak(utterance);
}}

speechBtn.addEventListener("click", e =>{{
    e.preventDefault();
    if(!synth.speaking){{
        textToSpeech("{js_text}");
    }}
    if("{js_text}".length > 80){{
        setInterval(()=>{{
            if(!synth.speaking && !isSpeaking){{
                isSpeaking = true;
                speechBtn.innerText = "Convert To Speech";
            }}else{{
            }}
        }}, 500);
        if(isSpeaking){{
            synth.resume();
            isSpeaking = false;
            speechBtn.innerText = "Stop Speech";
        }}else{{
            synth.cancel();
            isSpeaking = true;
            speechBtn.innerText = "Start Speech";
        }}
    }}else{{
        speechBtn.innerText = "Read Article";
    }}
}});
    """

    final_html = f"""<html><head><link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=Roboto&family=Roboto+Slab&display=swap" rel="stylesheet"><title>{title[0]}</title>{body_font}<meta charset="UTF-8"><style>{css}</style></head><body><div {div_style}><h2 style="margin-block-end: 0rem;">{title[0]}{form_html}</h2></div><div><p><b>{p_text}</b></p></div><script>{java_script}</script></body></html>"""
    return final_html
