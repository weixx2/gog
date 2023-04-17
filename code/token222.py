
import javalang as jl
import javalang.tree as jlt
import os
import re
import json
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec

#项目源文件proSource，特征文件proCSV（我没有），找java源文件的规则
class AstParser:
    def __init__(self, sPath, oPath):
        """
        程序的AST树解析
        :param sPath: 下载项目路径
        :param oPath: AST解析后的项目路径
        """
        self.sPath = sPath
        self.oPath = oPath
        self.TypeList = ['FormalParameter', 'BasicType', 'PackageDeclaration',
                         'InterfaceDeclaration', 'CatchClauseParameter', 'ClassDeclaration',
                         'MethodInvocation', 'SuperMethodInvocation', 'MemberReference', 'SuperMemberReference',
                         'ConstructorDeclaration', 'ReferenceType', 'MethodDeclaration', 'VariableDeclarator',
                         'IfStatement',
                         'WhileStatement', 'DoStatement', 'ForStatement', 'AssertStatement', 'BreakStatement',
                         'ContinueStatement',
                         'ReturnStatement', 'ThrowStatement', 'SynchronizedStatement',
                         'TryStatement', 'SwitchStatement', 'BlockStatement',
                         'StatementExpression', 'TryResource', 'CatchClause', 'CatchClauseParameter',
                         'SwitchStatementCase', 'ForControl', 'EnhancedForControl']

    def saveAstMap(self, proSource, reg=r'(.+).java$'):
        # print("local saveAstMap...")
        projectPath = self.sPath + proSource + "\\"
        projectJavaMap = {}
        for root, dirs, files in os.walk(projectPath):
            for each in files:
                tempPath = os.path.join(root, each)
                searchResult = re.search(reg, tempPath)
                if searchResult:
                    resultList = []
                    temp = searchResult.group(1)
                    tempJpath = '.'.join(temp.split("\\"))
                    with open(tempPath,encoding='utf-8') as file:
                        JavaContents = file.read()
                    try:
                        tree = jl.parse.parse(JavaContents)
                        #print(tempJpath)
                    except Exception:
                        # print(tempJpath)
                        continue
                    else:
                        for path, node in tree:
                            if isinstance(node, jlt.MethodInvocation) or isinstance(node,
                                                                                    jlt.SuperMethodInvocation):
                                resultList.append(str(node.member) + "()")
                                continue
                            if isinstance(node, jlt.ClassCreator):
                                resultList.append(str(node.type.name))
                                continue
                            if str(node) in self.TypeList and isinstance(node, jlt.Declaration):
                                resultList.append(str(node.name))
                                continue
                            if isinstance(node, jlt.AssertStatement) or isinstance(node, jlt.TryResource):
                                resultList.append(str(node.value))
                                continue
                            if str(node) in self.TypeList:
                                resultList.append(str(node))

                        tempJpath=tempJpath.split(".")[-1]
                        projectJavaMap[tempJpath] = resultList[1:]

        return projectJavaMap

class AstFactory:
    def __init__(self,AstParser):
        self.AstParser=AstParser

    def astProcessing(self,Projects,reg):
        trainASPName = self.AstParser.saveAstMap(Projects, reg)

        # print("trainASPName",trainASPName)

        return trainASPName

def getWord(path,trainASPName):
    # print("write all project words...")
    with open(path, "w")as f:
        #f.write(str(trainASPName))
        for i, k in trainASPName.items():
            for j in k:
                if k != "[]":
                    f.write(j)
                    f.write("  ")

def word2v(path,w2v,cl):
    # print("Word2Vec...")
    vocab = path
    # windows训练窗口的大小,min_count,词频阈值，
    model_test = Word2Vec(LineSentence(vocab), vector_size=30, window=5, min_count=3, workers=60, sg=1,
                          max_final_vocab=None)
    model_test.save(w2v+cl+".w2v")
    #model_test = Word2Vec.load('model_test.w2v')
    return model_test

def getEmbedding(path,trainASPName,model_test):
    count=0
    length=len(trainASPName.keys())
    with open(path,"w") as f:
            # print("progressing: 0.00%")
            for k,v in trainASPName.items():
                count+=1
                if(count/length==0.5 or count/length==0 or count/length==1):
                    pass
                    # print("progressing: ",'%.2f%%' % (count/length * 100))
                list=[]


                for i in v:
                    if (i in model_test.wv.index_to_key):
                        # list.extend(model_test.wv[i])
                        list.append(model_test.wv[i].tolist())
                trainASPName[k]=list



            f.write(json.dumps(str(trainASPName)))


