#-*-coding:utf-8-*-
'''
created on 2015-01-03

@author: yx

to get fb_post_share save in mysql
thread class
'''
import threading
from _fb_commensql import fb_mysql
from _fb_ import facebook_graph
import multiprocessing

class fb_post_comment(threading.Thread):
    def __init__(self,cookies,dictt,uid,usr_name,dyn):
        threading.Thread.__init__(self)
        self.fbsql = fb_mysql()
        self.fb = facebook_graph()
        self.fb.uid = uid
        self.fb.cookies = cookies
        self.dyn = dyn
        self.dictm = dictt
        self.dictm['from_name'] = usr_name
        self.usr_name = usr_name
    def run(self):
        from trend_topic import get_comments
        get_comments(self.fb,self.fbsql,self.dictm)
        print "get "+self.usr_name+self.dictm['msgid']+" comments--"+str(self.fbsql.show_result(self.dictm['msgid'],'comments'))
        self.fbsql.close_db()

class fb_post_share(threading.Thread):
    def __init__(self,queue,fb,lockname):
        threading.Thread.__init__(self)
        self.fbsql = fb_mysql()
        self.fb = fb
        self.lock = lockname
        self.queue = queue
    def run(self):
        from trend_topic import get_share_post
        from trend_topic import get_like
        import time
        while(1):
            self.lock.acquire()
            if not self.queue.empty():
                dictm = self.queue.get()
                self.lock.release()
                print "get "+dictm['msgid']
                get_share_post(self.fb,dictm['msgid'],dictm['fromid'],dictm['from_name'],self.fbsql,dictm['msgid'])
                get_like(self.fb,dictm['msgid'],dictm['fromid'],dictm['from_name'],self.fbsql,dictm['msgid'])
                print self.fb.uid+" get "+dictm['from_name']+dictm['msgid']+" sharepost--"+str(self.fbsql.show_result(dictm['msgid'],'share')) 
            else:
                self.lock.release()
                time.sleep(1)
        self.fbsql.close_db()
        
class fb_post_like(threading.Thread):
    def __init__(self,cookies,dictt,uid,usr_name,dyn):
        threading.Thread.__init__(self)
        self.fbsql = fb_mysql()
        self.fb = facebook_graph()
        self.fb.uid = uid
        self.fb.cookies = cookies
        self.dyn = dyn
        self.dictm = dictt
        self.dictm['from_name'] = usr_name
        self.usr_name = usr_name
    def run(self):
        from trend_topic import get_share_post
        from trend_topic import get_like
        print "get "+self.dictm['msgid']
        get_like(self.fb,self.dictm['msgid'],self.dictm['fromid'],self.dictm['from_name'],self.fbsql,self.dictm['msgid'])
        print "get "+self.usr_name+self.dictm['msgid']+" like--"+str(self.fbsql.show_result(self.dictm['msgid'],'like'))
        self.fbsql.close_db()


class fb_process(multiprocessing.Process):
    def __init__(self,u_info,userid):
        multiprocessing.Process.__init__(self)
        self.fb = facebook_graph()
        self.fb.login(u_info['user_name'],u_info['password'])
        self.fb.getaccess_token()
        self.fbsql = fb_mysql()
        self.act = self.fb.access_token
        self.dyn = u_info['dyn']
        self.uid = u_info['uid']
        self.cookies = self.fb.cookies
        self.fb.uid = u_info['uid']
        self.fb.dyn = u_info['dyn']
        self.usr_id = userid


    def run(self):
        import datetime
        from trend_topic import get_user_msg
        (dictmsg,usr_name) = get_user_msg(self.fb,self.fbsql,self.usr_id,7)
        threads = []
        for i in dictmsg:
            if (datetime.datetime.strptime(i['created_time'],'%Y-%m-%d %H:%M:%S')<(datetime.datetime.now()-datetime.timedelta(days=5))):
                threadx = fb_post_comment(self.cookies,i,self.uid,usr_name,self.dyn)
                threadx.start()
                threads.append(threadx)
            else:
                threadx = fb_post_share(self.cookies,i,self.uid,usr_name,self.dyn)
                threadx.start()
                threads.append(threadx)
            if threading.activeCount()>2:
                for t in threads:
                    t.join()
        for t in threads:
            t.join()

class fb_process_like(multiprocessing.Process):
    def __init__(self,u_info,userid):
        multiprocessing.Process.__init__(self)
        self.fb = facebook_graph()
        self.fb.login(u_info['user_name'],u_info['password'])
        self.fb.getaccess_token()
        self.fbsql = fb_mysql()
        self.act = self.fb.access_token
        self.dyn = u_info['dyn']
        self.uid = u_info['uid']
        self.cookies = self.fb.cookies
        self.fb.uid = u_info['uid']
        self.fb.dyn = u_info['dyn']
        self.usr_id = userid


    def run(self):
        import datetime
        from trend_topic import get_user_msg
        (dictmsg,usr_name) = get_user_msg(self.fb,self.fbsql,self.usr_id,5)
        threads = []
        for i in dictmsg:
            threadx = fb_post_like(self.cookies,i,self.uid,usr_name,self.dyn)
            threadx.start()
            threads.append(threadx)
            if threading.activeCount()>2:
                for t in threads:
                    t.join()
        for t in threads:
            t.join()


        
        


