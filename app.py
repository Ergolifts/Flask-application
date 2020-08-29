import pyrebase, dlib, cv2, shutil
from flask import Flask, jsonify
from PIL import Image, ImageDraw, ImageFilter

config = {
	"apiKey": "AIzaSyDYXEKNYm6bRxA782njD5-cr6E20shqf1I",
    "authDomain": "second-prototype-103b6.firebaseapp.com",
    "databaseURL": "https://second-prototype-103b6.firebaseio.com",
    "projectId": "second-prototype-103b6",
    "storageBucket": "second-prototype-103b6.appspot.com",
    "messagingSenderId": "660304409412",
    "appId": "1:660304409412:android:7dc0eeadf91dd723ae9d11"
}

#defining reference to firebase storage
firebase = pyrebase.initialize_app(config)
sto = firebase.storage()

#initialising flask app
app = Flask(__name__)

@app.route("/<parameter>")
def func(parameter):
	#extracting the image from firebase storage by parameter
	sto.child(parameter+"/input.png").download(parameter+"/input.png")

	#using the dlib library to detect face 
	detector = dlib.get_frontal_face_detector()

    #reading the image 
    img = cv2.imread(parameter+"/input.png")

    #converting the image to Grayscale which is a requirement for dlib
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    #detecting faces in image
    faces = detector(gray)
    for face in faces:
    	x1 = face.left()
        y1 = face.top() 
        x2 = face.right() 
        y2 = face.bottom() 
    
    
    rect = cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(500, 0, 100), thickness=4)

    #finding coordinates of rectangle
    detected_faces = dlib.rectangle(x1,y1,x2,y2)
    
    background = Image.open(parameter+"/input.png")
    foreground = Image.open("spiral1.png")
    
    #overlaping the golden ratio spiral over the detected face
    background.paste(foreground, (x1,y1), foreground)

    #saving the output image in server
    background.save(parameter+"/output.png")

    #putting output image back of firebase storage
	sto.child(parameter+"/output.png").put(parameter+"/output.png")

	#clearing the cache 
	shutil.rmtree(parameter)

	#returning an sucess message as reponse in json format
	return jsonify({'message':'output is ready as '+parameter+"/output.png"})

if __name__ == "__main__":
    app.run()