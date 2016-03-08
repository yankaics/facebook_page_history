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
    from save_post import fb_post_comment
    from save_post import fb_post_sharelike
    from _fb_commensql import fb_mysql
    import threading
    from fb_friend_thread import fb_friend
    from trend_topic import get_user_msg
    while(1):
        uid = '100008105866583'
        fb = facebook_graph()
        fb.login("heiheiyouok@gmail.com","blueapple")
        fb.getaccess_token()
        fbsql = fb_mysql()
        act = fb.access_token
        cookies = fb.cookies
        fb.uid = uid
        usr_id = '326683984410'
        #(dictmsg,usr_name) = get_user_msg(fb,fbsql,usr_id)
	gettime = datetime.datetime.now()+datetime.timedelta(days=-15)
        msglist = fbsql.get_line_msg(gettime.strftime("%y-%m-%d %H:%M:%S"))
        threads = []
        for i in msglist:
            print i
            msgtemp = dict()
            msgtemp['msgid'] = i[0]
            msgtemp['fromid'] = i[1]
            msgtemp['from_name'] = i[2]
            msgtemp['name'] = i[3]
            msgtemp['message'] = i[4]
            msgtemp['created_time'] = i[5]
            msgtemp['fromname'] = i[2]
            fbsql.insert_fb_msg(msgtemp)
            threadx = fb_post_sharelike(cookies,msgtemp,uid,i[2])
            threadx.start()
            threads.append(threadx)
            if threading.activeCount()>4:
                for t in threads:
                    t.join()
        for t in threads:
            t.join()
        print "done!!! get onece sourse!"
