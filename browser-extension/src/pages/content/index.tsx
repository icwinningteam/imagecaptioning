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
  await captionImages();

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

async function mediaTranscripts() {
  const sources: Map<string, mediaSource> = new Map();
  for (const e of document.getElementsByTagName("audio")) {
    let p = document.createElement("p")
    e.insertAdjacentElement("afterend", p);

    sources.set(e.src, { "type": "audio", "element": p })
  }

  for (const e of document.getElementsByTagName("video")) {
    let p = document.createElement("p")
    e.insertAdjacentElement("afterend", p);

    sources.set(e.src, { "type": "video", "element": p })
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
  // for (const e of document.getElementsByTagName("iframe")) {
  // }
}

async function captionImages() {
  let n = 0;
  let imgs = []
  for (const e of document.getElementsByTagName("img")) {
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
    figure.style = "display: inline; margin: 0;"

    const caption = document.createElement("figcaption");
    caption.id = `hackathon-caption-element-${n}`
    caption.innerText = existing_caption || e.title || e.alt || ""

    imgs.push({ "img": e, "caption": caption })

    e.insertAdjacentElement("beforebegin", figure);
    figure.appendChild(e);
    figure.insertAdjacentElement("beforeend", caption);
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
}

init();
