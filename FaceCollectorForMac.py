"""
Author: Kyle Mabry
This script will collect 30 images of a person's face.
The script is also capable of identifying the face in question and cropping the image to be a box that
includes only the face.
This script is meant to be run on a mac where the camera is built in.
Last edit made: 8/23/2020 KJM
"""

import cv2
import os
import sys
import face_recognition

# Define our faceCascade.
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# Number of frames we're collecting
numberFrames = 30
# Tell the computer which camera to use.
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_XI_FRAMERATE, 30)
number_of_frames = camera.get(numberFrames)

# This is the number of frames that we will be taking, as a list.
frames_OI = list(range(0, numberFrames + 1))

# Collect subjects name and update directory with a new file, or check if file already exists.
name = input("What's his/her Name? ")
pathDir = "./images/" + name
if not os.path.exists(pathDir):
    os.makedirs(pathDir)
    print("Directory Created")
else:
    print("Name already exists")
    sys.exit()


def collect_face_images():
    """This function will collect 30 images of a person's face. The function will also
    crop the image to be a box that includes only the face."""

    # This is where the camera actually records images and saves them.
    numberOfImagesCreated = 0
    for i in frames_OI:
        currentFrame = i
        camera.set(1, currentFrame)
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # The code will now collect 30 images.
        numberOfImagesCreated = i

        # Detect faces in the image using faceCascade.
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # update the user with how many faces were detected.
        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        # print(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Reposition, for some reason the x,y coordinates weren't correct.
            x0 = x - w
            y0 = y + h
            x1 = x0 + w
            y1 = y0 + h
            # Crop the image, taking only the face.
            cropped = gray[x0:x1, y0:y1]
            fileName = pathDir + "/" + name + str(i) + "_(" + str(x0) + "," + str(y0) + ").jpg"
            # Save the face-only image.
            cv2.imwrite(fileName, cropped)

    # uncomment these two lines when you want the image to be displayed to the user.
    # cv2.imshow("Faces found", cropped)
    # cv2.waitKey(0)  # Waits until a key is pressed.

    # Print to the user how many images were generated.
    print(str(numberOfImagesCreated) + " photos were generated.")

    # When we're done, release capture.
    camera.release()
    cv2.destroyAllWindows()


def recognize_known_faces():
    """From the faces that we've collected so far, this function will determine whether or not it has seen this
    person's face before."""

    all_images_directory = "./images/"
    current_participant_images = "./images/" + name
    os.chdir(all_images_directory)
    results = []
    for subdir, dirs, files in os.walk(all_images_directory):
        for directory in dirs:
            # this makes sure that we don't go into the directory of the current participant.
            if directory != name:
                for file in files:
                    known_image = face_recognition.load_image_file(file)
                    for subdir1, dirs1, files1 in os.walk(current_participant_images):
                        for file1 in files1:
                            unknown_image = face_recognition.load_image_file(file1)

                            known_participant_encoding = face_recognition.face_encodings(known_image)[0]
                            unknown_participant_encoding = face_recognition.face_encodings(unknown_image)[0]

                            results.append(face_recognition.compare_faces([known_participant_encoding],
                                                                          unknown_participant_encoding))

    return results


def main():
    """Main method that runs our code."""

    # Collect this participants face.
    collect_face_images()

    # Determine whether or not this this person has been "seen" by the camera before.
    results = recognize_known_faces()
    print(results)


# Entry point into our code.
if __name__ == "__main__":
    main()
