from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:zhy210320@localhost/测试库",encoding='utf-8',echo=False)



# 基于ORM的反射
Base = automap_base()
Base.prepare(engine, reflect=True)
tables = Base.classes
users = Base.classes.users
address = Base.classes.addresses

print('`'*50)
print(type(tables))
print('`'*50)
print(Base.classes.keys())
print('`'*50)

Session = sessionmaker(bind=engine)
session = Session()
session.add(address(email_address='233@qq.com',user_id='123',name='张三'))
session.commit()


'''
# 反射数据库列表
metadata = MetaData(engine)
metadata.reflect(bind=engine)
print(metadata.tables.keys())
# 举例
dicom = metadata.tables['dicom']
users = metadata.tables['users']
address = metadata.tables['addresses']
test = metadata.tables['test']
# 实例化
Session = sessionmaker(bind=engine)
session = Session()
session.add(test(id='1',name='张三')) # 报错
session.commit()

'''