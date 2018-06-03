# -*- coding: utf-8 -*-
import wx
import wx.xrc
import requests
import telnetlib
from time import sleep
import _thread as thread
from MyConfigParser import *

con = telnetlib.Telnet()

class LoginFrame(wx.Dialog):

    def __init__(self, parent):
        self.parseConfig()
        self.windowTitle = '登录'
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(250, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        loginSizer = wx.FlexGridSizer(0, 2, 0, 0)
        loginSizer.SetFlexibleDirection(wx.BOTH)
        loginSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.loginName = wx.StaticText(self, wx.ID_ANY, u"用户名", wx.DefaultPosition, wx.DefaultSize, 0)
        self.loginName.Wrap(-1)
        loginSizer.Add(self.loginName, 0, wx.ALL, 5)

        self.userName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        loginSizer.Add(self.userName, 0, wx.ALL, 5)

        self.loginPwd = wx.StaticText(self, wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.loginPwd.Wrap(-1)
        loginSizer.Add(self.loginPwd, 0, wx.ALL, 5)

        self.passwd = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        loginSizer.Add(self.passwd, 0, wx.ALL, 5)

        self.loginBtn = wx.Button(self, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.DefaultSize, 0)
        loginSizer.Add(self.loginBtn, 0, wx.ALL, 5)

        self.resetBtn = wx.Button(self, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.DefaultSize, 0)
        loginSizer.Add(self.resetBtn, 0, wx.ALL, 5)

        self.SetSizer(loginSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.loginBtn.Bind(wx.EVT_BUTTON, self.login)
        self.resetBtn.Bind(wx.EVT_BUTTON, self.reset)

    def __del__(self):
        pass

    def parseConfig(self):
        conf = MyConfigParser()
        conf.read("conf\\config.ini")
        sections = conf.sections()
        for section in sections:
            prefix = str(section)
            if prefix.startswith('server'):
                self.ip = conf.get(prefix,'ip')
                self.port = conf.get(prefix,'port')

    def connect(self):
        try:
            con.open(self.ip, self.port, timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='沪牌拍卖', size=(510, 400))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (200, 100))

    def showDialog(self, title, content, size):
        # 显示错误信息对话框
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()

    # Virtual event handlers, overide them in your derived class
    def login(self, event):
        # 认证
        url = 'http://card.hit.sh:8080/login?username=' + self.userName.Value + '&password=' + self.passwd.Value
        info = {'username': self.userName.Value, 'password': self.passwd.Value}
        ret = requests.get(url,data=info)
        if ret.status_code == 200:
            result = ret.text
            if result == 'success':
                # 初始化聊天服务器连接并打开聊天窗口
                self.connect()
                self.EndModal(wx.OK)
            else:
                dlg = wx.MessageDialog(None, u"用户名或密码错误", u"错误", wx.OK | wx.ICON_ERROR)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()
        else:
            dlg = wx.MessageDialog(None, u"服务请求异常"+str(ret.status_code)+"\n"+ret.text, u"错误", wx.OK | wx.ICON_ERROR)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Destroy()

    def reset(self, event):
        # event.Skip()
        self.userName.Clear()
        self.passwd.Clear()

class ChatFrame(wx.Frame):
    """
    聊天窗口
    """

    def __init__(self, parent, id, title, size):
        offset = (500,-150)
        wx.Frame.__init__(self, parent, id, title, pos=(494+offset[0],362+offset[1]))
        self.SetSize(size)
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(490, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos=(5, 320), size=(300, 25))
        self.sendButton = wx.Button(self, label="Send", pos=(310, 320), size=(58, 25))
        self.usersButton = wx.Button(self, label="Users", pos=(373, 320), size=(58, 25))
        self.closeButton = wx.Button(self, label="Close", pos=(436, 320), size=(58, 25))
        # 发送按钮绑定发送消息方法
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # Users按钮绑定获取在线用户数量方法
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # 关闭按钮绑定关闭方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        # 发送消息
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')

    def close(self, event):
        # 关闭窗口
        con.write(b'logout\n')
        con.close()
        self.Close()

    def receive(self):
        # 接受服务器的消息
        while True:
            try:
                sleep(0.6)
                result = con.read_very_eager()
                if result != '':
                    self.chatFrame.AppendText(result)
            except:
                continue