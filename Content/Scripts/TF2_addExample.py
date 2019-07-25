#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()

import tensorflow as tf
import unreal_engine as ue
from TFPluginAPI import TFPluginAPI

class ExampleAPI(TFPluginAPI):

	#expected optional api: setup your model for training
	def onSetup(self):

		self.a = tf.Variable([0.0], tf.float32)
		self.b = tf.Variable([0.0], tf.float32)

		self.op = tf.Variable(True, tf.bool)
		pass
		
	#expected optional api: parse input object and return a result object, which will be converted to json for UE4
	def onJsonInput(self, jsonInput):
		
		print(jsonInput)

		self.a = tf.dtypes.cast(jsonInput['a'], tf.float32)
		self.b = tf.dtypes.cast(jsonInput['b'], tf.float32)

		if self.op:
			return tf.add(self.a, self.b).numpy().tolist()
			
		else:
			return tf.subtract(self.a, self.b).numpy().tolist()

		
	

	#custom function to change the op
	def changeOperation(self, type):
		if(type == '+'):
			self.op = True

		elif(type == '-'):
			self.op = False

	def getVersion(self, jsonInput):

		ver = tf.__version__
		print(ver)
		return("GPU Available: ", tf.test.is_gpu_available())


	#expected optional api: start training your network
	def onBeginTraining(self):
		pass
    
#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def getApi():
	#return CLASSNAME.getInstance()
	return ExampleAPI.getInstance()