import os
import pydicom
import numpy
from matplotlib import pyplot
from PIL import Image
import PIL
import SimpleITK as sitk
import vtk
from vtkmodules.util import numpy_support
import cv2
import io
from natsort import natsorted



PathDicom = "E:/Dicom/test/DicomResource"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []
DcmName = []
for dirName, subdirList, fileList in sorted(os.walk(PathDicom)):
    fileList = natsorted(fileList)
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
            DcmName.append(filename)

'''
RefDs = pydicom.read_file(lstFilesDCM[0],force=True)
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(PathDicom)
reader.SetFileNames(dicom_names)
image = reader.Execute()
columns = RefDs.Columns
row = RefDs.Rows
ConstOrigin = image.GetOrigin()
ConstPixelSpacing = image.GetSpacing()
ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
'''
gap = len(DcmName) - 1
file_one = pydicom.read_file(lstFilesDCM[0],force=True)
z_one = file_one.ImagePositionPatient[2]
file_tow = pydicom.read_file(lstFilesDCM[gap],force=True)
z_tow = file_tow.ImagePositionPatient[2]
columns = file_one.Columns
row = file_one.Rows
ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
if z_one > z_tow:
    slice_gap = (z_one - z_tow)/gap
    ConstOrigin = (file_tow.ImagePositionPatient[0],file_tow.ImagePositionPatient[1],file_tow.ImagePositionPatient[2])
    ConstPixelSpacing = (float(file_tow.PixelSpacing[0]), float(file_tow.PixelSpacing[1]), float(slice_gap))
else:
    slice_gap = (z_tow - z_one)/gap
    ConstOrigin = (file_one.ImagePositionPatient[0],file_one.ImagePositionPatient[1],file_one.ImagePositionPatient[2])
    ConstPixelSpacing = (float(file_one.PixelSpacing[0]), float(file_one.PixelSpacing[1]), float(slice_gap))

image_1 = int(ConstPixelDims[0]//2)
image_2 = int(ConstPixelDims[1]//2)
image_3 = int(ConstPixelDims[2]//2)
x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0],ConstPixelSpacing[0])  # 0到（第一个维数加一*像素间的间隔），步长为constpixelSpacing
y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1],ConstPixelSpacing[1])  #
z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2],ConstPixelSpacing[2])  #
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=file_one.pixel_array.dtype)

# 遍历所有的dicom文件，读取图像数据，存放在numpy数组中
for filenameDCM in lstFilesDCM:
    ds = pydicom.read_file(filenameDCM,force=True)
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

'''
fig1 = pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, image_3]))  # 第三个维度表示现在展示的是第几层
pyplot.axis('off')
buffer_ = io.BytesIO()
pyplot.savefig(buffer_,format='png')
buffer_.seek(0)
img1 = PIL.Image.open(buffer_)
img_arr1 = numpy.asarray(img1)
buffer_.close()

fig2 = pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(y, z, numpy.fliplr(numpy.rot90((ArrayDicom[image_1, :, :]),3)))
pyplot.axis('off')
buffer_ = io.BytesIO()
pyplot.savefig(buffer_,format='png')
buffer_.seek(0)
img2 = PIL.Image.open(buffer_)
img_arr2 = numpy.asarray(img2)
buffer_.close()

fig3 = pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal','datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, z, numpy.fliplr(numpy.rot90((ArrayDicom[:, image_2, :]),3)))
pyplot.axis('off')
buffer_ = io.BytesIO()
pyplot.savefig(buffer_,format='png')
buffer_.seek(0)
img3 = PIL.Image.open(buffer_)
img_arr3 = numpy.asarray(img3)
buffer_.close()

pyplot.figure(figsize=(3,1),dpi=300)
pyplot.subplot(131)
pyplot.imshow(img_arr1)
pyplot.title('AxialSlice',fontsize=4,y=0.9)
pyplot.axis('off')
pyplot.xticks([])
pyplot.yticks([])
pyplot.subplot(132)
pyplot.imshow(img_arr2)
pyplot.title('CoronalSlice',fontsize=4,y=0.9)
pyplot.axis('off')
pyplot.xticks([])
pyplot.yticks([])
pyplot.subplot(133)
pyplot.imshow(img_arr3)
pyplot.title('SagitalSlice',fontsize=4,y=0.9)
pyplot.axis('off')
pyplot.xticks([])
pyplot.yticks([])
pyplot.tight_layout(pad=0.5,w_pad=2)
pyplot.subplots_adjust(wspace=0,hspace=0)
# pyplot.savefig('E:\\Dicom\\test\\images\\'+'image.jpg')
pyplot.show()

'''
'''
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, image_3]))  # 第三个维度表示现在展示的是第几层
pyplot.axis('off')
pyplot.savefig('E:\\Dicom\\test\\images\\'+'AxialSlice'+'.jpg',bbox_inches='tight',pad_inches=0.0)
pyplot.show()




pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(y, z, numpy.fliplr(numpy.rot90((ArrayDicom[image_1, :, :]),3)))
pyplot.axis('off')
pyplot.savefig('E:\\Dicom\\test\\images\\'+'CoronalSlice'+'.jpg',bbox_inches='tight',pad_inches=0.0)
pyplot.show()

pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, z, numpy.fliplr(numpy.rot90((ArrayDicom[:, image_2, :]),3)))
pyplot.axis('off')
pyplot.savefig('E:\\Dicom\\test\\images\\'+'SagitalSlice'+'.jpg',bbox_inches='tight',pad_inches=0.0)
pyplot.show()

'''

Array_vtk = numpy_support.numpy_to_vtk(ArrayDicom.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
imagedata = vtk.vtkImageData()
imagedata.SetOrigin(ConstOrigin)
imagedata.SetSpacing(ConstPixelSpacing)
imagedata.SetDimensions(ConstPixelDims)
imagedata.GetPointData().SetScalars(Array_vtk)
origin = numpy.array(ConstOrigin)
ConstPixelSpacing = numpy.array(ConstPixelSpacing)
ConstPixelDims = numpy.array(ConstPixelDims)
center = origin + (ConstPixelSpacing * ConstPixelDims / 2)
DirectionCosines_x = (0, 0, 1, 0, 1, 0, -1, 0, 0)
DirectionCosines_y = (1, 0, 0, 0, 0, -1, 0, 1, 0)
DirectionCosines_z = (1, 0, 0, 0, 1, 0, 0, 0, 1)

def mip_x():
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
    arr = (arr - numpy.min(arr)) / ((numpy.max(arr) - numpy.min(arr)) / 255)
    width = columns
    height = int(len(lstFilesDCM) * (ConstPixelSpacing[2] / ConstPixelSpacing[1]))
    dim = (width, height)
    resized = cv2.resize(numpy.rot90(arr, 1), dim, interpolation=cv2.INTER_AREA)
    return resized

def mip_y():
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
    arr = (arr - numpy.min(arr)) / ((numpy.max(arr) - numpy.min(arr)) / 255)
    width = int(len(lstFilesDCM) * (ConstPixelSpacing[2] / ConstPixelSpacing[0]))
    height = row
    dim = (width, height)
    resized = cv2.resize(numpy.rot90(arr, -1), dim, interpolation=cv2.INTER_AREA)
    # cv2.imwrite( path +'/'+ name +'.jpg', resized)
    return resized

def mip_z():
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
    arr = (arr - numpy.min(arr)) / ((numpy.max(arr) - numpy.min(arr)) / 255)
    arr = numpy.rot90(arr,-1)
    # cv2.imwrite(path+'/'+name+'.jpg', numpy.rot90(arr, -1))
    return arr


pyplot.figure(figsize=(3,1),dpi=300)
pyplot.subplot(131)
pyplot.imshow(mip_z(),cmap='gray')
pyplot.title('AxialSlice_MIP',fontsize=4,y=1.1)
pyplot.xticks([])
pyplot.yticks([])
pyplot.subplot(132)
pyplot.imshow(mip_x(),cmap='gray')
pyplot.title('CoronalSlice_MIP',fontsize=4,y=1.1)
pyplot.xticks([])
pyplot.yticks([])
pyplot.subplot(133)
pyplot.imshow(numpy.rot90(mip_y(),1),cmap='gray')
pyplot.title('SagitalSlice_MIP',fontsize=4,y=1.1)
pyplot.xticks([])
pyplot.yticks([])
pyplot.tight_layout(pad=1.3,w_pad=2)
pyplot.subplots_adjust(wspace=0,hspace=0)
# pyplot.savefig('E:\\Dicom\\test\\images\\'+'MIP_image.jpg')
pyplot.show()
