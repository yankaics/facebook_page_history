#-*-coding:utf-8-*-
'''
@create at 2014-12-31
2014年最后一天拉～～～

@author:yx

'''

import MySQLdb
'''
use renrengrap db to store fb data
'''
class fb_mysql():
    def __init__(self):
        try:
            self.conn = MySQLdb.Connect(host = 'localhost',user = 'root', passwd = '111111', db = 'renrengrap', port = 3306)
            self.cur = self.conn.cursor()
            self.conn.set_character_set('utf8')
            self.cur.execute('SET NAMES utf8;')
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0],e.args[1])
    def close_db(self):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0],e.args[1])

    def defind_by_self(self,mysqlstr):
        try:
            result = self.cur.execute(mysqlstr)
            if result !=0:
                return self.cur.fetchall()
            else:
                return None
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s"%(e.args[0],e.args[1])
             

    def insert_trending(self,data):
        if len(data)!=3:
            print str(data)+" too short!!"
            return None
        try:
            result = self.cur.execute('select * from trending where trqid =\'%s\';'%(data['trqid']))
            if result == 0:
                data['trqname'] = self.do_with_string(data['trqname'])
                self.cur.execute("insert into trending(trqid,trqname,trqurl) values(\"%s\",\"%s\",\"%s\");"%(data['trqid'],data['trqname'],data['trqurl']))
                self.conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0],e.args[1])

    def insert_fb_msg(self,data):
        import datetime
        nowtime = (datetime.datetime.now()-datetime.timedelta(hours=16)).strftime("%y-%m-%d %H:%M:%S")
        try:
            result = self.cur.execute("select update_time from user_msg where msgid = '%s';"%(data['msgid']))
            if result == 0 and data['shares_count']:
                data['message'] = self.do_with_string(data['message'])
                data['name'] = self.do_with_string(data['name'])
                print "msg==="+str(data)
                self.cur.execute("insert into user_msg(msgid,name,message,fromid,fromname,created_time,update_time,share_count,like_count) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d);"%(data['msgid'],data['name'],data['message'],data['fromid'],data['fromname'],data['created_time'],nowtime,data['shares_count'],data['like_count']))
                self.conn.commit()
                return None
            else:
                oldtime = self.cur.fetchone()[0]
                self.cur.execute("update trending_msg set update_time = '%s' where msgid = '%s';"%(nowtime,data['msgid']))
                self.conn.commit()
                return oldtime
        except Exception,e:
            print str(e)
            print date
    def insert_fb_share(self,data):
        try:
            #print "share==" + str(data)
            data['from_name'] = self.do_with_string(data['from_name'])
            data['to_name'] = self.do_with_string(data['to_name'])
            self.cur.execute("insert into share_fb_msg_new values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d) ON DUPLICATE KEY UPDATE fromid = \"%s\",from_name = \"%s\";"%(data['postid'],data['fromid'],data['toid'],data['from_name'],data['to_name'],data['created_time'],data['trend_mid'],data['like_count'],data['share_count'],data['fromid'],data['from_name']))
            self.conn.commit()
        except Exception,e:
            print str(e)
            print data
    
    def get_line_msg(self,time):
        try:
            result = self.cur.execute("select msgid,fromid,fromname,name,message,created_time,update_time from trending_msg where created_time > '%s'"%(time))
            if result !=0:
                return self.cur.fetchall()
            else:
                return None
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s"%(e.args[0],e.args[1])

    def insert_fb_like(self,data):
        import datetime
        nowtime = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        try:
            data['from_naem'] = self.do_with_string(data['from_name'])
            data['to_name'] = self.do_with_string(data['to_name'])
            self.cur.execute("insert into like_fb_msg_new values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\") ON DUPLICATE KEY UPDATE fromid = \"%s\",from_name = \"%s\";"%(data['fromid'],data['toid'],data['from_name'],data['to_name'],nowtime,data['trend_mid'],data['fromid'],data['from_name']))
            self.conn.commit()
        except Exception,e:
            print str(e)
            print data

    def insert_fb_comment(self,data):
        try:
            self.cur.execute("insert into comments_fb_msg_new values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d ,\"%s\") ON DUPLICATE KEY UPDATE fromid = \"%s\",from_name = \"%s\";"%(data['id'],data['fromid'],data['toid'],data['from_name'],data['to_name'],data['created_time'],data['like_count'],data['trend_mid'],data['fromid'],data['from_name']))
            self.conn.commit()
        except MySQLdb.Error,e:
            print "Mysql error %d: %s"%(e.args[0],e.arge[1])
            print data

    '''
    转义引号
    输入：str 需要查看的字符串
    '''
    def do_with_string(self,string):
        import re
        if string:
            return re.sub("\"","\"\"",string)
        else:
            return string
    
    def getidwithout(self):
        iid = dict()
        try:
            self.cur.execute('select distinct(fromid) from comments_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = comments_fb_msg_new.fromid) = 0;')
            comment_from = self.cur.fetchall()
            for i in comment_from:
                iid[i[0]] = None
            self.cur.execute('select distinct(toid) from comments_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = comments_fb_msg_new.toid) = 0;')
            comment_to = self.cur.fetchall()
            for i in comment_to:
                iid[i[0]] = None
            self.cur.execute('select distinct(fromid) from like_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = like_fb_msg_new.fromid) = 0;')
            like_from = self.cur.fetchall()
            for i in like_from:
                iid[i[0]] = None
            self.cur.execute('select distinct(toid) from like_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = like_fb_msg_new.toid) = 0;')
            like_to = self.cur.fetchall()
            for i in like_to:
                iid[i[0]] = None
            self.cur.execute('select distinct(fromid) from share_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = share_fb_msg_new.fromid) = 0;')
            share_from = self.cur.fetchall()
            for i in share_from:
                iid[i[0]] = None
            self.cur.execute('select distinct(toid) from share_fb_msg_new where(select count(1) as num from geted_friend where geted_friend.id = share_fb_msg_new.toid) = 0;')
            share_to = self.cur.fetchall()
            for i in share_to:
                iid[i[0]] = None
            return iid.keys()
        except MySQLdb.Error,e:
            print "MySQL error %d: %s"%(e.args[0],e.args[1])

    def process_item(self, item,idone):
        for i in item:
            try:
                result = self.cur.execute('select * from frd_fb where id_two=\'%s\' and id_one=\'%s\';'%(idone,i))
                if result == 0:    
                    self.cur.execute("insert into frd_fb(id_one,id_two) values(\"%s\",\"%s\");"%(idone,i))
                    self.conn.commit()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0],e.args[1])

    def markfrd(self,idone):
        try:
            self.cur.execute('insert into geted_friend(id) values(\"%s\");'%(idone))
            self.conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s"%(e.args[0],e.args[1])
    def show_result(self,strid,option):
        try:
            result = self.cur.execute('select count(*) from '+ option +'_fb_msg_new where trend_mid='+strid+';')
            if result != 0:
                return self.cur.fetchone()
        except MySQLdb.Error,e:
            print "MySQL error %d: %s"%(e.args[0],e.args[1])




