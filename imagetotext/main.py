from io import BytesIO
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor
import torch
from PIL import Image
import requests
import clip
from flask import Flask, request
import json

# gpt2 setup
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
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
app.static_folder = 'static'


# get auto generated description of an image
def get_desc(url):
    # get the image from the url
    response = requests.get(url)
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
        try:        # try to find the best description of the image and add it to the captions dictionary
            cap, im = get_desc(path)
            capts[path] = [cap, im]
        except:     # return an empty caption otherwise
            capts[path] = ['']
    # return the dictionary of url-[caption, image] pairs
    return capts


# use clip to choose the best caption between the given alt text and auto generated one
def choose_caption(arr):
    # array of possible captions
    comps = [arr[1], arr[2]]

    if len(arr) == 4:   # if the image has already been rendered
        image = preprocess(arr[3]).unsqueeze(0).to(device)
    else:               # if the image hasn't already been rendered
        response = requests.get(arr[0])
        image = preprocess(Image.open(BytesIO(response.content))).unsqueeze(0).to(device)

    # evaluate the captions
    text = clip.tokenize(comps).to(device)
    with torch.no_grad():
        logits_per_image, logits_per_text = modelC(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy().tolist()[0]

    # choose and return the caption with the highest probability
    c = {
        probs[0]: 0,
        probs[1]: 1
    }
    return comps[c[max(probs)]]


# get the best caption for evey image in the input array
def parse_images(inp):
    # get auto generated image caption
    convs = convert_img([i[0] for i in inp])
    image_and_captions = [[i[0], i[1], convs[i[0]][0], convs[i[0]][1]]
                          if len(convs[i[0]]) == 2 else
                          [i[0], i[1], convs[i[0]][0]]
                          for i in inp]
    # compare caption to given caption
    ret_array = []
    for i in image_and_captions:
        try:
            ret_array.append([i[0], choose_caption(i)])
        except:
            ret_array.append([i[0], i[1]])
    # convert to dictionary
    ret = dict()
    for r in ret_array:
        ret[r[0]] = r[1]
    return ret


@app.route("/api/caption", methods=["GET", "POST"])
def get_captions():
    data = json.loads(request.json)
    return parse_images(data.items())


if __name__ == '__main__':
    # pathTest = r"https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/POS16-F6-HOT-CHIP-2-%2827800033454%29_-_cropped.jpg/342px-POS16-F6-HOT-CHIP-2-%2827800033454%29_-_cropped.jpg"
    # pathTest2 = r"https://miro.medium.com/fit/c/224/224/1*VFOcTRCmJs8_k-1WLiynmA.jpeg"
    # captionTest = ''
    # captionTest2 = 'Build a serverless website using Amazon S3 and Route 53'
    # inp = [[pathTest, captionTest], [pathTest2, captionTest2]]
    #
    # print(parse_images(inp))

    app.run()     # Runs the webapp


