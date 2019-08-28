import vtk

filename = "E:/Dicom/test/DicomResource/1.3.12.2.1107.5.1.4.58073.30000010042701180060900001839.dcm"
reader = vtk.vtkDICOMImageReader()
reader.SetFileName(filename)
reader.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
#renderer.GetActiveCamera().SetPosition() #设置视点位置
#renderer.GetActiveCamera().SetViewUp(0, 1, 0)  #设置视点方向
renderer.SetBackground(0.1, 0.2, 0.4)  #设置背景颜色

renWin = vtk.vtkRenderWindow()
renWin.SetSize(640, 480)     #设置窗口大小
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()

renWin.Render()
iren.Start()