# coding=gbk
import cv2
import os
import pydicom
import numpy
import SimpleITK


PathDicom = "E:/Dicom/test/DicomResource"  # ��python�ļ�ͬһ��Ŀ¼�µ��ļ���,�洢dicom�ļ�
SaveRawDicom = "./SaveRaw/"  # ��python�ļ�ͬһ��Ŀ¼�µ��ļ���,�����洢mhd�ļ���raw�ļ�
lstFilesDCM = []

# ��PathDicom�ļ����µ�dicom�ļ���ַ��ȡ��lstFilesDCM��
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # �ж��ļ��Ƿ�Ϊdicom�ļ�
            # print(filename)
            lstFilesDCM.append(os.path.join(dirName, filename))  # ���뵽�б���

# ��һ��������һ��ͼƬ��Ϊ�ο�ͼƬ������Ϊ����ͼƬ������ͬά��
RefDs = pydicom.read_file(lstFilesDCM[0])  # ��ȡ��һ��dicomͼƬ
print(lstFilesDCM[0])

# �ڶ������õ�dicomͼƬ�����3DͼƬ��ά��
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))  # ConstPixelDims��һ��Ԫ��
print(ConstPixelDims)
# ���������õ�x�����y�����Spacing���õ�z����Ĳ��
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
print(ConstPixelSpacing)
# ���Ĳ����õ�ͼ���ԭ��
Origin = RefDs.ImagePositionPatient
print(Origin)
# ����ά�ȴ���һ��numpy����ά���飬����Ԫ��������Ϊ��pixel_array.dtype
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)  # array is a numpy array

# ���岽:�������е�dicom�ļ�����ȡͼ�����ݣ������numpy������
i = 0
for filenameDCM in lstFilesDCM:
    ds = pydicom.read_file(filenameDCM)
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
    # cv2.imwrite("out_" + str(i) + ".jpg", ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)])
    i += 1


def loadFileInformation(filename):
    information = {}
    ds = pydicom.read_file(filename)
    information['PatientID'] = ds.PatientID
    information['PatientName'] = ds.PatientName
    information['PatientBirthDate'] = ds.PatientBirthDate
    information['PatientSex'] = ds.PatientSex
    information['PatientSize'] = ds.PatientSize
    information['PatientWeight'] = ds.PatientWeight
    information['StudyID'] = ds.StudyID
    information['StudyDate'] = ds.StudyDate
    information['StudyTime'] = ds.StudyTime
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    # print(dir(ds))
    # print(type(information))
    return information


print(loadFileInformation(lstFilesDCM[0]))


# ����������numpy�������ת�ã����������ᣨx,y,z���任Ϊ��z,y,x��,������dicom�洢�ļ��ĸ�ʽ������һ��ά��Ϊz�����ͼƬ�ѵ�
ArrayDicom = numpy.transpose(ArrayDicom, (2, 0, 1))

# ���߲��������ڵ�numpy����ͨ��SimpleITKת��Ϊmhd��raw�ļ�
sitk_img = SimpleITK.GetImageFromArray(ArrayDicom, isVector=False)
sitk_img.SetSpacing(ConstPixelSpacing)
sitk_img.SetOrigin(Origin)
SimpleITK.WriteImage(sitk_img, os.path.join(SaveRawDicom, "sample" + ".mhd"))
