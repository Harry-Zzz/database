import pydicom
from matplotlib import pylab


filename = 'G:/test/Balerus_TB/351/X-RAY/20111004/1_1.dcm'
ds = pydicom.dcmread(filename,force=True)
# ds.dir()  # 查看病人所有信息字典keys
# print(ds.PatientName)  # 查看病人名字
# print(ds) # 查看病人所有信息字典， 如果出现某key对应值编码错误，先暂时跳过该key
# print(len(ds))
ds.PatientName = '0000'
ds.save_as(filename)

# 查看dicom对应图片值
# print('*******************')
# print(ds.pixel_array.shape)
# print(ds.pixel_array)
# 读取显示图片
# pylab.imshow(ds.pixel_array, cmap=pylab.cm.gray)
# pylab.axis('off')
# pylab.show()


'''
    hot 从黑平滑过度到红、橙色和黄色的背景色，然后到白色。
    cool 包含青绿色和品红色的阴影色。从青绿色平滑变化到品红色。
    gray 返回线性灰度色图。
    bone 具有较高的蓝色成分的灰度色图。该色图用于对灰度图添加电子的视图。
    white 全白的单色色图。 
    spring 包含品红和黄的阴影颜色。 
    summer 包含绿和黄的阴影颜色。
    autumn 从红色平滑变化到橙色，然后到黄色。 
    winter 包含蓝和绿的阴影色。
'''

##修改图片中的元素，不能直接使用data_array,需要转换成PixelData
# for n,val in enumerate(ds.pixel_array.flat): # example: zero anything < 300
#     if val < 300:
#         ds.pixel_array.flat[n]=0
# ds.PixelData = ds.pixel_array.tostring()
# ds.save_as('newfilename.dcm')