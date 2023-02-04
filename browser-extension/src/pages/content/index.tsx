import React from "react";
import { createRoot } from "react-dom/client";

function Content(): JSX.Element {
  return (
    <div className="absolute top-0 left-0 right-0 bottom-0 text-center h-full p-3 bg-gray-800">
      <header className="flex flex-col items-center justify-center text-white">
        <p>
          Edit <code>src/pages/content/index.jsx</code> and save to reload.
        </p>
        <a
          className="text-blue-400"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React!
        </a>
        <p>Content styled</p>
      </header>
    </div>
  );
}

async function init() {
  const rootContainer = document.body;
  if (!rootContainer) throw new Error("Can't find Content root element");
  const root = createRoot(rootContainer);

  let n = 0;
  let imgs = []
  for (const e of document.getElementsByTagName("img")) {
    const parent = e.parentElement;
    if (!parent) return;

    if (parent.tagName === "figure") {
      // if (parent.children.includes()) {
      // }
      return;
    }

    const figure = document.createElement("figure");
    figure.id = `hackathon-figure-element-${n}`
    figure.style = "display: inline; margin: 0;"

    const caption = document.createElement("figcaption");
    caption.id = `hackathon-caption-element-${n}`

    imgs.push({ "img": e, "caption": caption })

    figure.insertAdjacentElement("beforeend", caption);

    e.insertAdjacentElement("beforebegin", figure);
    figure.appendChild(e);
    n++;
  }

  let imgData = imgs.map(v => [v.img.src, v.caption.textContent || ""])

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


  // root.render(<Content />);
}

init();
