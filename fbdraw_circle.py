#-*-coding:utf-8-*-
'''
Created on 2014年12月29日

@author: yx
'''     
def gettripg():
    import networkx as nx
    import sys
    msg_id = '10152813633021336'
    c = '15704546335'
    path = sys.path[0]
    inputedg = open(path+'/share_result/'+msg_id+'_edge.txt','r')
    G0=nx.Graph()
    for x in inputedg.readlines():
        i = x.strip().split('\t')
        print i
        G0.add_edge(i[0], i[1])
    inputedg.close()
    G0.rtt= {}
    G0.size = {}
    G0.lable = {}
    for n in G0:
        if n==c:
            G0.rtt[n] = int(G0.degree(n))
            G0.size[n] = 50*int(G0.degree(n))
            G0.lable[n] = "c-"+n
        else:
            G0.rtt[n]= int(G0.degree(n))
            G0.size[n]= 50*int(G0.degree(n))
            if int(G0.degree(n))>10:
                G0.lable[n] = n
            else:
                G0.lable[n] = ""
    return G0,c
    
if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    g,center = gettripg()
    plt.figure(figsize=(8,8))
    pos = nx.graphviz_layout(g, 'twopi', center)
    #pos=nx.spectral_layout(g)
    nx.draw(g, pos, 
            node_color = [g.rtt[v] for v in g],
            #with_labels=True,
            lable = g.lable,
            alpha=0.5,
            node_size=[g.size[v] for v in g])
    nx.draw_networkx_labels(g,pos,g.lable,font_size=12)
    # adjust the plot limits
    '''
    xmax=1.4*max(xx for xx,yy in pos.values())
    ymax=1*max(yy for xx,yy in pos.values())
    plt.xlim(0,xmax)
    plt.ylim(0,ymax)'''
    
    plt.show()
    #plt.savefig("lanl_routes.png")
    
    
    
    
    
    
