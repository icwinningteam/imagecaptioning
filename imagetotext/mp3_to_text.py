import whisper


def beautify(text):
    words = text.split()
    delimiters = [".", "!", "?"]
    for i in range(len(words)):
        if words[i][-1] in delimiters:
            words[i] = words[i] + "<br>"
    return " ".join(words)


def mp3_to_text(filename):
    model = whisper.load_model("base")
    audio = whisper.load_audio(filename)

    # testing to consider translation
    audio_test_language = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio_test_language).to(model.device)
    _, probs = model.detect_language(mel)
    language = {max(probs, key=probs.get)}

    if language == "en":
        result = model.transcribe(audio, fp16=False)
    else:
        result = model.transcribe(audio, fp16=False, task="translate")
    return beautify(result["text"])
