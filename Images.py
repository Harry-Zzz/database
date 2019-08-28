import os
import pydicom
import numpy
from matplotlib import pyplot
from PIL import Image
import SimpleITK as sitk
import vtk
from vtkmodules.util import numpy_support
import cv2


# 用lstFilesDCM作为存放DICOM files的列表
PathDicom = "G:/Dalian_PETCT/2010-04__Studies/jie ming_P00000012_CT_2010-04-23_095007_PET^1.PETCT.WholeBody.HD.(Adult)_AC.CT_n329__00000"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []

for dirName, subdirList, fileList in sorted(os.walk(PathDicom)):
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            # print(filename)
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中




# 将第一张图片作为参考图
RefDs = pydicom.read_file(lstFilesDCM[0])  # 读取第一张dicom图片

# 建立三维数组
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
print(ConstPixelDims)
image_1 = int(RefDs.Rows//2)
image_2 = int(RefDs.Columns//2)
image_3 = int(len(lstFilesDCM)//2)

reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(PathDicom)
reader.SetFileNames(dicom_names)
image = reader.Execute()
# image_array = sitk.GetArrayFromImage(image)
# origin = image.GetOrigin()
spacing = image.GetSpacing()[2]
origin = image.GetOrigin()



# 得到spacing值 (mm为单位)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(spacing))

# 三维数据

x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])  # 0到（第一个维数加一*像素间的间隔），步长为constpixelSpacing
y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])  #
z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * spacing, spacing)  #
# z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * 2, 2)  #

ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
print(type(ArrayDicom))

# 遍历所有的dicom文件，读取图像数据，存放在numpy数组中
for filenameDCM in lstFilesDCM:
    ds = pydicom.read_file(filenameDCM)
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array




'''
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, image_3]))  # 第三个维度表示现在展示的是第几层
pyplot.axis('off')
# pyplot.savefig('E:\\Dicom\\test\\images\\'+'AxialSlice'+'.jpg')
pyplot.show()


pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, z, numpy.fliplr(numpy.rot90((ArrayDicom[image_1, :, :]),3)))
pyplot.axis('off')
# pyplot.savefig('E:\\Dicom\\test\\images\\'+'CoronalSlice'+'.jpg')
pyplot.show()

pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, z, numpy.fliplr(numpy.rot90((ArrayDicom[:, image_2, :]),3)))
pyplot.axis('off')
# pyplot.savefig('E:\\Dicom\\test\\images\\'+'SagitalSlice'+'.jpg')
pyplot.show()


Array_vtk = numpy_support.numpy_to_vtk(ArrayDicom.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
imagedata = vtk.vtkImageData()
imagedata.SetOrigin(origin)
imagedata.SetSpacing(ConstPixelSpacing)
imagedata.SetDimensions(ConstPixelDims)
imagedata.GetPointData().SetScalars(Array_vtk)

origin = numpy.array(origin)
ConstPixelSpacing = numpy.array(ConstPixelSpacing)
ConstPixelDims = numpy.array(ConstPixelDims)

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
# writer = vtk.vtkMetaImageWriter()
# writer.SetInputData(image)
# writer.SetFileName("E:/Dicom/test/DicomResource/test11.mhd")
# writer.Write()


vtk_data = image.GetPointData().GetScalars()
arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1],m[0])
arr = (arr - numpy.min(arr))/((numpy.max(arr)-numpy.min(arr))/255)
width = int(len(lstFilesDCM)*(ConstPixelSpacing[2]/ConstPixelSpacing[0]))
height = RefDs.Rows
dim = (width,height)
resized = cv2.resize(numpy.rot90(arr,-1),dim,interpolation=cv2.INTER_AREA)
cv2.imwrite('mip12.png',resized)




# PlaneOrigin = origin+(ConstPixelSpacing*ConstPixelDims)
# plane = vtk.vtkPlane()
# plane.SetOrigin(PlaneOrigin)
# #plane.Update()
# imageResliceMapper = vtk.vtkImageResliceMapper()
# imageResliceMapper.SetInputData(imagedata)
# imageResliceMapper.SetSlicePlane(plane)
# imageResliceMapper.SetSlabThickness(20)
# imageResliceMapper.SetSlabTypeToMax()
# imageResliceMapper.Update()
#
#
#
# print(type(imageResliceMapper.GetOutputPort()))
# output = imageResliceMapper.GetOutput().GetPoints().GetData()
# array = numpy_support.vtk_to_numpy(output)



# vtkSmartPointer < vtkPlane > plane = vtkSmartPointer < vtkPlane >::New();
# plane->SetOrigin(center)
# vtkSmartPointer < vtkImageResliceMapper > imageResliceMapper = vtkSmartPointer < vtkImageResliceMapper >::New();
# imageResliceMapper->SetInputConnection(reader->GetOutputPort());
# imageResliceMapper->SetSlicePlane(plane);
# imageResliceMapper->SetSlabThickness(20);
# imageResliceMapper->SetSlabTypeToMax();
# double
# thickness = imageResliceMapper->GetSlabThickness();

'''

