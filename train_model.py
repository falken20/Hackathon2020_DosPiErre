# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

print("[INFO] cargando imagenes incrustadas...")
data = pickle.loads(open("modelos/embeddings.pickle", "rb").read())
# encode the labels
print("[INFO] codificando etiquetas...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] entrenado modelo...")
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)

# write the actual face recognition model to disk
f = open("modelos/recognizer.pickle", "wb")
f.write(pickle.dumps(recognizer))
f.close()
# write the label encoder to disk
f = open("modelos/le.pickle", "wb")
f.write(pickle.dumps(le))
f.close()

