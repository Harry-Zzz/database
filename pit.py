from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from tag import Image_Para,Patient_Info,Get_image,One_image,Gdcm_image
import SimpleITK as sitk
import os
import pydicom
import shortuuid
from natsort import natsorted


# 1. 准备连接数据库基本信息
# 计算机ip地址
HOSTNAME = '127.0.0.1'
# 端口号
PORT = '3306'
# 连接数据库的名字
DATABASE = 'image_data'
# 数据库的账号和密码
USERNAME = 'root'
PASSWORD = 'zhy210320'
# 创建数据库引擎
DB_URI = 'mysql+mysqlconnector://{username}:{pwd}@{host}:{port}/{db}?charset=utf8'\
    .format(username =USERNAME,pwd = PASSWORD,host = HOSTNAME,port=PORT,db = DATABASE)
engine = create_engine(DB_URI,encoding='utf-8',echo=False)

# 基于ORM的反射
Base = automap_base()
Base.prepare(engine, reflect=True)
tables = Base.classes
#  print(Base.classes.keys())   # 数据库包含的列表

# 获取对应表格映射
baseinfo = Base.classes.base
patient = Base.classes.patient
image_para = Base.classes.image_para

# 获取实例
Session = sessionmaker(bind=engine)
session = Session()


PathDicom = 'G:/test/Osirix_Data/AGECANONIX/AGECANONIX/Specials 1CoronaryCTA_with_spiral _CTA_pre/CorCTA w-c  1.0  B20f - 6'
# 作图
lstFilesDCM = []
DcmName = []
for dirName, subdirList, fileList in sorted(os.walk(PathDicom)):
    fileList = natsorted(fileList)
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
            DcmName.append(filename)
# RefDs = pydicom.read_file(lstFilesDCM[0])
# # reader = sitk.ImageSeriesReader()
# # dicom_names = reader.GetGDCMSeriesFileNames(PathDicom)
# # reader.SetFileNames(dicom_names)
# # image = reader.Execute()
# # columns = RefDs.Columns
# # row = RefDs.Rows
# # ConstOrigin = image.GetOrigin()
# # ConstPixelSpacing = image.GetSpacing()
# # ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
ds = pydicom.read_file(lstFilesDCM[0],force=True)
gap = len(DcmName) - 1
file_one = pydicom.read_file(lstFilesDCM[0], force=True)
z_one = file_one.ImagePositionPatient[2]
file_tow = pydicom.read_file(lstFilesDCM[gap], force=True)
z_tow = file_tow.ImagePositionPatient[2]
columns = file_one.Columns
row = file_one.Rows
ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))
if z_one > z_tow:
    slice_gap = (z_one - z_tow) / gap
    ConstOrigin = (file_tow.ImagePositionPatient[0], file_tow.ImagePositionPatient[1], file_tow.ImagePositionPatient[2])
    ConstPixelSpacing = (float(file_tow.PixelSpacing[0]), float(file_tow.PixelSpacing[1]), float(slice_gap))
else:
    slice_gap = (z_tow - z_one) / gap
    ConstOrigin = (file_one.ImagePositionPatient[0], file_one.ImagePositionPatient[1], file_one.ImagePositionPatient[2])
    ConstPixelSpacing = (float(file_one.PixelSpacing[0]), float(file_one.PixelSpacing[1]), float(slice_gap))

# Get_image(PathDicom)  # 多张dicom
# One_image(PathDicom)    # 一张dicom
Gdcm_image(PathDicom)  #压缩dicom

# 添加信息：副表
para = Image_Para(PathDicom)
patient_info = Patient_Info(PathDicom)
i_id = shortuuid.uuid()
p_id = shortuuid.uuid()
session.add(image_para(id=i_id,dimsize=str(para['DimSize']),origin=str(para['Orign']),spacing=str(para['Spacing']),intercept=para['Intercept'],slope=para['Slope'],window_width=str(para['WindowWidth']),window_center=str(para['WindowCenter']),thumbnail=para['Thumbnail'],thumbnail_MIP=para['Thumbnail_MIP'],institution_name=para['InstitutionName'],manufacturer=para['Manufacturer'],series_des=para['Series_Des'],study_des=para['Study_Des']))
# session.add(image_para(id=i_id,dimsize=str(para['DimSize']),origin=str(para['Orign']),spacing=str(para['Spacing']),intercept=para['Intercept'],slope=para['Slope'],window_width=str(para['WindowWidth']),window_center=str(para['WindowCenter']),thumbnail=para['Thumbnail'],description=para['Description'],institution_name=para['InstitutionName'],manufacturer=para['Manufacturer'],series_des=para['Series_Des'],study_des=para['Study_Des']))
session.commit()
session.add(patient(id=p_id,patient_id=patient_info['ID'],patient_age=patient_info['Age'],patient_bd=patient_info['BirthDate'],patient_sex=patient_info['Sex'],patient_size=patient_info['Size'],patient_weight=patient_info['Weight'],study_date=patient_info['study_date'],study_time=patient_info['study_time']))
session.commit()


# 主表信息
i = 0
for i in range(len(lstFilesDCM)):
    info = {}
    info['id'] = shortuuid.uuid()
    info['filename'] = DcmName[i]
    info['modality'] = ds.Modality
    try:
        info['bodypart'] = ds.BodyPartExamined
    except AttributeError:
        info['bodypart'] = 'none'
    info['address'] = './'+'DataFile'+'/'+ dirName.split('/',2)[2] + '/' + DcmName[i]
    info['type'] = 'dcm'
    session.add(baseinfo(id=info['id'],file_name=info['filename'],modality=info['modality'],body_part=info['bodypart'],file_address=info['address'],data_type=info['type'],patient_id=p_id,image_id=i_id))
    session.commit()
    i = i+1
session.close()