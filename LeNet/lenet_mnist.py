# import the necessary packages
from utilities.nn import LeNet
from keras.optimizers import SGD
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets
from keras import backend as K
import matplotlib.pyplot as plt
import numpy as np

# grab the MNIST dataset (if this is the first time using this dataset then the 55MB download may take a minute)
print("[INFO] accessing MNIST...")
dataset = datasets.fetch_mldata("MNIST Original")
data = dataset.data

# if we are using "channels_first" ordering, then reshape the design matrix such that the matrix is num_samples x depth x rows x columns
if K.image_data_format() == "channels_first":
    data = data.reshape(data.shape[0], 1, 28, 28)
# otherwise we are using channels_last ordering, so the design matrix shape would be: num_samples, rows, column, depth
else:
    data = data.reshape(data.shape[0], 28, 28, 1)

# scale the input data to range [0, 1] and perform train test split
(trainX, testX, trainY, testY) = train_test_split(data/255.0,
                                                  dataset.target.astype("int"), test_size=0.25, random_state=42)

# convert the labels from integers to vectors
le = LabelBinarizer()
trainY = le.fit_transform(trainY)
testY = le.fit_transform(testY)

# initialize the optimizer and the model
print("[INFO] compiling model...")
opt = SGD(lr=0.001)
model = LeNet.build(width=28, height=28, depth=1, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit(trainX, trainY, validation_data=(testX, testY),
              batch_size=128, epochs=20, verbose=1)

# evaluate the network
print("[INFO] evaluating the network...")
predictions= model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1),
                            target_names=[str(x) for x in le.classes_]))

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 20), H.history["loss"], label="training loss")
plt.plot(np.arange(0, 20), H.history["val_loss"], label="validation loss")
plt.plot(np.arange(0, 20), H.history["acc"], label="training accuracy")
plt.plot(np.arange(0, 20), H.history["val_acc"], label="validation accuracy")
plt.title("Training loss and accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Training Loss/Accuracy")
plt.legend()
plt.savefig("lenet_minist.png")
plt.show()
