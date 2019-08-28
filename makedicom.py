import pydicom
import os

PathDicom = "G:/test/NeuroSeg_Imgs"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []
DCMname = []


for dirName, subdirList, fileList in sorted(os.walk(PathDicom)):
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
            # DCMname.append(filename)

# print(dirName)
# print(subdirList)
# print(fileList)
# print(filename)
# print(lstFilesDCM)
# print(DCMname)
# print(len(DCMname))
# print(len(lstFilesDCM))

i = 0
for i in range(len(lstFilesDCM)):
    ds = pydicom.dcmread(lstFilesDCM[i])
    ds.PatientName = '0000'
    ds.save_as(lstFilesDCM[i])
    i = i+1



# filename = r"E:\Dicom\test\DicomResource\1.3.12.2.1107.5.1.4.58073.30000010042701180060900001838.dcm"
# ds = pydicom.dcmread(filename)  # 读取dicom文件
# ds.PatientName = '0000'
# ds.save_as('E:/Dicom/test/DicomResource/1.3.12.2.1107.5.1.4.58073.30000010042701180060900001838.dcm') # 将修改后文件保存
# print(ds.PatientName)