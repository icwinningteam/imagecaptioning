import React from "react";
import { createRoot } from "react-dom/client";

function Content(): JSX.Element {
  return (
    <h1 className="text-red-600">howdy!</h1>
  );
}

async function init() {
  // const rootContainer = document.body;
  // if (!rootContainer) throw new Error("Can't find Content root element");
  // const root = createRoot(rootContainer);
  let customStyles = document.createElement("style");
  customStyles.innerHTML = ".transcript-button-hackathon:hover { background-color : #FFA726 }"

  document.getElementsByTagName("head")[0].appendChild(customStyles)
  const audioToTextFlag: boolean = (await chrome.storage.local.get(['audioToText'])).audioToText || false;
  const imageCaptioningFlag: boolean = (await chrome.storage.local.get(['imageCaptioning'])).imageCaptioning || false;
  if (audioToTextFlag) { await mediaTranscripts() }
  if (imageCaptioningFlag) { await captionImages() }

  // root.render(<Content />);
}

type mediaSource = {
  type: string,
  element: HTMLParagraphElement
}

type APIMediaData = {
  url: string,
  type: string,
}

type APIMediaResp = {
  url: string,
  transcript: string,
}

function createCaptionElement(mediaElement: HTMLElement, figureElement: HTMLElement, captionElement: HTMLElement) {
  let divElement = document.createElement("div");
  let showButton = document.createElement("button");
  showButton.innerText = "Hide"
  showButton.onclick = () => {
    if (captionElement.style.display == "none") {
      captionElement.style.display = "block";
      showButton.innerText = "Hide"
    } else {
      captionElement.style.display = "none";
      showButton.innerText = "Show"
    }
  };

  showButton.className = "transcript-button-hackathon"
  showButton.style = "box-sizing: border-box; width: calc(100% - 0.4rem); margin: 0.2rem; background-color: #FFB900; border-style: none; padding: 0.2rem; border-radius: 0.5rem;";
  figureElement.style = "display: inline; margin: 0;"
  let s = window.getComputedStyle(mediaElement)
  let margins = `margin-top: ${s.marginTop}; margin-bottom: ${s.marginBottom}; margin-left: ${s.marginLeft}; margin-right: ${s.marginRight};`
  let borders = `border-top: ${s.borderTop}; border-bottom: ${s.borderBottom}; border-left: ${s.borderLeft}; border-right: ${s.borderRight};`
  let paddings = `padding-top: ${s.paddingTop}; padding-bottom: ${s.paddingBottom}; padding-left: ${s.paddingLeft}; padding-right: ${s.paddingRight};`
  divElement.style = `width: ${s.width}; display: inline-block; border-radius: 0.5rem; background-color: #fff0c1; word-wrap: break-word; ${margins} ${borders} ${paddings}`

  mediaElement.style = "margin: 0 !important; border: 0 !important; padding: 0 !important;"

  captionElement.style = "padding-right: 0.25rem; padding-left: 0.25rem; padding-bottom: 0.25rem; color: black;"
  mediaElement.insertAdjacentElement("beforebegin", divElement);
  figureElement.appendChild(mediaElement);
  figureElement.appendChild(showButton)
  figureElement.insertAdjacentElement("beforeend", captionElement);
  divElement.appendChild(figureElement)

}

function createAudioCaptionElement(mediaElement: HTMLElement, captionElement: HTMLElement) {
  let divElement = document.createElement("div");
  let showButton = document.createElement("button");
  showButton.innerText = "Hide transcript"
  showButton.onclick = () => {
    if (captionElement.style.display == "none") {
      captionElement.style.display = "block";
      showButton.innerText = "Hide transcript"
    } else {
      captionElement.style.display = "none";
      showButton.innerText = "Show transcript"
    }
  };

  showButton.className = "transcript-button-hackathon"
  showButton.style = "box-sizing: border-box; width: calc(100% - 0.4rem); margin: 0.2rem; background-color: #FFB900; border-style: none; padding: 0.2rem; border-radius: 0.5rem;";

  let s = window.getComputedStyle(mediaElement)
  let margins = `margin-top: ${s.marginTop}; margin-bottom: ${s.marginBottom}; margin-left: ${s.marginLeft}; margin-right: ${s.marginRight};`
  let borders = `border-top: ${s.borderTop}; border-bottom: ${s.borderBottom}; border-left: ${s.borderLeft}; border-right: ${s.borderRight};`
  let paddings = `padding-top: ${s.paddingTop}; padding-bottom: ${s.paddingBottom}; padding-left: ${s.paddingLeft}; padding-right: ${s.paddingRight};`
  divElement.style = `display: inline-block; margin: 0; width: ${s.width}; display: inline-block; border-radius: 0.5rem; background-color: #fff0c1; word-wrap: break-word; ${margins} ${borders} ${paddings}`

  mediaElement.style = "margin: 0 !important; border: 0 !important; padding: 0 !important;"



  captionElement.style = "padding-right: 0.25rem; padding-left: 0.25rem; padding-bottom: 0.25rem; color: black; margin-block-start: 0.5rem;"
  mediaElement.insertAdjacentElement("beforebegin", divElement);
  divElement.appendChild(mediaElement)
  divElement.appendChild(showButton)
  divElement.appendChild(captionElement)
  captionElement.innerHTML = "Transcribing text..."
}

async function mediaTranscripts() {
  const sources: Map<string, mediaSource> = new Map();
  for (const e of document.getElementsByTagName("audio")) {
    console.log(`considering audio element ${e}`)
    console.log(e)
    let p = document.createElement("p")
    let audio_src = e.src
    for (const c of e.children) {
      console.log(c);
      console.log(c.tagName);
      if (c.tagName.toLowerCase() === "source") {
        console.log(`found src ${c.src}`)
        audio_src = c.src
        break;
      }
    }

    sources.set(audio_src, { "type": "audio", "element": p })
    createAudioCaptionElement(e, p);
  }

  for (const e of document.getElementsByTagName("video")) {
    if ((e.src || "") == "") continue;
    let p = document.createElement("p")

    sources.set(e.src, { "type": "video", "element": p })
    createAudioCaptionElement(e, p);
  }

  for (const e of document.getElementsByTagName("iframe")) {
    if (!e.src.startsWith("https://www.youtube.com/embed")) continue;

    let p = document.createElement("p")

    sources.set(e.src, { "type": "youtube", "element": p })
    createAudioCaptionElement(e, p);
  }

  let mediaData: APIMediaData[] = []
  sources.forEach((v, k) => mediaData.push({ "url": k, "type": v.type }))

  let resp = await fetch('http://localhost:5000/api/transcript', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(mediaData)
  });

  let respData: APIMediaResp[] = await resp.json()

  for (const item of respData) {
    sources.get(item.url)!["element"].innerHTML = item["transcript"]
  }

  // youtube embeds
}

async function captionImages() {
  let n = 0;
  let imgs = []
  for (const e of document.getElementsByTagName("img")) {
    if (e.width < 70 || e.height < 70) continue;
    const parent = e.parentElement;
    if (!parent) return;

    let existing_caption = null

    if (parent.tagName === "figure") {
      for (const p of parent.children) {
        if (p.tagName === "figcaption") {
          existing_caption = p.innerHTML;
          break;
        }
      }
      return;
    }

    const figure = document.createElement("figure");
    figure.id = `hackathon-figure-element-${n}`

    const caption = document.createElement("figcaption");
    caption.id = `hackathon-caption-element-${n}`
    caption.innerText = existing_caption || e.title || e.alt || "Generating caption..."

    imgs.push({ "img": e, "caption": caption })
    createCaptionElement(e, figure, caption)
    n++;
  }

  let imgData = imgs.map(v => [v.img.src, v.caption.innerText || ""])

  let resp = await fetch('http://localhost:5000/api/captions', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(imgData)
  });

  let respData: string[][] = await resp.json()

  for (const item of respData.entries()) {
    console.log(item);
    const index = item[0];
    const caption = item[1][1];
    imgs[index].caption.innerText = caption
    imgs[index].img.alt = caption
  }

  // let sumresp = await fetch('http://localhost:5000/api/summary', {
  //   method: "POST",
  //   headers: {
  //     'Content-Type': 'application/json'
  //   },
  //   body: JSON.stringify(document.URL)
  // });

  // const jsonData = (await sumresp.json()).data;
  // const utterance = new SpeechSynthesisUtterance(jsonData);
  // window.speechSynthesis.speak(utterance);

  // root.render(<Content />);
}

init();
