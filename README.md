# facebook_page_history
Facebook热度预测<br />
在Facebook主页前三小时预测最后总转发量<br />
以下是主页的预测信息<br />
 ![image](https://github.com/yxzero/facebook_page_history/blob/master/%E7%BD%91%E9%A1%B5%E6%88%AA%E5%9B%BE.png)

各主页SH模型评价结果<br />
主页 RMSE r 训练条数 测试条数<br />
National Geographic 0.27832594 0.85463737 144 48<br />
history	0.32737778	0.80040119	211	70<br />
nba	0.28694586	0.87730771	387	129<br />
Call of Duty	0.191666	0.93741442	169	56<br />
Grey''s Anatomy	0.26148896	0.85880176	223	74<br />
Fox News	0.3087333	0.85103412	422	140<br />
The Simpsons	0.24680658	0.90316968	219	72<br />
Kung Fu Panda	0.21722348	0.90204075	103	34<br />
Barack Obama	0.28865517	0.76637799	158	52<br />
Harry Potter	0.32935727	0.68182638	241	80<br />

连接强度定义是对于网络中的节点之间信息交互，通信频率等的强弱，可以把节点之间的连接分为强连接和弱连接。美国社会学家Mark Granovette[20]提出了弱连接（Weak Ties）理论，它的表示可以是一种由情感强度、亲密度（包括相互信任）、互助关系等纽带形成的线性组合。加入强连接进行热度预测<br />
主页	RMSE	r	p<br />
history	0.32166	0.89659	2.4<br />
barack obama	0.230931	0.85	1.75<br />
Harry Potter	0.300767	0.743038	0.1<br />
nba	0.247463	0.911004	  10<br />
National Geographic	0.262066	0.871456	1.3<br />
