import cv2
from deepface import DeepFace
import pandas as pd
import numpy as np
import time
from sklearn.metrics import confusion_matrix, recall_score, precision_score, accuracy_score, f1_score,roc_auc_score
from sklearn.metrics import cohen_kappa_score

from face_model import compare_frame_reinforce

label_file = pd.read_csv('./Evaluation/Interview_Label.csv')
test = label_file['Label'].tolist()


vpath = './Video/Elon_FPS.mp4'
input_photo = "./Photo/ElonMusk1.jpeg"
model = 2


def evaluate_model(result):
    y_pred = result
    y_test = test
    
    
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy: %f' % accuracy)


    precision = precision_score(y_test, y_pred)
    print('Precision: %f' % precision)


    recall = recall_score(y_test, y_pred)
    print('Recall: %f' % recall)


    f1 = f1_score(y_test, y_pred)
    print('F1 score: %f' % f1)
    
    
    kappa = cohen_kappa_score(y_test, y_pred)
    print('Kappa: %f' % kappa)
    
    


def test_metric(mlist):
   for num in mlist:
       print('Test Paprameter:  %f' % num)
       start_time = time.time()
       y_pred = compare_frame_reinforce(vpath,input_photo, model, metric=num)
       exe_time = time.time() - start_time
       evaluate_model(y_pred)
       print('Wall time: %f s' % round(exe_time,2))
       print()

def main():
	candidate_metrics = [0,1,2]
	test_metric(candidate_metrics)
 


if __name__ == "__main__":
    main()

