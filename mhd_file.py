import cv2
import SimpleITK as sitk
from matplotlib import pyplot
import numpy as np
from vtkmodules.util import numpy_support
import vtk


image =sitk.ReadImage('G:/test/ART_VC_uCT/OUTPUT_0000_Volume.mhd')
image_arr = sitk.GetArrayFromImage(image)
image_arr = image_arr.transpose()
ConstOrigin = image.GetOrigin()
ConstPixelSpacing = image.GetSpacing()
ConstPixelDims = np.shape(image_arr)
print(ConstPixelDims)

image_1 = int(ConstPixelDims[0]//2)
image_2 = int(ConstPixelDims[1]//2)
image_3 = int(ConstPixelDims[2]//2)

x = np.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0],ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1],ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2],ConstPixelSpacing[2])


pyplot.figure(dpi=300)
pyplot.subplot(1,3,1)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y,np.flipud(image_arr[:, :, image_3]).transpose())
# pyplot.axis('off')
# pyplot.savefig('G:/test/ART_VC_uCT/'+'AxialSlice'+'.jpg')
# pyplot.show()

pyplot.subplot(1,3,2)
# pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(y, z, np.fliplr(np.rot90((image_arr[image_1, :, :]),3)))
# pyplot.axis('off')
# pyplot.savefig('G:/test/ART_VC_uCT/'+'CoronalSlice'+'.jpg')
# pyplot.show()

pyplot.subplot(1,3,3)
# pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, z, np.fliplr(np.rot90((image_arr[:, image_2, :]),3)))
# pyplot.axis('off')
# pyplot.savefig('G:/test/ART_VC_uCT/'+'SagitalSlice'+'.jpg')
pyplot.show()



Array_vtk = numpy_support.numpy_to_vtk(image_arr.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
imagedata = vtk.vtkImageData()
imagedata.SetOrigin(ConstOrigin)
imagedata.SetSpacing(ConstPixelSpacing)
imagedata.SetDimensions(ConstPixelDims)
imagedata.GetPointData().SetScalars(Array_vtk)
origin = np.array(ConstOrigin)
ConstPixelSpacing = np.array(ConstPixelSpacing)
ConstPixelDims = np.array(ConstPixelDims)
center = origin + (ConstPixelSpacing * ConstPixelDims / 2)
DirectionCosines_x = (0, 0, 1, 0, 1, 0, -1, 0, 0)
DirectionCosines_y = (1, 0, 0, 0, 0, -1, 0, 1, 0)
DirectionCosines_z = (1, 0, 0, 0, 1, 0, 0, 0, 1)

Path = ('G:/test/ART_VC_uCT/')


def mip_x(path,name):
    ImageSlab = vtk.vtkImageSlabReslice()
    ImageSlab.SetInputData(imagedata)
    ImageSlab.SetResliceAxesOrigin(center)
    ImageSlab.SetResliceAxesDirectionCosines(DirectionCosines_x)
    ImageSlab.SetSlabThickness(ConstPixelSpacing[0]*ConstPixelDims[0])
    ImageSlab.SetBlendModeToMax()
    ImageSlab.SetSlabResolution(ConstPixelSpacing[0])
    ImageSlab.Update()
    image = ImageSlab.GetOutput()
    m = image.GetDimensions()
    vtk_data = image.GetPointData().GetScalars()
    arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1], m[0])
    arr = (arr - np.min(arr)) / ((np.max(arr) - np.min(arr)) / 255)
    width = ConstPixelDims[1]
    height = int(ConstPixelDims[2] * (ConstPixelSpacing[2] / ConstPixelSpacing[1]))
    dim = (width, height)
    resized = cv2.resize(np.rot90(arr, 1), dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite( path + name +'.jpg', resized)
    return None


def mip_y(path,name):
    ImageSlab = vtk.vtkImageSlabReslice()
    ImageSlab.SetInputData(imagedata)
    ImageSlab.SetResliceAxesOrigin(center)
    ImageSlab.SetResliceAxesDirectionCosines(DirectionCosines_y)
    ImageSlab.SetSlabThickness(ConstPixelSpacing[1]*ConstPixelDims[1])
    ImageSlab.SetBlendModeToMax()
    ImageSlab.SetSlabResolution(ConstPixelSpacing[1])
    ImageSlab.Update()
    image = ImageSlab.GetOutput()
    m = image.GetDimensions()
    vtk_data = image.GetPointData().GetScalars()
    arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1], m[0])
    arr = (arr - np.min(arr)) / ((np.max(arr) - np.min(arr)) / 255)
    width = int(ConstPixelDims[2] * (ConstPixelSpacing[2] / ConstPixelSpacing[0]))
    height = ConstPixelDims[0]
    dim = (width, height)
    resized = cv2.resize(np.rot90(arr, -1), dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite( path + name +'.jpg', resized)
    return None


def mip_z(path,name):
    ImageSlab = vtk.vtkImageSlabReslice()
    ImageSlab.SetInputData(imagedata)
    ImageSlab.SetResliceAxesOrigin(center)
    ImageSlab.SetResliceAxesDirectionCosines(DirectionCosines_z)
    ImageSlab.SetSlabThickness(ConstPixelSpacing[2] * ConstPixelDims[2])
    ImageSlab.SetBlendModeToMax()
    ImageSlab.SetSlabResolution(ConstPixelSpacing[2])
    ImageSlab.Update()
    image = ImageSlab.GetOutput()
    m = image.GetDimensions()
    vtk_data = image.GetPointData().GetScalars()
    arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1], m[0])
    arr = (arr - np.min(arr)) / ((np.max(arr) - np.min(arr)) / 255)
    cv2.imwrite( path + name +'.jpg', arr)
    return None

mip_x(Path,'x')
mip_y(Path,'y')
mip_z(Path,'z')