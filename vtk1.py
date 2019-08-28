import SimpleITK as sitk


pathdicom = 'E:/Dicom/test/DicomResource'


def loadFile(filename):
    ds = sitk.ReadImage(filename)

    img_array = sitk.GetArrayFromImage(ds)

    frame_num, width, height = img_array.shape

    return img_array, frame_num, width, height

a, b, c, d = loadFile(pathdicom)
print(a,b,c,d)
