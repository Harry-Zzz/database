import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

img = cv.imread('E:/Dicom/test/AxialSlice.jpg',cv.IMREAD_GRAYSCALE)
plt.imshow(img)
plt.show()

img_shape = img.shape
imgs = np.zeros(shape=(img_shape[0],img_shape[1],3),dtype=np.float32)
imgs[:,:,0]=img[:,:]
imgs[:,:,1]=img[:,:]
imgs[:,:,2]=img[:,:]

# cv.imshow('cv',imgs)
# # cv.waitKey()

plt.imshow(imgs)
plt.show()

print(type(imgs))
print(np.shape(imgs))
