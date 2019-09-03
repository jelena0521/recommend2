# 本代码仅为日记记录学习，不支持任何商业用途
#两个数据文件  一个为movies.csv 数据格式为  MovieID,Title,Genres 一个为ratings 数据格式为UserID,MovieID,Rating,Timestamp
#基于用户偏好的推荐 需要两个list 
#一个list1为物品类别[1,0,0,1]  长度为类别长度  属于该类别为1  不属于则为0
#一个list2为偏好[0.5,0.3,0.2,0.1]  长度与上面相同  每个类别数字的计算为sum(同类别物品评分-总AVG）/长度
#偏好结果为 sum（ list1*list2）/(moid(list1)*moid(list2))
#需要注意的地方  读取数据后的str和int格式
#清洗数据后需将数据存储 否则每次都重新运行速度很慢



