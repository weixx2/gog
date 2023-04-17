# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QFile, QFileInfo
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, \
    QLineEdit, QHBoxLayout, QComboBox, QMessageBox, QCheckBox, QTabWidget
import os
from deleteNotesSourse import trim_dir
#字符语义
from ascii.codeToASCII import find_java
from ascii.ASCIINormalization import ASCIINormalization,ASCIISize
#token语义
from token222 import getWord,getEmbedding,word2v
import token222
#RGB语义
from rgb.codeToRGB import find_javaRGB
from rgb.RGBNormalization import RGBNormalization,RGBSize
from rgb.RGBToPNG import RGBNormalizationPNG
#gog
from gog.getSide import C2C_Parse
from gog.generate_Graph import get_name_Graph
from gog.data_pretreatment import get_F2F_name,get_F2F_name_simple
from PyQt5.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GoGCIP')
        self.resize(530, 150)
        self.setMaximumSize(800, 150)
        self.setWindowIcon(QIcon("logoo.ico"))

        self.foo = 0 # 确认操作
        self.emb = 0 # 特征区分
        self.Normliz = 0 # 是否归一化
        #Create a tab widget\

        self.foo2 = 0 # 确认操作
        self.emb2 = 0 # 特征区分

        #分页面
        self.tabwidget = QTabWidget()
        self.tabwidget.setStyleSheet("""
            QTabBar::tab {
                background-color: #E8E8E8;
                border: 1px solid #C2C7CB;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 5px 15px;
            }

            QTabBar::tab:selected {
                background-color: #F2F2F2;
            }

            QTabBar::tab:!selected {
                margin-top: 2px;
            }

            QTabBar::tab:hover {
                background-color: #F2F2F2;
            }
        """)

        font = QFont("微软雅黑", 9)
        self.tabwidget.setFont(font)

        self.widget1 = QWidget()
        self.widget2 = QWidget()

        self.tabwidget.insertTab(1,self.widget1,"GoGCIP")
        self.tabwidget.insertTab(0,self.widget2,"GoG")
        # page1 info
        self.label1 = QLabel("项目路径：")
        self.lineEdit1 = QLineEdit()
        self.btn_choose1 = QPushButton("选择")
        self.label2 = QLabel("输出路径：")
        self.lineEdit2 = QLineEdit()
        self.btn_choose2 = QPushButton("选择")
        self.pushButton =  QPushButton(" 输出 ")
        self.pushButton2 = QPushButton("去除注释")
        self.btnHowToUse = QPushButton("使用说明")
        self.checkbox = QCheckBox("根据最大行列值统一化处理")
        self.info = QLabel()
        self.combox = QComboBox()
        self.init_combox()

        # page2 info
        self.label11 = QLabel("项目路径：")
        self.lineEdit11 = QLineEdit()
        self.btn_choose11 = QPushButton("选择")
        self.label22 = QLabel("输出路径：")
        self.lineEdit22 = QLineEdit()
        self.btn_choose22 = QPushButton("选择")
        self.pushButton11 =  QPushButton(" 抽取 ")
        self.btnHowToUse11 = QPushButton("使用说明")
        self.info11 = QLabel()
        self.combox11 = QComboBox()
        self.init_combox2()


        self.init_widget1()
        self.init_widget2()



        layout = QVBoxLayout()
        layout.addWidget(self.tabwidget)


        self.btn_choose1.clicked.connect(self.on_button_click_in)
        self.btn_choose2.clicked.connect(self.on_button_click_out)
        self.pushButton.clicked.connect(self.on_button_click_ok)
        self.pushButton2.clicked.connect(self.on_button_click_delete)
        self.btnHowToUse.clicked.connect(self.on_button_click_how)


        self.btn_choose11.clicked.connect(self.on_button_click_in_2)
        self.btn_choose22.clicked.connect(self.on_button_click_out_2)
        self.pushButton11.clicked.connect(self.on_button_click_ok_2)
        self.btnHowToUse11.clicked.connect(self.on_button_click_how_2)

        # Set the layout for the main window
        self.setLayout(layout)

        self.tabwidget.setCurrentIndex(0)
    def on_button_click_how(self):
        # textbrowser = QTextBrowser()
        # font = QFont("Microsoft YaHei", 12)
        # textbrowser.setFont(font)
        instructions = "一、使用步骤：\n-项目路径：需要处理的Java项目代码路径，注意是包含.java文件的项目，点击后方选择按钮进行选择\n\n-输出路径：语义特征生成后的保存路径，点击后方选择按钮进行选择\n\n-去除注释：本软件仅处理不带注释的Java文件，源代码可用该功能生成Java文件，源文件保存为.bat后缀\n\n-语义特征下拉框：选择需要提取的对应语义特征\n\n-输出：点击后对源文件进行语义特征抽取\n\n-根据最大行列值统一化处理：勾选后会进一步生成大小统一的数组文件，耗时较大，运行时软件可能卡顿，等待即可，可根据生成的-datanfo.txt-文件查看数据大小\n\n\n二、输出数据说明：\n-ASCII:①Source为字符语义原始数组②Normalize为字符语义统一维度的数据③dataInfo为数据信息\n\n-Token:①dataset为全部token②embedding为类对象的语义特征③w2vdata为word2vec模型\n\n-RGB:①Source为视觉语义原始数组②Normalize为视觉语义统一维度的数据③PNG为rgb结构的数组数据④Photos为对应类对象的图片⑤dataInfo为数据信息\n\n本软件为湖北大学硕士论文-《基于图中图神经网络的软件系统中类交互关系预测研究》中所提出的GoGCIP方法的代码语义特征数组提取工具，不包含模型训练\n\nCopyright (c) 2023 湖北大学 何鹏研究生团队  Authur:卫操   WeChat:gogforse"
        self.showMsg(instructions)
        # textbrowser.setText(instructions)
        # textbrowser.show()

    def on_button_click_how_2(self):
        # textbrowser = QTextBrowser()
        # font = QFont("Microsoft YaHei", 12)
        # textbrowser.setFont(font)
        instructions = "一、网络结构抽取：\n-项目路径：由DependencyFinder工具生成的结构化XML文件\n\n-输出路径：三种粒度链接关系文件保存路径\n\n-输出：三种粒度链接关系文件①P2P文件包粒度②C2C文件类粒度③F2F文件方法粒度\n\n二、图中图结构抽取：\n-项目路径：由网络结构抽取生成的结构化F2F文件\n\n-输出路径：三种链接关系的简化文件保存路径\n\n-输出：三种链接关系的简化①去除括号的name文件②只保留方法属性关系的simple文件③图中图文件graph\n\n本软件为软件学报论文-《基于图中图卷积神经网络的软件系统中类交互关系预测》中所提出的GoGCN方法的图中图特征提取工具，不包含模型训练\n\nCopyright (c) 2023 湖北大学 何鹏研究生团队  Authur:卫操   WeChat:gogforse"
        self.showMsg(instructions)
        # textbrowser.setText(instructions)
        # textbrowser.show()
    # 点击按钮选择文件路径
    def on_button_click_in(self):
        file_path= QFileDialog.getExistingDirectory(self, '选择文件')
        # 如果用户选择了文件，将文件路径显示在标签中
        if file_path:
            self.lineEdit1.setText(file_path)

    def on_button_click_in_2(self):
        file_path= QFileDialog.getOpenFileName(parent=None,caption='Open file',filter='All files (*);')[0]
        # 如果用户选择了文件，将文件路径显示在标签中
        if QFile.exists(file_path):
            self.lineEdit11.setText(file_path)
    # 点击按钮选择文件路径
    def on_button_click_out(self):
        file_path= QFileDialog.getExistingDirectory(self, '选择文件')
        # 如果用户选择了文件，将文件路径显示在标签中
        if file_path:
            self.lineEdit2.setText(file_path)

    def on_button_click_out_2(self):
        file_path= QFileDialog.getExistingDirectory(self, '选择文件')
        # 如果用户选择了文件，将文件路径显示在标签中
        if file_path:
            self.lineEdit22.setText(file_path)
    # 点击生成按钮
    def on_button_click_ok(self):
        if not os.path.exists(self.lineEdit1.text()):
            self.showMsg("项目文件夹路径不存在")
            return
        if not os.path.exists(self.lineEdit2.text()):
            self.showMsg("输出文件夹路径不存在")
            return
        if self.combox.currentIndex() == 0:
            #字符语义
            self.showMsg("是否确认生成字符语义？")
            if self.foo == 1:
                self.emb = 0
                self.showMsg("点击确认后开始生成，请耐心等待，耗费时间与性能相关...")
                self.changeBtnState()
                self.getEmb()
                self.showMsg("生成完成")
                self.tabwidget.setCurrentIndex(1)
                self.changeBtnState()
            self.foo = 0
        elif self.combox.currentIndex() == 1:
            self.showMsg("是否确认生成token语义？")
            if self.foo == 1:
                self.emb = 1
                self.showMsg("点击确认后开始生成，请耐心等待，耗费时间与性能相关...")
                self.changeBtnState()
                self.getEmb()
                self.showMsg("生成完成")
                self.tabwidget.setCurrentIndex(1)
                self.changeBtnState()
            self.foo = 0
        elif self.combox.currentIndex() == 2:
            self.showMsg("是否确认生成视觉语义？")
            if self.foo == 1:
                self.emb = 2
                self.showMsg("点击确认后开始生成，请耐心等待，耗费时间与性能相关...")
                self.changeBtnState()
                self.getEmb()
                self.showMsg("生成完成")
                self.tabwidget.setCurrentIndex(1)
                self.changeBtnState()
            self.foo = 0
        self.tabwidget.setCurrentIndex(1)
        # 执行
        return

        # 点击生成按钮
    def on_button_click_ok_2(self):
        if not os.path.exists(self.lineEdit11.text()):
            self.showMsg("项目文件夹路径不存在")
            return
        if not os.path.exists(self.lineEdit22.text()):
            self.showMsg("输出文件夹路径不存在")
            return
        if self.combox11.currentIndex() == 0:
            # 字符语义
            if not self.lineEdit11.text().split("\\")[-1].split('.')[-1] == "xml":
                self.showMsg("请选择-DependencyFinder-工具产生的xml文件作为输入")
                return
            self.showMsg("是否确认生成网络结构？")
            if self.foo2 == 1:
                self.emb2 = 0
                self.showMsg("点击确认后开始生成，请耐心等待，耗费时间与性能相关...")
                self.changeBtnState()
                self.getEmb2()
                self.showMsg("生成完成")
                self.tabwidget.setCurrentIndex(0)
                self.changeBtnState()
            self.foo = 0
        elif self.combox11.currentIndex() == 1:
            if "F2F" not in self.lineEdit11.text():
                self.showMsg("请选择生成网络结构,产生-F2F.txt-文件作为输入")
                return
            self.showMsg("是否确认生成图中图结构？")
            if self.foo2 == 1:
                self.emb2 = 1
                self.showMsg("点击确认后开始生成，请耐心等待，耗费时间与性能相关...")
                self.changeBtnState()
                self.getEmb2()
                self.showMsg("生成完成")
                self.tabwidget.setCurrentIndex(0)
                self.changeBtnState()
            self.foo = 0
        return

    # 点击清除代码注释
    def on_button_click_delete(self):
        if os.path.exists(self.lineEdit1.text()):
            self.showMsg("确认清除注释吗？该操作会产生新的文件")
            # 执行
            if self.foo == 1:
                self.showMsg("正在清除...")
                self.changeBtnState()
                self.deleteNote(self.lineEdit1.text())
                self.showMsg("清除完成")
                self.changeBtnState()
            self.foo = 0
            return
        else:
            self.showMsg("项目文件夹路径不存在")
            return

    # 弹窗信息
    def showMsg(self,str,flag = 0):
        msg = QMessageBox()
        msg.setWindowTitle('提示')
        msg.setText(str)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.buttonClicked.connect(self.msgBtnClicked)
        msg.exec_()
    # 弹窗选择
    def msgBtnClicked(self, btn):
        if self.tabwidget.currentIndex()==0:
            if btn.text() == 'OK':
                self.foo2 = 1
            elif btn.text() == 'Cancel':
                self.foo2 = 0
        if self.tabwidget.currentIndex()==1:
            if btn.text() == 'OK':
                self.foo = 1
            elif btn.text() == 'Cancel':
                self.foo = 0
    #视角

    # 改变按钮状态-不可选取
    def changeBtnState(self):# 样式未改变
        if self.tabwidget.currentIndex() == 1:
            state = not self.btn_choose1.isEnabled()
            if state:
                self.pushButton.setStyleSheet("")
                self.pushButton2.setStyleSheet("")
                self.btn_choose1.setStyleSheet("")
                self.btn_choose2.setStyleSheet("")
                self.pushButton.setStyleSheet(
                    'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.pushButton2.setStyleSheet(
                    'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose1.setStyleSheet(
                    'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose2.setStyleSheet(
                    'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
            else:
                self.pushButton.setStyleSheet("")
                self.pushButton2.setStyleSheet("")
                self.btn_choose1.setStyleSheet("")
                self.btn_choose2.setStyleSheet("")
                self.pushButton.setStyleSheet(
                    'background-color: #2c8def; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.pushButton2.setStyleSheet(
                    'background-color: #2c8def; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose1.setStyleSheet(
                    'background-color: #FFCD41; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose2.setStyleSheet(
                    'background-color: #FFCD41; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
            self.btn_choose1.setEnabled(state)
            self.btn_choose2.setEnabled(state)
            self.pushButton.setEnabled(state)
            self.pushButton2.setEnabled(state)
            self.tabwidget.setTabEnabled(0,state)
            self.tabwidget.setTabEnabled(1,state)
            #改变样式
        if self.tabwidget.currentIndex() == 0:
            state = not self.btn_choose11.isEnabled()
            if state:
                self.pushButton11.setStyleSheet("")
                self.btn_choose11.setStyleSheet("")
                self.btn_choose22.setStyleSheet("")
                self.pushButton11.setStyleSheet(
                    'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose11.setStyleSheet(
                    'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose22.setStyleSheet(
                    'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
            else:
                self.pushButton11.setStyleSheet("")
                self.btn_choose11.setStyleSheet("")
                self.btn_choose22.setStyleSheet("")
                self.pushButton11.setStyleSheet(
                    'background-color: #2c8def; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose11.setStyleSheet(
                    'background-color: #FFCD41; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
                self.btn_choose22.setStyleSheet(
                    'background-color: #FFCD41; color: grey; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
            self.btn_choose11.setEnabled(state)
            self.btn_choose22.setEnabled(state)
            self.pushButton11.setEnabled(state)
            self.tabwidget.setTabEnabled(0,state)
            self.tabwidget.setTabEnabled(1,state)
    # 实例化界面1
    def init_widget1(self):

        # 创建控件
        # 创建标签、文本框和按钮
        self.pushButton.setCursor(Qt.PointingHandCursor)
        self.pushButton2.setCursor(Qt.PointingHandCursor)
        self.btn_choose1.setCursor(Qt.PointingHandCursor)
        self.btn_choose2.setCursor(Qt.PointingHandCursor)
        self.btnHowToUse.setCursor(Qt.PointingHandCursor)

        font = QFont('Arial', 10)  # 设置字体和大小
        self.lineEdit1.setFont(font)
        self.lineEdit2.setFont(font)

        self.info.setText("Copyright (c) 2023 何鹏研究生团队 Author:weixx  WeChat:gogforse")
        font = QFont("Segoe UI")
        color = QColor(Qt.blue)
        self.info.setFont(font)
        self.info.setStyleSheet("color: {}".format(color.name()))

        # 创建水平布局并添加控件
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.label1)
        h_layout1.addWidget(self.lineEdit1)
        h_layout1.addWidget(self.btn_choose1)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.label2)
        h_layout2.addWidget(self.lineEdit2)
        h_layout2.addWidget(self.btn_choose2)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(self.combox,0,Qt.AlignLeft)
        h_layout3.addWidget(self.checkbox,0,Qt.AlignRight)
        h_layout3.addWidget(self.btnHowToUse,0,Qt.AlignRight)
        h_layout3.setStretch(1,8)

        hbox = QHBoxLayout()
        hbox.addWidget(self.pushButton2,0,Qt.AlignLeft)
        hbox.addWidget(self.pushButton,0,Qt.AlignRight)


        # 创建垂直布局并添加控件
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout3)
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(hbox)
        v_layout.addWidget(self.info,0,Qt.AlignRight)
        v_layout.setSpacing(8)
        # 设置布局
        self.widget1.setLayout(v_layout)

        # 设置背景图片

        # 设置标签和按钮样式
        self.label1.setStyleSheet('color: black; font-size: 16px;')
        self.label2.setStyleSheet('color: black; font-size: 16px;')
        self.lineEdit1.setStyleSheet('background-color: white; border-radius: 10px; padding: 5px 10px;')
        self.lineEdit2.setStyleSheet('background-color: white; border-radius: 10px; padding: 5px 10px;')
        self.pushButton.setStyleSheet(
            'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')#22D789
        self.pushButton2.setStyleSheet(
            'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
        self.btn_choose1.setStyleSheet(
            'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
        self.btn_choose2.setStyleSheet(
            'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
        self.btnHowToUse.setStyleSheet(
            'background-color: #22D789; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')#2c8def

    # 实例化界面2
    def init_widget2(self):

        # 创建控件
        # 创建标签、文本框和按钮
        self.pushButton11.setCursor(Qt.PointingHandCursor)
        self.btn_choose11.setCursor(Qt.PointingHandCursor)
        self.btn_choose22.setCursor(Qt.PointingHandCursor)
        self.btnHowToUse11.setCursor(Qt.PointingHandCursor)

        font = QFont('Arial', 10)  # 设置字体和大小
        self.lineEdit11.setFont(font)
        self.lineEdit22.setFont(font)

        self.info11.setText("Copyright (c) 2023 何鹏研究生团队 Author:weixx  WeChat:gogforse")
        font = QFont("Segoe UI")
        color = QColor(Qt.blue)
        self.info11.setFont(font)
        self.info11.setStyleSheet("color: {}".format(color.name()))

        # 创建水平布局并添加控件
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.label11)
        h_layout1.addWidget(self.lineEdit11)
        h_layout1.addWidget(self.btn_choose11)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.label22)
        h_layout2.addWidget(self.lineEdit22)
        h_layout2.addWidget(self.btn_choose22)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(self.combox11,0,Qt.AlignLeft)
        h_layout3.addWidget(self.btnHowToUse11,0,Qt.AlignRight)
        h_layout3.setStretch(1,8)

        hbox = QHBoxLayout()
        hbox.addWidget(self.pushButton11,0,Qt.AlignRight)


        # 创建垂直布局并添加控件
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout3)
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(hbox)
        v_layout.addWidget(self.info11,0,Qt.AlignRight)
        v_layout.setSpacing(8)
        # 设置布局
        self.widget2.setLayout(v_layout)

        # 设置背景图片

        # 设置标签和按钮样式
        self.label11.setStyleSheet('color: black; font-size: 16px;')
        self.label22.setStyleSheet('color: black; font-size: 16px;')
        self.lineEdit11.setStyleSheet('background-color: white; border-radius: 10px; padding: 5px 10px;')
        self.lineEdit22.setStyleSheet('background-color: white; border-radius: 10px; padding: 5px 10px;')
        self.pushButton11.setStyleSheet(
            'background-color: #2c8def; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')#22D789
        self.btn_choose11.setStyleSheet(
            'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
        self.btn_choose22.setStyleSheet(
            'background-color: #FFCD41; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')
        self.btnHowToUse11.setStyleSheet(
            'background-color: #22D789; color: white; font-size: 16px; border-radius: 10px; padding: 5px 10px;')#2c8def
    # 实例化下拉框
    def init_combox(self):
        self.combox.addItem("字符语义")
        self.combox.addItem("token语义")
        self.combox.addItem("视觉语义")
        self.combox.setFont(QFont("SimSun", 12))  # 设置字体为Arial，字号为12

    def init_combox2(self):
        self.combox11.addItem("网络结构")
        self.combox11.addItem("图中图结构")
        self.combox11.setFont(QFont("SimSun", 12))  # 设置字体为Arial，字号为12

    # 删除代码注释
    def deleteNote(self,pathIn):
        trim_dir(pathIn)

    # 三种语义特征
    def getEmb(self):
        if self.emb == 0:#字符语义
            self.ascii()
        elif self.emb == 1:
            self.token()
        elif self.emb == 2:
            self.RGB()

    def getEmb2(self):
        if self.emb2 == 0:#字符语义
            self.graph()
        elif self.emb2 == 1:
            self.gog()
    def graph(self):
        c2c = C2C_Parse()
        c2c.classParse(self.lineEdit11.text(),self.lineEdit22.text())
    def gog(self):
        path1 = self.lineEdit11.text()
        path2 = self.lineEdit22.text()+"\\result\\F2F_name.txt.txt"
        path3 = self.lineEdit22.text()+"\\result\\F2F_name_simple.txt"
        path4 = self.lineEdit22.text()+"\\result\\F2F_name_Graph.txt"
        get_F2F_name(path1,path2)
        get_F2F_name_simple(path2,path3)
        get_name_Graph(path3,path4)
    def ascii(self):
        dataIn = self.lineEdit1.text()
        dataOut = self.lineEdit2.text()
        # 创建存放文件夹
        dataOutSource = dataOut + "//Ascii//Source//"
        dataOutNormail = dataOut + "//Ascii//Normalize//"
        dataInfo = dataOut + "//Ascii//dataInfo.txt"
        if not os.path.exists(dataOutSource):
            os.makedirs(dataOutSource)
        if not os.path.exists(dataOutNormail):
            os.makedirs(dataOutNormail)
        # 生成原始文件
        find_java(dataIn, dataOutSource)
        # 统计文件数量
        nums = len(os.listdir(dataOutSource))
        # 归一处理
        maxX, maxY, maxXClass, maxYClass, maxXAll, maxYAll, countMaxR_1000, countMaxC_1000, countMaxR_500, countMaxC_500, countMaxR_100_200, countMaxC_200_300 = ASCIISize(
            dataOutSource)
        with open(dataInfo, 'w') as f:
            f.write("最大行列：" + '[' + str(maxX) + ',' + str(maxY) + ']\n')
            f.write("[最大行文件：" + str(maxXClass) + ',' + '最大列文件' + str(maxYClass) + ']\n')
            f.write("[总共行数：" + str(maxXAll) + ',' + '总共列数' + str(maxYAll) + ']\n')
            f.write("[平均行数：" + str(maxXAll / nums) + ',' + '平均列数' + str(maxYAll / nums) + ']\n')
            f.write("[大于1000的行的类个数：" + str(countMaxR_1000) + ',' + '大于1000的列的类个数' + str(
                countMaxC_1000) + ']\n')
            f.write(
                "[大于500的行的类个数：" + str(countMaxR_500) + ',' + '大于500的列的类个数' + str(countMaxC_500) + ']\n')
            f.write("[100~200的行的类个数：" + str(countMaxR_100_200) + ',' + '200~300的列的类个数' + str(
                countMaxC_200_300) + ']\n')
        # 运行核心
        if self.checkbox.isChecked():
            ASCIINormalization(dataOutSource, dataOutNormail, maxX, maxY)

    def token(self):
        dataIn = self.lineEdit1.text()
        dataOut = self.lineEdit2.text()
        outputPath = dataOut+'//token//dataset//'
        outputPathw = dataOut+'//token//dataset//datasetW//'
        outputPathw2v = dataOut+'//token//w2vdata//'
        embeddingpath = dataOut+'//token//embedding//'

        if not os.path.exists(outputPathw2v):
            os.makedirs(outputPathw2v)
        if not os.path.exists(outputPathw):
            os.makedirs(outputPathw)
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        if not os.path.exists(embeddingpath):
            os.makedirs(embeddingpath)

        AstParser = token222.AstParser(dataIn, outputPath)
        AstFactory = token222.AstFactory(AstParser)
        # 字典
        trainASPName = AstFactory.astProcessing("", r'(.+).java$')
        getWord(outputPath + "datasetW\\" + "token", trainASPName)
        model_test = word2v(outputPath + "datasetW\\" + "token",outputPathw2v, "token")
        getEmbedding(embeddingpath + "token" + ".json", trainASPName, model_test)


    def RGB(self):
        dataIn = self.lineEdit1.text()
        dataOut = self.lineEdit2.text()
        # 创建存放文件夹
        dataOutSource = dataOut + "//RGB//"
        dataOutNormail = dataOut + "//RGB//Normalize//"
        dataPNG = dataOut + "//RGB//Source//"
        dataPNG2 = dataOut + "//RGB//PNG//"

        if not os.path.exists(dataOutSource):
            os.makedirs(dataOutSource)
        if not os.path.exists(dataOutNormail):
            os.makedirs(dataOutNormail)
        if not os.path.exists(dataPNG):
            os.makedirs(dataPNG)
        if not os.path.exists(dataPNG2):
            os.makedirs(dataPNG2)
        dataInfo = dataOut + "//RGB//dataInfo.txt"
        # 生成原始文件
        find_javaRGB(dataIn, dataOutSource, "")
        # 统计文件数量
        nums = len(os.listdir(dataOutSource))
        # 归一处理
        maxX, maxY, maxXClass, maxYClass, maxXAll, maxYAll, countMaxR_1000, countMaxC_1000, countMaxR_500, countMaxC_500, countMaxR_100_200, countMaxC_200_300 = RGBSize(
            dataPNG)
        with open(dataInfo, 'w') as f:
            f.write("最大行列：" + '[' + str(maxX) + ',' + str(maxY) + ']\n')
            f.write("[最大行文件：" + str(maxXClass) + ',' + '最大列文件' + str(maxYClass) + ']\n')
            f.write("[总共行数：" + str(maxXAll) + ',' + '总共列数' + str(maxYAll) + ']\n')
            f.write("[平均行数：" + str(maxXAll / nums) + ',' + '平均列数' + str(maxYAll / nums) + ']\n')
            f.write("[大于1000的行的类个数：" + str(countMaxR_1000) + ',' + '大于1000的列的类个数' + str(
                countMaxC_1000) + ']\n')
            f.write(
                "[大于500的行的类个数：" + str(countMaxR_500) + ',' + '大于500的列的类个数' + str(countMaxC_500) + ']\n')
            f.write("[100~200的行的类个数：" + str(countMaxR_100_200) + ',' + '200~300的列的类个数' + str(
                countMaxC_200_300) + ']\n')
        # 生成图片
        dataPhotos = dataOutSource + "Photos//"
        if not os.path.exists(dataPhotos):
            os.makedirs(dataPhotos)
        RGBNormalizationPNG(dataPNG2,dataPhotos)
        # 运行核心
        if self.checkbox.isChecked():
            RGBNormalization(dataPNG, dataOutNormail, maxX, maxY)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
