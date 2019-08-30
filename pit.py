from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from tag import Image_Para,Patient_Info
import SimpleITK as sitk
import os
import pydicom
import numpy
from matplotlib import pyplot
from PIL import Image
import PIL
from vtkmodules.util import numpy_support
import cv2
import io
import shortuuid


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
baseinfo = Base.classes.baseinfo
patient = Base.classes.patient
image_para = Base.classes.image_para

# 获取实例
Session = sessionmaker(bind=engine)
session = Session()

# 添加信息
PathDicom = 'E:/Dicom/test/DicomResource'

para = Image_Para(PathDicom)
patient_info = Patient_Info(PathDicom)
i_id = shortuuid.uuid()
p_id = shortuuid.uuid()
session.add(image_para(id=i_id,dimsize=str(para['DimSize']),origin=str(para['Orign']),spacing=str(para['Spacing']),intercept=para['Intercept'],slope=para['Slope'],window_width=str(para['WindowWidth']),window_center=str(para['WindowCenter']),thumbnail=para['Thumbnail'],thumbnail_MIP=para['Thumbnail_MIP'],description=para['Description'],institution_name=para['InstitutionName'],manufacturer=para['Manufacturer']))
session.commit()
session.add(patient(id=p_id,patient_id=patient_info['ID'],patient_age=patient_info['Age'],patient_bd=patient_info['BirthDate'],patient_sex=patient_info['Sex'],patient_size=patient_info['Size'],patient_weight=patient_info['Weight'],study_date=patient_info['study_date'],study_time=patient_info['study_time']))
session.commit()


# 主表信息
lstFilesDCM = []
DcmName = []
for dirName, subdirList, fileList in sorted(os.walk(PathDicom)):
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            # print(filename)
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
            DcmName.append(filename)
RefDs = pydicom.read_file(lstFilesDCM[0])
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(PathDicom)
reader.SetFileNames(dicom_names)
image = reader.Execute()
columns = RefDs.Columns
row = RefDs.Rows
ConstOrigin = image.GetOrigin()
ConstPixelSpacing = image.GetSpacing()
ConstPixelDims = (int(row), int(columns), len(lstFilesDCM))

i = 0
for i in range(len(lstFilesDCM)):
    info = {}
    info['id'] = shortuuid.uuid()
    info['filename'] = DcmName[i]
    info['modality'] = RefDs.Modality
    info['bodypart'] = RefDs.BodyPartExamined
    info['address'] = dirName + '/' + DcmName[i]
    info['type'] = 'dcm'
    session.add(baseinfo(id=info['id'],file_name=info['filename'],modality=info['modality'],body_part=info['bodypart'],file_address=info['address'],data_type=info['type'],patient_id=p_id,image_id=i_id))
    session.commit()
    i = i+1

session.close()