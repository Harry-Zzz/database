import os
import pydicom
import numpy
from matplotlib import pyplot
from PIL import Image
import SimpleITK as sitk
from mayavi import mlab


# 用lstFilesDCM作为存放DICOM files的列表
PathDicom = "G:/Dalian_PETCT/2010-04__Studies/chen da gao_P00000016_CT_2010-04-27_095034_PET^3.PETCT.WholeBody.Brain.HD.(Adult)_CT.WB..3.0..B30f_n435__00000"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []

for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            # print(filename)
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中



# 将第一张图片作为参考图
RefDs = pydicom.read_file(lstFilesDCM[0])  # 读取第一张dicom图片

# 建立三维数组
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

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



# 得到spacing值 (mm为单位)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(spacing))

# 三维数据

x = numpy.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])  # 0到（第一个维数加一*像素间的间隔），步长为constpixelSpacing
y = numpy.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])  #
z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * spacing, spacing)  #
# z = numpy.arange(0.0, (ConstPixelDims[2] + 1) * 2, 2)  #

ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# 遍历所有的dicom文件，读取图像数据，存放在numpy数组中
for filenameDCM in lstFilesDCM:
    ds = pydicom.read_file(filenameDCM)
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array


# mlab.contour3d(ArrayDicom)
# mlab.show()

vol = mlab.pipeline.volume(mlab.pipeline.scalar_field(ArrayDicom), name='3-d ultrasound ')
mlab.show()
