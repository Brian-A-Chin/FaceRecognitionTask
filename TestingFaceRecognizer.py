"""
Author: Kyle Mabry
This is a simple script to be used as a sanity check. It just makes sure that everything is working on the
face_recognition side of things.
Last edit made: 08/29/2020
"""

import face_recognition

# Load the images we're going to be comapring.
known_image = face_recognition.load_image_file("kyle.jpg")
unknown_image = face_recognition.load_image_file("unknown.jpg")
unknown_image1 = face_recognition.load_image_file("unknown1.jpg")

# Encode the images.
known_face_encoding = face_recognition.face_encodings(known_image)[0]
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
unknown_face_encoding1 = face_recognition.face_encodings(unknown_image1)[0]

# Make a list of known faces.
known_images = [unknown_face_encoding, unknown_face_encoding1]

# Get the results of our comparison.
results = face_recognition.compare_faces(known_images, known_face_encoding)

# Print the results for the user to see.
print("Results: " + str(results))

