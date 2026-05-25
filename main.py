import mediapipe as mp 
import cv2
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from playsound import playsound
from pathlib import Path



model_path= "pose_landmarker_full.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

posture_status=True #true means good status
forward_lean=0
bad_posture_start=None
alert= False

base_path= Path(__file__).parent
sound_file= base_path/"beep.mp3"
forward_high_threshold=-0.10
forward_low_threshold=-0.30
# Create a pose landmarker instance with the live stream mode:
def process_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    if(result.pose_landmarks):
        global forward_lean,posture_status,bad_posture_start,alert
        
        person= result.pose_landmarks[0]
        right_ear= person[8]
        right_shoulder= person[12]
        
        side_lean= right_ear.x-right_shoulder.x # Might add in future
        forward_lean= right_ear.z-right_shoulder.z
        
        if forward_lean>forward_high_threshold or forward_lean<forward_low_threshold:
            posture_status=False
            if bad_posture_start==None:
                bad_posture_start=time.time()
                alert=False
        else:
            posture_status=True
            bad_posture_start=None
            alert=False
        
        if bad_posture_start is not None:
            elapsed= time.time()- bad_posture_start
            if elapsed>4 and not alert:  # if bad posture remains for more than 4 seconds and alert aint activated already
                playsound(str(sound_file))
                alert=True
    #print('pose landmarker result: {}'.format(result))

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=process_result)

with PoseLandmarker.create_from_options(options) as landmarker:
    cap= cv2.VideoCapture(0)
    while True:
        ret,frame= cap.read()
        
        if not ret:
            break
        frame=cv2.flip(frame,1)
        rgb_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        if posture_status:
            cv2.putText(frame,"GOOD POSTURE",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2) 
        else:
            cv2.putText(frame,"BAD POSTURE",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
        cv2.imshow("Webcam",frame)
        mp_image= mp.Image(image_format=mp.ImageFormat.SRGB, data= rgb_frame)
        current_time= time.time()
        Timestamp= int(current_time*1000) #Converting to milliseconds
        landmarker.detect_async(mp_image, Timestamp)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
    
        
    cap.release()
    cv2.destroyAllWindows()

    
    
