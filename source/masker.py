# importing cv2 and matplotlid\b
import cv2
import tensorflow as tflow
import matplotlib.pyplot as plt
from deepface import DeepFace
import os
import json

# Apparently for monitoring, it only shows in terminals
# tflow.debugging.set_log_device_placement(True)

# Set up Prefetching
AUTOTUNE = tflow.data.AUTOTUNE

print("Num GPUs Available: ", len(tflow.config.list_physical_devices("GPU")))
print(tflow.config.list_physical_devices("GPU"))
print("Num CPUs Available: ", len(tflow.config.list_physical_devices("CPU")))
print(tflow.config.list_physical_devices("CPU"))

# loading image
# img = cv2.imread(
#     r"downloads\recent.png"
# )
pwd = os.getcwd()
print(pwd)
# img = cv2.imread(
#     r"..\downloads\rdface.jpg"
# )

# list contents in the directory
print(os.listdir(r"classifiers"))

# loading image
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +'classifiers\haarcascade_frontalface_default.xml')


# ####################
# # Code block open under here
# # Leave open for future fine tuning 
# # by isolating specific features



# ####################

# print("hello" ,img)
# # showing image using plt
# plt.imshow(img)
# color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(color_img)

# prediction = DeepFace.analyze(color_img)

# print(prediction)