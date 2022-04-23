import cv2
from deepface import DeepFace

vpath = './Video/Elon_FPS.mp4'
input_photo = "./Photo/ElonMusk1.jpeg"
model = 1

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


def compare_frame_reinforce(vpath,input_photo,model):

    '''
    @param: vpath: path of the mp4 video file
    @param: imput_photo: path of the photo file to compare
    @param model: int index for model selection

    @returns: a boolean list with length equals to the second count
    		  of the video. Each element: True for match found,
    		  False for not found

    		  returns False if face not found in uploaded image


    '''
    # Model Selection, currently uses Facenet
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    
    # Crops face for uploaded image
    upload_crop = face_crop(cv2.imread(input_photo))
    if type(upload_crop) == bool : return False
    
    # Read video file frame by frame
    video_cap = cv2.VideoCapture(vpath) 
    fps = video_cap.get(5)
    success, img = video_cap.read()
    
    frame_count = 0
    final_result = []
    while success:
        # Only extract one frame per second
        if frame_count % round(fps) == 0:
            frame_crop = face_crop(img)
            if type(frame_crop) == bool: # If no face found
                final_result.append(False)   
            else:
            	# Match frame with upload image
                result = DeepFace.verify(frame_crop, upload_crop, model_name = models[model],distance_metric = "euclidean_l2", enforce_detection=False)
                final_result.append(result['verified']) # Append True to list if match found
                # Reinforced, if the frame highly match the photo, use the face cropped from the fram
                # to make future comparsion, will be updated constantly if another highly match is found 
                if result['distance'] <=0.6 : 
                    upload_crop = frame_crop
        
        success,img = video_cap.read()
        frame_count+=1
    
    return final_result


def consecutive_secs(inputs):

    '''

    Convert the boolean list to indexes of "consecutive seconds"
    One 'Skip second' is allowed

    '''

    res = []
    temp = []
    false_num = 0
    for idx, item in enumerate(inputs):
        if idx==0:
            continue
        if item:
            if false_num == 1:
                temp.append(idx-1)
            false_num = 0
            temp.append(idx)
        else:
            false_num += 1
            if false_num == 2:
                res.append(temp)
                temp = []

    if false_num == 1:
        res.append(temp)

    res = [l for l in res if len(l)>1 ]
        
    return res

def debug_display(frame_list):

    '''
    Print the duration of matched clips found
    '''

    for item in frame_list:
        start = item[0]
        end = item[-1]
        print(str(start//60) + 'm:' + str(start%60) + 's  TO   ' + str(end//60) + 'm:' + str(end%60) + 's'   )
        print()


def main():
    result_list = compare_frame_reinforce(vpath,input_photo,model)
    frame_list = consecutive_secs(result_list)
    debug_display(frame_list)


if __name__ == "__main__":
    main()
