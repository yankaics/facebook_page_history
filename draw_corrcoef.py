#-*-coding:utf-8-*-
'''
Created on 2015年5月27日

@author: yx
'''
from __future__ import division

def rmse(predictions, targets):
    import numpy as np 
    return np.sqrt(((predictions.getA1() - targets.getA1()) ** 2).mean())

def draw_corre(xdata,ydata,xlabelstr='',ylabelstr='',titlestr='',testdata=None,testdatax = None,testdatay = None,notshow = None):
    import numpy as np
    from matplotlib.pyplot import *
    xarr = []
    for i in xdata:
        xarr.append([1.0,i])
    xMat = np.mat(xarr)
    yMat = np.mat(ydata).T
    xTx = xMat.T*xMat
    if np.linalg.det(xTx) == 0.0 :
        print 'xTx 矩阵的逆无！！'
        return
    ws = xTx.I * (xMat.T*yMat)
    xCopy = xMat.copy()
    xCopy.sort(0)
    yHatcopy = xCopy*ws
    if testdata != None or testdatax != None:
        testy = []
        wst = ws.getA1()
        if testdata:
            for i in testdata.keys():
                testy.append(wst[0]+wst[1]*i)
            yHat = np.mat(testdata.values())
        else:
            for i in testdatax:
                testy.append(wst[0]+wst[1]*i)
            yHat = np.mat(testdatay)
        testmaty = np.mat(testy)
        pr = np.corrcoef(testmaty,yHat)[0][1]
        rmsenum = rmse(testmaty.T,yHat)
        print '皮尔孙相关系数：'+str(pr)
        print 'rmse:'+str(rmsenum)
    if not notshow:
        xlabel(xlabelstr)
        ylabel(ylabelstr)
        title(titlestr) 
        plot(xdata,ydata,'r*')
        if testdata:
            plot(testdata.keys(),testdata.values(),'ko')
        if testdatax != None:
            plot(testdatax,testdatay,'ko')
        plot(xCopy[:,1],yHatcopy)
        show() 
    return (pr,rmsenum)
