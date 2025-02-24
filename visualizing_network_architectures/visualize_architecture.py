# import thee necessary packages
from utilities.nn import LeNet
from keras.utils import plot_model

# initialize Lenet and then write the network architecture visualization graph to disk
model = LeNet.build(28, 28, 1, 10)
plot_model(model, to_file="lenet.jpg", show_shapes=True)
