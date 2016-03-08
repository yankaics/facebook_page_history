#-*-coding:utf-8-*-
'''
Created on 2015年4月24日

@author: yx
'''
from __future__ import division
from _fb_commensql import fb_mysql
pagelist = {
        '8429246183':'history',
        '8245623462':'nba',
        '92304305160':'Will Smith',
        '6815841748':'Barack Obama',
        '29534858696':'The Simpsons',
        '23497828950':'National Geographic',
        '229899403738458':'Call of Duty',
        '68471055646':'GreysAnatomy',
        '18128947058':'Kung Fu Panda',
        '156794164312':'Harry Potter'
        }
def fandefind(page_name):
    fbsql = fb_mysql()
    if page_name=='all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
        #alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    dicttoid = {}
    for i in alllist:
        if i[1] in dicttoid:
            dicttoid[i[1]] += 1
        else:
            dicttoid[i[1]] = 1
    dictnum = {}
    peoplenum = len(dicttoid)
    for i in dicttoid.keys():
        if dicttoid[i] in dictnum:
            dictnum[dicttoid[i]] += 1
        else:
            dictnum[dicttoid[i]] = 1
    drawline(dictnum,page_name,peoplenum)

def drawline(dictnum,page_name,peoplenum):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy = {}
    for i in dictnum:
        y = dictnum[i]/peoplenum*100
        dictxy[i] = y
    fig, (ax0, ax1) = subplots(nrows=2)
    ax0.set_xlabel('fan_share_num_log10')
    ax0.set_ylabel('number_log10')
    ax1.set_xlabel('fan_share_num_log10')
    ax1.set_ylabel('fan_share_num_%')
    ax0.set_title(page_name+' fan_difind')
    ax0.plot(np.log10(dictnum.keys()),np.log10(dictnum.values()),'ro')
    ax1.plot(np.log10(dictxy.keys()),dictxy.values(),'ro')
    #plot(dictnum.keys(),dictnum.values(),'ro')
    show()

def seepercent(page_name):
    import datetime
    import numpy as np
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
        #alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    dicttoid = {}
    msgdict = {}
    onehoursdict = {}
    for i in alllist:
        if i[0] not in msgdict:
            msgdict[i[0]] = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
            temptime = msgdict[i[0]][1]+datetime.timedelta(hours=11)
            #temptime = datetime.datetime.strptime(msgdict[i[0]][1],"%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=1)
            strtime = temptime.strftime("%Y-%m-%d %H:%M:%S")
            onehoursdict[i[0]] = fbsql.defind_by_self('select toid from share_fb_msg_new where trend_mid=\'%s\' and created_time<\'%s\''%(i[0],strtime))
    dictxy = dict()
    for i in msgdict:
        if onehoursdict[i]:
            dictxy[len(onehoursdict[i])] = fbsql.defind_by_self('select count(postid) from share_fb_msg_new where trend_mid=\'%s\' group by(trend_mid)'%i)[0]
    for i in dictxy:
        print str(i)+':'+str(dictxy[i])
    xlabel('11_hours get_count')
    ylabel('all_get')
    title(page_name+' 11_hour:all_time') 
    #plot(dictavg.keys(),dictavg.values(),'ro')
    plot(dictxy.keys(),dictxy.values(),'ro')
    show()

def allshare(page_name,hours,justgetdata=None):
    import datetime
    import numpy as np
    from draw_corrcoef import draw_corre
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
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
    dictx = []
    dicty = []
    allcount = 0
    for i in msgdict:
        if onehoursdict[i] and msgdict[i][0]:
            allcount += 1
            dictx.append(len(onehoursdict[i])) 
            dicty.append(msgdict[i][0])
    if justgetdata:
        return (onehoursdict,msgdict)
    testdatax = []
    testdatay = []
    dicttrainx = []
    dicttrainy = []
    argrmdict = dict()
    arragerdm = np.random.choice(len(dictx),int(len(dictx)*0.25),replace=False)
    for i in arragerdm:
        argrmdict[i] = None
    for i in range(len(dictx)):
        if i in argrmdict:
            testdatax.append(dictx[i])
            testdatay.append(dicty[i])
        else:
            dicttrainx.append(dictx[i])
            dicttrainy.append(dicty[i])
    print '总数据：'+str(allcount)
    print '训练数据：'+str(len(dicttrainx))
    print '测试数据：'+str(len(testdatax))
    xlabel = str(hours)+'_hours get_count'
    ylabel = 'share_count'
    title = page_name+' '+str(hours)+'_hour:all_time_true_share_count'
    return draw_corre(xdata=np.log10(dicttrainx),ydata=np.log10(dicttrainy),xlabelstr=xlabel, ylabelstr=ylabel, titlestr=title, testdatax=np.log10(testdatax),testdatay = np.log10(testdatay))
    
def percentfan(hotfannum,dicttoid,percent):
    import operator
    hotfan = {}
    if percent == '%':
        templist = []
        templist = sorted(dicttoid.iteritems(),key = operator.itemgetter(1),reverse=True)
        changepercent = int(len(dicttoid)*hotfannum//100)
        print '前'+str(changepercent)+'人:最少转发-'+str(templist[changepercent][1])+'条'
        for i in range(changepercent):
            hotfan[templist[i][0]] = None
    else:
        for i in dicttoid.keys():
            if dicttoid[i]>=hotfannum:
                hotfan[i] = None
    return hotfan

def sharefan(page_name,hotfannum,hours,percent = '',justgetdata=None,hotnot=None):
    import datetime
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        msgdict = {}
        onehoursdict = {}
        hotfan = []
        for i in pagelist:
            alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
            dicttoid = {}
            for i in alllist:
                if i[0] not in msgdict:
                    msgdict[i[0]] = fbsql.defind_by_self('select share_count,created_time,fromname from user_msg where msgid=\'%s\''%i[0])[0]
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
            hotfan = dict(hotfan,**percentfan(hotfannum,dicttoid,percent))
            
        #alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
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
        hotfan = percentfan(hotfannum,dicttoid,percent)
    if justgetdata:
        return (hotfan,onehoursdict,msgdict)
    return drawhotfun(hotfan,onehoursdict,msgdict,page_name,hotfannum,hours,percent,hotnot)

def drawhotfun(hotfan,onehoursdict,msgdict,page_name,hotfannum,hours,percent,hotnot): 
    import numpy as np
    from draw_corrcoef import draw_corre
    dictx = []
    dicty = []
    for i in onehoursdict.keys():
        tempx = 0
        if onehoursdict[i]:
            if len(onehoursdict[i])<len(hotfan):
                for j in onehoursdict[i]:
                    if j[0] in hotfan:
                        tempx += 1
            else:
                for j in hotfan:
                    if (j,) in onehoursdict[i]:
                        tempx += 1
            if not hotnot:
                x = tempx/len(onehoursdict[i])
            else:
                x = (len(onehoursdict[i])-tempx)/len(onehoursdict[i])
            if msgdict[i][0] and x > 0:
                y = msgdict[i][0]
                dictx.append(x)
                dicty.append(y)
    testdatax = []
    testdatay = []
    dicttrainx = []
    dicttrainy = []
    argrmdict = dict()
    arragerdm = np.random.choice(len(dictx),int(len(dictx)*0.25),replace=False)
    for i in arragerdm:
        argrmdict[i] = None
    for i in range(len(dictx)):
        if i in argrmdict:
            testdatax.append(dictx[i])
            testdatay.append(dicty[i])
        else:
            dicttrainx.append(dictx[i])
            dicttrainy.append(dicty[i])
    print '训练数据：'+str(len(dicttrainx))
    print '测试数据：'+str(len(testdatax))
    xlabel = 'hot_fan_p'
    ylabel = 'share_count'
    title = page_name+' fan_difind:share_'+str(hotfannum)+percent+'up time:'+str(hours-8)+'h'
    return draw_corre(xdata=np.log10(dicttrainx), ydata=np.log10(dicttrainy), xlabelstr=xlabel, ylabelstr=ylabel, titlestr=title, testdatax=np.log10(testdatax), testdatay=np.log10(testdatay))

def sharefan_num(page_name,limitnum,hot_fan_defind,percent=''):
    import datetime
    fbsql = fb_mysql()
    msgdict = {}
    onehoursdict = {}
    hotfan = []
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            dicttoid = {}
            alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
            for i in alllist:
                if i[0] not in msgdict:
                    msgdict[i[0]] = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
                    onehoursdict[i[0]] = fbsql.defind_by_self('select toid from share_fb_msg_new where trend_mid=\'%s\' order by(created_time) limit %s'%(i[0],limitnum))
                if i[1] in dicttoid:
                    dicttoid[i[1]] += 1
                else:
                    dicttoid[i[1]] = 1
            hotfan = dict(percentfan(hot_fan_defind,dicttoid,percent),**hotfan)
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,toid from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
        dicttoid = {}
        for i in alllist:
            if i[0] not in msgdict:
                msgdict[i[0]] = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
                onehoursdict[i[0]] = fbsql.defind_by_self('select toid from share_fb_msg_new where trend_mid=\'%s\' order by(created_time) limit %s'%(i[0],limitnum))
            if i[1] in dicttoid:
                dicttoid[i[1]] += 1
            else:
                dicttoid[i[1]] = 1
        hotfan = percentfan(hot_fan_defind,dicttoid,percent)
    drawhotfun_num(hotfan,onehoursdict,msgdict,page_name,limitnum,str(hot_fan_defind)+percent)

def drawhotfun_num(hotfan,onehoursdict,msgdict,page_name,limitnum,hot_fan_defind): 
    import numpy as np
    from matplotlib.pyplot import *
    dictxy = {}
    dictxyf = {}
    for i in onehoursdict.keys():
        tempx = 0
        if onehoursdict[i]:
            for j in hotfan:
                if (j,) in onehoursdict[i]:
                    tempx += 1
            x = tempx/len(onehoursdict[i])
            if msgdict[i][0]:
                y = msgdict[i][0]
                if x not in dictxy:
                    dictxy[x] = [y]
                    dictxyf[x] = y
                else:
                    dictxy[x].append(y)
                    dictxyf[x] = y
    dictavg = {}
    for i in dictxy:
        print str(i)+':'+str(dictxy[i])
        dictavg[i] = np.mean(dictxy[i])
    xlabel('hot_fan_p')
    ylabel('share_count')
    title(page_name+' fan_difind:share_'+hot_fan_defind+'up limit_num:'+limitnum) 
    #plot(dictavg.keys(),dictavg.values(),'ro')
    plot(np.log10(dictavg.keys()),np.log10(dictavg.values()),'ro')
    show()

def deep_fan_num(page_name,limit_num):
    import numpy as np
    import datetime
    fbsql = fb_mysql()
    sharedict = dict()
    if page_name=='all':
        msglist = []
        for i in pagelist:
            msglist += fbsql.defind_by_self('select share_fb_msg_new.trend_mid, user_msg.share_count from user_msg,share_fb_msg_new where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')  group by(share_fb_msg_new.trend_mid)'%i)
        #msglist = fbsql.defind_by_self('select share_fb_msg_new.trend_mid, user_msg.share_count from user_msg,share_fb_msg_new where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\') group by(share_fb_msg_new.trend_mid)')
    else:
        msglist = fbsql.defind_by_self('select share_fb_msg_new.trend_mid, user_msg.share_count from user_msg,share_fb_msg_new where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname =\'%s\' group by(share_fb_msg_new.trend_mid)'%(page_name))
    for i in msglist:
        templist = fbsql.defind_by_self('select like_count from share_fb_msg_new where trend_mid=\'%s\' order by(created_time) limit %s'%(i[0],limit_num))
        sharedict[i[0]] = {}
        sharedict[i[0]]['share_count'] = i[1]
        sharedict[i[0]]['like_num'] = 0
        for j in templist:
            if j > 0:
                sharedict[i[0]]['like_num'] += 1
    drawlikenum_num(sharedict,page_name,limit_num)

def drawlikenum_num(sharedict,page_name,limit_num):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy={}
    for i in sharedict.keys():
        if sharedict[i]['share_count']:
            print i+':'+str(sharedict[i]['like_num'])+','+str(sharedict[i]['share_count'])
            x = sharedict[i]['like_num']
            dictxy[x] = sharedict[i]['share_count']
    xlabel('like_num')
    ylabel('share_count')
    title(page_name+' like_num-share_count limit_count:'+limit_num) 
    #plot(dictxy.keys(),dictxy.values(),'ro')
    plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    show()

def deep_fan(page_name,strchoose,strgetdata = None):
    import numpy as np
    import datetime
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
        #alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    timedict = dict()
    for i in alllist:
        if i[0] not in timedict:
            tempdict = {}
            tempdetail = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
            tempdict['share_count'] = tempdetail[0]
            tempdict['created_time'] = tempdetail[1]
            tempdict['line_time']=tempdict['created_time']+datetime.timedelta(hours=11)
            #tempdict['share'] = dict()
            tempdict['like_num'] = 0
            tempdict['like_max'] = 0
            tempdict['all_num'] = 0
            tempdict['like_sum'] = 0
            if not tempdict['share_count']:
                continue
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                #tempdict['share'][i[1]] = [i[2]]
                tempdict['all_num'] = 1
                if i[4] >0:
                    tempdict['like_num']+=1
                    tempdict['like_sum']+=i[4]
                    if i[4]>tempdict['like_max']:
                        tempdict['like_max'] = i[4]
            timedict[i[0]] = tempdict
        else:
            tempdict = timedict[i[0]]
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                tempdict['all_num'] += 1
                if i[4] >0:
                    tempdict['like_num']+=1
                    tempdict['like_sum']+=i[4]
                    if i[4]>tempdict['like_max']:
                        tempdict['like_max'] = i[4]
    if strchoose == 'num':
        drawlikenum(timedict,page_name,strgetdata)
    elif strchoose == 'sum':
        drawlikesum(timedict,page_name,strgetdata)
    else:
        drawlikedefind(timedict,page_name,strgetdata)
        

def drawlikenum(sharedict,page_name,strgetdata):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy={}
    for i in sharedict.keys():
        print i+':'+str(sharedict[i]['like_num'])+','+str(sharedict[i]['like_max'])
        if sharedict[i]['all_num'] > 0:
            #x = sharedict[i]['like_num']/sharedict[i]['all_num']
            x = sharedict[i]['like_num']
            dictxy[x] = sharedict[i]['share_count']
    if strgetdata:
        return dictxy
    xlabel('like_num 11h')
    ylabel('share_count')
    title(page_name+' like_per:share_count time:11h') 
    #plot(dictxy.keys(),dictxy.values(),'ro')
    plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    show()

def drawlikedeep(sharedict,page_name,strgetdata):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy={}
    for i in sharedict.keys():
        print i+':'+str(sharedict[i]['like_num'])+','+str(sharedict[i]['like_max'])
        x = sharedict[i]['like_max']
        dictxy[x] = sharedict[i]['share_count']
    if strgetdata:
        return dictxy
    xlabel('like_max 11h')
    ylabel('share_count')
    title(page_name+' like_max:share_count time:11h') 
    #plot(dictxy.keys(),dictxy.values(),'ro')
    plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    show()

def drawlikesum(sharedict,page_name,strgetdata):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy={}
    for i in sharedict.keys():
        print i+':'+str(sharedict[i]['like_num'])+','+str(sharedict[i]['like_max'])
        if sharedict[i]['all_num'] > 0:
            #x = sharedict[i]['like_sum']/sharedict[i]['all_num']
            x = sharedict[i]['like_sum']
            dictxy[x] = sharedict[i]['share_count']
    if strgetdata:
        return dictxy
    xlabel('like_sum/all_num 11h')
    ylabel('share_count')
    title(page_name+' like_expectation:share_count time:11h') 
    #plot(dictxy.keys(),dictxy.values(),'ro')
    plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    show()

def likesum_nothotfan(page_name,hotnum,timeline,percent = '',justgetdata=None):
    import numpy as np
    import datetime
    from draw_corrcoef import draw_corre
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        hotfan = []
        for i in pagelist:
            eachlist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
            alllist += eachlist
            dicttoid = {}
            for j in eachlist:
                if j[2] in dicttoid:
                    dicttoid[j[2]] += 1
                else:
                    dicttoid[j[2]] = 1
            hotfan = dict(hotfan,**percentfan(hotnum,dicttoid,percent))
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
        dicttoid = {}
        for i in alllist:
            if i[2] in dicttoid:
                dicttoid[i[2]] += 1
            else:
                dicttoid[i[2]] = 1
        hotfan = percentfan(hotnum,dicttoid,percent)
    timedict = dict()
    for i in alllist:
        if i[0] not in timedict:
            tempdict = {}
            tempdetail = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
            tempdict['share_count'] = tempdetail[0]
            tempdict['created_time'] = tempdetail[1]
            tempdict['line_time']=tempdict['created_time']+datetime.timedelta(hours=timeline)
            tempdict['all_num'] = 0
            tempdict['like_sum'] = 0
            tempdict['all_like_sum'] = 0
            if not tempdict['share_count']:
                continue
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                tempdict['all_num'] = 1
                if i[4] >0:
                    if i[2] not in hotfan:
                        tempdict['like_sum']+=i[4]
                    tempdict['all_like_sum']+=i[4]
            timedict[i[0]] = tempdict
        else:
            tempdict = timedict[i[0]]
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                tempdict['all_num'] += 1
                if i[4] >0: 
                    if i[2] not in hotfan:
                        tempdict['like_sum']+=i[4]
                    tempdict['all_like_sum']+=i[4]
    dictx = []
    dicty = []
    if justgetdata:
        return timedict
    for i in timedict.keys():
        print i+':'+str(timedict[i]['like_sum'])
        if timedict[i]['all_num'] > 0 and timedict[i]['like_sum']>0:
            x = timedict[i]['like_sum']
            dictx.append(x)
            dicty.append(timedict[i]['share_count'])
    testdatax = []
    testdatay = []
    dicttrainx = []
    dicttrainy = []
    argrmdict = dict()
    arragerdm = np.random.choice(len(dictx),int(len(dictx)*0.25),replace=False)
    for i in arragerdm:
        argrmdict[i] = None
    for i in range(len(dictx)):
        if i in argrmdict:
            testdatax.append(dictx[i])
            testdatay.append(dicty[i])
        else:
            dicttrainx.append(dictx[i])
            dicttrainy.append(dicty[i])
    print '训练数据：'+str(len(dicttrainx))
    print '测试数据：'+str(len(testdatax))
    xlabel='like_sum_notfan/all_num '+str(timeline)+'h'
    ylabel='share_count'
    title=page_name+' like_sum_notfan:share_count time:'+str(timeline-8)+'h fan_defind:'+str(hotnum)+percent+'up'
    return draw_corre(xdata=np.log10(dicttrainx), ydata=np.log10(dicttrainy), xlabelstr=xlabel, ylabelstr=ylabel, titlestr=title, testdatax=np.log10(testdatax), testdatay=np.log10(testdatay))

def twolikesum_nothotfan(page_name,hotnum,hotnum2,timeline):
    import numpy as np
    import datetime
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
        #alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.fromid,toid,share_fb_msg_new.created_time,share_fb_msg_new.like_count from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    timedict = dict()
    dicttoid = {}
    for i in alllist:
        if i[2] in dicttoid:
            dicttoid[i[2]] += 1
        else:
            dicttoid[i[2]] = 1
    hotfan = {}
    for i in dicttoid.keys():
        if dicttoid[i] >= hotnum:
            hotfan[i] = None
    hotfan2 = {}
    for i in dicttoid.keys():
        if dicttoid[i] >= hotnum2:
            hotfan2[i] = None
    print 'hotfan > 80:'+str(hotfan2)
    for i in alllist:
        if i[0] not in timedict:
            tempdict = {}
            tempdetail = fbsql.defind_by_self('select share_count,created_time from user_msg where msgid=\'%s\''%i[0])[0]
            tempdict['share_count'] = tempdetail[0]
            tempdict['created_time'] = tempdetail[1]
            tempdict['line_time']=tempdict['created_time']+datetime.timedelta(hours=timeline)
            tempdict['all_num'] = 0
            tempdict['like_sum'] = 0
            tempdict['like_sum2'] = 0
            if not tempdict['share_count']:
                continue
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                tempdict['all_num'] = 1
                if i[4] >0 and (i[2] not in hotfan):
                    tempdict['like_sum']+=i[4]
                if i[4] >0 and (i[2] in hotfan2):
                    tempdict['like_sum2']+=i[4]
            timedict[i[0]] = tempdict
        else:
            tempdict = timedict[i[0]]
            if i[3] < tempdict['line_time'] and i[1]!=i[2]:
                tempdict['all_num'] += 1
                if i[4] >0 and (i[2] not in hotfan):
                    tempdict['like_sum']+=i[4]
                if i[4] >0 and (i[2] in hotfan2):
                    tempdict['like_sum2']+=i[4]
    dictxy={}
    dictxy2={}
    for i in timedict.keys():
        print i+':'+str(timedict[i]['like_sum'])
        if timedict[i]['all_num'] > 0:
            #x = timedict[i]['like_sum']/timedict[i]['all_num']
            x = timedict[i]['like_sum']
            dictxy[x] = timedict[i]['share_count']
            x = timedict[i]['like_sum2']
            dictxy2[x] = timedict[i]['share_count']
    xlabel('like_sum_notfan/all_num '+str(timeline)+'h')
    ylabel('share_count')
    print dictxy2
    title(page_name+' like_sum_notfan:share_count time:'+str(timeline)+'h fan_defind:'+str(hotnum)+'-'+str(hotnum2)+'up') 
    #plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    plot(np.log10(dictxy2.keys()),np.log10(dictxy2.values()),'*')
    show()
                    
    
def drawlikedefind(sharedict,page_name):
    import numpy as np
    from matplotlib.pyplot import *
    dictxy={}
    for i in sharedict.keys():
        print i+':'+str(sharedict[i]['like_num'])+','+str(sharedict[i]['like_max'])
        if sharedict[i]['all_num'] > 0:
            '''
            like_num = (sharedict[i]['like_num']-minlike_num)/like_num_sub
            like_sum = (sharedict[i]['like_sum']-minlike_sum)/like_sum_sub
            '''
            like_sum = sharedict[i]['like_sum']
            like_num = sharedict[i]['like_num']
            like_max = sharedict[i]['like_max']
            x = (like_sum*like_num)
            #x = np.log10(like_sum)*0.8+np.log10(like_num)*0.2
            dictxy[x] = sharedict[i]['share_count']
            #dictxy[x]  = np.log10(sharedict[i]['share_count'])
    xlabel('like_sum*like_num/all_num 11h')
    ylabel('share_count')
    title(page_name+' like_expectation:share_count time:11h') 
    #plot(dictxy.keys(),dictxy.values(),'ro')
    plot(np.log10(dictxy.keys()),np.log10(dictxy.values()),'ro')
    show()

def getBfs(root,sharemap):
    maxlevel = 0 
    if root in sharemap.keys():
        for i in sharemap[root]:
            leveli = 1+getBfs(i,sharemap)
            if leveli > maxlevel:
                maxlevel=leveli
    return maxlevel

def share_time(page_name,hoursdefind):
    import numpy as np
    import datetime
    import numpy as np
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    if page_name == 'all':
        alllist = []
        for i in pagelist:
            alllist += fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.created_time from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromid = \'%s\')'%i)
        #alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.created_time from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and (user_msg.fromname = \'history\' or user_msg.fromname = \'Will Smith\' or user_msg.fromname = \'nba\')')
    else:
        alllist = fbsql.defind_by_self('select user_msg.msgid,share_fb_msg_new.created_time from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    timedict = dict()
    time_count = {}
    for i in range(hoursdefind):
        time_count[i] = 0
    for i in alllist:
        if i[0] not in timedict:
            tempdict = {}
            tempdict['created_time'] = fbsql.defind_by_self('select created_time from user_msg where msgid=\'%s\''%i[0])[0][0]
            tempdict['time_count'] = {}
            minus = i[1] - tempdict['created_time'] 
            temphours = minus.days*24 + minus.seconds//3600
            if temphours < hoursdefind and temphours > 0:
                print i[1]
                print tempdict['created_time']
                print temphours
                time_count[temphours] += 1
            timedict[i[0]] = tempdict
        else:
            tempdict = timedict[i[0]]
            minus = i[1] - tempdict['created_time']
            temphours = minus.days*24 + minus.seconds//3600
            if temphours < hoursdefind and temphours > 0:
                time_count[temphours] += 1 
    dictxy={}
    msgnum = len(timedict)
    for i in time_count.keys():
        print str(i)+':'+str(time_count[i])
        y = time_count[i]/msgnum
        dictxy[i] = y
    xlabel('each_hours')
    ylabel('avg_share')
    title(page_name+'avg share num of each time') 
    plot(dictxy.keys(),dictxy.values(),'ro')
    show()      

def post_time(page_name,choose = 'page'):
    import datetime
    import numpy as np
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    basictime = datetime.datetime.strptime('00:00:00','%H:%M:%S')
    if choose == 'page':
        if page_name == 'all':
            alllist = []
            for i in pagelist:
                alllist += fbsql.defind_by_self('select created_time from user_msg where fromid = \'%s\''%i)
        else:
            alllist = fbsql.defind_by_self('select created_time from user_msg where fromname=\''+page_name+'\'')
    else:
        if page_name == 'all':
            alllist = []
            for i in pagelist:
                alllist += fbsql.defind_by_self('select share_fb_msg_new.created_time from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromid = \'%s\''%i)
        else:
            alllist = fbsql.defind_by_self('select share_fb_msg_new.created_time from share_fb_msg_new,user_msg where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromname=\''+page_name+'\'')
    time_count = {}
    for i in range(48):
        time_count[i*0.5] = 0
    for i in alllist:
        if i[0]:
            minus = i[0] - basictime
            if choose == 'page':
                time_count[(minus.seconds//1800)*0.5] += 1
            else:
                temp8 = ((minus.seconds//1800)+32)%48
                time_count[temp8*0.5] += 1
    xx = []
    yy = []
    for i in range(48):
        xx.append(i*0.5)
        yy.append(time_count[i*0.5])
    bar(time_count.keys(),time_count.values(),width=0.5,align = 'edge',color='green')
    plot(xx,yy, 'r--')
    xlabel('each 0.5h')
    if choose == 'page':
        ylabel('page post count')
        title(page_name+' page post count per 0.5h')
    else:
        ylabel('user post count')
        title(page_name+' user post count per 0.5h')
    show()    

if __name__ == '__main__':
    #fandefind('all')
    sharefan('all',hotfannum=0.05,hours=11,percent = '%',hotnot = None)
    #sharefan_num('all',limitnum='100',hot_fan_defind=0.03,percent = '%')
    #deep_fan_num('all',limit_num='100')
    #seepercent('all')
    #deep_fan('all',strchoose='num')
    #likesum_nothotfan('all',hotnum=2,timeline=11,percent = '')
    #twolikesum_nothotfan(page_name='all',hotnum=2,hotnum2=20,timeline=11)
    #share_time('all',360)
    #post_time('all','user')
    #allshare('all')

