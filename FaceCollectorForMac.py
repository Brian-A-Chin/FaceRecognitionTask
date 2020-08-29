"""
Author: Kyle Mabry
This script will collect 30 images of a person's face.
The script is also capable of identifying the face in question.
This script is meant to be run on a mac where the camera is built in.
Last edit made: 8/29/2020 KJM
"""

import cv2
import os
import sys
import face_recognition
from tqdm import tqdm


def collect_face_images(faceCascade, frames_OI, camera, name, pathDir):
    """This function will collect 30 images of a person's face in RGB format."""

    # This is where the camera actually records images and saves them.
    numberOfImagesCreated = 0
    for i in frames_OI:
        currentFrame = i
        camera.set(1, currentFrame)
        ret, frame = camera.read()
        # The code will now collect 30 images.
        numberOfImagesCreated = i

        file_name = (pathDir + "/" + name + "_" + str(i) + ".jpg")
        # Save the face-only image.
        cv2.imwrite(file_name, frame)

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
    # get the directory that we need to be in.
    directory = file_name_only.split("_")[0]
    for subdir, dirs, files in os.walk(root):
        for file in files:
            # if we've found our file.
            if file == file_name_only:
                # if the current directory isn't where the file is located, change it.
                if os.getcwd().split("/")[-1] != directory:
                    os.chdir(os.getcwd() + "/" + directory)
                    # get the whole path. load the image.
                    participant_image = face_recognition.load_image_file(file)
                else:
                    participant_image = face_recognition.load_image_file(file)

    # return the image.
    return participant_image


def put_images_into_list(name):
    """From the faces that we've collected so far this function will place the image objects into a list."""

    current_participant_images = "./images/" + name
    os.chdir(current_participant_images)
    root = "."
    current_participant = []
    # get all of the image file names of current participant.
    for subdir0, dirs0, files0 in os.walk(root):
        for file0 in files0:
            # Append the current image to the list of images.
            current_participant.append(get_image(file0))

    # Now get all of the image file names of previous participants.
    # go back one directory.
    os.chdir('..')
    previous_participants = []
    for subdir, dirs, files in os.walk(root):
        for file in files:
            if file.split("_")[0] != name:
                # Append the current image to the list of images.
                previous_participants.append(get_image(file))

    return previous_participants, current_participant


def recognize_known_faces(name):
    """Does the actual recognition of faces for each image in the list, if any 10 images match then we will return
    true that this is the same person."""

    # get the lists of both unknown and known images.
    previous_participants, current_participant = put_images_into_list(name)

    # Create a final results list:
    final_results = []
    # for each image in the list of images for previous and current participants.
    for unknown_person in tqdm(current_participant):
        unknown_encoding = face_recognition.face_encodings(unknown_person)[0]
        for known_person in previous_participants:
            known_encoding = face_recognition.face_encodings(known_person)[0]
            final_results.append(face_recognition.compare_faces([known_encoding], unknown_encoding))

    true_counter = 0
    for result in final_results:
        if str(result[0]) == "True":
            true_counter += 1

    if true_counter >= 1:
        print("This person was seen before this many times: " + str(true_counter/3))
    else:
        print("This person has not been seen before: " + str(true_counter/3))


def main():
    """Main method that runs our code."""

    # Define our faceCascade.
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # Number of frames we're collecting (add one to the number). 
    numberFrames = 2
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
    recognize_known_faces(name)


# Entry point into our code.
if __name__ == "__main__":
    main()
