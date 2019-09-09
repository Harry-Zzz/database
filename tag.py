import pydicom
import SimpleITK as sitk
import os
import pydicom
import numpy
from matplotlib import pyplot
from PIL import Image
import PIL
from vtkmodules.util import numpy_support
import cv2
import io
import vtk
from natsort import natsorted
from matplotlib import pylab


def Patient_Info(filepath):
    information = {}
    lstFilesDCM = []
    for dirName, subdirList, fileList in os.walk(filepath):
        fileList = natsorted(fileList)
        for filename in fileList:
            if ".dcm" in filename.lower():
                lstFilesDCM.append(os.path.join(dirName, filename))

    ds = pydicom.read_file(lstFilesDCM[0],force=True)
    information['ID'] = ds.PatientID
    try:
        information['Age'] = ds.PatientAge
    except AttributeError:
        information['Age'] = '0'
    try:
        information['BirthDate'] = ds.PatientBirthDate
    except AttributeError:
        information['BirthDate'] = '0'
    try:
        information['Sex'] = ds.PatientSex
    except AttributeError:
        information['Sex'] = 'none'
    try:
        information['Size'] = ds.PatientSize
    except AttributeError:
        information['Size'] = '0'
    try:
        information['Weight'] = ds.PatientWeight
    except AttributeError:
        information['Weight'] = '0'
    information['study_date'] = ds.StudyDate
    information['study_time'] = ds.StudyTime
    return information



# print(type(Patient_Info(filename)))



def Image_Para(filepath):
    information = {}
    lstFilesDCM = []
    DcmName = []
    for dirName, subdirList, fileList in os.walk(filepath):
        fileList = natsorted(fileList)
        for filename in fileList:
            if ".dcm" in filename.lower():
                lstFilesDCM.append(os.path.join(dirName, filename))
                DcmName.append(filename)
    ds = pydicom.read_file(lstFilesDCM[0],force=True)
    gap = len(DcmName) - 1
    file_one = pydicom.read_file(lstFilesDCM[0], force=True)
    z_one = file_one.ImagePositionPatient[2]
    file_tow = pydicom.read_file(lstFilesDCM[gap], force=True)
    z_tow = file_tow.ImagePositionPatient[2]
    columns = file_one.Columns
    row = file_one.Rows
    ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
    if z_one > z_tow:
        slice_gap = (z_one - z_tow) / gap
        ConstOrigin = (file_tow.ImagePositionPatient[0], file_tow.ImagePositionPatient[1], file_tow.ImagePositionPatient[2])
        ConstPixelSpacing = (float(file_tow.PixelSpacing[0]), float(file_tow.PixelSpacing[1]), float(slice_gap))
    else:
        slice_gap = (z_tow - z_one) / gap
        ConstOrigin = (file_one.ImagePositionPatient[0], file_one.ImagePositionPatient[1], file_one.ImagePositionPatient[2])
        ConstPixelSpacing = (float(file_one.PixelSpacing[0]), float(file_one.PixelSpacing[1]), float(slice_gap))
    information['DimSize'] = ConstPixelDims
    information['Orign'] = ConstOrigin
    information['Spacing'] = ConstPixelSpacing
    try:
        information['Intercept'] = ds.RescaleIntercept
    except AttributeError:
        information['Intercept'] = 'none'
    try:
        information['Slope'] = ds.RescaleSlope
    except AttributeError:
        information['Slope'] = 'none'
    information['WindowCenter'] = ds.WindowCenter
    information['WindowWidth'] = ds.WindowWidth
    information['Thumbnail'] = str('./'+'DataFile'+'/'+filepath.split('/',2)[2] + '/' + 'image.jpg')
    information['Thumbnail_MIP'] = str('./'+'DataFile'+'/'+filepath.split('/',2)[2] + '/' + 'MIP_image.jpg')
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    information['Series_Des'] = ds.SeriesDescription
    information['Study_Des'] = ds.StudyDescription
    return information


# def loadFileInformation(filename):
#     information = {}
#     ds = pydicom.read_file(filename,force=True)
#     information['BodyPart'] = ds.BodyPartExamined
#     information['PatientID'] = ds.PatientID
#     information['PatientPosition'] = ds.PatientPosition
#     information['PatientName'] = ds.PatientName
#     information['PatientBirthDate'] = ds.PatientBirthDate
#     information['PatientSex'] = ds.PatientSex
#     information['PatientSize'] = ds.PatientSize
#     information['PatientWeight'] = ds.PatientWeight
#     information['PixelSpacing'] = ds.PixelSpacing
#     information['SeriesDescription'] = ds.SeriesDescription
#     information['SamplesPerPixel'] = ds.SamplesPerPixel
#     information['InstitutionName'] = ds.InstitutionName
#     information['ImageType'] = ds.ImageType
#     information['Manufacturer'] = ds.Manufacturer
#     information['WindowCenter'] = ds.WindowCenter
#     information['WindowWidth'] = ds.WindowWidth
#     information['PixelData'] = ds.PixelData
#     # try:
#     #     information['None'] = ds.wewqeqeq
#     # except AttributeError:
#     #     information['None'] = None
#     # print(dir(ds))
#     # print(type(information))
#     return information
def Get_image(filepath):
    lstFilesDCM = []
    DcmName = []
    for dirName, subdirList, fileList in sorted(os.walk(filepath)):
        fileList = natsorted(fileList)
        for filename in fileList:
            if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
                lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
                DcmName.append(filename)

    gap = len(DcmName) - 1
    file_one = pydicom.read_file(lstFilesDCM[0], force=True)
    z_one = file_one.ImagePositionPatient[2]
    file_tow = pydicom.read_file(lstFilesDCM[gap], force=True)
    z_tow = file_tow.ImagePositionPatient[2]
    columns = file_one.Columns
    row = file_one.Rows
    ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
    if z_one > z_tow:
        slice_gap = (z_one - z_tow) / gap
        ConstOrigin = (
        file_tow.ImagePositionPatient[0], file_tow.ImagePositionPatient[1], file_tow.ImagePositionPatient[2])
        ConstPixelSpacing = (float(file_tow.PixelSpacing[0]), float(file_tow.PixelSpacing[1]), float(slice_gap))
    else:
        slice_gap = (z_tow - z_one) / gap
        ConstOrigin = (
        file_one.ImagePositionPatient[0], file_one.ImagePositionPatient[1], file_one.ImagePositionPatient[2])
        ConstPixelSpacing = (float(file_one.PixelSpacing[0]), float(file_one.PixelSpacing[1]), float(slice_gap))
    image_1 = int(ConstPixelDims[0] // 2)
    image_2 = int(ConstPixelDims[1] // 2)
    image_3 = int(ConstPixelDims[2] // 2)
    x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])  # 0到（第一个维数加一*像素间的间隔），步长为constpixelSpacing
    y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])  #
    z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])  #
    ArrayDicom = numpy.zeros(ConstPixelDims, dtype=file_one.pixel_array.dtype)

    # 遍历所有的dicom文件，读取图像数据，存放在numpy数组中
    for filenameDCM in lstFilesDCM:
        ds = pydicom.read_file(filenameDCM)
        ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

    pyplot.figure(dpi=300)
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

    pyplot.figure(dpi=300)
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

    pyplot.figure(dpi=300)
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
    pyplot.savefig(filepath+'/'+'image.jpg')
    pyplot.show()

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
        ImageSlab.SetSlabThickness(ConstPixelSpacing[0] * ConstPixelDims[0])
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
        ImageSlab.SetSlabThickness(ConstPixelSpacing[1] * ConstPixelDims[1])
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
        arr = numpy.rot90(arr, -1)
        # cv2.imwrite(path+'/'+name+'.jpg', numpy.rot90(arr, -1))
        return arr

    pyplot.figure(figsize=(3, 1), dpi=300)
    pyplot.subplot(131)
    pyplot.imshow(mip_z(), cmap='gray')
    pyplot.title('AxialSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(132)
    pyplot.imshow(mip_x(), cmap='gray')
    pyplot.title('CoronalSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(133)
    pyplot.imshow(numpy.rot90(mip_y(), 1), cmap='gray')
    pyplot.title('SagitalSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.tight_layout(pad=1.3, w_pad=2)
    pyplot.subplots_adjust(wspace=0, hspace=0)
    pyplot.savefig(filepath + '/'+'MIP_image.jpg')
    pyplot.show()
    return None

def One_image(filepath):
    lstFilesDCM = []
    DcmName = []
    for dirName, subdirList, fileList in sorted(os.walk(filepath)):
        fileList = natsorted(fileList)
        for filename in fileList:
            if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
                lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
                DcmName.append(filename)
    ds = pydicom.dcmread(lstFilesDCM[0], force=True)
    pylab.imshow(ds.pixel_array, cmap=pylab.cm.gray)
    pylab.axis('off')
    pylab.savefig(filepath + '/'+'image.jpg')
    pylab.show()
    return None

def Gdcm_image(filepath):
    lstFilesDCM = []
    DcmName = []
    for dirName, subdirList, fileList in sorted(os.walk(filepath)):
        fileList = natsorted(fileList)
        for filename in fileList:
            if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
                lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
                DcmName.append(filename)
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filepath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    image_arr = sitk.GetArrayFromImage(image)
    image_arr = image_arr.transpose()
    ConstOrigin = image.GetOrigin()
    ConstPixelSpacing = image.GetSpacing()
    ConstPixelDims = numpy.shape(image_arr)

    image_1 = int(ConstPixelDims[0] // 2)
    image_2 = int(ConstPixelDims[1] // 2)
    image_3 = int(ConstPixelDims[2] // 2)

    x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])

    fig1 = pyplot.figure(dpi=300)
    pyplot.axes().set_aspect('equal', 'datalim')
    pyplot.set_cmap(pyplot.gray())
    pyplot.pcolormesh(x, y, numpy.flipud(image_arr[:, :, image_3]).transpose())  # 第三个维度表示现在展示的是第几层
    pyplot.axis('off')
    buffer_ = io.BytesIO()
    pyplot.savefig(buffer_, format='png')
    buffer_.seek(0)
    img1 = PIL.Image.open(buffer_)
    img_arr1 = numpy.asarray(img1)
    buffer_.close()

    fig2 = pyplot.figure(dpi=300)
    pyplot.axes().set_aspect('equal', 'datalim')
    pyplot.set_cmap(pyplot.gray())
    pyplot.pcolormesh(y, z, numpy.fliplr(numpy.rot90((image_arr[image_1, :, :]), 3)))
    pyplot.axis('off')
    buffer_ = io.BytesIO()
    pyplot.savefig(buffer_, format='png')
    buffer_.seek(0)
    img2 = PIL.Image.open(buffer_)
    img_arr2 = numpy.asarray(img2)
    buffer_.close()

    fig3 = pyplot.figure(dpi=300)
    pyplot.axes().set_aspect('equal', 'datalim')
    pyplot.set_cmap(pyplot.gray())
    pyplot.pcolormesh(x, z, numpy.fliplr(numpy.rot90((image_arr[:, image_2, :]), 3)))
    pyplot.axis('off')
    buffer_ = io.BytesIO()
    pyplot.savefig(buffer_, format='png')
    buffer_.seek(0)
    img3 = PIL.Image.open(buffer_)
    img_arr3 = numpy.asarray(img3)
    buffer_.close()

    pyplot.figure(figsize=(3, 1), dpi=300)
    pyplot.subplot(131)
    pyplot.imshow(img_arr1)
    pyplot.title('AxialSlice', fontsize=4, y=0.9)
    pyplot.axis('off')
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(132)
    pyplot.imshow(img_arr2)
    pyplot.title('CoronalSlice', fontsize=4, y=0.9)
    pyplot.axis('off')
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(133)
    pyplot.imshow(img_arr3)
    pyplot.title('SagitalSlice', fontsize=4, y=0.9)
    pyplot.axis('off')
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.tight_layout(pad=0.5, w_pad=2)
    pyplot.subplots_adjust(wspace=0, hspace=0)
    pyplot.savefig(filepath + '/'+'image.jpg')
    pyplot.show()

    Array_vtk = numpy_support.numpy_to_vtk(image_arr.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
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
        ImageSlab.SetSlabThickness(ConstPixelSpacing[0] * ConstPixelDims[0])
        ImageSlab.SetBlendModeToMax()
        ImageSlab.SetSlabResolution(ConstPixelSpacing[0])
        ImageSlab.Update()
        image = ImageSlab.GetOutput()
        m = image.GetDimensions()
        vtk_data = image.GetPointData().GetScalars()
        arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1], m[0])
        arr = (arr - numpy.min(arr)) / ((numpy.max(arr) - numpy.min(arr)) / 255)
        width = ConstPixelDims[1]
        height = int(ConstPixelDims[2] * (ConstPixelSpacing[2] / ConstPixelSpacing[1]))
        dim = (width, height)
        resized = cv2.resize(numpy.rot90(arr, 1), dim, interpolation=cv2.INTER_AREA)
        # cv2.imwrite( path + name +'.jpg', resized)
        return resized

    def mip_y():
        ImageSlab = vtk.vtkImageSlabReslice()
        ImageSlab.SetInputData(imagedata)
        ImageSlab.SetResliceAxesOrigin(center)
        ImageSlab.SetResliceAxesDirectionCosines(DirectionCosines_y)
        ImageSlab.SetSlabThickness(ConstPixelSpacing[1] * ConstPixelDims[1])
        ImageSlab.SetBlendModeToMax()
        ImageSlab.SetSlabResolution(ConstPixelSpacing[1])
        ImageSlab.Update()
        image = ImageSlab.GetOutput()
        m = image.GetDimensions()
        vtk_data = image.GetPointData().GetScalars()
        arr = numpy_support.vtk_to_numpy(vtk_data).reshape(m[1], m[0])
        arr = (arr - numpy.min(arr)) / ((numpy.max(arr) - numpy.min(arr)) / 255)
        width = int(ConstPixelDims[2] * (ConstPixelSpacing[2] / ConstPixelSpacing[0]))
        height = ConstPixelDims[0]
        dim = (width, height)
        resized = cv2.resize(numpy.rot90(arr, -1), dim, interpolation=cv2.INTER_AREA)
        # cv2.imwrite( path + name +'.jpg', resized)
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
        # cv2.imwrite( path + name +'.jpg', arr)
        return arr

    pyplot.figure(figsize=(3, 1), dpi=300)
    pyplot.subplot(131)
    pyplot.imshow(numpy.rot90(mip_z(), 2), cmap='gray')
    pyplot.title('AxialSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(132)
    pyplot.imshow(mip_x(), cmap='gray')
    pyplot.title('CoronalSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.subplot(133)
    pyplot.imshow(numpy.rot90(mip_y(), 1), cmap='gray')
    pyplot.title('SagitalSlice_MIP', fontsize=4, y=1.1)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.tight_layout(pad=1.3, w_pad=2)
    pyplot.subplots_adjust(wspace=0, hspace=0)
    pyplot.savefig(filepath + '/'+'MIP_image.jpg')
    pyplot.show()
    return None