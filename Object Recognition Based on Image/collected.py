# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:07:01 2018

@author: HP
"""

#图片命名格式为： 'label1_train1',...,'labeln_trainn',...
#Label统一用数字表示（01-25）（一共25类）
#图片全部在文件夹train2里（已经分好类了），没有分好类的在train_img里
import os
import csv

path='D:/ZJU/train_img'
path2 = './train2'

def count(path):      
    ls = os.listdir(path)
    count = 0
    for i in ls:
        if os.path.isfile(os.path.join(path,i)):
            count += 1
    return count



def get_file_names(path):
    name_list=[]
    dirs = os.listdir(path)
    for dir in dirs:
        #print(dir)
        name_list.append(dir)
    return name_list
#print(get_file_names('D:/ZJU/test_img'))





    
