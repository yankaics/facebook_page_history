import threading
from _fb_commensql import fb_mysql
from _fb_ import facebook_graph
import multiprocessing
from log import logw
import datetime
import time

class user_msg(threading.Thread):
    def __init__(self,fb,usr_id,queue,lockname):
        threading.Thread.__init__(self)
        self.fb = fb
        self.usr_id = usr_id
        self.fbsql = fb_mysql()
        self.queue = queue
        self.lock = lockname

    def run(self):
        import re
        import urllib
        import json 
        last_time = time.mktime(datetime.datetime.now().timetuple())
        page = self.fb.get_referense('/v2.3/'+self.usr_id)
        dictusr = json.loads(page)
        url = dictusr['link']
        usr_name = dictusr['username']
        page = self.fb.getnextpage(url,port = '8580') 
        datalist = []
        datamsg = re.findall('\{"feedbacktargets":\[(.*?)\],"comments":',page,re.S)
        page = page.replace('\\','')
        fb_dtsg = re.findall('name="fb_dtsg" value="(.*?)"',page,re.S)[0]
        parmlist = re.findall('"PagePostsSectionPagelet", (.*?), null',page,re.S)
        logw(self.usr_id+str(parmlist))
        for k in range(len(parmlist)):
            if k<0:
                continue
            parmi = parmlist[k]
            parm = json.loads(parmi.decode('ascii'))
            pdata = {'__pc':'EXP1:DEFAULT','__a':'1','__dyn':self.fb.dyn,'__req':'5','__rev':'1674690','__user':self.fb.uid}
            #pdata['data'] = '{"segment_index":'+str(parm['segment_index'])+',"page_index":'+str(parm["page_index"])+',"page":'+str(parm['page'])+',"column":"main","post_section":{"profile_id":'+str(parm['post_section']['profile_id'])+',"start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+',"is_pages_redesign":true},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":false}'.encode('ascii')
            if parm['cursor'] == None:
                parm['cursor'] = 'null'
            pdata['data'] = '{"page":"'+str(parm['page'])+'","column":"'+parm['column']+'","post_section":{"profile_id":"'+str(parm['post_section']['profile_id'])+'","start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+'},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":null,"cursor":"'+parm['cursor']+'"}'.encode('ascii')
            ftentidentifier = re.findall('\{"ftentidentifier":"(\d*?)".*?"outer_object_element_id":"(.*?)"',page,re.S)
            dictftenidentifier = dict()
            for i in ftentidentifier:
                dictftenidentifier[i[0]] = i[1]
                lasttime = None
            if len(datamsg)>0:
                for dm in datamsg:
                    target = json.loads(dm)
                    tempdata = dict()
                    tempdata['msgid'] = target['targetfbid']
                    tempdata['shares_count'] = target['sharecount']
                    tempdata['comments_count'] = target['commentcount']
                    tempdata['like_count'] = target['likecount']
                    if tempdata['msgid'] in dictftenidentifier:
                        (tempdata['created_time'],tempdata['fromid'])=self.getmsgsend(tempdata['msgid'],tempdata['shares_count'],tempdata['like_count'])
                        tempdata['fb_dtsg'] = fb_dtsg
                        tempdata['outerid'] = dictftenidentifier[tempdata['msgid']]
                        tempdata['from_name'] = usr_name
                        if tempdata['created_time']:
                            if datetime.datetime.strptime(tempdata['created_time'],"%Y-%m-%d %H:%M:%S")>datetime.datetime.strptime('2015-12-01 00:00:00',"%Y-%m-%d %H:%M:%S"):
                                self.lock.acquire()
                                self.queue.put(tempdata)
                                self.lock.release()
                            else:
                                return
                            '''
                            outputx = open('msg.txt','a+')
                            outputx.write(str(tempdata)+'\n')
                            outputx.close()
                            '''

            while(True):
                now_time = time.mktime(datetime.datetime.now().timetuple())
                if (now_time-last_time)/60 > 20:
                    print "reflesh access_token!!"
                    self.fb.getaccess_token()
                    last_time = now_time
                page = self.fb.getnextpage('https://www.facebook.com/ajax/pagelet/generic.php/PagePostsSectionPagelet',params = pdata,port = '8580')
                datamsg = re.findall('\{"feedbacktargets":\[(.*?)\],"comments":',page,re.S)
                page = page.replace('\\','')
                tempdict = re.findall('"PagePostsSectionPagelet", (.*?), null',page,re.S)
                ftentidentifier = re.findall('\{"ftentidentifier":"(\d*?)".*?"outer_object_element_id":"(.*?)"',page,re.S)
                dictftenidentifier = dict()
                for i in ftentidentifier:
                    dictftenidentifier[i[0]] = i[1]
                if len(tempdict)==0:
                    break 
                parm = tempdict[0] 
                parm = json.loads(parm.decode('ascii'))
                pdata = {'__pc':'EXP1:DEFAULT','__a':'1','__dyn':self.fb.dyn,'__req':'5','__rev':'1674690','__user':self.fb.uid}
                #pdata['data'] = '{"segment_index":'+str(parm['segment_index'])+',"page_index":'+str(parm["page_index"])+',"page":'+str(parm['page'])+',"column":"main","post_section":{"profile_id":'+str(parm['post_section']['profile_id'])+',"start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+',"is_pages_redesign":true},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":false}'.encode('ascii')
                if parm['cursor'] == None:
                    parm['cursor'] = 'null'
                pdata['data'] = '{"page":"'+str(parm['page'])+'","column":"'+parm['column']+'","post_section":{"profile_id":"'+str(parm['post_section']['profile_id'])+'","start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+'},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":null,"cursor":"'+parm['cursor']+'"}'.encode('ascii')
                if len(datamsg)>0:
                    for dm in datamsg:
                        target = json.loads(dm)
                        tempdata = dict()
                        tempdata['msgid'] = target['targetfbid']
                        tempdata['shares_count'] = target['sharecount']
                        tempdata['comments_count'] = target['commentcount']
                        tempdata['like_count'] = target['likecount']
                        if tempdata['msgid'] in dictftenidentifier:
                            (tempdata['created_time'],tempdata['fromid']) = self.getmsgsend( tempdata['msgid'],tempdata['shares_count'],tempdata['like_count'])
                            fb_dtsg = re.findall('name="fb_dtsg" value="(.*?)"',page,re.S)[0]
                            tempdata['fb_dtsg'] = fb_dtsg
                            tempdata['from_name'] = usr_name
                            tempdata['outerid'] = dictftenidentifier[tempdata['msgid']]
                            if tempdata['created_time']:
                                if datetime.datetime.strptime(tempdata['created_time'],"%Y-%m-%d %H:%M:%S")>datetime.datetime.strptime('2015-12-01 00:00:00',"%Y-%m-%d %H:%M:%S"):
                                    self.lock.acquire()
                                    self.queue.put(tempdata)
                                    self.lock.release()
                                else:
                                    return
            logw(self.usr_id+parmi)
        


    def getmsgsend(self,msg_id,shares_count,like_count):
        import json
        from trend_topic import change_time_type_api
        the_page = self.fb.get_referense('/v2.3/'+msg_id)
        try:
            post_dict = json.loads(the_page)
            if 'error' not in post_dict:
                #print post_dict
                data = {}
                data['msgid'] = post_dict['id']
                data['shares_count'] = shares_count
                data['like_count'] = like_count
                if 'name' in post_dict:
                    data['name'] = post_dict['name']
                else:
                    data['name'] = None
                if 'message' in post_dict:
                    data['message'] = post_dict['message']
                else:
                    data['message'] = None
                if 'from' in post_dict:
                    data['fromid'] = post_dict['from']['id']
                    data['fromname'] = post_dict['from']['name']
                else:
                    data['fromid'] = None
                    data['fromname'] = None
                if 'created_time' in post_dict:
                    data['created_time'] = change_time_type_api(post_dict['created_time'])
                elif 'updated_time' in post_dict:
                    data['created_time'] = change_time_type_api(post_dict['updated_time'])
                else:
                    data['created_time'] = None
                if datetime.datetime.strptime(data['created_time'],"%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime('2015-12-01 00:00:00',"%Y-%m-%d %H:%M:%S"):
                    self.fbsql.insert_fb_msg(data)
                return (data['created_time'],data['fromid'])
            else:
                print msg_id
                print the_page
                return (None,None)
        except Exception,e:
            print str(e)
            #print str(e)+the_page
            return (None,None)



