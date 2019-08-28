import pydicom


filename = './DicomResource/1.3.12.2.1107.5.1.4.58073.30000010042701180060900001838.dcm'
ds = pydicom.read_file(filename,force=True)
# file.close()
#
print(ds.dir())
# print(len(ds.dir()))
#
# for dss in ds.dir():
#     print(dss)

def loadFileInformation(filename):
    information = {}
    ds = pydicom.read_file(filename,force=True)
    information['PatientID'] = ds.PatientID
    information['SliceThickness'] = ds.SliceThickness
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


print(loadFileInformation(filename))




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
# # print("1")
