# importing cv2 and matplotlid\b
import cv2
import tensorflow as tflow
import matplotlib.pyplot as plt

# from deepface import DeepFace
import os


# Defensive error handling to avoid crashing and to successfully bound faces
def recursive_cascade_factor(
    gray_image, cascade_effect, scaleFactor, minNeighbors, minSize
):
    """Recursive cascade factor to avoid errors"""
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
    """Wrapper for the cascade factor"""
    try:
        face = recursive_cascade_factor(
            gray_image, cascade_effect, scaleFactor, minNeighbors, minSize
        )

        return face

    except:
        return cascade_factor_wrapper(
            gray_image, cascade_effect, scaleFactor + 0.1, minNeighbors, minSize
        )


def save_masked_image(img_path):
    """Saves the masked image"""
    img_rgb = masker(img_path)
    plt.imshow(img_rgb)
    plt.savefig("masked_image.png")


def masker(img_path, output_path="mask.png"):
    """Creates a mask of image"""

    img = cv2.imread(img_path)

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # consider moving to root folder
    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    face = cascade_factor_wrapper(gray_image, faceCascade, 1.1, 5, (40, 40))

    print(face)
    print(face[0])

    for x, y, w, h in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 4)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_rgb[
        face[0][1] : face[0][1] + face[0][3], face[0][0] : face[0][0] + face[0][2]
    ] = [
        0,
        0,
        0,
    ]

    # cv2.imwrite("mask.png", img_rgb)
    plt.imshow(img_rgb)
    # save the image
    plt.savefig(output_path)

    return img_rgb
