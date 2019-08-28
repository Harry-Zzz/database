import uuid
import shortuuid
# https://github.com/skorokithakis/shortuuid

'''
print(uuid.uuid1())
print(int(uuid.uuid1().hex,16)) # 一种uuid的转化方法
print(shortuuid.uuid()) # 默认22位长度
print(type(shortuuid.uuid()))
print(shortuuid.uuid()[:15]) # 自定义长度，不保证唯一
'''
i = 0
for i in range(10):
    print(shortuuid.uuid())
    i=i+1