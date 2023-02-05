import requests
import mp3_to_text
import mp4_to_mp3
import youtube_to_mp3

def get_audio_transcript(url):
    with open("audio_file.mp3") as f:
        f.write(requests.get(url).content)
        return mp3_to_text("audio_file.mp3")

def get_video_transcript(url):
    with open("video_file.mp4") as f:
        f.write(requests.get(url).content)
        mp4_to_mp3("video_file.mp4","audio_file.mp3")
        return mp3_to_text("audio_file.mp3")

def get_youtube_transcript(url):
    youtube_to_mp3(url)
    return mp3_to_text()

def convert_audio_to_transcripts(dict_input_list):
    for i in range(len(dict_input_list)):
        if(dict_input_list[i]['type'] == "audio"):
            transcript = get_audio_transcript(dict_input_list[i]['url'])
        elif(dict_input_list[i]['type'] == "video"):
            transcript = get_video_transcript(dict_input_list[i]['url'])
        elif(dict_input_list[i]['type'] == "video"):
            transcript = get_youtube_transcript(dict_input_list[i]['url'])
        else:
            print("This shouldn't be here!")
        del dict_input_list[i]['type']
        dict_input_list[i]['transcript'] = transcript
    return dict_input_list
    # actually dict_output_list




# receive links from list of dictionaries with  url and  type(audio, video, youtube)
# open local file for mp3 and convert to text
# format of return : list of dictionaries with url and transcript










