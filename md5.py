import hashlib

a1 = 'W20181'
b1 = 'HZTW20181'

def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + hl.hexdigest())
    return hl.hexdigest()


def md5Value(a,b):

    return genearteMD5(a+genearteMD5(b)+'BJJX@&(@LONGGANG$^#*@&#')
