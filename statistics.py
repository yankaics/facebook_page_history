#-*-coding:utf-8-*-
'''
Created on 2015年4月24日

@author: yx
'''
from __future__ import division
from _fb_commensql import fb_mysql

def sharedegree(pagelist):
    import numpy as np
    from matplotlib.pyplot import *
    fbsql = fb_mysql()
    sharedict = dict()
    for i in pagelist.keys():
        alllist = fbsql.defind_by_self('select share_fb_msg_new.trend_mid,count(postid) from user_msg,share_fb_msg_new where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromid = \''+i+'\' group by(share_fb_msg_new.trend_mid)')
        for j in alllist:
            if j[1] not in sharedict:
                sharedict[j[1]] = 1
            else:
                sharedict[j[1]] += 1
    fig, (ax0, ax1) = subplots(nrows=2)
    ax0.plot(sharedict.keys(),sharedict.values(),'ro')
    ax1.plot(np.log10(sharedict.keys()),np.log10(sharedict.values()),'o')
    ax0.set_title('share_degree')
    show()
    


def getnumpage(page):
    tempdictshare = {}
    fbsql = fb_mysql()
    alllistshare = fbsql.defind_by_self('select share_fb_msg_new.fromid,toid from user_msg,share_fb_msg_new where share_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromid = \'%s\''%(page))
    for i in alllistshare:
        tempdictshare[i[0]] = None
        tempdictshare[i[1]] = None
    tempdictlike = {}
    alllistlike = fbsql.defind_by_self('select like_fb_msg_new.fromid,toid from user_msg,like_fb_msg_new where like_fb_msg_new.trend_mid = user_msg.msgid and user_msg.fromid = \'%s\''%(page))
    for i in alllistlike:
        tempdictlike[i[0]] = None
        tempdictlike[i[1]] = None
    return [len(tempdictshare),len(tempdictlike)]

if __name__ == '__main__':
    pagelist = {
        '8429246183':'history',
        '8245623462':'nba',
        '92304305160':'willsmith',
        '6815841748':'barackobama',
        '29534858696':'TheSimpsons',
        '23497828950':'natgeo',
        '229899403738458':'CallofDuty',
        '68471055646':'GreysAnatomy'
        }
    '''
    for i in pagelist.keys():
        result = getnumpage(i)
        print pagelist[i] + ':' + str(result[0]) + ',' + str(result[1])
    '''
    sharedegree(pagelist)
