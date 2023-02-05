from moviepy.editor import *

def mp4_to_mp3(mp4, mp3):
    file_to_convert = AudioFileClip(mp4)
    file_to_convert.write_audiofile(mp3)
    file_to_convert.close()

# video_file_path = ""
# audio_file_path= video_file_path[:-4] + ".mp3"
# mp4_to_mp3(video_file_path, audio_file_path)