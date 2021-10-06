# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:54:58 2021

@author: cleme
"""
import numpy as np
import itertools
import operator
import cv2 as cv
from statistics import mean
from collections import OrderedDict

# version 
print( cv.__version__)


def clean(L):
    L_clean=[0,0]
    for i in range( len(L)-1):
    # print(i,L[i])
        if(  L[i] != L[i+1]   ):
            print(i)
            L_clean.append(L[i])
      
    return L_clean

def find_combination(indice , Liste):
     Alerte = False
     chaine_cara=''
     for i in range( len(Liste)-1):
         chaine_cara= chaine_cara+str(Liste[i])
     if indice  in chaine_cara :
         Alerte=True
        
     return Alerte
         
         
         
def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
 
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]




nbframe=1 
t_gateopen=0
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    
    exit()
    
L_cnt=[] 
L =[0,0] 
combi =''
 

    
while True:
    nbframe =nbframe+1
    print('nbframe :')
    print(nbframe)
    
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame gray', gray)
    
    cv.imshow('frame',frame)
    
    
    
    
    hsvim = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # yellow color
    lower = np.array([40, 122, 200], dtype = "uint8")
    upper = np.array([60, 255, 255], dtype = "uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper)
    skinRegionHSV=cv.inRange(hsvim, np.array([20, 100, 100]), np.array([30, 255, 255] ))
    blurred = cv.blur(skinRegionHSV, (2,2))
    ret,thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)
    cv.imshow("thresh", thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
     
    if not  contours  :
        contours = [[[337, 456]], [[338, 457]], [[338, 459]], [[337, 460]]]
        
    contours = max(contours, key=lambda x: cv.contourArea(x))
    
    cv.drawContours(frame, [contours], -1, (255,255,0), 2)
    cv.imshow("contours", frame)
    hull = cv.convexHull(contours) 
    cv.drawContours(frame, [hull], -1, (0, 255, 255), 2)
    cv.imshow("hull", frame)
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    if defects is not None:
      cnt = 0
    for i in range(defects.shape[0]):  # calculate the angle
      s, e, f, d = defects[i][0]
      start = tuple(contours[s][0])
      end = tuple(contours[e][0])
      far = tuple(contours[f][0])
      a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
      b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
      c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
      angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
      if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
        cnt += 1
        cv.circle(frame, far, 4, [0, 0, 255], -1)
    if cnt > 0:
      cnt = cnt+1
    cv.putText(frame, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)
    
    L_cnt.append(cnt)
    cv.putText(frame, str(most_common(L_cnt)), (0, 150), cv.FONT_HERSHEY_SIMPLEX,1, (255, 255, 0) , 2, cv.LINE_AA)
     
    if len(L_cnt)==10 :
        combi = combi+ str(most_common(L_cnt))
        L.append(str(most_common(L_cnt)))
        L_cnt=[]
    
    print(combi)
    #print(   clean(L)   )
    clean(L)
    Alerte = find_combination('54' , L)
    print('Alerte : ' ,Alerte)
    print('tgate',t_gateopen) 
    if Alerte == True and t_gateopen<40:
         
        
         cv.putText(frame, 'Gate Open', (0, 350), cv.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0) , 2, cv.LINE_AA)
         t_gateopen =t_gateopen+1
         
    if t_gateopen:
         t_gateopen=0
         Alerte = False
         L_cnt=[0]
          
    
    cv.imshow('final_result',frame)    
    
   
        
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()






# traitement 

