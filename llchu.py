#-*-coding:utf-8-*-
'''
Created on 2016年1月22日

@author: yx
'''

from __future__ import division
from _fb_commensql import fb_mysql

def standRegres_share(page_name,hotnum,timeline,percent = '',notshow = None):
    from fan import sharefan
    from fan import likesum_nothotfan
    from numpy import *
    #loaddata
    dataMat = []
    labelMat = []
    (hotfan,onehoursdict,msgdict) = sharefan(page_name=page_name,hotfannum=hotnum,hours=timeline,percent=percent,justgetdata=True)
    id2num = dict()
    lendatanum = 0
    for i in onehoursdict:
        if onehoursdict[i] and msgdict[i]:
            id2num[i] = lendatanum
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
    xMat = mat(dataMat); yMat = mat(labelMat).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print '没有解'
        return
    ws = xTx.I * (xMat.T*yMat)
    ws = ws.getA1()
    print ws
    while(1):
        test_id = raw_input('please input id:')
        if test_id == 'q':
            break
        print xMat[id2num[test_id]]
        tempx = dataMat[id2num[test_id]]
        print tempx
        testresult = 10**(ws[0]*tempx[0] + ws[1]*tempx[1] + ws[2])
        print '预测结果:' + str(testresult)
        print '真实结果:' + str(msgdict[test_id][0])

def change_draw_fan(page_name,hotfannum,hours):
    import datetime
    import numpy as np
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    begin_time = datetime.datetime(2015, 12, 15)
    hotfan = list()
    for k in range(40):
        hotfan.append(0)
        timenow_time = (begin_time + datetime.timedelta(days=k)).strftime("%Y-%m-%d %H:%M:%S")
        print timenow_time
        alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\' and user_msg.created_time<\''+timenow_time+'\'')
        dicttoid = {}
        msgdict = {}
        onehoursdict = {}
        for i in alllist:
            if i[0] not in msgdict:
                msgdict[i[0]] = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
                temptime = msgdict[i[0]][1]+datetime.timedelta(hours=hours)
                strtime = temptime.strftime("%Y-%m-%d %H:%M:%S")
                onehoursdict[i[0]] = fbsql.defind_by_self('select toid from share_fb_msg_new where trend_mid=\'%s\' and created_time<\'%s\''%(i[0],strtime))
                if not onehoursdict[i[0]]:
                    temptime = msgdict[i[0]][1]+datetime.timedelta(hours=hours+3)
                    strtime = temptime.strftime("%Y-%m-%d %H:%M:%S")
                    onehoursdict[i[0]] = fbsql.defind_by_self('select toid from share_fb_msg_new where trend_mid=\'%s\' and created_time<\'%s\''%(i[0],strtime))
            if i[1] in dicttoid:
                dicttoid[i[1]] += 1
            else:
                dicttoid[i[1]] = 1  
        for j in dicttoid.keys():
            if dicttoid[j]>=hotfannum:
                hotfan[k] += 1
        hotfan[k] = hotfan[k]/len(dicttoid)
        print hotfan[k]
    xlabel('begin at 2015-12-15 each 1 day')
    ylabel('hot_fan_num')
    title('Tsai Ing-wen hotfan percent') 
    #plot(dictavg.keys(),dictavg.values(),'ro')
    plot(range(40), hotfan)
    show()

if __name__ == '__main__':
    #standRegres_share(page_name='朱立倫',hotnum=0.8,timeline=11,percent = '%')
    #standRegres_share(page_name='蔡英文 Tsai Ing-wen',hotnum=0.5,timeline=11,percent = '%')
    #change_draw_fan('朱立倫', 10, 11)
    #change_draw_fan('蔡英文 Tsai Ing-wen', 10, 11)
    standRegres_share(page_name='Donald J. Trump',hotnum=0.8,timeline=11,percent = '%')
    #change_draw_fan('Donald J. Trump', 10, 11)
