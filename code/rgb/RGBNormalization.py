import os
import numpy as np

#统计本项目的最大行列
def RGBSize(path):
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
        maxXAll+=countX
        if maxX < countX:
            maxX = countX
            maxXClass = dir
        if countX >= 1000:
            countMaxR_1000=countMaxR_1000+1
        if countX >= 500:
            countMaxR_500=countMaxR_500+1
        if countX >= 100 and countX <= 200:
            countMaxR_100_200=countMaxR_100_200+1
        with open(path+'\\'+dir,'r',encoding='utf-8')as f:
            # 局部最大行
            maxLocalCol = 0
            for i in f:
                countY = len(i.split(" "))
                if countY>maxLocalCol:
                    maxLocalCol = countY
                if maxY < countY:
                    maxY = countY
                    maxYClass = dir
            #本类的最大值

            if maxLocalCol >= 1000:
                countMaxC_1000 = countMaxC_1000 + 1
            if maxLocalCol >= 500:
                countMaxC_500 = countMaxC_500 + 1
            if maxLocalCol >= 200 and maxLocalCol <= 300:
                countMaxC_200_300 = countMaxC_200_300 + 1
            maxYAll = maxYAll + maxLocalCol
    # with open(path+"\\RGBMax.txt",'w',encoding='utf-8')as f:
    #     f.write("["+str(maxX)+","+str(maxY)+"]")
    return maxX,maxY,maxXClass,maxYClass,maxXAll,maxYAll,countMaxR_1000,countMaxC_1000,countMaxR_500,countMaxC_500,countMaxR_100_200,countMaxC_200_300

#进行归一化处理
def RGBNormalization(pathIn,pathOut,maxX,maxY):
    for dir in os.listdir(pathIn):
        # dir 是要处理的文件名
        RGBMatrix(pathIn+'\\'+dir, pathOut, dir,maxX, maxY)

def RGBMatrix(pathIn,pathOut,dir,maxX,maxY):
    #使用反向填充
    matrix = np.ones([maxX, maxY]) * 255
    # 保存到txt
    # 进行替换,读取源文件 进行字符替换
    with open(pathIn, 'r',encoding='utf-8') as f:
        x = 0
        for i in f.readlines():
            list = i.strip("\n").split(' ')
            for y in range(len(list)):
                a = list[y]
                if(a!=''):
                    matrix[x][y] = int(a)
            x += 1
    np.savetxt(pathOut+'\\'+dir, matrix, fmt='%d')





