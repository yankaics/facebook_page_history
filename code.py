#-*-coding:utf-8-*-
'''
Created on 2014年12月18日

@author: yx
'''
import re
import time
from user_msg_thread import user_msg
from save_post import fb_post_share
from _fb_ import facebook_graph
 

#from createstr import create_string
                
if __name__ == '__main__':
    import threading
    import Queue
    import datetime
    queue = Queue.Queue()
    queueLock = threading.Lock()
    starttime = datetime.datetime.now()
    user_list = [ 
        {'user_name':'cbmosmob@hotmail.com','password':'zkv43569','uid':'100008695960267','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},       
        {'user_name':'momcaxoc@hotmail.com','password':'rum405','uid':'100008674180639','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},
        {'user_name':'nkofgsle685756@163.com','password':'blueshit','uid':'100009482529891','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},
        {'user_name':'jaymajme@hotmail.com','password':'vtlr1781','uid':'100008735853208','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUW3F6xt2UnwPzUaqwFUgx-y28rxuEjzUyVWxeUlxiex2Ey3uiuummdxCVUKmFAdxq5u78'},
        {'user_name':'rluundxu+001@gmail.com','password':'blueshit','uid':'100008304904369','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},
        {'user_name':'blueshitshit@gmail.com','password':'blueshit','uid':'100008265490891','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},
        {'user_name':'heiheiyouok@gmail.com','password':'blueapple','uid':'100008105866583','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'},
        {'user_name':'oqlaa800@163.com','password':'blueshit','uid':'100009493089178','dyn':'7AmajEzUGBym5Q9UoHaEWC5ECiHwKyWgS8DCqrWo8popyUWdwIhEngK5UcU-2CEau48vEwy6UnG4U-8KuEjK5okzEgG8wTADDBBzopKubBGp3omxnxO'}, 
        ]
    get_list = [
        #'8429246183','8245623462','122177661170978','39581755672','127810744027768','16307558831','13652355666','52150999700','152083869857','6281559092'
        #'92304305160',#willsmith
        #'6815841748',#barackobama
        #'29534858696',#TheSimpsons
        #'23497828950',#natgeo
        #'229899403738458',#CallofDuty
        #'68471055646',#GreysAnatomy
        #'156794164312',#harrypottermovie
        #'18128947058',#kungfupanda
        #'15704546335',#FoxNews
        #'161564697227628',#Snoopy
        #'10150145806225128',#https://www.facebook.com/llchu
        #'46251501064',#https://www.facebook.com/tsaiingwen
	    '889307941125736',#https://www.facebook.com/hillaryclinton/
        '153080620724',#https://www.facebook.com/DonaldTrump
        ]
    for i in user_list:
        fb = facebook_graph()
        fb.login(i['user_name'],i['password'])
        fb.getaccess_token()
        fb.uid = i['uid']
        fb.dyn = i['dyn']
        i['fb'] = fb
    jobs = []
    produce = user_msg(user_list[0]['fb'],get_list[0],queue,queueLock)
    produce.start()
    jobs.append(produce)
    j = 1
    for j in range(1,len(user_list)):
        costom = fb_post_share(queue,user_list[j]['fb'],queueLock)
        costom.start()
        jobs.append(costom)
    for pj in jobs:
        pj.join() 
    lasttime = datetime.datetime.now()
    print lasttime-starttime


    '''
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
        starttime = datetime.datetime.now()
        user_list = ['6281559092','122177661170978','39581755672','127810744027768','16307558831','13652355666','52150999700','8245623462','152083869857','8429246183']
        for i in user_list:
            uid = '100008105866583'
            fb = facebook_graph()
            fb.login("heiheiyouok@gmail.com","blueapple")
            fb.getaccess_token()
            fbsql = fb_mysql()
            act = fb.access_token
            cookies = fb.cookies
            fb.uid = uid
            usr_id = i
            (dictmsg,usr_name) = get_user_msg(fb,fbsql,usr_id)
            threads = []
            for i in dictmsg:
                if (datetime.datetime.strptime(i['created_time'],'%Y-%m-%d %H:%M:%S')<(datetime.datetime.now()-datetime.timedelta(days=5))):
                    threadx = fb_post_comment(cookies,i,uid,usr_name)
                    threadx.start()
                    threads.append(threadx)
                else:
                    threadx = fb_post_sharelike(cookies,i,uid,usr_name)
                    threadx.start()
                    threads.append(threadx)
                if threading.activeCount()>10:
                    for t in threads:
                        t.join()
            for t in threads:
                t.join()
        print "done!!! get onece sourse!"
        lasttime = datetime.datetime.now()
        print lasttime-starttime
    '''
