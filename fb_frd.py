#-*-coding:utf-8-*-
'''
created on 2014年3月10日

@author: yx 

'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import httplib2
import socks
import urllib
import urllib2


class fb_frd():
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type',1)
        profile.set_preference('network.proxy.http','127.0.0.1')
        profile.set_preference('network.proxy.http_port',8580)
        profile.set_preference('network.proxy.ssl','127.0.0.1')
        profile.set_preference('network.proxy.ssl_port',8580)
        profile.update_preferences()
        self.driver = webdriver.Firefox(profile)
        self.cookies = dict()
        self.access_token = ''
        self.host = "https://graph.facebook.com/v2.2/"
        self.headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:34.0) Gecko/20100101 Firefox/34.0"}
        self.h = httplib2.Http('.cache',disable_ssl_certificate_validation = True,timeout = 20,proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,'localhost',8087,proxy_user = 'yuxuanzero@gmail.com', proxy_pass = 'huangzhaoling660703'))
    
    def login(self):
        url = "https://www.facebook.com"
        self.driver.get(url)
        elem = self.driver.find_element_by_id('email')
        elem.send_keys('blueshitshit@gmail.com')
        elem = self.driver.find_element_by_id('pass')
        elem.send_keys('blueshit')
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        html_source = self.driver.page_source
        if "Please re-enter your password" in html_source or "Incorrect Email" in html_source:
            print "password error!!"
            self.driver.close()
            exit()
        else:
            print "login success\n"
        get_cookies = self.driver.get_cookies()
        '''
        for cookie in get_cookies:
            self.cookies[cookie['name']] = cookie['value']
        print self.cookies
        self.headers['Cookie'] = str(self.cookies)
        '''
        self.headers['Cookie'] = ''
        for cookie in get_cookies:
            self.headers['Cookie'] += cookie['name']+'='+cookie['value']+';'
        self.driver.close()


    def requesturl(self,url):
        for i in range(5):
            try:
                self.headers['cache-control'] = 'no-cache'
                print url
                response,content = self.h.request(url,'GET',headers=self.headers,redirections = 20)
                return content
            except Exception,e:
                print str(e)+'----'+'get nextpage:'+url
        return None
        

        '''
        import requests
        for i in range(10):
            try:
                req = requests.get(url,cookies = self.cookies)
                print req.content
                html = req.content
                return html
            except Exception,e:
                print str(e)
        '''

    def getaccess_token(self,string = None):
            import re
            if string:
                self.access_token = string
            else:
                for i in range(10):
                    try:
                        print 'get access_token'
                        content = self.requesturl("https://developers.facebook.com/tools/explorer/145634995501895/permissions?version=v2.2&__asyncDialog="+str(i)+"&__user=100008265490891&__a=1&__dyn=5U463-i3S2e4oK4pomXWo5O12wAxu13w&__req=18&__rev=1544977")
                        asc=re.findall('{"__m":"m_18_1"},{"__m":"m_18_4"},"(.*?)"',content,re.S)#为access_token
                        if len(asc) > 0:
                            self.access_token = '?access_token='+asc[0]
                            print asc[0]
                            print self.access_token
                            break
                    except Exception,e:
                        print str(e)

    def detail_friends(self,frd_sourse):
        import re
        import json
        frd_sourse = frd_sourse.replace('\\','')
        item = re.findall('data-profileid="(\d*?)" type="button" data-cansuggestfriends="true" data-cancelref="unknown" data-floc="friends_tab">',frd_sourse,re.S)
        dictfriend = {}
        for i in item:
            the_page = self.requesturl(self.host + i + self.access_token)
            post_dict = json.loads(the_page)
            link = post_dict['link']
            trueid = re.findall('https://www.facebook.com/app_scoped_user_id/(\d*?)/',link,re.S)[0]
            true_name = post_dict['first_name']+' '+post_dict['last_name']
            dictfriend[trueid] = true_name
        '''
        获得滚动的下一页url
        '''
        
        #temp_data = {"collection_token":"","cursor":"","tab_key":"friends","profile_id":None,"overview":False,"ftid":None,"order":None,"sk":"friends","importer_state":None}

        temp_data = '%2C%22overview%22%3Afalse%2C%22ftid%22%3Anull%2C%22order%22%3Anull%2C%22sk%22%3A%22friends%22%2C%22importer_state%22%3Anull%7D'
        outputx = open("iii.txt",'w')
        outputx.write(frd_sourse)
        outputx.close()
        dataitem = re.findall('\["pagelet_timeline_app_collection_(\d*):(\d*):(\d*)",{"__m":".*?"},"(.*?)="\]\],',frd_sourse,re.S)
        print dataitem
        if len(dataitem) > 0:
            temp_data = '%7B%22collection_token%22%3A%22'+str(dataitem[0][0])+'%3A'+str(dataitem[0][1])+'%3A'+str(dataitem[0][2])+'%22%2C%22cursor%22%3A%22'+dataitem[0][3] + '%3D%22%2C%22tab_key%22%3A%22friends%22%2C%22profile_id%22%3A'+str(dataitem[0][0]) + temp_data
            nexturl = 'https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?data='+temp_data+'&__user=100008265490891&__a=1&__dyn=7nmajEyl2qmdzpQ9UoHbgWDxi9ACxO4oKA8ABGeqrWo8popyUWdDx24Qq69poW8xOdyedy8e998O48&__req=8&__rev=1624746'
        else:
            nexturl = None
        return nexturl,dictfriend

    
    
    def get_usr_friend(self,usr_id):
        import re
        import json
        the_page = self.requesturl(self.host + usr_id + self.access_token)
        post_dict = json.loads(the_page)
        if post_dict:
            the_page = self.requesturl(post_dict['link'])
            item = re.findall('<a class="_6-6" href="(\S*?)" data-tab-key="friends">Friends',the_page,re.S)
            if len(item) > 0 :
                friendurl = item[0]
            else:
                print "error! cannot get friendurl  "+usr_id
                return
        else:
            print "error! cannot get profile!! "+usr_id
        html = self.requesturl(friendurl)
        if "All Friends" in html:
            print "get "+usr_id+" friends"
        else:
            print "None Public"
            return
        allfrd = {}
        nexturl,list_frd = self.detail_friends(html)
        allfrd = dict(allfrd,**list_frd)
        while(nexturl):
            html = self.requesturl(nexturl)
            nexturl,list_frd = self.detail_friends(html)
            allfrd = dict(allfrd,**list_frd)
        return allfrd
        

if __name__ == '__main__':
    fb_diver = fb_frd()
    fb_diver.login()
    fb_diver.getaccess_token()
    print fb_diver.get_usr_friend('821276697933399')



             
