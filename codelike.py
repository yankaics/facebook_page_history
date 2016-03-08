#-*-coding:utf-8-*-
'''
Created on 2014年12月18日

@author: yx
'''
import re
import time
#from createstr import create_string
                
if __name__ == '__main__':
    import multiprocessing
    from save_post import fb_process_like
    user_list = [#{'user_name':'huluzhupo@gmail.com','password':'jbnhu789','uid':'100008395831331','dyn':'7nmajEyl2lm9o-t2u59G85ku699Esx6iqAdy9VQC-C26m6oKezob4q68K5Uc-dwIxbxjyV8izaG8Czrw'},
        {'user_name':'blueshitshit@gmail.com','password':'blueshit','uid':'100008265490891','dyn':'7nmajEyl2lm9o-t2u5bHaEWCueyp9Esx6iqAdy9VCC-C26m6oKewWhEoyUnwPUS2O4K5ebAxacGEyqdK'}    
        ]
    get_list = ['8429246183']
    #,'6281559092','122177661170978','39581755672','127810744027768','16307558831','13652355666','52150999700','8245623462','152083869857']
    jobs = []
    j = 0
    for i in get_list:
        proc = fb_process_like(user_list[j],i)
        proc.start()
        j = (j+1)%len(user_list)
        jobs.append(proc)
        if len(multiprocessing.active_children())>(len(user_list)-1):
            for pj in jobs:
                pj.join()
    for pj in jobs:
        pj.join() 

