import numpy as np
import os

def find_java(path,savePath):
    for i in os.listdir(path):
        path_split = i.split('.')
        second_dir = os.path.join(path, i)
        # 这里的nii可以换成你想要遍历寻找的文件格式
        if os.path.isdir(second_dir):
            # 证明是文件夹
            find_java(second_dir,savePath)
        elif path_split[-1] == 'java' and os.path.isfile(second_dir) :
            javaFileName = '.'.join(path_split) + '.ASCIImatrix'
            #转变为ascii数组，f1为写入文件的位置，f2为读取的源代码文件
            with open(savePath+javaFileName+'.txt',"a", encoding='UTF-8')as f1:
                with open(second_dir,'r', encoding='UTF-8')as f2:
                    for i in f2.readlines():
                        ascii = np.fromstring(i, dtype=np.uint8)
                        f1.write(",".join('%s' %id for id in ascii.tolist()))
                        f1.write("\n")
    # 找到对应格式的文件，开始进行自己的处理  也可以将其保存到自己定义的文件夹内]


# path = [r"D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\\jakarta-ant-1.3",
#         r"D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\commons-codec-master",
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\jakarta-ant-1.5',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-maven-3.6.3',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-jmeter-5.4.1',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-ivy-2.5.0']
#
# savePath = [r"D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\\ant1.3\\",
#             r"D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\code\Source\\",
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ant1.5\Source\\',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\maven\Source\\',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\jmeter\Source\\',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ivy\Source\\']
#
# find_java(path[5],savePath[5])