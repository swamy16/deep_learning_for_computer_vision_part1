# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from utilities.nn import MiniVGGNet
from keras.callbacks import LearningRateScheduler
from keras.optimizers import SGD
from keras.datasets import cifar10
import matplotlib.pyplot as plt
import numpy as np
import argparse

def step_decay(epoch):
    # initialize the base initial learning rate, drop factor and epochs to drop every
    initAlpha = 0.01
    factor = 0.5
    dropEevery = 5

    alpha = initAlpha*(factor**np.floor((1+epoch)/dropEevery))

    # return the learning rate
    return float(alpha)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
                help="path to the output loss accuracy plot")
args = vars(ap.parse_args())

# load the training testing data and scale it to the range [0, 1]
print("[INFO] loading the CIFAR10 dataset...")
((trainX, trainY), (testX, testY)) = cifar10.load_data()
trainX = trainX.astype("float")/255.0
testX = testX.astype("float")/255.0

# convert the labels from integers to vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.fit_transform(testY)

# initialize the label names for CIFAR-10 dataset
labelNames = ["airplane", "automobile", "bird", "cat", "deer",
              "dog", "frog", "horse", "ship", "truck"]

# define the set of callbacks to be passed to the model during training
"""
The below line initializes our list of callbacks. Depending on how the callback is defined, keras will call this function at the start and end of every epoch, 
minibatch update etc. The LearningRateScheduler will call the step decay at the end of every epoch allowing us to the learning prior to the next epoch starting. 
"""
callbacks = [LearningRateScheduler(step_decay)]

# initialize the optimizer and model
opt = SGD(lr =0.01, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
               metrics=["accuracy"])

# train the network
H = model.fit(trainX, trainY, validation_data=(testX, testY),
              batch_size=64, epochs=40, callbacks=callbacks, verbose=1)

# evaluate the network
print("[INFO] evaluating the network...")
predictions = model.predict(testX, batch_size=64)
print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1),
                            target_names=labelNames))

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 40), H.history["loss"], label="training loss")
plt.plot(np.arange(0, 40) H.history["val_loss"], label="validation loss")
plt.plot(np.arange(0, 40), H.history["acc"], label="training accuracy")
plt.plot(np.arange(0, 40), H.history["val_acc"], label="training accuracy")
plt.title("Training loss and accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy/Loss")
plt.legend()
plt.savefig(args["output"])