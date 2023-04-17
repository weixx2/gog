def complex(Graph_list,dot,node):
    for j in Graph_list:
        list1 = j.split("\t")
        list2 = list1[0].split(".")
        list3 = list1[1].split(".")
        if list2[1] not in dot:
            dot.append(list2[1])  # 记录所有的边,a.index(76)获取下标
        else:
            pass
        if list3[1] not in dot:
            dot.append(list3[1])  # 记录所有的边,a.index(76)获取下标
        else:
            pass
    for j in Graph_list:
        list1 = j.split("\t")
        list2 = list1[0].split(".")
        list3 = list1[1].split(".")
        node_1 = dot.index(list2[1])
        node_2 = dot.index(list3[1])
        node.append((node_1, node_2))
    return dot,node

def get_name_Graph(in_path,out_path):
    count = 0
    Graph_name = None
    with open(in_path,"r") as f:
        with open(out_path,"a") as f2:
            i=f.readline()
            dot = []
            node = []
            Graph_list = []
            i = i.strip("\n")
            list1 = i.split("	")
            list2 = list1[0].split(".")
            list3 = list1[1].split(".")
            Graph_name = list2[0]
            while i!="end":
                i=i.strip("\n")
                list1=i.split("	")
                list2=list1[0].split(".")
                list3 = list1[1].split(".")
                if list2[0]==list3[0] and list2[0]==Graph_name:
                    Graph_list.append(i)
                    i = f.readline()
                    if i=="end":#考虑到最后一个的情况
                        dot,node=complex(Graph_list,dot,node)
                        dict = {}
                        dict[Graph_name] = (dot, node)
                        if dict[Graph_name] != ([], []):
                            f2.write(str(dict)+"\n")
                            count+=1
                elif list2[0]!=list3[0] and list2[0]==Graph_name:
                    i = f.readline()
                else:#同一图的读取完毕，Graph_list放着对应链接关系
                    if Graph_list:
                        dot,node=complex(Graph_list,dot,node)
                    else:
                        i=f.readline()

                    dict = {}
                    dict[Graph_name] = (dot, node)
                    if  dict[Graph_name]!=([],  []):
                        f2.write(str(dict) + "\n")
                        count += 1
                    #变更图名
                    dot = []
                    node = []
                    Graph_list = []
                    i = i.strip("\n")
                    list1 = i.split("\t")
                    list2 = list1[0].split(".")
                    list3 = list1[1].split(".")
                    Graph_name = list2[0]


if __name__ == '__main__':
    """
    通过 F2F_name_simple 文件
    这里获得了类的内部图结构 F2F_name_Graph
    将打印出的 F2F_name_Graph 复制到 F2F_name_Graph.txt即可
    下一步 将内部结构转换成数组形式-------跳转 数据预处理_1.3
    
    """
    # path_1 = r"C:\Users\gogforse\Desktop\测试文件夹\result\F2F_name_simple.txt"
    # path_2 = r"C:\Users\gogforse\Desktop\测试文件夹\result\F2F_name_Graph.txt"
    # get_name_Graph(path_1,path_2)

