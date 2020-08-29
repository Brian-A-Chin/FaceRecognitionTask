import face_recognition

known_image = face_recognition.load_image_file("kyle.jpg")
unknown_image = face_recognition.load_image_file("unknown.jpg")
unknown_image1 = face_recognition.load_image_file("unknown1.jpg")

known_face_encoding = face_recognition.face_encodings(known_image)[0]
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
unknown_face_encoding1 = face_recognition.face_encodings(unknown_image1)[0]

known_images = [unknown_face_encoding, unknown_face_encoding1]

results = face_recognition.compare_faces(known_images, known_face_encoding)

print("Results: " + str(results))

