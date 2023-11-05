# importing cv2 and matplotlid\b
import cv2
import tensorflow as tflow
import matplotlib.pyplot as plt

# from deepface import DeepFace
import os

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
img = cv2.imread(r"downloads" + os.sep + "rdface.jpg")

# ####################
# # Code block open under here
# # Leave open for future fine tuning
# # by isolating specific features


# ####################

# to gray
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Defensive error handling to avoid crashing and to successfully bound faces
def recursive_cascade_factor(gray_image, scaleFactor, minNeighbors, minSize):
    face = faceCascade.detectMultiScale(
        gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize
    )
    if len(face) == 0:
        return recursive_cascade_factor(
            gray_image, scaleFactor + 0.1, minNeighbors, minSize
        )
    else:
        return face


def cascade_factor_wrapper(gray_image, scaleFactor, minNeighbors, minSize):
    try:
        face = recursive_cascade_factor(gray_image, scaleFactor, minNeighbors, minSize)

        return face

    except:
        return cascade_factor_wrapper(
            gray_image, scaleFactor + 0.1, minNeighbors, minSize
        )


face = cascade_factor_wrapper(gray_image, 1.1, 5, (40, 40))

for x, y, w, h in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 4)


img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)

# mask the part of the image that is bounded
img_rgb[face[0][1] : face[0][1] + face[0][3], face[0][0] : face[0][0] + face[0][2]] = [
    0,
    0,
    0,
]

plt.imshow(img_rgb)
