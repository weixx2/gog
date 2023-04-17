#只保留最后一位名称的链接关系
import re
def get_F2F_name(in_path,out_path):
    with open(in_path,"r") as f:
        with open(out_path,"w") as f2:
            for i in f.readlines():
                i=i.strip("\n")
                i=i.split("\t")
                if "(" in i[0] or "{" in i[0]:
                    a = re.findall("^.*[({]", i[0])[0].strip("(").strip("{")
                else:a=i[0]
                if "(" in i[1] or "{" in i[1]:
                    b = re.findall("^.*[({]", i[1])[0].strip("(").strip("{")
                else:
                    b = i[1]
                f2.write(a)
                f2.write("\t")
                f2.write(b)
                f2.write("\n")

def get_F2F_name_simple(in_path,out_path):
    with open(in_path,"r") as f:
        with open(out_path,"w") as f2:
            for i in f.readlines():
               list3 = []
               i=i.strip("\n")
               list1=i.split("	")
               for j in list1:
                   list2 = j.split(".")
                   list3.append(list2[-2])
                   list3.append(list2[-1])
               f2.write(list3[0])
               f2.write(".")
               f2.write(list3[1])
               f2.write("	")
               f2.write(list3[2])
               f2.write(".")
               f2.write(list3[3])
               f2.write("\n")
            f2.write("end")
 
if __name__ == '__main__':

    """
    获得了方法的简单结构文件F2F_name_simple
    可以判断这个方法属于哪一个类了
    下一步构建类的内部图字典----------跳转文件 generate_Graph.py
    动态变量：
    path_1：原始F2F结构
    path_2：去掉括号的F2F结构
    path_3：只保留前一个类名的F2F结构
    """

    # path_1 = r"C:\Users\gogforse\Desktop\测试文件夹\result\1.3.F2F.txt"
    # # 一个输入两个输出
    # path_2=r"C:\Users\gogforse\Desktop\测试文件夹\result\F2F_name.txt"
    # path_3=r"C:\Users\gogforse\Desktop\测试文件夹\result\F2F_name_simple.txt"
    # get_F2F_name(path_1,path_2)
    # get_F2F_name_simple(path_2,path_3)
