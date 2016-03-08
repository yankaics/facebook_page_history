#-*-coding:utf-8-*-
'''
created on 2014年12月24日

@author: yx

get facebook trending and topic 

'''


'''
get facebook trending 
top 10
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def change_time_type_api(time):
    temp = time.split('T')
    return temp[0]+' '+temp[1].split('+')[0]

def change_time_type(stime):
    import datetime
    return datetime.datetime.strptime(stime,'%A, %B %d, %Y at %I:%M%p').strftime("%Y-%m-%d %H:%M:%S")


def get_trending(fb,filename,fbsql):
    import re
    f = open(filename,'r')
    fstr = f.read()
    f.close()
    fb_trend_list = re.findall("href=\"(/topic.*?)\"",fstr,re.S)
    print fb_trend_list
    for i in fb_trend_list:
        data = {}
        tempi = re.sub('amp;','',i)
        tempi = re.sub('whfrt','wtfrt',tempi)
        fdata = re.findall('/topic/(.*?)/(.*?)\?',tempi,re.S)
        print fdata
        data['trqid'] = fdata[0][1]
        data['trqname'] = fdata[0][0]
        data['trqurl'] = 'https://www.facebook.com'+tempi
        fbsql.insert_trending(data)
        item = get_first_topic(fb,tempi)
        for i_item in item:
            getmsgsend(fb,i_item,fbsql,data['trqid'])
        

def get_first_topic(fb,url):
    import re
    the_page = fb.getnextpage('https://www.facebook.com'+url)
    outputx = open('trending.txt','w')
    outputx.write(the_page)
    outputx.close()
    item = re.findall('<div class="_5bl2 _3u1" data-bt="&#123;&quot;id&quot;:(.*?),',the_page,re.S)
    
    item1 = re.findall('<div class="_5bl2 _3u1 _412p" data-bt="&#123;&quot;id&quot;:(.*?),',the_page,re.S)
    item = item + item1
    print item
    return item

'''
get sharepost of each msg of facebook
@parem
fb: facebook class
id: mag id
newdict: useful_data

@return 
a dict :{usr_id_dir:usr_id_sourse,```}

'''
def get_share_post(fb,msg_id,usr_id,usr_name,fbsql,trend_msg):
    import re
    import json
    import time
    import datetime
    the_page = fb.getnextpage("https://www.facebook.com/shares/view?id="+msg_id,port = '8580')
    listone = re.findall('<span class="fwb"><a href=.*?id=(\d*)&.*?>([^\>]*?)</a></span> via <span class="fwb"><a href=.*?id=(\d*)&.*?>([^\>]*?)</a></span></span></div></h5><div class="_5pcp"><span><span class="fsm fwn fcg"><a class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?" target=""><abbr title="(.*?)" data-utime',the_page,re.S)
    
    #listtwo = re.findall('class="fwb"><a class="profileLink" href=.*?id=(\d*).*?>([^\>]*?)</a></span> shared <a class="profileLink" href=.*?id=(\d*).*?>([^\>]*?)</a>.*?</span></div></h5><div class="_5pcp"><span><span class="fsm fwn fcg"><a class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?" target=""><abbr title="(.*?)" data-utime',the_page,re.S)
    listtwo = re.findall('class="fwb"><a class="profileLink" href=.*?id=(\d*).*?>([^\>]*?)</a></span> shared <a class="profileLink" href=.*?id=(\d*).*?>([^\>]*?)</a>.*?<div class="_5pcp"><span><span class="fsm fwn fcg"><a class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?" target.*?><abbr title="(.*?)" data-utime',the_page,re.S)
    listone = listone+listtwo
    likedict = dict()
    listlike = re.findall('\{"feedbacktargets":\[(.*?)\],"comments":',the_page,re.S)
    for i in listlike:
        templike = json.loads(i)
        likedict[templike["targetfbid"]] = [templike['likecount'],templike['sharecount']]
    datatemp = dict()
    for i in listone:
        datatemp["postid"] = i[5]
        datatemp["fromid"] = i[2]
        datatemp["from_name"] = i[3]
        datatemp["toid"] = i[0]
        datatemp["to_name"] = i[1]
        datatemp["created_time"] = change_time_type(i[6])
        datatemp["trend_mid"] = trend_msg
        if i[5] in likedict:
            datatemp['like_count']  = likedict[i[5]][0]
            datatemp['share_count'] = likedict[i[5]][1]
            fbsql.insert_fb_share(datatemp)
            if datatemp['like_count']>0:
                try:
                    get_like(fb,datatemp['postid'],datatemp['toid'],datatemp['to_name'],fbsql,trend_msg)
                except Exception,e:
                    print str(e)
            if datatemp['share_count'] > 0:
                get_share_post(fb,datatemp['postid'],datatemp['toid'],datatemp['to_name'],fbsql,trend_msg)
    listtwo = re.findall('{"ajaxpipe_token":"(.*?)"',the_page,re.S)
    rev = re.findall('"revision":(\d*?),',the_page,re.S)
    i = 1
    listtemp = {}
    controller = 0
    while(len(listtwo)>0): 
        i = i+1
        try:
            page2 = fb.getnextpage("https://www.facebook.com/ajax/pagelet/generic.php/ViewSharesPagelet?ajaxpipe=1&ajaxpipe_token="+listtwo[0]+"&no_script_path=1&data=%7B%22load%22%3A"+str(i-1)+"%2C%22target_fbid%22%3A%22"+msg_id+"%22%2C%22pager_fired_on_init%22%3Atrue%7D&__user="+fb.uid+"&__a=1&__dyn="+fb.dyn+"&__req=jsonp_"+str(i)+"&__rev="+rev[0]+"&__adt="+str(i),port = '8580')
            listtemp = getdetaillist(fb,page2,trend_msg,msg_id,usr_id,usr_name,fbsql)
            #time.sleep(1)
        except Exception,e:
            print str(e)
        if len(listtemp) == 0:
                controller += 1
        else:
            controller = 0
        if controller == 5:
            break

        
def getdetaillist(fb,page,trend_msg,msg_id,usr_id,usr_name,fbsql):
    import re
    import json
    import datetime
    page = page.replace('\\','')
    page = page.decode('utf-8') 
    listtwo = re.findall('hovercard="/ajax/hovercard/user.php\?id=(\d*?)&amp;extragetparams=.*?">([^\>]*?)\u003C/a>\u003C/span> via \u003Cspan class="fwb">\u003Ca href=.*?data-hovercard="/ajax/hovercard/page.php\?id=(\d*?)&amp;extragetparams=.*?">([^\>]*?)\u003C/a>\u003C/span>\u003C/span>\u003C/div>\u003C/h5>\u003Cdiv class="_5pcp">\u003Cspan>\u003Cspan class="fsm fwn fcg">\u003Ca class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?".*?\u003Cabbr title="([^\>]*?)" data-utime=',page,re.S)
    listthree = re.findall('data-ft="&#123;&quot;tn&quot;:&quot;l&quot;&#125;" data-hovercard="/ajax/hovercard/user.php\?id=\d*?">([^\>]*?)\u003C/a>\u003C/span> shared a \u003Ca href=".*?/posts/(\d*?)">link\u003C/a>.\u003C/span>\u003C/div>\u003C/h5>\u003Cdiv class="_5pcp">\u003Cspan>\u003Cspan class="fsm fwn fcg">\u003Ca class="_5pcq" href=.*?>\u003Cabbr title="([^\>]*?)" data-utime=',page,re.S)
    #listtwo2 = re.findall('data-ft="&#123;&quot;tn&quot;:&quot;l&quot;&#125;" data-hovercard="/ajax/hovercard/user.php\?id=(\d*?)">([^\>]*?)\u003C/a>\u003C/span> shared \u003Ca class="profileLink" href=".*?id=(\d*?)">([^\>]*?)\u003C/a>.*?\u003C/span>\u003C/div>\u003C/h5>\u003Cdiv class="_5pcp">\u003Cspan>\u003Cspan class="fsm fwn fcg">\u003Ca class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?".*?\u003Cabbr title="([^\>]*?)" data-utime=',page,re.S)
    listtwo2 = re.findall('data-ft="&#123;&quot;tn&quot;:&quot;l&quot;&#125;" data-hovercard="/ajax/hovercard/user.php\?id=(\d*?)">([^\>]*?)\u003C/a>\u003C/span> shared \u003Ca class="profileLink" href=".*?id=(\d*?)">([^\>]*?)\u003C/a>.*?\u003Cdiv class="_5pcp">\u003Cspan>\u003Cspan class="fsm fwn fcg">\u003Ca class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?".*?\u003Cabbr title="([^\>]*?)" data-utime=',page,re.S)
    listtwo = listtwo + listtwo2
    listfour = re.findall('hovercard="/ajax/hovercard/user.php\?id=(\d*?)&amp;extragetparams=.*?">([^\>]*?)\u003C/a>\u003C/span>\u003C/div>\u003C/h5>\u003Cdiv class="_5pcp">\u003Cspan>\u003Cspan class="fsm fwn fcg">\u003Ca class="_5pcq" href="/.*?(story_fbid=|posts/)(\d*).*?".*?\u003Cabbr title="([^\>]*?)" data-utime=',page,re.S)
    listall = dict()
    listone = re.findall('\{"feedbacktargets":\[(.*?)\],"comments":',page,re.S)
    for i in listone:
        listone_dict = json.loads(i)
        dicttemp = dict()
        dicttemp['postid'] = listone_dict['targetfbid']
        dicttemp['like_count']  = listone_dict['likecount']
        dicttemp['share_count'] = listone_dict['sharecount']
        dicttemp['toid'] = listone_dict['ownerid']
        dicttemp['trend_mid'] = trend_msg
        listall[dicttemp['postid']] = dicttemp

    for i in listtwo:
        if i[5] in listall:
            listall[i[5]]['to_name'] = i[1]
            listall[i[5]]['fromid'] = i[2]
            listall[i[5]]['from_name'] = i[3]
            listall[i[5]]['created_time'] = change_time_type(i[6])
    for i in listthree:
        if i[1] in listall:
            listall[i[1]]['to_name'] = i[0]
            listall[i[1]]['fromid'] = usr_id
            listall[i[1]]['from_name'] = usr_name
            listall[i[1]]['created_time'] = change_time_type(i[2])
    for i in listfour:
        if i[3] in listall:
            listall[i[3]]['to_name'] = i[1]
            listall[i[3]]['fromid'] = usr_id
            listall[i[3]]['from_name'] = usr_name
            listall[i[3]]['created_time'] = change_time_type(i[4])
    for i in listall.keys():
        dicttemp = listall[i]
        if 'fromid' not in dicttemp:
            dicttemp['fromid'] = usr_id
            dicttemp['from_name'] = usr_name
            dicttemp['to_name'] = 'onone'
            dicttemp['created_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fbsql.insert_fb_share(dicttemp)
        if dicttemp['like_count']>0:
            try:
                get_like(fb,dicttemp['postid'],dicttemp['toid'],dicttemp['to_name'],fbsql,trend_msg)
            except Exception,e:
                print str(e)
        if dicttemp['share_count'] > 0:
            get_share_post(fb,dicttemp['postid'],dicttemp['toid'],dicttemp['to_name'],fbsql,trend_msg)
    return listall


def get_like(fb,msg_id,usr_id,usr_name,fbsql,trend_msg):
    import re
    import time
    page = fb.getnextpage("http://www.facebook.com/browse/likes?id="+msg_id,port = '8580')
    page.decode('utf-8')
    listone = re.findall('data-hovercard="/ajax/hovercard/user.php\?id=(\d*?)&amp;extragetparams=%7B%22hc_location%22%3A%22profile_browser%22%7D">([^\>]*?)</a></div></div></div></div></div>',page,re.S)
    likedict = dict()
    likedict['fromid'] = usr_id
    likedict['from_name'] = usr_name
    likedict['trend_mid'] = trend_msg
    for i in listone:
        likedict['toid'] = i[0]
        likedict['to_name'] = i[1]
        fbsql.insert_fb_like(likedict)
    i = 1
    page = fb.getnextpage("https://www.facebook.com/ajax/browser/list/likes/?id="+msg_id+"&beforetime=0&aftertime=0&start="+str(i*100)+"&__user="+fb.uid+"&__a=1&__dyn="+fb.dyn+"&__req=1&__rev=1670980",port = '8580')
    while(like_detail(page,fb,msg_id,usr_id,usr_name,fbsql,trend_msg)>0):
        i += 1
        #time.sleep(1)
        page = fb.getnextpage("https://www.facebook.com/ajax/browser/list/likes/?id="+msg_id+"&beforetime=0&aftertime=0&start="+str(i*100)+"&__user="+fb.uid+"&__a=1&__dyn="+fb.dyn+"&__req=1&__rev=1670980",port = '8580')

def like_detail(page,fb,msg_id,usr_id,usr_name,fbsql,trend_msg):
    import re
    page = page.replace('\\','')
    page = page.decode('utf-8')  
    listone = re.findall('data-hovercard="/ajax/hovercard/user.php\?id=(\d*?)&amp;extragetparams=\u00257B\u002522hc_location\u002522\u00253A\u002522profile_browser\u002522\u00257D">([^\>]*?)\u003C/a>\u003C/div>\u003C/div>\u003C/div>\u003C/div>\u003C/div>',page,re.S)
    likedict = dict()
    likedict['fromid'] = usr_id
    likedict['from_name'] = usr_name
    likedict['trend_mid'] = trend_msg
    for i in listone:
        likedict['toid'] = i[0]
        likedict['to_name'] = i[1]
        fbsql.insert_fb_like(likedict)
    return len(listone)

def getmsgsend(fb,msg_id,fbsql):
    import json
    the_page = fb.get_referense('/v2.3/'+msg_id)
    try:
        post_dict = json.loads(the_page)
        if 'error' not in post_dict:
            data = {}
            data['msgid'] = post_dict['id']
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
            else:
                data['created_time'] = None
            fbsql.insert_fb_msg(data)
            return (data['created_time'],data['fromid'])
        else:
            print the_page
            return (None,None)
    except Exception,e:
        print str(e)+the_page
        return (None,None)



def get_user_msg(fb,fbsql,usr_id,days):
    import re
    import urllib
    import json
    import datetime
    page = fb.get_referense('/v2.3/'+usr_id)
    dictusr = json.loads(page)
    url = dictusr['link']
    usr_name = dictusr['username']
    page = fb.getnextpage(url,port = '8580')
    datalist = []
    datamsg = re.findall('\{"feedbacktargets":\[(.*?)\],"comments":',page,re.S)
    page = page.replace('\\','')
    fb_dtsg = re.findall('name="fb_dtsg" value="(.*?)"',page,re.S)[0]
    parm = re.findall('"PagePostsSectionPagelet", (.*?), null',page,re.S)[0]
    print re.findall('"PagePostsSectionPagelet", (.*?), null',page,re.S)
    parm = json.loads(parm.decode('ascii'))
    pdata = {'__a':'1','__dyn':fb.dyn,'__req':'5','__rev':'1674690','__user':fb.uid}
    pdata['data'] = '{"segment_index":'+str(parm['segment_index'])+',"page_index":'+str(parm["page_index"])+',"page":'+str(parm['page'])+',"column":"main","post_section":{"profile_id":'+str(parm['post_section']['profile_id'])+',"start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+',"is_pages_redesign":true},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":false}'.encode('ascii')
    ftentidentifier = re.findall('\{"ftentidentifier":"(\d*?)".*?"outer_object_element_id":"(.*?)"',page,re.S)
    dictftenidentifier = dict()
    for i in ftentidentifier:
        dictftenidentifier[i[0]] = i[1]
    lasttime = None
    if len(datamsg)>0:
        for i in datamsg:
            target = json.loads(i)
            tempdata = dict()
            tempdata['msgid'] = target['targetfbid']
            tempdata['comments_count'] = target['commentcount']
            tempdata['share_count'] = target['sharecount']
            tempdata['like_count'] = target['likecount']
            (tempdata['created_time'],tempdata['fromid'])= getmsgsend(fb,i[0],fbsql)
            tempdata['fb_dtsg'] = fb_dtsg
            tempdata['outerid'] = dictftenidentifier[tempdata['msgid']]
            if tempdata['created_time']:
                datalist.append(tempdata)
                #lasttime = tempdata['created_time']
                lasttime = datetime.datetime.strptime(tempdata['created_time'],'%Y-%m-%d %H:%M:%S')
    if lasttime == None:
        lasttime = datetime.datetime.now()
    while(lasttime >(datetime.datetime.now()-datetime.timedelta(days=days))):
        page = fb.getnextpage('https://www.facebook.com/ajax/pagelet/generic.php/PagePostsSectionPagelet',params = pdata,port = '8580')
        datamsg = re.findall('"targetfbid":"(\d*?)".*?"commentcount":(\d*?),',page,re.S)
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
        pdata = {'__a':'1','__dyn':fb.dyn,'__req':'5','__rev':'1674690','__user':fb.uid}
        pdata['data'] = '{"segment_index":'+str(parm['segment_index'])+',"page_index":'+str(parm["page_index"])+',"page":'+str(parm['page'])+',"column":"main","post_section":{"profile_id":'+str(parm['post_section']['profile_id'])+',"start":'+str(parm['post_section']['start'])+',"end":'+str(parm['post_section']['end'])+',"query_type":'+str(parm['post_section']['query_type'])+',"filter":'+str(parm['post_section']['filter'])+',"is_pages_redesign":true},"section_index":'+str(parm['section_index'])+',"hidden":false,"posts_loaded":'+str(parm['posts_loaded'])+',"show_all_posts":false}'.encode('ascii')
        last_time = None
        if len(datamsg)>0:
            for i in datamsg:
                tempdata = dict()
                tempdata['msgid'] = i[0]
                tempdata['comments_count'] = i[1]
                (tempdata['created_time'],tempdata['fromid'])= getmsgsend(fb,i[0],fbsql)
                fb_dtsg = re.findall('name="fb_dtsg" value="(.*?)"',page,re.S)[0]
                tempdata['fb_dtsg'] = fb_dtsg
                tempdata['outerid'] = dictftenidentifier[tempdata['msgid']]
                if tempdata['created_time']:
                    datalist.append(tempdata)
                    lasttime = datetime.datetime.strptime(tempdata['created_time'],'%Y-%m-%d %H:%M:%S')
        if lasttime==None:
            break
    return (datalist,usr_name)

def get_ttstamp(fb_dtsg):
    ttstamp = '2'
    for i in fb_dtsg:
        ttstamp += str(ord(i))
    return ttstamp


def get_comments(fb,fbsql,msgdict):
    import re
    import json
    import time
    postdata = dict()
    postdata['ft_ent_identifier'] = msgdict['msgid']
    postdata['viewas'] = 'undefined'
    postdata['source'] = ''
    postdata['orderingmode'] = 'filtered'
    postdata['feed_context'] = '{"fbfeed_context":true,"location_type":36,"is_starred":false,"is_pinned_post":false,"can_moderate_timeline_story":false,"profile_id":'+msgdict['fromid']+',"outer_object_element_id":"'+msgdict['outerid']+'","object_element_id":"'+msgdict['outerid']+'","is_ad_preview":false,"is_editable":false}'.encode('ascii')
    postdata['__user'] = fb.uid
    postdata['__a'] = '1'
    postdata['__dyn'] = fb.dyn
    postdata['__req'] = 'c'
    postdata['fb_dtsg'] = msgdict['fb_dtsg']
    postdata['ttstamp'] = get_ttstamp(msgdict['fb_dtsg'])
    postdata['__rev'] = '1674690'
    if msgdict['comments_count'] <= 20:
        offset = 0
        length = int(msgdict['comments_count'])
    else:
        offset = int(msgdict['comments_count'])-20
        length = 20
    while(length >0):
        postdata['offset'] = str(offset)
        postdata['length'] = str(length)
        time.sleep(2)
        page = fb.postpage("https://www.facebook.com/ajax/ufi/comment_fetch.php",data = postdata,port = '8580')
        process_comment(fb,page,msgdict['fromid'],msgdict['from_name'],fbsql,msgdict['msgid'],postdata['fb_dtsg'],msgdict['outerid'])
        if offset <= 20:
            length = offset
            offset = 0
        else:
            offset -= 20
            length = 20

def process_comment(fb,page,usr_id,usr_name,fbsql,trend_msg,fb_dtsg,outerid):
    import re
    import json
    listc = re.findall('"comments":\[(.*?),"profiles":\[',page,re.S)
    if(len(listc)==0):
        return 0
    listcomments = json.loads('['+listc[0])
    listprofiles = json.loads('['+re.findall('"profiles":\[(.*?),"actions":',page,re.S)[0])
    listr = re.findall('"replies":\{(.*?)\},"featuredcommentlists"',page,re.S)
    if len(listr)==0:
        listreplies = {}
    else:
        listreplies = json.loads('{'+listr[0])
    for ic in listcomments:
        tempdata = dict()
        tempdata['id'] = ic['id']
        tempdata['fromid'] = ic['author']
        tempdata['toid'] = usr_id
        tempdata['to_name'] = usr_name
        tempdata['like_count'] = ic['likecount']
        tempdata['trend_mid'] = trend_msg
        tempdata['created_time'] = change_time_type(ic['timestamp']['verbose'])
        for ip in listprofiles:
            if ip['id'] == ic['author']:
                tempdata['from_name'] = ip['name']
                break
        tempdata['replies'] = listreplies[ic['id']]['range']['offset']
        fbsql.insert_fb_comment(tempdata)
        if int(tempdata['replies'])>0:
            get_replies(fb,fbsql,tempdata,fb_dtsg,outerid)
    return len(listcomments)

 
def get_replies(fb,fbsql,comment_dict,fb_dtsg,outerid):
    import re
    import json
    postdata = 'ft_ent_identifier='+comment_dict['trend_mid']+'&parent_comment_ids[0]='+comment_dict['id']+'&source&offsets[0]=0&lengths[0]='+str(comment_dict['replies'])+'&feed_context=%7B%22fbfeed_context%22%3Atrue%2C%22location_type%22%3A36%2C%22is_starred%22%3Afalse%2C%22is_pinned_post%22%3Afalse%2C%22can_moderate_timeline_story%22%3Afalse%2C%22profile_id%22%3A'+comment_dict['toid']+'%2C%22outer_object_element_id%22%3A%22'+outerid+'%22%2C%22object_element_id%22%3A%22'+outerid+'%22%2C%22is_ad_preview%22%3Afalse%2C%22is_editable%22%3Afalse%7D&__user='+fb.uid+'&__a=1&__dyn='+fb.dyn+'&__req=c&fb_dtsg='+fb_dtsg+'&ttstamp='+get_ttstamp(fb_dtsg)+'&__rev=1682066'.encode('ascii')
    page = fb.postpage("https://www.facebook.com/ajax/ufi/reply_fetch.php",data = postdata,port = '8580')
    listc = re.findall('"comments":\[(.*?),"profiles":\[',page,re.S)
    if(len(listc)==0):
        return 0
    listcomments = json.loads('['+listc[0])
    listprofiles = json.loads('['+re.findall('"profiles":\[(.*?),"actions":',page,re.S)[0])
    for ic in listcomments:
        tempdata = dict()
        tempdata['id'] = ic['id']
        tempdata['fromid'] = ic['author']
        tempdata['toid'] = comment_dict['fromid']
        tempdata['to_name'] = comment_dict['from_name']
        tempdata['like_count'] = ic['likecount']
        tempdata['trend_mid'] = comment_dict['trend_mid']
        tempdata['created_time'] = change_time_type(ic['timestamp']['verbose'])
        for ip in listprofiles:
            if ip['id'] == ic['author']:
                tempdata['from_name'] = ip['name']
                break
        fbsql.insert_fb_comment(tempdata)

    


'''
def get_share_post(fb,msg_id,usr_id,usr_name,fbsql,trend_msg):
    import json
    import sys
    cur_path = sys.path[0] 
    the_page = fb.get_referense('/v2.3/'+msg_id+'/sharedposts')

    #get_like(fb,msg_id,usr_id,usr_name,fbsql,trend_msg)#get likes
    if the_page: 
        try:
            dict = json.loads(the_page)
            while(True):
                if 'error' in dict:
                    print the_page
                    break
                produce_share(fb,dict,usr_id,usr_name,fbsql,trend_msg)
                if 'paging' not in dict:
                    break
                page = dict['paging']
                if 'next' not in page:
                    break
		else:
		    print trend_msg+" has next"
                the_page = fb.getnextpage(page['next'].decode('utf-8'))
                dict = json.loads(the_page)
            print "done!!get "+msg_id+"share_post!!"
        except Exception,e:
            print str(e)


produce the share_dict file
@parem
fb
sdict: each dict of share
newdict: key-share_id value-[from ,to,share_count,created_time]
usr_id: id of create user 

@return
update newdict


def produce_share(fb,sdict,usr_id,usr_name,fbsql,trend_msg):
    for i in sdict['data']:
        data = {}
        data['postid'] = i['id']
        data['fromid'] = usr_id
        data['from_name'] = usr_name
        data['toid'] = i['from']['id']
        data['to_name'] = i['from']['name']
        data['created_time'] = chang_time_type(i['created_time'])
        data['trend_mid'] = trend_msg
        if 'shares' in i:
            share_count = i['shares']['count']
            uid_post = data['postid'].split('_')
            get_share_post(fb,uid_post[1],uid_post[0],data['from_name'],fbsql,trend_msg)
        else:
            share_count = 0
        fbsql.insert_fb_share(data)

def get_like(fb,msg_id,usr_id,usr_name,fbsql,trend_msg):
    import json
    data = {}
    data['fromid'] = usr_id
    data['from_name'] = usr_name
    data['trend_mid'] = trend_msg
    the_page = fb.get_referense('/v2.3/'+msg_id+'/likes')
    if the_page:
        try:
            dict = json.loads(the_page)
            while(True):
                if 'error' in dict:
                    print the_page
                    break
                for i in dict['data']:
                    data['toid'] = i['id']
                    data['to_name'] = i['name']
                    fbsql.insert_fb_like(data)
                if 'paging' not in dict:
                    break
                page = dict['paging']
                if 'next' not in page:
                    break
                the_page = fb.getnextpage(page['next'].decode('utf-8'))
                dict = json.loads(the_page)
        except Exception,e:
            print str(e)
        print "done!get "+msg_id+" likes"

def get_comments(fb,cid,usr_id,usr_name,fbsql,trend_msg):
   import json
    data = {}
    data['fromid'] = usr_id
    data['from_name'] = usr_name
    data['trend_mid'] = trend_msg
    the_page = fb.get_referense('/v2.3/'+cid+'/comments')
    if the_page:
        try:
            dict = json.loads(the_page)
            while(True):
                if 'error' in dict:
                    print the_page
                    break
                if len(dict['data']) == 0:
                    break
                for i in dict['data']:
                    data['id'] = i['id']
                    data['toid'] = i['from']['id']
                    data['to_name'] = i['from']['name']
                    data['created_time'] = chang_time_type(i['created_time'])
                    data['like_count'] = i['like_count']
                    fbsql.insert_fb_comment(data)
                    get_comments(fb,data['id'],data['toid'],data['to_name'],fbsql,trend_msg)
                if 'paging' not in dict:
                    break
                page = dict['paging']
                if 'next' not in page:
                    break
                the_page = fb.getnextpage(page['next'].decode('utf-8'))
                dict = json.loads(the_page)
        except Exception,e:
            print str(e)
        
'''
