#-*-coding:utf-8-*-
'''
Created on 2015年5月27日

@author: yx
'''
from __future__ import division

def devide_data(datamat,labelmat):
    import numpy as np
    testx = []
    testy = []
    samplex = []
    sampley = []
    datalen = len(datamat)
    argrmdict = dict()
    arragerdm = np.random.choice(datalen,int(datalen*0.25),replace=False)
    for i in arragerdm:
        argrmdict[i] = None
    for i in range(datalen):
        if i in argrmdict:
            testx.append(datamat[i])
            testy.append(labelmat[i])
        else:
            samplex.append(datamat[i])
            sampley.append(labelmat[i])
    return (samplex,sampley,testx,testy)

def standRegres_share(page_name,hotnum,timeline,percent = '',notshow = None):
    from fan import sharefan
    from fan import likesum_nothotfan
    from numpy import *
    #loaddata
    dataMat = []
    labelMat = []
    (hotfan,onehoursdict,msgdict) = sharefan(page_name=page_name,hotfannum=hotnum,hours=timeline,percent=percent,justgetdata=True)
    lendatanum = 0
    for i in onehoursdict:
        if onehoursdict[i] and msgdict[i]:
            lendatanum += 1
            tempx = 0
            for j in onehoursdict[i]:
                if j[0] in hotfan:
                    tempx += 1
            x = tempx/len(onehoursdict[i])
            if msgdict[i][0]:
                y = msgdict[i][0]
                if x > 0:
                    dataMat.append([log10(x),log10(len(onehoursdict[i])),1.0])
                else:
                    x = 1
                    dataMat.append([log10(x),log10(len(onehoursdict[i])),1.0])
                labelMat.append(log10(y))
    print '总条数：'+str(lendatanum)
    print '总数据：'+str(len(dataMat))
    testx = []
    testy = []
    (dataMat,labelMat,testx,testy) = devide_data(dataMat,labelMat)
    print '训练数据：'+str(len(dataMat))
    print '测试数据：'+str(len(testx))
    xMat = mat(dataMat); yMat = mat(labelMat).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print '没有解'
        return
    ws = xTx.I * (xMat.T*yMat)
    return drawtest(dataMat,labelMat,ws.getA1(),page_name,hotnum,timeline,testx,testy,percent=percent,xlabelinput=['share_hourall','share_hotfan_per'],titleinput='shareall and sharehotfan:share_count',notshow = notshow)

def standRegres_like(page_name,hotnum,timeline,percent = '',notshow = None):
    from fan import sharefan
    from fan import likesum_nothotfan
    from numpy import *
    #loaddata
    dataMat = []
    labelMat = []
    timedict = likesum_nothotfan(page_name=page_name,hotnum=hotnum,timeline=timeline,percent=percent,justgetdata=True)
    lendatanum = 0
    for i in timedict:
        if timedict[i]['all_like_sum']>0:
            lendatanum += 1
            if timedict[i]['like_sum'] <= 0:
                dataMat.append([log10(timedict[i]['all_like_sum']),log10(1),1.0])
            else:
                dataMat.append([log10(timedict[i]['all_like_sum']),log10(timedict[i]['like_sum']),1.0])
            labelMat.append(log10(timedict[i]['share_count']))
    print '总条数：'+str(lendatanum)
    print '总数据：'+str(len(dataMat))
    testx = []
    testy = []
    (dataMat,labelMat,testx,testy) = devide_data(dataMat,labelMat)
    print '训练数据：'+str(len(dataMat))
    print '测试数据：'+str(len(testx))
    xMat = mat(dataMat); yMat = mat(labelMat).T
    xTx = xMat.T*xMat 
    if linalg.det(xTx) == 0.0:
        print '没有解'
        print xTx
        return
    ws = xTx.I * (xMat.T*yMat)
    return drawtest(dataMat,labelMat,ws.getA1(),page_name,hotnum,timeline,testx,testy,percent=percent,xlabelinput=['like_hourall','like_nothotfan'],titleinput='like_all and like_not_hotfan:share_count',notshow = notshow)

def standRegres(page_name,hotnum,timeline,percent = '',notshow = None):
    from fan import sharefan
    from fan import likesum_nothotfan
    from numpy import *
    #loaddata
    dataMat = []
    labelMat = []
    (hotfan,onehoursdict,msgdict) = sharefan(page_name=page_name,hotfannum=hotnum,hours=timeline,percent=percent,justgetdata=True)
    timedict = likesum_nothotfan(page_name=page_name,hotnum=hotnum,timeline=timeline,percent=percent,justgetdata=True)
    lendatanum = 0
    for i in onehoursdict:
        if i in timedict:
            tempx = 0
            #lendatanum += 1
            if not onehoursdict[i]:
                if msgdict[i][0]>50:
                    print str(msgdict[i][0])+msgdict[i][2]+str(msgdict[i][1])+' '+i
                continue
            lendatanum += 1
            for j in hotfan:
                if (j,) in onehoursdict[i]:
                    tempx += 1
            x = tempx/len(onehoursdict[i])
            if msgdict[i][0]:
                if x <=0 :
                    x = 1
                if timedict[i]['like_sum'] <= 0:
                    timedict[i]['like_sum'] = 1
                y = msgdict[i][0]
                dataMat.append([log10(x),log10(timedict[i]['like_sum']),1.0])
                labelMat.append(log10(y))
    #计算w
    print '总条数：'+str(lendatanum)
    print '总数据：'+str(len(dataMat))
    testx = []
    testy = []
    (dataMat,labelMat,testx,testy) = devide_data(dataMat,labelMat)
    print '训练数据：'+str(len(dataMat))
    print '测试数据：'+str(len(testx))
    xMat = mat(dataMat); yMat = mat(labelMat).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print '没有解'
        return
    ws = xTx.I * (xMat.T*yMat)
    return drawtest(dataMat,labelMat,ws.getA1(),page_name,hotnum,timeline,testx,testy,percent=percent,xlabelinput=['sharehotfan','like_not_fan'],titleinput='like_sum_notfan and sharehotfan:share_count',notshow = notshow)
                
def drawtest(dataMat,labelMat,ws,page_name,hotnum,timeline,testx,testy,percent='',xlabelinput='',titleinput='',notshow = None):
    import numpy as np
    from draw_corrcoef import draw_corre
    testdatax = []
    testdatay = []
    dictx = []
    dicty = []
    for i in range(len(dataMat)):
        tempx = dataMat[i]
        x = ws[0]*tempx[0] + ws[1]*tempx[1] + ws[2]
        y = labelMat[i]
        dictx.append(x)
        dicty.append(y)
    for i in range(len(testx)):
        tempx = testx[i]
        x = ws[0]*tempx[0] + ws[1]*tempx[1] + ws[2]
        y = testy[i]
        testdatax.append(x)
        testdatay.append(y) 
    xlabel = str(ws[0])+'*'+xlabelinput[0]+'+'+str(ws[1])+'*'+xlabelinput[1]+'+'+str(ws[2])+' '+str(timeline-8)+'h'
    ylabel = 'share_count'
    title = page_name+' '+titleinput+' time:'+str(timeline-8)+'h fan_defind:'+str(hotnum)+percent+'up'
    return draw_corre(xdata=dictx,ydata=dicty,xlabelstr=xlabel,ylabelstr=ylabel,titlestr=title,testdatax=testdatax,testdatay = testdatay,notshow=notshow)

def drawwise(datax,rmsedatay,prdatay,titlestr):
    import numpy as np
    from matplotlib.pyplot import *
    xlabel('eps')
    ylabel('rss_error')
    title(titlestr) 
    plot(datax,rmsedatay,'r--',label='rmse')
    plot(datax,prdatay,'--',label='R')
    legend = legend(loc='upper right', shadow=True)
    show()
    return

def stagewiseshare(hours):
    datax=[];rmsedatay=[];prdatay=[]
    for i in range(5,500,5):
        esp = i/100
        print esp
        datax.append(esp)
        (rmse,rp) = standRegres_share(page_name='all',hotnum=esp,timeline=hours,percent='%',notshow = True)
        prdatay.append(rp)
        rmsedatay.append(rmse)
    '''
    for i in range(5,10,1):
        esp = i
        print esp
        datax.append(esp)
        (rmse,rp) = standRegres_share(page_name='all',hotnum=esp,timeline=hours,percent='%',notshow = True)
        prdatay.append(rp)
        rmsedatay.append(rmse)
    '''
    return drawwise(datax,rmsedatay,prdatay,'share and sharehotfan in '+str(hours-8))

def stagewiselike(hours):
    datax=[];rmsedatay=[];prdatay=[]
    for i in range(2,10):
        esp = i
        print esp
        datax.append(esp)
        rmse = 0;rp=0;
        for j in range(10):
            (temprmse,temprp) = standRegres_like(page_name='all',hotnum=esp,timeline=hours,percent='',notshow = True)
            rmse += temprmse
            rp += temprp
        rmse = rmse/10
        rp = rp/10
        prdatay.append(rp)
        rmsedatay.append(rmse)
    return drawwise(datax,rmsedatay,prdatay,'share and sharehotfan in '+str(hours-8))

if __name__ == '__main__':
    #stagewiseshare(hours=11)
    stagewiselike(hours=11)
    #standRegres(page_name='all',hotnum=1,timeline=11,percent = '%')
    #standRegres_share(page_name='all',hotnum=0.05,timeline=11,percent = '%')
    #standRegres_like(page_name='all',hotnum=2,timeline=11,percent = '')

