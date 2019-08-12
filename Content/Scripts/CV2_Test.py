import unreal_engine as ue
import numpy as np
from PIL import ImageGrab
import cv2

def resize_image(img, scale_percent = 50):
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height) 
	return cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

class CV2_Window:

	# this is called on game start
	def begin_play(self):
		ue.log('Begin Play on CV2_Window class')

		# this is called at every 'tick'
	def tick(self, delta_time):
		screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
		# Reduce the size of the image and convert to grayscale
		# to reduce processing overhead for our NN
		screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		screen = resize_image(screen, 25)
		
		cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
		cv2.moveWindow('window', 2000, 500)

		# if cv2.waitKey(25) & 0xFF == ord('q'):
		# 	cv2.destroyAllWindows()
		# 	break
