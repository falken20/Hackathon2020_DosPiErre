import requests
from flask import Flask, render_template, url_for, request, Markup
from flask_cors import CORS
import base64
import numpy as np
import imutils
import pickle
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from config import urladminback

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class_labels=['Vaya te noto con algo de enfado','Y me gusta que estés alegre','No tienes una cara muy expresiva hoy...','Aunque pareces algo triste','Tienes cara de sorpresa, jeje']
    
@app.route('/')
def feedback():

	return render_template('foto.html')   


@app.route('/', methods=['POST'])
def upload_archivo():

	usuario = ''
	usutexto = ''	
	expformat = ''
	formato="data:image/png;base64,"

	response = render_template('nomatch.html')

	#obtenemos la foto y convertimos a cv2
	uploaded_file = request.files['file']

	if uploaded_file.filename != '':
	
		imagen = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

		#indentificamos al usuario si no es feedback anonimo
		usuario = reconoce(imagen)

		#generamos la imagen de respuesta
		retimg = imagen_retorno(imagen)		
		
		if usuario != "nomatch":
		
			#identificamos la expresión
			expresion = estado(imagen)
	
			#generamos la salida html
			
			urlSafeEncodedBytes = base64.urlsafe_b64encode(usuario.encode("utf-8"))
			urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
			urllogin = urladminback + urlSafeEncodedStr			
				
			#devolvemos resultados		
			response = render_template('respuesta.html', 
				valusuario=usuario, 
				valretimg=formato + retimg, 
				valexpresion=expresion,
				valurl=urllogin)

			return response
	
		response = render_template('retry.html', 
			valretimg=formato + retimg)

	return response


def reconoce(imagen):
	
	name="nomatch"
	text=""

	# load our serialized face detector from disk
	print("[INFO] cargando detector de caras...")
	protoPath = "modelos/deploy.prototxt"
	modelPath = "modelos/res10_300x300_ssd_iter_140000.caffemodel"
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
	# load our serialized face embedding model from disk
	print("[INFO] cargando identificador de caras...")
	embedder = cv2.dnn.readNetFromTorch("modelos/openface_nn4.small2.v1.t7")
	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open("modelos/recognizer.pickle", "rb").read())
	le = pickle.loads(open("modelos/le.pickle", "rb").read())

	# load the image, resize it to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image dimensions
	
	image = imutils.resize(imagen, width=600)
	(h, w) = image.shape[:2]
	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for the
			# face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# extract the face ROI
			face = image[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue
				
			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
				(0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]

	return name


def estado(frame):

	label = ""
	preds = []

	face_classifier=cv2.CascadeClassifier('modelos/haarcascade_frontalface_default.xml')
	classifier = load_model('modelos/EmotionDetectionModel.h5')

	labels=[]
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces=face_classifier.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray=gray[y:y+h,x:x+w]
		roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

		if np.sum([roi_gray])!=0:
			roi=roi_gray.astype('float')/255.0
			roi=img_to_array(roi)
			roi=np.expand_dims(roi,axis=0)

			preds=classifier.predict(roi)[0]
			label=class_labels[preds.argmax()]

	return label


def imagen_retorno(img):

	_,im_arr = cv2.imencode('.png', img) 
	im_bytes = im_arr.tobytes()
	im_b64 = base64.b64encode(im_bytes)

	return im_b64.decode('utf-8')



if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
