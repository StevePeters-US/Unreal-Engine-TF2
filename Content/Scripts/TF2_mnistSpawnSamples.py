#converted for ue4 use from
#https://github.com/tensorflow/docs/blob/master/site/en/tutorials/_index.ipynb

#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

import tensorflow as tf
mnist = tf.keras.datasets.mnist

import unreal_engine as ue
from TFPluginAPI import TFPluginAPI

#additional includes
#from tensorflow.python.keras import backend as K	#to ensure things work well with multi-threading
import numpy as np   	#for reshaping input
import operator      	#used for getting max prediction from 1x10 output array
import random

class MnistTutorial(TFPluginAPI):

	#keras stop callback
	class StopCallback(tf.keras.callbacks.Callback):
		def __init__(self, outer):
			self.outer = outer

		def on_train_begin(self, logs={}):
			self.losses = []

		def on_batch_end(self, batch, logs={}):
			if(self.outer.shouldStop):
				#notify on first call
				if not (self.model.stop_training):
					ue.log('Early stop called!')
				self.model.stop_training = True

			else:
				if(batch % 5 == 0):
					#json convertible types are float64 not float32
					logs['acc'] = np.float64(logs['acc'])
					logs['loss'] = np.float64(logs['loss'])
					self.outer.callEvent('TrainingUpdateEvent', logs, True)

				#callback an example image from batch to see the actual data we're training on
				if((batch*self.outer.batch_size) % 100 == 0):
					index = random.randint(0,self.outer.batch_size)*batch
					self.outer.jsonPixels['pixels'] = self.outer.x_train[index].ravel().tolist()
					self.outer.callEvent('PixelEvent', self.outer.jsonPixels, True)


	#Called when TensorflowComponent sends Json input
	def onJsonInput(self, jsonInput):
		#build the result object
		result = {'prediction':-1}

		#If we try to predict before training is complete
		if not hasattr(self, 'model'):
			ue.log_warning("Warning! No 'model' found, prediction invalid. Did training complete?")
			return result

		#prepare the input, reshape 784 array to a 1x28x28 array
		x_raw = jsonInput['pixels']
		x = np.reshape(x_raw, (1, 28, 28))

		predictions = self.model.predict(x)
		#ue.log(predictions)

		# #run the input through our network using stored model and graph
		# with self.graph.as_default():
		# 	output = self.model.predict(x)

		#convert output array to max value prediction index (0-10)
		#index, value = max(enumerate(output[0]), key=operator.itemgetter(1))

		index, value = max(enumerate(predictions[0]), key=operator.itemgetter(1))

		#Optionally log the output so you can see the weights for each value and final prediction
		ue.log('Predictions array: ' + str(predictions) + ',\nPrediction: ' + str(index))

		result['prediction'] = index

		return result

	#Called when TensorflowComponent signals begin training (default: begin play)
	#@tf.function
	def onBeginTraining(self):
		ue.log("starting MnistTutorial training")

		#training parameters
		self.batch_size = 128
		num_classes = 10
		epochs = 1 		
		
		(x_train, y_train),(x_test, y_test) = mnist.load_data()
		x_train, x_test = x_train / 255.0, x_test / 255.0

		model = tf.keras.models.Sequential([
			tf.keras.layers.Flatten(input_shape=(28, 28)),
			tf.keras.layers.Dense(512, activation=tf.nn.relu),
			tf.keras.layers.Dropout(0.2),
			tf.keras.layers.Dense(num_classes, activation=tf.nn.softmax)
			])
		model.compile(optimizer='adam',
					loss='sparse_categorical_crossentropy',
					metrics=['accuracy'])

		model.fit(x_train, y_train, epochs=epochs)
		model.evaluate(x_test, y_test)
		
		# self.outer.jsonPixels['pixels'] = self.outer.x_train[index].ravel().tolist()
		# self.outer.callEvent('PixelEvent', self.outer.jsonPixels, True)
		
		ue.log("Training complete.")

		#store our model for prediction
		#self.graph = tf.get_default_graph()
		self.model = model

#required function to get our api
def getApi():
	#return CLASSNAME.getInstance()
	return MnistTutorial.getInstance()
