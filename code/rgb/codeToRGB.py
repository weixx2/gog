import numpy as np
import os

#java关键字
JavaKeyWords = ["abstract","assert","boolean","break","byte","case","catch","char","class",
                "continue","default","do","double","else","enum","extends","final","finally",
                "float","for","if","implements","import","int","interface","instanceof","long",
                "native","new","package","private","protected","public","return","short","static",
                "strictfp","super","switch","synchronized","this","throw","throws","transient",
                "try","void","volatile","while","true","false","null","goto","const"]
#都是规范代码，运算符也是空格分开的
JavaOperators = ["+","-","*","/","%","~","!","++","--","==","!=",">",
                 "<",">=","<=","&","~","|","^","&&","||","=","+=","-=",
                 "*=","/=","&=","^=","|=","<<=",">>=","instanceof"]
#直接与代码相连的
JavaOperatorsConnect = ["(",")","{","}",";",":","\""]

def find_javaRGB(path,pathSave,dataName):
    for i in os.listdir(path):
        path_split = i.split('.')
        second_dir = os.path.join(path, i)
        # 这里的nii可以换成你想要遍历寻找的文件格式
        if os.path.isdir(second_dir):
            # 证明是文件夹
            find_javaRGB(second_dir,pathSave,dataName)
        elif path_split[-1] == 'java' and os.path.isfile(second_dir) :
            javaFileName = '.'.join(path_split) + '.RGBmatrix'
            #转变为RGB数组，f1为写入文件的位置，f2为读取的源代码文件
            with open(pathSave+'\\'+dataName+'PNG\\'+javaFileName+'.txt',"w", encoding='UTF-8')as f3:
                with open(pathSave+'\\'+dataName+'\\'+'Source\\'+javaFileName+'.txt',"w", encoding='UTF-8')as f1:
                    with open(second_dir,'r', encoding='UTF-8')as f2:
                        for i in f2:
                            rgb = codeToRgb(i)
                            if (rgb == ""):
                                f1.write("255 255 255 ")
                            else:
                                f1.write(rgb)
                            f1.write("\n")
                        # 写入PNG矩阵------------------------
                            rgb = codeToRgbPNG(i)
                            if (rgb == ""):
                                f3.write("255,255,255 ")
                            else:
                                f3.write(rgb)
                            f3.write("\n")
    # 找到对应格式的文件，开始进行自己的处理  也可以将其保存到自己定义的文件夹内]

#读取代码行，切分成rgb，输入是一行代码，输出是一行rgb数字
def codeToRgb(code):
    rgbResult = ""
    line = code.strip("\n").split(" ")
    for i in line:
        if(i in JavaKeyWords):
            rgbResult += "255 0 0 "*len(i)       #关键字 红色
        elif(i in JavaOperators):
            rgbResult += "251 255 0 " * len(i)   #运算符 黄色
        else:                                   #没有空格间隔 需逐字分析
            flag = False  # 表示没有引号
            for k in i:
                if(flag):
                    rgbResult += "0 255 0 "        #输出内容  绿色
                elif(k in JavaOperatorsConnect):  #连接运算符
                    rgbResult += "251 255 0 "      #运算符 黄色
                    if(k == "\""):                #输出语句  绿色
                        flag = ~flag
                else:                             #普通代码  蓝色
                    rgbResult += "0 255 255 "
    return  rgbResult

def codeToRgbPNG(code):
    rgbResult = ""
    line = code.strip("\n").split(" ")
    for i in line:
        if(i in JavaKeyWords):
            rgbResult += "255,0,0 "*len(i)       #关键字 红色
        elif(i in JavaOperators):
            rgbResult += "251,255,0 " * len(i)   #运算符 黄色
        else:                                   #没有空格间隔 需逐字分析
            flag = False  # 表示没有引号
            for k in i:
                if(flag):
                    rgbResult += "0,255,0 "        #输出内容  绿色
                elif(k in JavaOperatorsConnect):  #连接运算符
                    rgbResult += "251,255,0 "      #运算符 黄色
                    if(k == "\""):                #输出语句  绿色
                        flag = ~flag
                else:                             #普通代码  蓝色
                    rgbResult += "0,255,255 "
    return  rgbResult

# path = ["D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\\jakarta-ant-1.3",
#         "D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\commons-codec-master",
#         'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\jakarta-ant-1.5',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-maven-3.6.3',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-jmeter-5.4.1',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\apache-ivy-2.5.0',
#         r'D:\Papers\gogforse\抽象语法树代码\mycode\sourcedata\accumulo-2.0.0-alpha-2']
#
# pathSave = r"D:\Papers\gogforse\抽象语法树代码\mycode\preJavaCodeRGB"
#
# datas = ['ant1.3','code','ant1.5','maven','jmeter','ivy','acc']
#
# #处理code文件
# find_javaRGB(path[6],pathSave,datas[6])