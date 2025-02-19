import whisper
import os
import cv2

# Load the whisper model
model = whisper.load_model("base")
path = "/mnt/r/"
recursive = True

def detect_objects_in_video(video_path):
    # Load the pre-trained object detection model
    model = cv2.dnn.readNetFromCaffe("path/to/model.prototxt", "path/to/model.caffemodel")

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects in the frame
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        model.setInput(blob)
        detections = model.forward()

        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                class_label = "Object {}".format(class_id) # Replace with actual class labels

                # Get bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (x, y, x2, y2) = box.astype("int")

                # Draw bounding box and label
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        #cv2.imshow("Video", frame)
        cv2.imwrite('output_image.jpg', frame)
        
        # cv2.write
        # if cv2.waitKey(1) == ord('q'):
        #     break

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



#transcode_path(path, recursive)
detect_objects_in_video(path + "2021-01-17\GH010034.MP4")

