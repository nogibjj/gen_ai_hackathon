# importing cv2 and matplotlid\b
import cv2
import tensorflow as tflow
import matplotlib.pyplot as plt

# from deepface import DeepFace
import os


def parse_details(some_string):
    """Parse the facial details from the string"""

    feature_modifiers = {
        "face": [(x, y), (x + w, y + h)],
        "eyes": [(x, int(y + h / 2)), (x + w, y + h)],
        "righteye": [(x + int(w / 2), int(y + h / 2)), (x + w, y + h)],
        "lefteye": [(x, int(y + h / 2)), (x + int(w / 2), y + h)],
        "nose": [(x + int(w / 4), y), (x + int(w / 2) + int(w / 4), y + h)],
        "mouth": [(x, y), (x + w, y + int(h / 2))],
        "jaw": [(x, y), (x + w, y + int(h / 2))],
        "chin": [(x, y), (x + w, y + int(h / 2))],
        "eyebrow": [(x, int(y + h / 2)), (x + w, y + h)],
        "righteyebrow": [(x + int(w / 2), int(y + h / 2)), (x + w, y + h)],
        "lefteyebrow": [(x, int(y + h / 2)), (x + int(w / 2), y + h)],
        "forehead": [(x, int(y + h / 2)), (x + w, y + h)],
    }

    some_string_formatted = some_string.lower().replace(" ", "")

    features = []
    for key in feature_modifiers.keys():
        if key in some_string_formatted:
            features.append(key)

    if ("face" in features) or (
        ("eyes" in features)
        and (("mouth" in features) or ("jaw" in features) or ("chin" in features))
    ):
        return ["face"]

    else:
        return features


# Defensive error handling to avoid crashing and to successfully bound faces
def recursive_cascade_factor(
    gray_image, cascade_effect, scaleFactor, minNeighbors, minSize
):
    face = cascade_effect.detectMultiScale(
        gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize
    )
    if len(face) == 0:
        return recursive_cascade_factor(
            gray_image, cascade_effect, scaleFactor + 0.1, minNeighbors, minSize
        )
    else:
        return face


def cascade_factor_wrapper(
    gray_image, cascade_effect, scaleFactor, minNeighbors, minSize
):
    try:
        face = recursive_cascade_factor(
            gray_image, cascade_effect, scaleFactor, minNeighbors, minSize
        )

        return face

    except:
        return cascade_factor_wrapper(
            gray_image, cascade_effect, scaleFactor + 0.1, minNeighbors, minSize
        )


def plot_feature(feature_list, face_coordinates):
    """Plot the feature"""
    x = face_coordinates[0][0]
    y = face_coordinates[0][1]
    w = face_coordinates[0][2]
    h = face_coordinates[0][3]

    feature_modifiers = {
        "face": [x, y, x + w, y + h],
        "eyes": [x, int(y + h / 2), x + w, y + h],
        "righteye": [x + int(w / 2), int(y + h / 2), x + w, y + h],
        "lefteye": [x, int(y + h / 2), x + int(w / 2), y + h],
        "nose": [x + int(w / 4), y, x + int(w / 2) + int(w / 4), y + h],
        "mouth": [x, y, x + w, y + int(h / 2)],
        "jaw": [x, y, x + w, y + int(h / 2)],
        "chin": [x, y, x + w, y + int(h / 2)],
        "eyebrow": [x, int(y + h / 2), x + w, y + h],
        "righteyebrow": [x + int(w / 2), int(y + h / 2), x + w, y + h],
        "lefteyebrow": [x, int(y + h / 2), x + int(w / 2), y + h],
        "forehead": [x, int(y + h / 2), x + w, y + h],
    }
    for f in feature_list:
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 4)


# Apparently for monitoring, it only shows in terminals
# tflow.debugging.set_log_device_placement(True)

# Set up Prefetching
AUTOTUNE = tflow.data.AUTOTUNE

# Set up the data
pwd = os.getcwd()
print(pwd)
img = cv2.imread(r"..\downloads" + os.sep + "rdface.jpg")

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
face = cascade_factor_wrapper(gray_image, faceCascade, 1.1, 5, (40, 40))
cascade_list = parse_details("Look at the eyes")

findings = []

for cascade in cascade_list:
    face = cascade_factor_wrapper(gray_image, cascade, 1.1, 12, (40, 40))

    findings.append(face)

# face = cascade_factor_wrapper(gray_image, 1.1, 5, (40, 40))

for face in findings:
    for x, y, w, h in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 4)


img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)

for face in findings:
    img_rgb[
        face[0][1] : face[0][1] + face[0][3], face[0][0] : face[0][0] + face[0][2]
    ] = [
        0,
        0,
        0,
    ]

# mask the part of the image that is bounded
img_rgb[face[0][1] : face[0][1] + face[0][3], face[0][0] : face[0][0] + face[0][2]] = [
    0,
    0,
    0,
]

plt.imshow(img_rgb)
