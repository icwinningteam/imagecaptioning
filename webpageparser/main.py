import newspaper
import nltk
from flask import Flask, request
import json

nltk.download('punkt')


# flask setup
app = Flask(__name__)
app.static_folder = 'static'


def get_summary(url):

    # Extract web data
    url_i = newspaper.Article(url="%s" % url, language='en', fetch_images=True)
    url_i.download()
    url_i.parse()
    url_i.nlp()
    summ = url_i.summary
    ret = ""
    for line in summ.splitlines():
        ret += line.split(' ', 1)[1] + '\n'
    return ret


@app.route("/api/caption", methods=["GET", "POST"])
def get_captions():
    data = json.loads(request.json)
    return get_summary(data.items())


if __name__ == '__main__':
    app.run()       # Runs the webapp
