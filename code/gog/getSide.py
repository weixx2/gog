import os
from os.path import join
from shutil import  copyfile
class C2C_Parse():
    def __init__(self):
        self.dir = ''
        self.path = ''
        self.temp = ''
        self.cclass = ''
        self.dclass = ''
        self.set = set()
        self.f = False
        self.a=''
        self.b=''
        self.c=''
        self.s = ''
        self.s2 = ''
    def classParse(self, dir,p3):
        p = dir.split("/")
        p2 = ''
        filename = p[-1]
        for i in range(len(p)-2):
            p2 = p2+p[i]+"/"
        p3 = p3+"/result"
        # p3 = p2+"\\result"
        if not os.path.exists(p3):
            os.makedirs(p3)
        p4 = p3+"/"+filename
        copyfile(dir,p4)
        self.s = p4.split('xml')
        self.s2 = self.s[0]+"txt"
        if not os.path.exists(self.s2):
            os.rename(p4,self.s2)
        with open(self.s2,'r')as f:
            path = self.s[0]+"C2C.txt"
            with open(path,'w')as f2:
                self.temp = f.readline()
                while(self.temp!=''):
                    if "<class confirmed=\"yes\">" in self.temp:
                        self.f = True
                        self.temp = f.readline()
                        self.a = self.temp.strip().split(">")
                        self.b = self.a[1].strip().split("<")
                        self.cclass = self.b[0]
                        self.temp = f.readline()
                    if self.f and ("outbound type=\"class\" confirmed=\"yes\"" in self.temp) :
                        self.a = self.temp.strip().split(">");
                        self.b = self.a[1].strip().split("<");
                        self.dclass = self.b[0]
                        self.set.add(self.dclass)
                    if self.f and ("</class>" in self.temp) :
                        self.f = False;
                        if (len(self.set) > 0) :
                            for i in self.set:
                                if not i==(self.cclass):
                                    f2.write(self.cclass+'\t'+i+'\n')
                        self.set.clear();
                    self.temp = f.readline()
        self.packageParse()
        self.featureParse()

    def packageParse(self):
        with open(self.s2,'r')as f:
            path = self.s[0]+"P2P.txt"
            with open(path,'w')as f2:
                self.temp = f.readline()
                while(self.temp!=''):
                    if "<package confirmed=\"yes\">" in self.temp:
                        self.f = True
                        self.temp = f.readline()
                        self.a = self.temp.strip().split(">")
                        self.b = self.a[1].strip().split("<")
                        self.cclass = self.b[0]
                        self.temp = f.readline()
                    if self.f and ("outbound type=\"class\" confirmed=\"yes\"" in self.temp) :
                        self.a = self.temp.strip().split(">");
                        self.b = self.a[1].strip().split("<");
                        self.c = self.b[0].split('\\.')
                        self.dclass = self.c[0]
                        for i in range(len(self.c)-1):
                            self.dclass = self.dclass+"."+self.c[i+1]
                        self.set.add(self.dclass)
                    if self.f and "outbound type=\"feature\" confirmed=\"yes\"" in self.temp:
                        a=self.temp.strip().split('>')
                        if "(" in self.temp:
                            self.b = self.a[1].strip().split('\\(')
                        else:
                            self.b=self.a[1].strip().split('<')
                        self.c = self.b[0].split("\\.")
                        self.dclass = self.c[0]
                        for i in range(len(self.c)-2):
                            i=i+1
                            self.dclass = self.dclass+'.'+self.c[i]
                        self.set.add(self.dclass)
                    if self.f and ("</class>" in self.temp) :
                        self.f = False;
                        if (len(self.set) > 0) :
                            for i in self.set:
                                if not i==(self.cclass):
                                    f2.write(self.cclass+'\t'+i+'\n')
                        self.set.clear();
                    self.temp = f.readline()

    def featureParse(self):
        with open(self.s2,'r')as f:
            path = self.s[0]+"F2F.txt"
            with open(path,'w')as f2:
                self.temp = f.readline()
                while(self.temp!=''):
                    if "<feature confirmed=\"yes\">" in self.temp:
                        self.f = True
                        self.temp = f.readline()
                        self.a = self.temp.strip().split(">")
                        self.b = self.a[1].strip().split("<")
                        self.cclass = self.b[0]
                        self.temp = f.readline()
                    if self.f and ("outbound type=\"feature\" confirmed=\"yes\"" in self.temp) :
                        self.a = self.temp.strip().split(">");
                        self.b = self.a[1].strip().split("<");
                        self.dclass = self.b[0]
                        self.set.add(self.dclass)
                    if self.f and ("</feature>" in self.temp) :
                        self.f = False;
                        if (len(self.set) > 0) :
                            for i in self.set:
                                if not i==(self.cclass):
                                    f2.write(self.cclass+'\t'+i+'\n')
                        self.set.clear();
                    self.temp = f.readline()

