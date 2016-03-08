def logw(stringl):
    import datetime
    nowtime = datetime.datetime.now()
    outputx = open('log.txt','a+')
    outputx.write(str(nowtime)+': '+stringl+'\n')
    outputx.close()

