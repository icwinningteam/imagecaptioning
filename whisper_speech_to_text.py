import whisper
from pytube import YouTube
import os

# # url = "https://www.youtube.com/watch?v=S5FyS7tQuUw"
# try:
#     youtube = YouTube(url)

#     # extracting audio
#     vid = youtube.streams.filter(only_audio=True).first()

#     destination = "."

#     # downloading 
#     out_file = vid.download(output_path=destination)


#     base, ext = os.path.splitext(out_file)
#     new_file = base + ".mp3"
#     os.rename(out_file, new_file)
#     print(youtube.title + " has been successfully downloaded.")
# except:
#     print("No URL passed!")




def beautify(text):
    words = text.split()
    delimiters = [".", "!", "?"]
    for i in range(len(words)):
        if words[i][-1] in delimiters:
            words[i] = words[i] + "\n"
    return " ".join(words)


model = whisper.load_model("base")
audio = whisper.load_audio("test_audio/french_audio.mp3")

# testing to consider translation
audio_test_language = whisper.pad_or_trim(audio)
mel = whisper.log_mel_spectrogram(audio_test_language).to(model.device)
_, probs = model.detect_language(mel)
language = {max(probs, key=probs.get)}

if(language == "en"):
    result = model.transcribe(audio, fp16=False)
else:
    result = model.transcribe(audio, fp16=False, task="translate")
print(beautify(result["text"]))
