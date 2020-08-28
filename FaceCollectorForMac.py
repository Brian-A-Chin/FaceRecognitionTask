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


def collect_face_images(faceCascade, frames_OI, camera, name, pathDir):
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
            file_name = (pathDir + "/" + name + str(i) + "_(" + str(x0) + "," + str(y0) + ").jpg")
            # Save the face-only image.
            saved = cv2.imwrite(file_name, cropped)
            print("Did the image save? " + str(saved))  # DEBUG

    # Print to the user how many images were generated.
    print(str(numberOfImagesCreated) + " photos were generated.")

    # When we're done, release capture.
    camera.release()
    cv2.destroyAllWindows()


def get_image(file_name_only):
    """Given a file, this function will search, starting from the root directory to find the given file.
    This function will return the full file-path to that file."""

    root = "."
    participant_image = ""
    for subdir, dirs, files in os.walk(root):
        if dirs:
            for directory in dirs:
                print(subdir)
                for file in files:
                    print(file)
                    # if we've found our file.
                    if file == file_name_only:
                        cur_dir = os.getcwd() + "/" + directory
                        os.chdir(cur_dir)
                        # get the whole path.
                        print(os.curdir)
                        # load the image.
                        print("Filename:" + file)
                        participant_image = face_recognition.load_image_file(file)
        else:
            for file in files:
                print(file)
                # if we've found our file.
                if file == file_name_only:
                    cur_dir = os.getcwd()
                    os.chdir(cur_dir)
                    # get the whole path.
                    print(os.curdir)
                    # load the image.
                    print("Filename:" + file)
                    participant_image = face_recognition.load_image_file(file)

    # return the image.
    return participant_image


def recognize_known_faces(name):
    """From the faces that we've collected so far, this function will determine whether or not it has seen this
    person's face before."""

    current_participant_images = "./images/" + name
    os.chdir(current_participant_images)
    root = "."
    current_participant = []
    # get all of the image file names of current participant.
    for subdir0, dirs0, files0 in os.walk(root):
        for file0 in files0:
            # Append the current image to the list of images.
            current_participant = get_image(file0)
    print("current participant image: " + str(current_participant))
    known_encoding = face_recognition.face_encodings(current_participant)

    # Now get all of the image file names of previous participants.
    # go back one directory.
    os.chdir('..')
    previous_participants = []
    for subdir, dirs, files in os.walk(root):
        for directory in dirs:
            if name != directory:
                for file in files:
                    # Append the current image to the list of images.
                    previous_participants = get_image(file)

    # Perform face encodings on these images.
    unknown_encoding = face_recognition.face_encodings(previous_participants)

    # compare the current participant to previous participants.
    results = face_recognition.compare_faces(known_encoding, unknown_encoding)

    print("Are these two images the same person: " + str(results))

    return results


def main():
    """Main method that runs our code."""

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

    # Collect this participants face.
    collect_face_images(faceCascade, frames_OI, camera, name, pathDir)

    # Determine whether or not this this person has been "seen" by the camera before.
    results = recognize_known_faces(name)
    print("These are the final results: " + str(results))


# Entry point into our code.
if __name__ == "__main__":
    main()
