import pydicom
import SimpleITK as sitk
import os

# filename = './DicomResource/1.3.12.2.1107.5.1.4.58073.30000010042701180060900001838.dcm'


def Patient_Info(filepath):
    information = {}
    lstFilesDCM = []
    for dirName, subdirList, fileList in os.walk(filepath):
        for filename in fileList:
            if ".dcm" in filename.lower():
                lstFilesDCM.append(os.path.join(dirName, filename))

    ds = pydicom.read_file(lstFilesDCM[0],force=True)
    information['ID'] = ds.PatientID
    information['Age'] = ds.PatientAge
    information['BirthDate'] = ds.PatientBirthDate
    information['Sex'] = ds.PatientSex
    information['Size'] = ds.PatientSize
    information['Weight'] = ds.PatientWeight
    information['study_date'] = ds.StudyDate
    information['study_time'] = ds.StudyTime
    return information



# print(type(Patient_Info(filename)))



def Image_Para(filepath):
    information = {}
    lstFilesDCM = []

    for dirName, subdirList, fileList in os.walk(filepath):
        for filename in fileList:
            if ".dcm" in filename.lower():
                lstFilesDCM.append(os.path.join(dirName, filename))

    ds = pydicom.read_file(lstFilesDCM[0],force=True)
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filepath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    columns = ds.Columns
    row = ds.Rows
    ConstOrigin = image.GetOrigin()
    ConstPixelSpacing = image.GetSpacing()
    ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
    information['DimSize'] = ConstPixelDims
    information['Orign'] = ConstOrigin
    information['Spacing'] = ConstPixelSpacing
    information['Intercept'] = ds.RescaleIntercept
    information['Slope'] = ds.RescaleSlope
    information['WindowCenter'] = ds.WindowCenter
    information['WindowWidth'] = ds.WindowWidth
    information['Thumbnail'] = str(filepath + '/' + 'image.jpg')
    information['Thumbnail_MIP'] = str(filepath + '/' + 'MIP_image.jpg')
    information['Description'] = ds.StudyDescription
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    return information

# PathDicom = 'E:/Dicom/test/DicomResource'
# print(Patient_Info(PathDicom))
# print(Image_Para(PathDicom))



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
#
#
# print(loadFileInformation(filename))

