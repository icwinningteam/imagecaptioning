# EasyWeb

A Chrome browser extension focused on making the web more accessible

Provides
 - Automated image captioning for uncaptioned images, and replacement of poor captions
 - Automated transcript generation for audio clips, video clips, and video
   embeds (e.g. Youtube videos)
- "EasyRead" mode providing a simplified view of the main content of a page along with an option for it to be read to the user with text to speech software.

## Development
The frontend is contained in `browser-extension`, the backend in
`imagetotext`.

Install dependencies with
```
npm install (in browser-extension)
pip3 install -r requirements.txt (in imagetotetxt)
```

Additional libraries not contained in the `requirements.txt` may need to be
installed.

Run with two commands:
```
npm run start chrome
python3 main.py
```

The python server on start up will require some time to download all the
required AI models, along with having to load the models on start up.


