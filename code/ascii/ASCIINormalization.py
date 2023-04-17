import os
import numpy as np

#统计本项目的最大行列
def ASCIISize(path):
    maxXAll = 0
    maxYAll = 0
    countMaxR_1000 = 0
    countMaxC_1000 = 0
    countMaxR_500 = 0
    countMaxC_500 = 0
    countMaxR_100_200 = 0
    countMaxC_200_300 = 0

    maxX=0
    maxY=0
    maxXClass =""
    maxYClass =""
    for dir in os.listdir(path):
        countX = len(open(path + '\\' + dir, 'rU').readlines())
        maxXAll += countX
        if maxX < countX:
            maxX = countX
            maxXClass = dir

        if countX >= 1000:
            countMaxR_1000 = countMaxR_1000 + 1
        if countX >= 500:
            countMaxR_500 = countMaxR_500 + 1
        if countX >= 100 and countX <= 200:
            countMaxR_100_200 = countMaxR_100_200 + 1

        with open(path+'\\'+dir,'r')as f:
            maxLocalCol = 0
            for i in f:
                countY = len(i.split(","))
                if countY>maxLocalCol:
                    maxLocalCol = countY
                if maxY < countY:
                    maxY = countY
                    maxYClass = dir
            if maxLocalCol >= 1000:
                countMaxC_1000 = countMaxC_1000 + 1
            if maxLocalCol >= 500:
                countMaxC_500 = countMaxC_500 + 1
            if maxLocalCol >= 200 and maxLocalCol <= 300:
                countMaxC_200_300 = countMaxC_200_300 + 1
            maxYAll = maxYAll + maxLocalCol

    # print(path,"最大行列：",'[',maxX,',',maxY,']')

    return maxX,maxY,maxXClass,maxYClass,maxXAll,maxYAll,countMaxR_1000,countMaxC_1000,countMaxR_500,countMaxC_500,countMaxR_100_200,countMaxC_200_300


#进行归一化处理
def ASCIINormalization(pathIn,pathOut,maxX,maxY):
    for dir in os.listdir(pathIn):
        # dir 是要处理的文件名
        ASCIIMatrix(pathIn+'//'+dir, pathOut, dir,maxX, maxY)


def ASCIIMatrix(pathIn,pathOut,dir,maxX,maxY):
    matrix = np.ones([maxX, maxY]) * -1
    # 保存到txt
    # 进行替换,读取源文件 进行字符替换
    with open(pathIn, 'r') as f:
        x = 0
        for i in f.readlines():
            list = i.split(',')
            for y in range(len(list)):
                matrix[x, y] = list[y]
            x += 1
    np.savetxt(pathOut+'\\'+dir, matrix, fmt='%d')


# #源矩阵路径
# pathIns = ['D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\\ant1.3\\ant1.3',
#           'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\code\Source',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ant1.5\Source',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\maven\Source',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\jmeter\Source',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ivy\Source']
# #归一化矩阵路径
# pathOuts = [r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\\ant1.3\\ant1.3Normalize',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\code\Normalize',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ant1.5\Normalize',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\maven\Normalize',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\jmeter\Normalize',
#             r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeASCII\ivy\Normalize']
#
# classNums = [470,147,1398,1283,1388,654]


# maxX,maxY,maxXClass,maxYClass,maxXAll,maxYAll,countMaxR_1000,countMaxC_1000,countMaxR_500,countMaxC_500,countMaxR_100_200,countMaxC_200_300 = ASCIISize(pathIns[5])
# print( "最大行列：", '[', maxX, ',', maxY, ']')
# print( "[最大行文件：", maxXClass, ',','最大列文件', maxYClass, ']')
# print( "[总共行数：", maxXAll, ',','总共列数', maxYAll, ']')
# print( "[平均行数：", maxXAll/classNums[5], ',','平均列数', maxYAll/classNums[5], ']')
# print( "[大于1000的行的类个数：", countMaxR_1000, ',','大于1000的列的类个数', countMaxC_1000, ']')
# print( "[大于500的行的类个数：", countMaxR_500, ',','大于500的列的类个数', countMaxC_500, ']')
# print( "[100~200的行的类个数：", countMaxR_100_200, ',','200~300的列的类个数', countMaxC_200_300, ']')
#
# #运行核心
# ASCIINormalization(pathIns[5],pathOuts[5],maxX,maxY)

