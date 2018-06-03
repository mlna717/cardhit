# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import win32gui
from MyConfigParser import *
from LoginFrame import *
from CardHit import *


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):

    def __init__(self, parent):
        self.windowTitle = '沪牌拍卖系统'
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=self.windowTitle, pos=wx.DefaultPosition,
                          size=wx.Size(480, 481), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.isLogin = False
        self.cardHit = CardHit()

        self.file = "conf\\config.ini"
        self.conf = MyConfigParser()
        self.conf.read(self.file)

        outSizer = wx.FlexGridSizer(0, 2, 0, 0)
        outSizer.SetFlexibleDirection(wx.BOTH)
        outSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.title = wx.StaticText(self, wx.ID_ANY, u"沪牌拍卖系统", wx.DefaultPosition, wx.DefaultSize, 0)
        self.title.Wrap(-1)
        self.title.SetFont(wx.Font(30, 70, 90, 90, False, wx.EmptyString))

        outSizer.Add(self.title, 0, wx.ALL, 5)

        self.loginBtn = wx.Button(self, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.DefaultSize, 0)
        outSizer.Add(self.loginBtn, 0, wx.ALL, 5)

        strategySizer = wx.BoxSizer(wx.VERTICAL)

        straSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"策略1"), wx.VERTICAL)

        self.comm1 = wx.StaticText(straSizer1.GetStaticBox(), wx.ID_ANY, u"说明：设置固定金额，最低价加300大于等于该固定金额时出价",
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.comm1.Wrap(-1)
        straSizer1.Add(self.comm1, 0, wx.ALL, 5)

        dtlInfoSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.seq1 = wx.StaticText(straSizer1.GetStaticBox(), wx.ID_ANY, u"序号：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.seq1.Wrap(-1)
        dtlInfoSizer1.Add(self.seq1, 0, wx.ALL, 5)

        seqList1Choices = [u"1", u"2"]
        self.seqList1 = wx.Choice(straSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, seqList1Choices,
                                  0)
        self.seqList1.SetSelection(0)
        dtlInfoSizer1.Add(self.seqList1, 0, wx.ALL, 5)

        self.priceLabel = wx.StaticText(straSizer1.GetStaticBox(), wx.ID_ANY, u"价格：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.priceLabel.Wrap(-1)
        dtlInfoSizer1.Add(self.priceLabel, 0, wx.ALL, 5)

        self.price = wx.TextCtrl(straSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                 0)
        dtlInfoSizer1.Add(self.price, 0, wx.ALL, 5)

        straSizer1.Add(dtlInfoSizer1, 1, wx.EXPAND, 5)

        btnSizer1 = wx.GridBagSizer(0, 0)
        btnSizer1.SetFlexibleDirection(wx.BOTH)
        btnSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.saveBtn1 = wx.Button(straSizer1.GetStaticBox(), wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer1.Add(self.saveBtn1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.resetBtn1 = wx.Button(straSizer1.GetStaticBox(), wx.ID_ANY, u"重置", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer1.Add(self.resetBtn1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.runBtn1 = wx.Button(straSizer1.GetStaticBox(), wx.ID_ANY, u"运行", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer1.Add(self.runBtn1, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        straSizer1.Add(btnSizer1, 1, wx.EXPAND, 5)

        strategySizer.Add(straSizer1, 1, wx.EXPAND, 5)

        straSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"策略2"), wx.VERTICAL)

        self.comm2 = wx.StaticText(straSizer2.GetStaticBox(), wx.ID_ANY, u"说明：指定时间在最低价基础上增加指定金额出价", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        self.comm2.Wrap(-1)
        straSizer2.Add(self.comm2, 0, wx.ALL, 5)

        dtlInfoSizer2 = wx.GridSizer(0, 2, 0, 0)

        self.seq2 = wx.StaticText(straSizer2.GetStaticBox(), wx.ID_ANY, u"序号：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.seq2.Wrap(-1)
        dtlInfoSizer2.Add(self.seq2, 0, wx.ALL, 5)

        seqList2Choices = [u"1", u"2"]
        self.seqList2 = wx.Choice(straSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, seqList2Choices,
                                  0)
        self.seqList2.SetSelection(0)
        dtlInfoSizer2.Add(self.seqList2, 0, wx.ALL, 5)

        self.offTimeLabel = wx.StaticText(straSizer2.GetStaticBox(), wx.ID_ANY, u"出价时间：", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.offTimeLabel.Wrap(-1)
        dtlInfoSizer2.Add(self.offTimeLabel, 0, wx.ALL, 5)

        gbSizer3 = wx.GridBagSizer(0, 0)
        gbSizer3.SetFlexibleDirection(wx.BOTH)
        gbSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        hourPickChoices = [u"11"]
        self.hourPick = wx.ComboBox(straSizer2.GetStaticBox(), wx.ID_ANY, u"11", wx.DefaultPosition, wx.DefaultSize,
                                    hourPickChoices, 0)
        self.hourPick.SetSelection(0)
        gbSizer3.Add(self.hourPick, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        minuPickChoices = [u"00", u"01", u"02", u"03", u"04", u"05", u"06", u"07", u"08", u"09", u"10", u"11", u"12", u"13",
                           u"14", u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27",
                           u"28", u"29", u"30"]
        self.minuPick = wx.ComboBox(straSizer2.GetStaticBox(), wx.ID_ANY, u"00", wx.DefaultPosition, wx.DefaultSize,
                                    minuPickChoices, 0)
        self.minuPick.SetSelection(0)
        gbSizer3.Add(self.minuPick, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        secPickChoices = [u"00", u"01", u"02", u"03", u"04", u"05", u"06", u"07", u"08", u"09", u"10", u"11", u"12", u"13",
                          u"14", u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27",
                          u"28", u"29", u"30", u"31", u"32", u"33", u"34", u"35", u"36", u"37", u"38", u"39", u"40", u"41",
                          u"42", u"43", u"44", u"45", u"46", u"47", u"48", u"49", u"50", u"51", u"52", u"53", u"54", u"55",
                          u"56", u"57", u"58", u"59"]
        self.secPick = wx.ComboBox(straSizer2.GetStaticBox(), wx.ID_ANY, u"00", wx.DefaultPosition, wx.DefaultSize,
                                   secPickChoices, 0)
        self.secPick.SetSelection(0)
        gbSizer3.Add(self.secPick, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        dtlInfoSizer2.Add(gbSizer3, 1, wx.EXPAND, 5)

        self.addPriceLabel = wx.StaticText(straSizer2.GetStaticBox(), wx.ID_ANY, u"加价金额：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.addPriceLabel.Wrap(-1)
        dtlInfoSizer2.Add(self.addPriceLabel, 0, wx.ALL, 5)

        self.addPrice = wx.TextCtrl(straSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                    wx.Size(150, -1), 0)
        dtlInfoSizer2.Add(self.addPrice, 0, wx.ALL, 5)

        straSizer2.Add(dtlInfoSizer2, 1, wx.EXPAND, 5)

        btnSizer2 = wx.GridBagSizer(0, 0)
        btnSizer2.SetFlexibleDirection(wx.BOTH)
        btnSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.saveBtn2 = wx.Button(straSizer2.GetStaticBox(), wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer2.Add(self.saveBtn2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.resetBtn2 = wx.Button(straSizer2.GetStaticBox(), wx.ID_ANY, u"重置", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer2.Add(self.resetBtn2, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.runBtn2 = wx.Button(straSizer2.GetStaticBox(), wx.ID_ANY, u"运行", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer2.Add(self.runBtn2, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        straSizer2.Add(btnSizer2, 1, wx.EXPAND, 5)

        strategySizer.Add(straSizer2, 1, wx.EXPAND, 5)

        outSizer.Add(strategySizer, 1, wx.EXPAND, 5)

        compSizer = wx.BoxSizer(wx.VERTICAL)

        self.compRunBtn = wx.Button(self, wx.ID_ANY, u"运行", wx.Point(-1, -1), wx.Size(-1, -1), 0)
        compSizer.Add(self.compRunBtn, 0, wx.ALL, 5)

        self.compComment = wx.StaticText(self, wx.ID_ANY, u"说明：此处针对组\n合策略模式，点击\n运行前必须要选择\n策略中的序号，将\n按照序号依次判断\n执行",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.compComment.Wrap(-1)
        compSizer.Add(self.compComment, 0, wx.ALL, 5)

        outSizer.Add(compSizer, 1, wx.EXPAND, 5)

        self.SetSizer(outSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.loginBtn.Bind(wx.EVT_BUTTON, self.popLoginWdw)
        self.saveBtn1.Bind(wx.EVT_BUTTON, self.saveStra1)
        self.resetBtn1.Bind(wx.EVT_BUTTON, self.resetStra1)
        self.runBtn1.Bind(wx.EVT_BUTTON, self.runStra1)
        self.saveBtn2.Bind(wx.EVT_BUTTON, self.saveStra2)
        self.resetBtn2.Bind(wx.EVT_BUTTON, self.resetStra2)
        self.runBtn2.Bind(wx.EVT_BUTTON, self.runStra2)
        self.compRunBtn.Bind(wx.EVT_BUTTON, self.compRun)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def popLoginWdw(self, event):
        loginFrame = LoginFrame(self)
        ret = loginFrame.ShowModal()
        if ret == wx.OK:
            self.title.SetLabel(loginFrame.userName.Value+"登录成功")
            self.isLogin = True
    def saveStra1(self, event):
        self.clearStrategy()
        self.conf.add_section('strategy=pointPrice')
        self.conf.set('strategy=pointPrice','pointPrice',self.price.Value)
        self.showSuccess(event)

    def resetStra1(self, event):
        self.price.Clear()

    def runStra1(self, event):
        if self.checkLogin() == True:
            self.saveStra1(None)
            self.cardHit.executeStrategy()

    def saveStra2(self, event):
        self.clearStrategy()
        self.conf.add_section('strategy=pointTimeAndAddPrice')
        self.conf.set('strategy=pointTimeAndAddPrice', 'time', self.hourPick.Value+':'+self.minuPick.Value+':'+self.secPick.Value)
        self.conf.set('strategy=pointTimeAndAddPrice', 'add', self.addPrice.Value)
        self.showSuccess(event)
    def resetStra2(self, event):
        self.hourPick.Value='11'
        self.minuPick.Value='00'
        self.secPick.Value='00'
        self.addPrice.Clear()

    def runStra2(self, event):
        if self.checkLogin() == True:
            self.saveStra2(None)
            self.cardHit.executeStrategy()

    def loopList(self,list,seq):
        for val in list:
            if int(val[0]) == seq:
                return val[1]

    def saveCompStra1(self):
        self.conf.set('strategy=compose', 'stra1', 'pointPrice')
        self.conf.set('strategy=compose', 'pointPrice', self.price.Value)

    def saveCompStra2(self):
        self.conf.set('strategy=compose', 'stra2', 'pointTimeAndAddPrice')
        self.conf.set('strategy=compose', 'time',
                      self.hourPick.Value + ':' + self.minuPick.Value + ':' + self.secPick.Value)
        self.conf.set('strategy=compose', 'add', self.addPrice.Value)

    def saveCompStra(self,event):
        self.clearStrategy()
        self.conf.add_section('strategy=compose')

        idx = 1
        list = []
        list.append((self.seqList1.GetString(self.seqList1.GetSelection()),'stra1'))
        list.append((self.seqList2.GetString(self.seqList2.GetSelection()),'stra2'))
        while idx<=len(list):
            if self.loopList(list, idx) == 'stra1':
                self.saveCompStra1()
            if self.loopList(list, idx) == 'stra2':
                self.saveCompStra2()
            idx = idx + 1
        self.showSuccess(event)

    def compRun(self, event):
        if self.checkLogin() == True:
            self.saveCompStra(None)
            self.cardHit.executeStrategy()

    def clearStrategy(self):
        self.conf.remove_section('strategy=pointTimeAndAddPrice')
        self.conf.remove_section('strategy=pointPrice')
        self.conf.remove_section('strategy=compose')

    def showSuccess(self,event):
        self.conf.write(open(self.file,"w"))
        # 直接点击运行时不弹出该提示框
        if event != None:
            dlg = wx.MessageDialog(None, u"保存成功", u"提示", wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()

    def checkLogin(self):
        if self.isLogin == False:
            dlg = wx.MessageDialog(None, u"登录成功后才可以运行", u"提示", wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                self.popLoginWdw(None)
            dlg.Destroy()
        return self.isLogin


if __name__ == "__main__":
    isLogin = False
    app = wx.App()
    mainFrame = MainFrame(None)
    mainFrame.Show()
    app.MainLoop()