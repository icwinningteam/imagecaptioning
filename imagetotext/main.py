from io import BytesIO
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor
import torch
from PIL import Image
import requests
import clip
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from cairosvg import svg2png
import json
from logging.config import dictConfig
import newspaper
import nltk
from htmlbuilder import easy_read
from mp3_to_text import mp3_to_text
from mp4_to_mp3 import mp4_to_mp3
from youtube_to_mp3 import youtube_to_mp3

nltk.download("punkt")

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


# gpt2 setup
model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
feature_extractor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# clip setup
modelC, preprocess = clip.load("ViT-B/32", device=device)

# flask setup
app = Flask(__name__)
app.static_folder = "static"
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# get auto generated description of an image
def get_desc(url):
    # get the image from the url
    # this will randomly fail on urls that it will accept if
    # you just re-run it. I don't even know.
    response = requests.get(url)
    app.logger.info(f"processing {url}")
    if url.endswith(".svg"):
        data = svg2png(bytestring=response.text)
        i_image = Image.open(BytesIO(data))
    else:
        i_image = Image.open(BytesIO(response.content))

    # convert image to rgb mode
    if i_image.mode != "RGB":
        i_image = i_image.convert(mode="RGB")

    images = [i_image]

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # generate and formate caption
    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]

    # return caption and image (image is returned to improve efficiency of choose_caption
    return preds[0], i_image


# convert list of urls to dictionary of urls and lists of caption and image objects
def convert_img(paths):
    capts = dict()
    for path in paths:
        try:  # try to find the best description of the image and add it to the captions dictionary
            cap, im = get_desc(path)
            capts[path] = [cap, im]
        except Exception as e:  # return an empty caption otherwise
            print("convert failed ", e)
            capts[path] = [""]
    # return the dictionary of url-[caption, image] pairs
    return capts


# use clip to choose the best caption between the given alt text and auto generated one
def choose_caption(arr):
    # array of possible captions
    comps = [arr[1], arr[2]]

    if len(arr) == 4:  # if the image has already been rendered
        image = preprocess(arr[3]).unsqueeze(0).to(device)
    else:  # if the image hasn't already been rendered
        response = requests.get(arr[0])
        image = (
            preprocess(Image.open(BytesIO(response.content))).unsqueeze(0).to(device)
        )

    # evaluate the captions
    text = clip.tokenize(comps).to(device)
    with torch.no_grad():
        logits_per_image, logits_per_text = modelC(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy().tolist()[0]

    # choose and return the caption with the highest probability
    c = {probs[0]: 0, probs[1]: 1}
    return comps[c[max(probs)]]


# get the best caption for evey image in the input array
def parse_images(inp):
    # get auto generated image caption
    convs = convert_img([i[0] for i in inp])
    image_and_captions = [
        [i[0], i[1], convs[i[0]][0], convs[i[0]][1]]
        if len(convs[i[0]]) == 2
        else [i[0], i[1], convs[i[0]][0]]
        for i in inp
    ]
    # compare caption to given caption
    ret_array = []
    for i in image_and_captions:
        print(f"given {i[0]} {i[1]}")
        try:
            ret_array.append([i[0], choose_caption(i)])
        except Exception as e:
            print("choose_caption failed ", e)
            ret_array.append([i[0], i[1]])

    return ret_array


@app.route("/api/captions", methods=["GET", "POST"])
@cross_origin()
def get_captions():
    # return jsonify([[i[0], "dummy caption wooooooooooooo"] for i in request.json])
    parsed = parse_images(request.json)
    app.logger.debug("generated captions")
    app.logger.debug(parsed)
    return jsonify(parsed)


def get_summary(url):
    # Extract web data
    url_i = newspaper.Article(url="%s" % url, language="en", fetch_images=True)
    url_i.download()
    url_i.parse()
    url_i.nlp()
    summ = url_i.summary
    ret = ""
    for line in summ.splitlines():
        ret += line.split(" ", 1)[1] + "\n"
    return ret


@app.route("/api/summary", methods=["GET", "POST"])
@cross_origin()
def get_summary_handler():
    data = request.json
    summary = get_summary(data)
    print(summary)
    return jsonify({"data": summary})


@app.route("/api/easyread", methods=["GET", "POST"])
@cross_origin()
def easy_read_handler():
    print(request.json)
    return easy_read(request.json["data"])


def get_audio_transcript(url):
    with open("audio_file.mp3", "wb") as f:
        f.write(requests.get(url).content)
        return mp3_to_text("audio_file.mp3")


def get_video_transcript(url):
    with open("video_file.mp4", "wb") as f:
        f.write(requests.get(url).content)
        mp4_to_mp3("video_file.mp4", "audio_file.mp3")
        return mp3_to_text("audio_file.mp3")


def get_youtube_transcript(url):
    youtube_to_mp3(url)
    return mp3_to_text("audio_file.mp3")


def convert_audio_to_transcripts(dict_input_list):
    for i in range(len(dict_input_list)):
        if dict_input_list[i]["type"] == "audio":
            transcript = get_audio_transcript(dict_input_list[i]["url"])
        elif dict_input_list[i]["type"] == "video":
            transcript = get_video_transcript(dict_input_list[i]["url"])
        elif dict_input_list[i]["type"] == "youtube":
            transcript = get_youtube_transcript(dict_input_list[i]["url"])
        else:
            print("This shouldn't be here!")
        del dict_input_list[i]["type"]
        dict_input_list[i]["transcript"] = transcript
    return dict_input_list
    # actually dict_output_list


# receive links from list of dictionaries with  url and  type(audio, video, youtube)
# open local file for mp3 and convert to text
# format of return : list of dictionaries with url and transcript


@app.route("/api/transcript", methods=["GET", "POST"])
@cross_origin()
def transcript_handler():
    print("given transcript requests: ", request.json)
    return jsonify(convert_audio_to_transcripts(request.json))


if __name__ == "__main__":
    # pathTest = r"https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/POS16-F6-HOT-CHIP-2-%2827800033454%29_-_cropped.jpg/342px-POS16-F6-HOT-CHIP-2-%2827800033454%29_-_cropped.jpg"
    # pathTest2 = r"https://miro.medium.com/fit/c/224/224/1*VFOcTRCmJs8_k-1WLiynmA.jpeg"
    # captionTest = ''
    # captionTest2 = 'Build a serverless website using Amazon S3 and Route 53'
    # inp = [[pathTest, captionTest], [pathTest2, captionTest2]]
    #
    # print(parse_images(inp))

    app.run()  # Runs the webapp
