import SimpleITK as sitk
import numpy as np


reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames('E:/Dicom/test/DicomResource')
reader.SetFileNames(dicom_names)
image = reader.Execute()
image_array = sitk.GetArrayFromImage(image)
origin = image.GetOrigin()
spacing = image.GetSpacing()
columns = image.GetColumns()
cow = image.GetRows()

print(np.shape(image_array))
print(origin)
print(spacing)
print(dim)