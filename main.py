import mediapipe as mp 
import cv2
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path= "pose_landmarker_full.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the live stream mode:
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    if(result.pose_landmarks):
        person= result.pose_landmarks[0]
        nose= person[0]
        right_ear= person[8]
        left_ear= person[7]
        left_shoulder= person[11]
        right_shoulder= person[12]
        '''print(nose.x,nose.y)
        print(right_ear.x,right_ear.y)
        print(left_ear.x,left_ear.y)
        print(left_shoulder.x,left_shoulder.y)
        print(right_shoulder.x,right_shoulder.y)'''
        print(right_ear.z-right_shoulder.z)
    #print('pose landmarker result: {}'.format(result))

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with PoseLandmarker.create_from_options(options) as landmarker:
    cap= cv2.VideoCapture(0)
    while True:
        ret,frame= cap.read()
        
        if not ret:
            break
        frame=cv2.flip(frame,1)
        rgb_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
        cv2.imshow("Webcam",frame)
        mp_image= mp.Image(image_format=mp.ImageFormat.SRGB, data= rgb_frame)
        current_time= time.time()
        Timestamp= int(current_time*1000) #Converting to milliseconds
        landmarker.detect_async(mp_image, Timestamp)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
    
        
    cap.release()
    cv2.destroyAllWindows()

    
    
