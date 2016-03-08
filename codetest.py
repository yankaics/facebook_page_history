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

#uid = '100008395831331'
uid = '100008105866583'

fb = facebook_graph()
fb.uid = uid
#fb.login("huluzhupo@gmail.com","jbnhu789")
fb.login("heiheiyouok@gmail.com","blueapple")
fb.getaccess_token()
fbsql = fb_mysql()
act = fb.access_token
cookies = fb.cookies
usr_name = 'NBA'
di = dict()
di['msgid'] = '10153112524823463'
di['fromid'] = '8245623462'
threadx = fb_post_sharelike(cookies,di,uid,usr_name)
threadx.start()
threadx.join()



