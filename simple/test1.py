import SimpleITK as sitk
import numpy
import vtk
from vtkmodules.util import numpy_support
import cv2

PathDicom = "E:/Dicom/test/DicomResource"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []


reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(PathDicom)
reader.SetFileNames(dicom_names)
image = reader.Execute()
image_array = sitk.GetArrayFromImage(image)  # z, y, x
origin = image.GetOrigin()  # x, y, z
spacing = image.GetSpacing()  # x, y, z
Dim = image.GetDimension()

image_array.transpose()


Array_vtk = numpy_support.numpy_to_vtk(image_array.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
imagedata = vtk.vtkImageData()
imagedata.SetOrigin(origin)
imagedata.SetSpacing(spacing)
imagedata.SetDimensions(Dim)
imagedata.GetPointData().SetScalars(Array_vtk)

origin = numpy.array(origin)
ConstPixelSpacing = numpy.array(spacing)
ConstPixelDims = numpy.array(Dim)

center = origin + (ConstPixelSpacing * ConstPixelDims / 2)


DirectionCosines_x = (0, 0, 1, 0, 1, 0, -1, 0, 0)
DirectionCosines_y = (1, 0, 0, 0, 0, -1, 0, 1, 0)
DirectionCosines_z = (1, 0, 0, 0, 1, 0, 0, 0, 1)

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
# print(m)
writer = vtk.vtkMetaImageWriter()
writer.SetInputData(image)
writer.SetFileName("E:/Dicom/test/DicomResource/test11.mhd")
writer.Write()


vtk_data = image.GetPointData().GetScalars()
arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1],m[0])
# print(numpy.max(arr))
# print(numpy.min(arr))
arr = (arr - numpy.min(arr))/((numpy.max(arr)-numpy.min(arr))/255)

print(numpy.shape(arr))

width = int(len(lstFilesDCM)*(ConstPixelSpacing[2]/ConstPixelSpacing[0]))
height = Dim[0]
dim = (width,height)
resized = cv2.resize(numpy.rot90(arr,-1),dim,interpolation=cv2.INTER_AREA)


cv2.imwrite('mip12.png',resized)
