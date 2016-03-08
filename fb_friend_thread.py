#-*-coding:utf-8-*-
'''
create at 2015年3月24日

@author:yuxuan
得到facebook的朋友线程
'''
import threading
from _fb_commensql import fb_mysql
from _fb_ import facebook_graph
class fb_friend(threading.Thread):
    def __init__(self,fb,fid,act):
        threading.Thread.__init__(self)
        self.fid = fid
        self.fbsql = fb_mysql()
        self.fb = fb
    def run(self): 
        item = self.fb.get_usr_friend(self.fid)
        if item:
            self.fbsql.process_item(item.keys(),self.fid)
            print self.fid+' '+str(len(item))
        self.fbsql.markfrd(self.fid)
        self.fbsql.close_db()


