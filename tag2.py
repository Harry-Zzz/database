import pydicom
import matplotlib.pyplot as plt
import os
import numpy as np
import dicom

#
# ds = pydicom.dcmread('./DicomResource/1.3.12.2.1107.5.1.4.58073.30000010042701180060900001857.dcm')
# plt.figure(figsize=(10, 10))
# plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
# plt.show()


INPUT_FOLDER = './DicomResource/'
patients = os.listdir(INPUT_FOLDER)
patients.sort()

def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices

print(load_scan(INPUT_FOLDER))