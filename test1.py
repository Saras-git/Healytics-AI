import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
import cv2
import PIL.Image
from PIL import Image

rdate="11-03-2023"
regno="342333"
name="Rajan"
age="25"
og="Heart, Liver"
blood_grp="O+ve"
aadhar="5468756465456"

    

fn="C2.jpg"
image = cv2.imread('static/img/ogcert.jpg',cv2.IMREAD_UNCHANGED)


position = (300,172)
cv2.putText(image, rdate, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (632,172)
cv2.putText(image, regno, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (262,206)
cv2.putText(image, name, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (282,248)
cv2.putText(image, age, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (348,361)
cv2.putText(image, og, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (145,476)
cv2.putText(image, blood_grp, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (191,526)
cv2.putText(image, aadhar, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)


'''position = (330,610)
cv2.putText(image, name, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (620,610)
cv2.putText(image, regno, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (720,560)
cv2.putText(image, rdate, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)


position = (450,650)
cv2.putText(image, dept, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (160,690)
cv2.putText(image, year, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)


position = (120,730)
cv2.putText(image, dob, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)'''



