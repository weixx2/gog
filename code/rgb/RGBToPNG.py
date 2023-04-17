from PIL import Image
import math
import os
#遍历RGB矩阵文件
def RGBNormalizationPNG(pathIn,pathOut):
    for dir in os.listdir(pathIn):
        # dir 是要处理的文件名
        rgbToPng(pathIn+'//'+dir, pathOut, dir)


#单文件转为PNG
def rgbToPng(rgbText,Png,dir):
    #先统计行数
    x=0
    y=0
    with open(rgbText,'r') as f:
        for i in f.readlines():
            x+=1
            max = 0
            for j in i.strip("\n").split(" "):
                max+=1
            y = y if y > max else max
    im = Image.new("RGB", (y+3, x+3))   #创建图片
    #白色填充
    for i in range(y+3):
        for j in range(x+3):
            im.putpixel((i, j), (255,255,255))

    x = 0;
    with open(rgbText,'r') as f:
        for i in f.readlines():
            rgb = i.strip("\n").split(" ")
            y = 0;
            for j in rgb:
                line = j.strip("\n").split(",")
                if('' not in line):
                    yanse= (int(line[0]), int(line[1]), int(line[2]))
                    im.putpixel((y+1, x+1), yanse)    #将rgb转化为像素
                y += 1
            x += 1
    #写入图片位置
    im.save(Png+"\\"+dir+".png")   #im.save('flag.jpg')保存为jpg图片


# PNGList = ['D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\\ant1.3PNG',
#            'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\code\PNG',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\ant1.5\PNG',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\maven\PNG',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\jmeter\PNG',
#            r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\ivy\PNG']
# PNGSaveList = ['D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\\ant1.3Photos',
#                'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\code\Photos',
#                r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\ant1.5\Photos',
#                r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\maven\Photos',
#                r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\jmeter\Photos',
#                r'D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB\ivy\Photos']
#
# # param1：RGB矩阵的所有文件
# # param2: 图片存储的位置
# RGBNormalizationPNG(PNGList[5],PNGSaveList[5])