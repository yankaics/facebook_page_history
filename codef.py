#-*-coding:utf-8-*-
'''
Created on 2014年12月18日

@author: yx
'''
import re
import time
#from createstr import create_string
                
if __name__ == '__main__':
    import sys
    import datetime
    from _fb_ import facebook_graph
    from trend_topic import get_trending
    from trend_topic import get_share_post
    from trend_topic import getmsgsend
    import datetime
    import time
    from _fb_commensql import fb_mysql
    import threading
    from fb_friend_thread import fb_friend
    while(1):
        uid = '100008105866583'
        fb = facebook_graph()
        fb.login("heiheiyouok@gmail.com","blueapple")
        fb.getaccess_token()
        fbsql = fb_mysql()
        act = fb.access_token
        fb.uid = uid
        fbflist = fbsql.getidwithout()
        fbsql.close_db()
        print "should get %d!!"%len(fbflist)
        threads = []
        last_time = time.mktime(datetime.datetime.now().timetuple())
        for i in fbflist:
            threadx = fb_friend(fb,i,act)
            threadx.start()
            threads.append(threadx)
            now_time = time.mktime(datetime.datetime.now().timetuple())
            if (now_time-last_time)/60 > 20:
                print "reflesh access_token!!"
                fb.getaccess_token()
                act = fb.access_token
                last_time = now_time
                time.sleep(600)
            if threading.activeCount()>3:
                for t in threads:
                    t.join()
        for t in threads:
            t.join()
        '''
        fb = facebook_graph()
        fb.login()
        fb.getaccess_token()
        fbsql = fb_mysql()
        get_trending(fb,'facebookpage.txt',fbsql)
        act = fb.access_token
        cookies = fb.cookies
        gettime = (datetime.datetime.now()-datetime.timedelta(hours=16))+datetime.timedelta(days=-1)
        msglist = fbsql.get_line_msg(gettime.strftime("%y-%m-%d %H:%M:%S"))
	print msglist
        print "should get msg:%d" %len(msglist)
        fbsql.close_db()
        threads = []
        last_time = time.mktime(datetime.datetime.now().timetuple())
        for i in msglist:
            print 'get msgid: '+i[0]
            threadx = fb_post_thread(cookies,act,i[0],i[1],i[2])
            threadx.start()
            threads.append(threadx)
            now_time = time.mktime(datetime.datetime.now().timetuple())
            if (now_time-last_time)/60 > 30:
                print "reflesh access_token!!"
                fb.getaccess_token()
                act = fb.access_token
                last_time = now_time
            if threading.activeCount()>10:
                if (now_time-last_time)/60 > 30:
                    print "reflesh access_token!!"
                    fb.getaccess_token()
                    act = fb.access_token
                    last_time = now_time
                for t in threads:
                    t.join()
        for t in threads:
            t.join()
	'''
        print "done!!! get onece sourse!"
