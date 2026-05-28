import mediapipe as mp 
import cv2
import time
import numpy as np
import threading
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
forward_high_threshold=0
forward_low_threshold=0
calibration_flag=False
leans=[]
calibration_start_time=None
calibration_elapsed=0
head_offset_threshold = 0.05
shoulder_tilt_threshold = 0.03

#SOUND CALL FUNCTION

def play_sound():
    playsound(str(sound_file))
# Create a pose landmarker instance with the live stream mode:
def process_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    if(result.pose_landmarks):
        global forward_lean,posture_status,bad_posture_start,alert,forward_high_threshold,forward_low_threshold,calibration_flag,leans,calibration_start_time,calibration_elapsed
        
        person = result.pose_landmarks[0]

        # landmarks
        nose = person[0]

        left_ear = person[7]
        right_ear = person[8]

        left_shoulder = person[11]
        right_shoulder = person[12]

        # FORWARD LEAN
        forward_lean = right_ear.z - right_shoulder.z
        
        # SIDE HEAD LEAN
        shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
        head_offset = nose.x - shoulder_mid_x

        # SHOULDER TILT
        shoulder_tilt = abs(left_shoulder.y - right_shoulder.y)
        
        if not calibration_flag:

            # first calibration frame
            if calibration_start_time is None:
                calibration_start_time = time.time()

            # collect one sample THIS frame
            leans.append(forward_lean)

            # check elapsed calibration time
            calibration_elapsed = time.time() - calibration_start_time

            if calibration_elapsed > 10:

                lean_arr = np.array(leans)
                avg_posture = np.mean(lean_arr)

                forward_high_threshold = avg_posture + 0.15
                forward_low_threshold = avg_posture - 0.15

                calibration_flag = True
                leans.clear()
        elif (
            forward_lean > forward_high_threshold
            or forward_lean < forward_low_threshold
            or abs(head_offset) > head_offset_threshold
            or shoulder_tilt > shoulder_tilt_threshold
        ):
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
                threading.Thread(target=play_sound).start()
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
        remaining= 10 - int(calibration_elapsed)
        if not calibration_flag:
            cv2.putText(frame,f"SIT STRAIGHT",(40,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,200),2) 
            cv2.putText(frame,f"Calibrating:{remaining}S",(40,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,200),2) 
        elif posture_status:
            cv2.putText(frame,"GOOD POSTURE",(40,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2) 
        else:
            cv2.putText(frame,"BAD POSTURE",(40,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
        cv2.imshow("Webcam",frame)
        mp_image= mp.Image(image_format=mp.ImageFormat.SRGB, data= rgb_frame)
        current_time= time.time()
        Timestamp= int(current_time*1000) #Converting to milliseconds
        landmarker.detect_async(mp_image, Timestamp)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    
    
