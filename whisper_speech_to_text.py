import whisper
from pytube import YouTube
import os

# url = "https://www.youtube.com/watch?v=S5FyS7tQuUw"
try:
    youtube = YouTube(url)

    # extract only audio
    vid = youtube.streams.filter(only_audio=True).first()

    # check for destination to save file
    destination = "."

    # download the file
    out_file = vid.download(output_path=destination)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    print(youtube.title + " has been successfully downloaded.")
except:
    print("No URL passed!")

# result of success


def beautify(text):
    words = text.split()
    delimiters = [".", "!", "?"]
    for i in range(len(words)):
        if words[i][-1] in delimiters:
            words[i] = words[i] + "\n"
    return " ".join(words)


model = whisper.load_model("base")
audio = whisper.load_audio("test_audio/french_audio.mp3")
result = model.transcribe(audio, fp16=False, task="translate")
print(beautify(result["text"]))
