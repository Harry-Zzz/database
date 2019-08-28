import vtk
# from vtk.util.misc import vtkGetDataRoot
#
#
# VTK_DATA_ROOT = vtkGetDataRoot()


reader = vtk.vtkDICOMImageReader()
reader.SetFileName("E:/Dicom/test/DicomResource")
d = reader.GetOutputPort()
b = reader.GetPixelSpacing()
c = reader.GetWidth()
print(b)
print(c)
print(d)



sobel = vtk.vtkImageSobel2D()
sobel.SetInputConnection(reader.GetOutputPort())
# sobel.ReleaseDataFlagOff()

# viewer = vtk.vtkImageViewer()
# viewer.SetInputConnection(sobel.GetOutputPort())
# viewer.SetColorWindow(400)
# viewer.SetColorLevel(0)
# viewer.Render()