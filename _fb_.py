#-*-coding:utf-8-*-
'''
Created on 2014年12月18日

@author: yx
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import urllib
import urllib2


class facebook_graph():

    def __init__(self):
        self.cookies = dict()
        self.access_token = ''
        self.s = requests.Session()
        self.host = "https://graph.facebook.com" 
        self.headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:34.0) Gecko/20100101 Firefox/34.0"}
        self.uid = ''
        self.dyn = ''

    def login(self,email,password):
        while(True):
            try:
                profile = webdriver.FirefoxProfile()
                profile.set_preference('network.proxy.type',1)
                profile.set_preference('network.proxy.http','127.0.0.1')
                profile.set_preference('network.proxy.http_port',8580)
                profile.set_preference('network.proxy.ssl','127.0.0.1')
                profile.set_preference('network.proxy.ssl_port',8580)
                profile.update_preferences()
                driver = webdriver.Firefox(profile)
                url = "https://www.facebook.com"
                driver.get(url)
                elem = driver.find_element_by_id('email')
                elem.send_keys(email)
                elem = driver.find_element_by_id('pass')
                elem.send_keys(password)
                elem.send_keys(Keys.RETURN)
                time.sleep(1)
                html_source = driver.page_source
                if "Please re-enter your password" in html_source or "Incorrect Email" in html_source:
                    print "password error!!"
                    driver.close()
                    exit()
                else:
                    print "login success\n"
                get_cookies = driver.get_cookies()
        
                for cookie in get_cookies:
                    self.cookies[cookie['name']] = cookie['value']
                driver.close()
                outputx = open('facebookpage.txt','w')
                outputx.write(self.getnextpage("https://www.facebook.com",port = '8580'))
                outputx.close()
                return
            except Exception,e:
                print str(e)

    def getnextpage(self,page,port = '8580',params=None):
        import time
        proxies = {'http': 'http://127.0.0.1:'+port,'https': 'http://127.0.0.1:'+port}
        while(True):
            try:
                response=self.s.get(page,proxies=proxies,cookies=self.cookies,verify = False,headers = self.headers,timeout = 20,params=params)
                return response.content
            except Exception,e:
                time.sleep(2)
                print str(e)+'----'+'get nextpage:'+page
        return None

    def postpage(self,page,port = '8087',data = None):
        proxies = {'http':'http://127.0.0.1:'+port,'https':'http://127.0.0.1:'+port} 
        while(True):
            try:
                response = self.s.post(page,data=data,proxies=proxies,cookies=self.cookies,verify=False,headers = self.headers,timeout = 20)
                return response.content
            except Exception,e:
                print str(e)+'----'+'post:' +page
                time.sleep(20)
        return None


    def getaccess_token(self,string = None):
        import re
        if string:
            self.access_token = string
        else:
            while(True):
                i = 5
                try:
                    print 'get access_token'
                    content = self.getnextpage("https://developers.facebook.com/tools/explorer/145634995501895/permissions?version=v2.2&__asyncDialog="+str(i)+"&__user="+self.uid+"&__a=1&__dyn=7nmajEyl2lm9o-t2u59G85ku699Esx6iqAdy9VQC-C26m6oKezob4q68K5Uc-dwIxbxjyV8izaG8Czrw&__req=18&__rev=1544977")
                    #asc=re.findall('{"__m":"m_18_1"},{"__m":"m_18_4"},"(.*?)"',content,re.S)#为access_token
                    asc=re.findall('{"__m":"__inst_33519630_18_0"},{"__m":"__inst_835c633a_18_0"},"(.*?)"',content,re.S)#为access_token
                    if len(asc) > 0:
                        self.access_token = '?access_token='+asc[0]
                        print self.access_token
                    break
                except Exception,e:
                    print str(e)

    def get_referense(self,token):
        import json
        req = self.host+token+self.access_token
        while(True):
            try:
                return self.getnextpage(req)
            except Exception,e:
                print str(e)
        return None

    def detail_friends(self,frd_sourse):
        import re
        import json
        frd_sourse = frd_sourse.replace('\\','')
        outputx= open('frd.txt','w')
        outputx.write(frd_sourse)
        outputx.close()
        item = re.findall('data-profileid="(\d*?)"',frd_sourse,re.S)
        dictfriend = {}
        for i in item:
            dictfriend[i] = None
        '''
        获得滚动的下一页url
        '''
        
        #temp_data = {"collection_token":"","cursor":"","tab_key":"friends","profile_id":None,"overview":False,"ftid":None,"order":None,"sk":"friends","importer_state":None}

        temp_data = '%2C%22overview%22%3Afalse%2C%22ftid%22%3Anull%2C%22order%22%3Anull%2C%22sk%22%3A%22friends%22%2C%22importer_state%22%3Anull%7D'
        dataitem = re.findall('\["pagelet_timeline_app_collection_(\d*):(\d*):(\d*)",{"__m":".*?"},"(.*?)"\]\],',frd_sourse,re.S)
        if len(dataitem) > 0:
            temp_data = '%7B%22collection_token%22%3A%22'+str(dataitem[0][0])+'%3A'+str(dataitem[0][1])+'%3A'+str(dataitem[0][2])+'%22%2C%22cursor%22%3A%22'+dataitem[0][3] + '%3D%22%2C%22tab_key%22%3A%22friends%22%2C%22profile_id%22%3A'+str(dataitem[0][0]) + temp_data
            nexturl = 'https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?data='+temp_data+'&__user='+self.uid+'&__a=1&__dyn=7nmajEyl2qm6VQ9UoHbgWDxi9ACxO4oKA8Ay8VFLFwxBxCbzES2N6xybxu3fzoy3rxjx27WG8CBDw&__req=8&__rev=1624746'
        else:
            nexturl = None
        return nexturl,dictfriend

    
    
    def get_usr_friend(self,usr_id):
        import re
        import json
        the_page = self.getnextpage(self.host + '/v2.2/' + usr_id + self.access_token)
        post_dict = json.loads(the_page)
        if post_dict:
            the_page = self.getnextpage(post_dict['link'],'8580')
            item = re.findall('<a class="_6-6" href="(\S*?)" data-tab-key="friends">Friends',the_page,re.S)
            if len(item) > 0 :
                friendurl = item[0]
            else:
                print "error! cannot get friendurl  "+usr_id
                return
        else:
            print "error! cannot get profile!! "+usr_id
            return
        html = self.getnextpage(friendurl,port = '8580')
        if "All Friends" not in html:
            print "None Public "+usr_id
            return
        allfrd = {}
        nexturl,list_frd = self.detail_friends(html)
        allfrd = dict(allfrd,**list_frd)
        while(nexturl):
            html = self.getnextpage(nexturl,'8580')
            nexturl,list_frd = self.detail_friends(html)
            allfrd = dict(allfrd,**list_frd)
        return allfrd

'''
import urllib2
import cookielib
import urllib
import os



class facebook_graph():
    
    #this class get facebook sdk of graph:
    
    def __init__(self):
        #proxy = '127.0.0.1:8580'
        proxy = 'yuxuanzero@gmail.com:huangzhaoling660703@127.0.0.1:8087' 
        self.access_token = "?access_token="
        self.host = "https://graph.facebook.com/"
        self.cj = cookielib.MozillaCookieJar('cookies.txt')
        if os.access('cookies.txt',os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel = 0),
        urllib2.HTTPSHandler(debuglevel = 0),
        urllib2.HTTPCookieProcessor(self.cj),
        urllib2.ProxyHandler({'https':proxy}) 
        )
        self.opener.addheaders = [('User-Agent',("Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:34.0) Gecko/20100101 Firefox/34.0"))]
        
    def login(self):
        posturl ='https://login.facebook.com/login.php'
        pd = {'email' : 'blueshitshit@gmail.com',
            'pass' : 'blueshit',
            }
        postdata = urllib.urlencode(pd)
        while(5):
            try:
                response = self.opener.open(posturl,postdata,timeout = 20)
                if response.getcode() == 200 :
                    print "logon in !!!"
                    text = response.read()
                    output_txt = open("facebookpage.txt",'w')
                    output_txt.write(text)
                    output_txt.close()
                    self.cj.save()
                    break
                else:
                    print "error!!"
            except Exception,e:
                print str(e)
                
    def getnextpage(self,page):
        while(5):
            try:
                print "get "+page
                response = self.opener.open(page,timeout = 20)
                thepage = response.read()
                self.cj.save()
                return thepage
                break
            except Exception,e:
                print str(e)

    def getaccess_token(self):
        import re
        i=1
        while(i<=5):
            try:
                response = self.opener.open("https://developers.facebook.com/tools/explorer/145634995501895/permissions?version=v2.2&__asyncDialog="+str(i)+"&__user=100008265490891&__a=1&__dyn=5U463-i3S2e4oK4pomXWo5O12wAxu13w&__req=18&__rev=1544977",timeout=20)
                data = response.read()
                asc = re.findall('{"__m":"m_18_1"},{"__m":"m_18_4"},"(.*?)"',data,re.S)#为access_token
                if len(asc) > 0:
                    self.access_token += asc[0]
                    print self.access_token
                    break
            except Exception,e:
                print str(e)

    
    def get_referense(self,token):
        import json 
        req = self.host+token+self.access_token
        for i in range(5):
            try:
                response = self.opener.open(req,timeout=20)
                the_page = response.read()
                return the_page
            except Exception,e:
                print str(e)  

'''
