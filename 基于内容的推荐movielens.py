#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:47:03 2019

@author: liujun
"""



#构建信息矩阵
#计算电影的信息矩阵  用[1,0,0....]这种格式来表示电影的类别
#计算用户的偏好矩阵  avg(sum(x-avg_x)) [0.5,0.6.....]
#计算用户与电影的cos   余弦相似度=信息矩阵*偏好矩阵/(|信息矩阵|*|偏好矩阵|)
import pandas as pd
import numpy as np 
import math


#计算电影的信息矩阵
def movies_data(path1='./movies.csv'): #格式为MovieID,Title,Genres
        items=pd.read_csv(path1)
        movies_id=set(items['MovieID'].values)
        all_genre=[]
        movie_dict={}  #{movieid:文字表示[种类]}
        movie_matrix={} #{movieid:数字表示的【种类】}
        for movie_id in movies_id:
            genres=items[items['MovieID']==movie_id]['Genres'].values[0].split('|')
            all_genre.extend(genres)
            all_genres=set(all_genre)
            movie_dict.setdefault(movie_id,[]).extend(genres)
        for key in movie_dict.keys():
            movie_matrix[str(key)]=[0]*len(all_genres)
            for genre in movie_dict[key]:
                genre_index=list(all_genres).index(genre)
                movie_matrix[str(key)][genre_index]=1
        return movie_dict,movie_matrix,all_genres


               
#计算用户的偏好矩阵  
def users_data(path2='./ratings.csv'):#格式为UserID,MovieID,Rating,Timestamp
        movie_dict,movie_matrix,all_genres=movies_data(path1='/Users/liujun/Desktop/推荐系统/章节代码/5-chapter/data/movies.csv')
        users_dict={}
        user_matrix={} 
        users=pd.read_csv('./ratings.csv')
        user_ids=set(users['UserID'].values)
        for user in user_ids:
            users_dict.setdefault(str(user),{})
        with open('./ratings.csv','r') as f:
            for line in f.readlines():
                if not line.startswith('UserID'):
                    user,movieid,rate=line.split(',')[:3]
                    users_dict[user][movieid]=int(rate)
        for user in users_dict.keys():
           user_matrix[user]=[]
           score_list=users_dict[user].values()
           score_avg=sum(score_list)/len(score_list)
           for genre in all_genres:
               score_sum=0
               score_len=0
               for movieid in users_dict[user].keys():
                   if genre in movie_dict[int(movieid)]:
                       score_sum=score_sum+(users_dict[user][movieid]-score_avg)
                       score_len=score_len+1
               if score_len==0:
                   user_matrix[user].append(0)
               else:
                   user_matrix[user].append(score_sum/score_len)
        return user_matrix    


class CBRecommend:
    def __init__(self,k):
        self.k=k   #给客户推荐的个数
#获取特定用户未评分的电影ID列表
    def none_score(self,user):
        moviesid=pd.read_csv('/Users/liujun/Desktop/推荐系统/章节代码/5-chapter/data/movies.csv')['MovieID'].values
        ratings=pd.read_csv('/Users/liujun/Desktop/推荐系统/章节代码/5-chapter/data/ratings.csv')
        have_score_movies=ratings[ratings['UserID']==user]['MovieID'].values
        none_score_movies=set(moviesid)-set(have_score_movies)
        return none_score_movies
    
    
#获取特定用户的评分列表
    def user_hobby(self,user,movie):
        user_matrix =users_data(path2='./ratings.csv')
        movie_dict,movie_matrix,all_genres=movies_data(path1='./movies.csv')
        hobby=sum(np.array(user_matrix[str(user)])*np.array(movie_matrix[str(movie)]))
        hobby_1=math.sqrt(sum(math.pow(a,2) for a in user_matrix[str(user)]))
        hobby_2=math.sqrt(sum(math.pow(b,2) for b in movie_matrix[str(movie)]))
        return hobby/(hobby_1*hobby_2)
        
    def recommend(self,user):
        user_result={}
        for movie in list(self.none_score(user)):
            user_result[movie]=self.user_hobby(user,movie)
        result=sorted(user_result.items(), key=lambda x:x[1],reverse=True)[:self.k]
        print(result)
        return result
    
    
if __name__=='__main__':
    cb=CBRecommend(k=10)
    cb.recommend(1)
                  
                   
                       
               
           
               
                       
                       
           
               
            
            