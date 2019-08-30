import  sqlalchemy
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime #区分大小写
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime


# 1. 准备连接数据库基本信息
# 计算机ip地址
HOSTNAME = '127.0.0.1'
# 端口号
PORT = '3306'
# 连接数据库的名字
DATABASE = 'book_manager'
# 数据库的账号和密码
USERNAME = 'root'
PASSWORD = 'zhy210320'
# 创建数据库引擎
DB_URI = 'mysql+mysqlconnector://{username}:{pwd}@{host}:{port}/{db}?charset=utf8'\
    .format(username =USERNAME,pwd = PASSWORD,host = HOSTNAME,port=PORT,db = DATABASE)
engine = create_engine(DB_URI,encoding='utf-8',echo=False)


# 2. 生成orm基类
Base = declarative_base()
# 创建orm表格
class BaseInfo(Base):
    __tablename__ = 'baseinfo'
    id = Column(String(22),primary_key=True,nullable=False,)
    file_name = Column(String(50),nullable=False)
    modality = Column(String(20))
    body_part = Column(String(20))
    file_address = Column(String(255))
    data_type = Column(String(20))
    create_time = Column(DateTime,default=datetime.now)
    update_time = Column(DateTime,onupdate=datetime.now,default=datetime.now)
    patient_id = Column(Integer,ForeignKey('patient.id'))
    patient = relationship('Patient', back_populates='BaseInform')
    image_id = Column(Integer,ForeignKey('image_para.id'))
    image_para = relationship('Image_Parameter',back_populates='BaseInform')


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer,primary_key=True)
    patient_id = Column(Integer)
    patient_age = Column(Integer)
    patient_bd = Column(Integer)
    patient_sex = Column(Integer)
    patient_size = Column(Integer)
    patient_weight = Column(Integer)
    base_info = relationship('BaseInfo',back_populates='patient')


class Image_Parameter(Base):
    __tablename__ = 'image_para'
    id = Column(Integer,primary_key=True)
    study_id = Column(Integer)
    study_date = Column(String(20))
    study_time = Column(String(20))
    dimsize = Column(Integer)
    origin = Column(Integer)
    spacing = Column(Integer)
    offset = Column(Integer)
    window_width = Column(Integer)
    window_center = Column(Integer)
    institution_name = Column(String(50))
    manufacturer = Column(String(50))
    image_address = Column(String(50))
    base_info = relationship('BaseInfo', back_populates='image_para')


Base.metadata.create_all(engine)  # 创建表结构















'''
#创建连接
engine=create_engine("mysql+pymysql://root:zhy210320@localhost/测试库",encoding='utf-8',echo=True)


# 生成orm基类
base = declarative_base()


class user(base):
    __tablename__ = 'users'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

    def __repr__(self):
        return "<user(id='%d',name='%s',  password='%s')>" % (self.id,
                                                              self.name, self.password)


class Address(base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("user", backref="addresses")


    def __repr__(self):
        return "<Address(email_address='%s',id='%d',user_id='%d')>" % (self.email_address, self.id, self.user_id)


base.metadata.create_all(engine)  # 创建表结构
'''

'''
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话，class,不是实例
Session = Session_class()  # 生成session实例
obj = Session.query(user).first()

addr_obj = Session.query(Address).first()
print(addr_obj.user)  # 在addresses表中通过user来查询users表中的数据。
print(addr_obj.user.name)

Session.commit()  # 提交，使前面修改的数据生效。

'''

'''
#生成orm基类
#关联一个表
base=declarative_base()
class user(base):
    __tablename__ = 'users' #表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))
base.metadata.create_all(engine) #创建表结构
'''

'''
#单表数据存储
#生成orm基类
base=declarative_base()
class user(base):
    __tablename__ = 'users' #表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))
base.metadata.create_all(engine) #创建表结构
Session_class=sessionmaker(bind=engine) ##创建与数据库的会话，class,不是实例
Session=Session_class()   #生成session实例
user_obj = user(name="rr",password="123456") #插入你要创建的数据对象，每执行一次都会新增一次数据。
Session.add(user_obj)  #把要创建的数据对象添加到这个session里
Session.commit() #提交，使前面修改的数据生效。
Session.close()
'''