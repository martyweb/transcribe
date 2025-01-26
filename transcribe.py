#import moviepy.editor as mp
#import speech_recognition as sr
import whisper
import os

# # Load your video file
# video = mp.VideoFileClip("/mnt/r/2021-01-02/GH010018.MP4")

# # Extract audio from the video
# video.audio.write_audiofile("/mnt/r/2021-01-02/GH010018.wav")

# # Initialize recognizer
# recognizer = sr.Recognizer()

# # Load the extracted audio
# audio = sr.AudioFile("/mnt/r/2021-01-02/GH010018.wav")

# with audio as source:
#     audio_file = recognizer.record(source)

# # Transcribe the audio
# text = recognizer.recognize_google(audio_file)

#print(text)

def create_srt(transcription, filename="subtitles.srt"):
    with open(filename, "w") as f:
        for i, segment in enumerate(transcription['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text']

            # Convert time format to SRT
            def srt_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = int(seconds % 60)
                milliseconds = int((seconds - int(seconds)) * 1000)
                return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

            f.write(f"{i+1}\n")
            f.write(f"{srt_time(start)} --> {srt_time(end)}\n")
            f.write(f"{text.strip()}\n\n")

# Load the whisper model
model = whisper.load_model("base")

path = "/mnt/r/2021-01-02/"

#loop through files in director
for filename in os.listdir(path):

    #check extention
    if(filename.lower().endswith("mp4")):
        #filename = "GH010018.MP4"
        filename_noext = filename.split(".")[0]
        result = model.transcribe(path + filename, word_timestamps=True)
        create_srt(result, path + filename_noext + ".srt")