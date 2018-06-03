from MyConfigParser import *
from PIL import ImageGrab
from PIL import Image
from pyocr import libtesseract
from PAM30 import PAMIE
from mouseclick import *
import win32gui
import time
class CardHit:
    hwnd = None
    tuple = ()
    cBox = ()
    pBox = ()
    vBox = ()
    dskX = 0
    dskY = 0
    url = ''
    title = ''
    wait = 5
    isDebugOn = 'off'
    isOpen = False;
    strategy = ''
    pointTimeAndAddPrice = {}
    pointDiffPrice = {}
    pointPrice = {}
    compList = []
    mouse = mouseclick()
    def __init__(self):
        None
    def parseConfig(self):
        conf = MyConfigParser()
        conf.read("conf\\config.ini")
        sections = conf.sections()
        isSetStg = False
        for section in sections:
            prefix = str(section)
            if prefix.startswith('strategy'):
                if isSetStg:
                    raise RuntimeError('策略只能设置一种')
                isSetStg = True
                self.strategy = prefix.split("=")[1]
                if self.strategy == 'pointTimeAndAddPrice':
                    self.pointTimeAndAddPrice['time'] = conf.get(prefix, 'time')
                    self.pointTimeAndAddPrice['add'] = conf.get(prefix, 'add')
                if self.strategy == 'pointDiffPrice':
                    self.pointDiffPrice['pointPrice'] = conf.get(prefix, 'pointPrice')
                    self.pointDiffPrice['diff'] = conf.get(prefix, 'diff')
                if self.strategy == 'pointPrice':
                    self.pointPrice['pointPrice'] = conf.get(prefix, 'pointPrice')
                if self.strategy == 'compose':
                    self.compList = conf.items('strategy=compose')
            if prefix.startswith('baseInfo'):
                self.url = conf.get(prefix,'url')
                self.title = conf.get(prefix,'title')
                self.wait = int(conf.get(prefix,'wait'))
                self.isDebugOn = conf.get(prefix,'isDebugOn')
            if prefix.startswith('position'):
                self.tuple = (int(conf.get(prefix,'x')),int(conf.get(prefix,'y')),int(conf.get(prefix,'w')),int(conf.get(prefix,'h')))
    def enumChildHandler(self,hwnd,title):
        text = str(win32gui.GetWindowText(hwnd))
        if text.startswith(title):
            self.hwnd = hwnd
            offset = win32gui.GetWindowRect(hwnd)
            self.dskX = offset[0]
            self.dskY = offset[1]
    def enumHandler(self,hwnd,title):
        if win32gui.IsWindowVisible(hwnd):
            text = str(win32gui.GetWindowText(hwnd))
            if text.startswith(title):
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, self.tuple[0], self.tuple[1], self.tuple[2], self.tuple[3], win32con.SWP_SHOWWINDOW)
                win32gui.EnumChildWindows(hwnd,self.enumChildHandler,title)
    def open(self, url,title):
        PAMIE(url)
        time.sleep(self.wait)
        win32gui.EnumWindows(self.enumHandler, title)
        self.isOpen = True
    def imgCapture(self,box):
        im = ImageGrab.grab(box).resize((800, 200),Image.ANTIALIAS)
        im.show('verify',None)
        return
    def getImg2Code(self,box):
        im = ImageGrab.grab(box).resize((800, 200),Image.ANTIALIAS)
        textcode = libtesseract.image_to_string(im)
        return textcode
    def countSeconds(self,time1,time2):
        return (int(time1.split(':')[0])-int(time2.split(':')[0]))*3600+(int(time1.split(':')[1])-int(time2.split(':')[1]))*60+(int(time1.split(':')[2])-int(time2.split(':')[2]))
    def translate(self,box):
        newBox = (round(box[0]*(self.dskX/1600)),round(box[1]*(self.dskY/900)),round(box[2]*(self.dskX/1600)),round(box[3]*(self.dskY/900)))
        return newBox
    def startAction(self,actionPrice):
        textBox = (self.tuple[0] + 692+self.dskX, self.tuple[1] + 412+self.dskY)
        self.mouse.mouse_dclick(textBox[0],textBox[1])
        self.mouse.key_input('backspace')
        self.mouse.key_input(actionPrice)
        time.sleep(0.5)
        bidBox = (self.tuple[0] + 792+self.dskX, self.tuple[1] + 412+self.dskY)
        self.mouse.mouse_click(bidBox[0],bidBox[1])
        # time.sleep(1)
        # self.imgCapture(vBox)
        # cfmBox = (cTuple[0] + 712+self.dskX, cTuple[1] + 422+self.dskY)
        # mouse.mouse_click(cfmBox[0],cfmBox[1])
    def dealTimeAndAddPrice(self):
        pointTime = self.pointTimeAndAddPrice['time']
        pointPrice = self.pointTimeAndAddPrice['add']
        print('策略设置为指定时间:' + pointTime + ',最低价加上指定价格:' + pointPrice)
        while True:
            try:
                now = self.getImg2Code(self.cBox)
                diff = self.countSeconds(pointTime, now)
                print('主机时间为:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + ',拍牌服务器时间为:' + now + ',距指定时间:' + pointTime + '相差:' + str(diff))
                if diff <= 0:
                    price = int(self.getImg2Code(self.pBox))
                    self.startAction(str(price + int(pointPrice)))
                    break
                time.sleep(0.5)
            except BaseException:
                continue

    def dealPointDiffPrice(self):
        pointPrice = self.pointDiffPrice['pointPrice']
        diff = self.pointDiffPrice['diff']
        interval = diff.split(',')
        min = interval[0]
        max = interval[1]
        print('策略设置为最低价和设置价格:' + pointPrice + ',相差区间为:[' + diff + ']时出价')
        self.startAction(pointPrice)
        textBox = (self.tuple[0] + 542 + self.dskX,self.tuple[1] + 497+self.dskY)
        while True:
            price = int(self.getImg2Code(self.pBox))
            actDiff = int(pointPrice) - price
            print('当前最低价:'+str(price)+',和设置的最低价:'+pointPrice+'相差'+str(actDiff))
            if actDiff >= int(min) and actDiff <= int(max):
                mouse = mouseclick()
                mouse.mouse_click(textBox[0],textBox[1])
                break
            time.sleep(0.5)
    def dealPointPrice(self):
        pointPrice = self.pointPrice['pointPrice']
        print('策略设置为最低价加300大于等固定金额' + pointPrice + '时出价')
        self.startAction(pointPrice)
        textBox = (self.tuple[0] + 542 + self.dskX,self.tuple[1] + 497+self.dskY)
        while True:
            price = int(self.getImg2Code(self.pBox))
            actDiff = int(pointPrice) - price
            print('当前最低价:'+str(price)+',和设置的最低价:'+pointPrice+'相差'+str(actDiff))
            if actDiff <= 300:
                mouse = mouseclick()
                mouse.mouse_click(textBox[0],textBox[1])
                break
            time.sleep(0.5)
    def dealComp(self):
        while len(self.compList)>0:
            tuple = self.compList.pop(0)
            if tuple[0].startswith('stra'):
                if tuple[1] == 'pointPrice':
                    # 需要获取其后一个元素
                    temp = self.compList.pop(0)
                    self.pointPrice[temp[0]] = temp[1]
                    self.dealPointPrice()
                if tuple[1] == 'pointTimeAndAddPrice':
                    # 需要获取其后两个元素
                    temp = self.compList.pop(0)
                    self.pointTimeAndAddPrice[temp[0]] = temp[1]
                    temp = self.compList.pop(0)
                    self.pointTimeAndAddPrice[temp[0]] = temp[1]
                    self.dealTimeAndAddPrice()
    def executeStrategy(self):
        self.parseConfig()
        if self.isOpen == False:
            self.open(self.url, self.title)
        time.sleep(2)
        cx = self.tuple[0] + 142 + self.dskX
        cy = self.tuple[1] + 397 + self.dskY
        self.cBox = (cx, cy, cx + 70, cy + 15)
        if self.isDebugOn == 'on':
            self.imgCapture(self.cBox)

        px = self.tuple[0] + 169 + self.dskX
        py = self.tuple[1] + 412 + self.dskY
        self.pBox = (px, py, px + 53, py + 17)
        if self.isDebugOn == 'on':
            self.imgCapture(self.pBox)

        vx = self.tuple[0] + 472 + self.dskX
        vy = self.tuple[1] + 392 + self.dskY
        self.vBox = (vx, vy, vx + 190, vy + 90)
        if self.isDebugOn == 'on':
            self.imgCapture(self.vBox)

        # 策略1：设置固定金额，最低价加300大于等于该固定金额时出价
        if self.strategy == 'pointPrice':
            self.dealPointPrice()
        # 策略2：指定时间在最低价基础上增加指定金额出价
        elif self.strategy == 'pointTimeAndAddPrice':
            self.dealTimeAndAddPrice()
        # 策略3：设置固定金额，和最低价在指定范围内，则出价
        elif self.strategy == 'pointDiffPrice':
            self.dealPointDiffPrice()
        # 组合策略
        elif self.strategy == 'compose':
            self.dealComp()