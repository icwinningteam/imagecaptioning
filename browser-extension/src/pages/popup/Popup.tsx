import React from "react";

// import logo from "@assets/img/logo.svg";

import "@pages/options/index.css";

export default function Popup(): JSX.Element {
  return (
    <><link href="index.css" rel="stylesheet" type="text/css" /><script type="module" src="index.js"></script><div className="container">
      <div id="header">EasyWeb</div>
      <div className="component">
        <div>Text to Speech</div>
        <label className="switch">
          <input type="checkbox" />
          <span className="slider round"></span>
        </label>
      </div>

      <div className="component">
        <div>Voice</div>
        <select name="cars" id="cars">
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>


      <div className="component">
        <div>Speed</div>
        <div className="slidecontainer">
          <input type="range" min="1" max="100" value="50" className="slider" id="myRange" />
        </div>
      </div>

      <div className="component">
        <div>Image Captioning</div>
        <label className="switch">
          <input type="checkbox" />
          <span className="slider round"></span>
        </label>
      </div>
      <div>


        <div className="component">
          <div>Read Summary</div>
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
        </div>


        <div className="component">
          <div>Easy Reader</div>
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
        </div>

        <div className="component">
          <div>Audio to Text</div>
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
        </div>
      </div>
    </div></>
  );
}
