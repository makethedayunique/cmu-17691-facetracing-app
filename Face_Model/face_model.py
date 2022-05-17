import cv2
from deepface import DeepFace
import os
import time
import glob
from datetime import timedelta


model = 2 #Facenet 512
metric= 2 # L2 Eucledian

def face_crop(image):

    """
    @param: image: image vectroized by CV2 
    @return: image: face only

    Process an image and crop the face identified,
    returns image for the first face detected only
    returns False no face detected

    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    if len(faces)==0: return False
    else:    
        (x, y, w, h) = faces[0]
        image = image[y:y+h, x:x+w]
    return image


def compare_frame_reinforce(vpath,input_photo,model,metric):

    '''
    @param: vpath: path of the mp4 video file
    @param: imput_photo: path of the photo file to compare
    @param model: int index for model selection
    @param metric: int index for metric selection 

    @returns: a boolean list with length equals to the second count
    		  of the video. Each element: True for match found,
    		  False for not found

    		  returns False if face not found in uploaded image


    '''
    # Model Selection, currently uses Facenet512 and L2 Eucledian
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    
    # Crops face for uploaded image
    upload_crop = face_crop(cv2.imread(input_photo))
    if type(upload_crop) == bool : return False
    
    # Read video file frame by frame
    video_cap = cv2.VideoCapture(vpath) 
    fps = video_cap.get(5)
    success, img = video_cap.read()
    
    frame_count = 0
    final_result = []
    verified_frames = []
    while success:
        # Only extract one frame per second
        if frame_count % round(fps) == 0:
            frame_crop = face_crop(img)
            if type(frame_crop) == bool: # If no face found
                final_result.append(False)   
                verified_frames.append(None)
            else:
            	# Match frame with upload image
                result = DeepFace.verify(frame_crop, upload_crop, model_name = models[model],distance_metric = metrics[metric], enforce_detection=False)
                final_result.append(result['verified']) # Append True to list if match found
                verified_frames.append(img)
                # Reinforced, if the frame highly match the photo, use the face cropped from the fram
                # to make future comparsion, will be updated constantly if another highly match is found 
                if result['distance'] <= 0.8 * result['threshold'] : 
                    upload_crop = frame_crop

        
        success,img = video_cap.read()
        frame_count+=1
    
    return final_result, verified_frames


def consecutive_secs(inputs, verified_frames):

    '''

    Convert the boolean list to indexes of "consecutive seconds"
    One 'Skip second' is allowed

    '''

    res = []
    temp = []
    merged_frames = []
    first_frame = None
    false_num = 0
    for idx, item in enumerate(inputs):
        if idx==0:
            continue
        if item:
            if false_num == 1:
                temp.append(idx-1)
            false_num = 0
            temp.append(idx)
            if first_frame is None:
                first_frame = verified_frames[idx]
        else:
            false_num += 1
            if false_num == 2:
                if (len(temp) > 1):
                    res.append(temp)
                    temp = []
                    merged_frames.append(first_frame)
                    first_frame = None

    if false_num == 1:
        # res.append(temp)
        if (len(temp) > 1):
            res.append(temp)
            temp = []
            merged_frames.append(first_frame)
            first_frame = None

    # res = [l for l in res if len(l)>1 ]
        
    return res, merged_frames


def save_frame(frames, image_dir):
    images = []
    for idx, frame in enumerate(frames):
        img_path = image_dir+"img"+str(idx)+".jpg"
        cv2.imwrite(img_path, frame)
        images.append(img_path)
    return images
            

def debug_display(frame_list):

    '''
    Print the duration of matched clips found
    '''

    for item in frame_list:
        start = item[0]
        end = item[-1]
        print(str(start//60) + 'm:' + str(start%60) + 's  TO   ' + str(end//60) + 'm:' + str(end%60) + 's'   )
        print()

def convert_to_timeslots(frame_list):
    """
    Convert frame list into the format UI required
    """
    timeslots = []
    for item in frame_list:
        # start = str(item[0]//3600) + ':' + str(item[0]//60) + ':' + str(item[0]%60)
        # end = str(item[-1]//3600) + ':' + str(item[-1]//60) + ':' + str(item[-1]%60)
        # ========================Use=Datetime.timedelta=============================
        start = str(timedelta(seconds=item[0]))
        end = str(timedelta(seconds=item[-1]))
        timeslots.append([start, end])
    return timeslots

def cleanup(image_dir):
    """
    Clean up the directory for clipped images
    """
    files = glob.glob(image_dir + '*')
    for f in files:
        os.remove(f)

def dbg_main():
    vpath = './Video/Elon_FPS.mp4'
    image_dir = './Photo/capture/'
    input_photo = "./Photo/ElonMusk1.jpeg"

    result_list, verified_frames = compare_frame_reinforce(vpath,input_photo,model,metric)
    frame_list, merged_frames = consecutive_secs(result_list, verified_frames)
    debug_display(frame_list)
    paths = save_frame(merged_frames, image_dir)
    print(convert_to_timeslots(frame_list))
    print(paths)

def get_face_trace(vpath, image_path, image_dir):
    result_list, verified_frames = compare_frame_reinforce(vpath,image_path,model,metric)
    frame_list, merged_frames = consecutive_secs(result_list, verified_frames)
    timeslots = convert_to_timeslots(frame_list)
    images = save_frame(merged_frames, image_dir)
    return images, timeslots

if __name__ == "__main__":
    dbg_main()
