import urllib.request
import sys
import getopt
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from PIL import Image

def get_image(url, file_name):
    with urllib.request.urlopen(url) as resource:
        with open(file_name, 'wb') as f:
            f.write(resource.read())

def extract_face(image_name, face_image_name):
    print("Extracting Face....")
    detection_image = plt.imread(image_name)
    image = Image.open(image_name)
    detector = MTCNN()
    
    # Find faces
    faces = detector.detect_faces(detection_image)
    
    # Claculate coordinates of bound box
    x1, y1, width, height = faces[0]["box"]
    x2, y2, = x1 + width, y1 + height
    bound_box = (x1, y1, x2, y2)

    # Crop to the bounds of the face
    face_image = image.crop(bound_box)

    # Save face image
    face_image.save(face_image_name)

def edit(in_image, out_image, new_face_name, save_faces=False):
    print("Starting Edit....")
    detection_image = plt.imread(in_image)
    image = Image.open(in_image)
    detector = MTCNN()
    
    new_face = Image.open(new_face_name)
    
    # Finding the faces in the image
    print("Detecting Faces....")
    faces = detector.detect_faces(detection_image)
    
    # Edditing the new face onto all the faces in the image
    print("Editing Image....")
    amount = 0
    for face in faces:
        print("Changing a Face....")
        
        # Keeping track of which number face is being changed
        amount += 1

        # Save images of the original faces
        if (save_faces):
            x1, y1, width, height = face["box"]
            x2, y2, = x1 + width, y1 + height
            bound_box = (x1, y1, x2, y2)
            image.crop(bound_box).save(str(amount) + ".jpg")

        # Size the image of the new face to fit the size of the original
        new_face_sized = new_face.resize((face["box"][2], face["box"][3]))

        # Put the new face onto the original
        image.paste(new_face_sized, (face["box"][0], face["box"][1]))
    
    print("Faces Changed:")
    print(amount)
    print("Saving Image....")
    image.save(out_image)
    print("Edit Done")

# Setting up command line arguments
try:
    args, vals = getopt.getopt(sys.argv[1:], 'esu:i:o:f:n:',
    ["extract", "save", "url=", "in=", "out=", "face=", "new-face-image="])
except getopt.error as err:
    print(str(err))
    sys.exit(2)

# Variables that are controlled by command line arguments
extract = False
save = False
is_url = False
url = ""
in_file = "./in_image.jpg"
out_file = "./out_image.jpg"
face_file = "./face.jpg"
full_face_file = "./face_image.jpg"

# Setting all command line argument varriables
for current_arg, current_val in args:
    if current_arg in ("-e", "--extract"):
        extract = True
        print("Will extract face from face image")
    elif current_arg in ("-s", "--save"):
        save = True
        print("Will save original faces")
    elif current_arg in ("-u", "--url"):
        url = current_val
        is_url = True
        print("Will get image from url")
    elif current_arg in ("-i", "--in"):
        in_file = current_val
    elif current_arg in ("-o", "--out"):
        out_file = current_val
    elif current_arg in ("-f", "--face"):
        face_file = current_val
    elif current_arg in ("-n", "--new-face-image"):
        full_face_file = current_val


if (is_url):
    print("Getting Image....")
    get_image(url, in_file)

if (extract):
    extract_face(full_face_file, face_file)

edit(in_file, out_file, face_file, save) 
