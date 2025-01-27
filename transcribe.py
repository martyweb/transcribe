import whisper
import os

# Load the whisper model
model = whisper.load_model("base")
path = "/mnt/r/"
recursive = True

def create_srt(transcription, filename):
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

def transcode_path(path, recursive=False):
    cnt = 0
    err=0 
    
    #check path
    if(not os.path.exists(path)):
        #raise Exception(f'{path} does not exist')
        print(f'{path} does not exist')
        return 0
    
    #if(not path.endswith('/')): path+='/'
    
    print(f'{len(os.listdir(path))} file(s) in {path}')
    
    #loop through files in directory
    for filename in os.listdir(path):
        
        #recursive transcode
        fullpath = os.path.join(path, filename)
        if(os.path.isdir(fullpath) and recursive): 
            transcode_path(fullpath, recursive)
        
        #check extention
        if(filename.lower().endswith("mp4")):
            #filename = "GH010018.MP4"
            filename_noext = filename.split(".")[0]
            
            try:
                
                #check for existing SRT
                srt_file = os.path.join(path, filename_noext) + ".srt"
                if(not os.path.exists(srt_file)):
                    print(f'transcribing {fullpath}')
                    result = model.transcribe(fullpath, word_timestamps=True)
                    create_srt(result, srt_file)
                    cnt+=1
                else:
                    print(f'{srt_file} exists, skipping')
            except Exception as e:
                print(e)
                #err+=1
            
    print(f'{cnt} files transcribed')



transcode_path(path, recursive)

