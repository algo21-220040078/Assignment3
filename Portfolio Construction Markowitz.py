# -*- coding: utf-8 -*-
"""
Created on Fri May 14 22:15:10 2021

@author: Administrator
"""

import tushare as ts            #开源财经数据接口包
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   #绘图工具

#数据获取
#沪深300
data=pd.DataFrame()
data0=ts.get_hist_data('hs300','2018-01-01','2020-12-01')
data0=data0['close']    #取收盘价
data0=data0[::-1]      #按日期由小到大
data['hs300']=data0

#中国平安
data1=ts.get_hist_data('601318','2018-01-01','2020-12-01')
data1=data1['close']     
data1=data1[::-1]       
data['601318']=data1

#游族网络
data2=ts.get_hist_data('002174','2018-01-01','2020-12-01')
data2=data2['close']     
data2=data2[::-1]      
data['002174']=data2

#京东方A
data3=ts.get_hist_data('000725','2018-01-01','2020-12-01')
data3=data3['close']     
data3=data3[::-1]       
data['000725']=data3

data = data. dropna ()   
data. head ()           

#收益均值、协方差
returns = np.log (data/ data. shift(1))
returns. mean()*252
#计算均值
returns. cov()       #计算协方差
returns. corr()       #计算相关系数

noa=4
weights=np. random. random(noa)
weights/=np. sum(weights)
weights

np. sum(returns. mean()*weights)
np. dot(weights.T,np.dot(returns. cov(), weights))
np. sqrt(np.dot(weights.T,np.dot(returns. cov(), weights)))


#蒙特卡洛模拟生成点
port_returns=[]
port_variance=[]
for p in range(4000):
   weights=np.random.random(noa)
   weights/=np.sum(weights)
   port_returns.append(np.sum(returns.mean()*252*weights))
   port_variance.append(np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights))))
   
   

port_returns=np.array(port_returns)
port_variance=np.array(port_variance)
risk_free=0.015
plt.figure(figsize=(10,5))     #设置图表大小
plt.scatter(port_variance,port_returns,c=(port_returns-risk_free)/port_variance,marker='o')
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')



#夏普最大的投资组合
def statistics(weights):
    weights=np.array(weights)
    port_returns=np.sum(returns.mean()*weights)*252
    port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
    return np.array([port_returns,port_variance,port_returns/port_variance])
import scipy.optimize as sco
def min_sharpe(weights):
    return -statistics(weights)[2]       
cons=({'type':'eq','fun':lambda x:np.sum(x)-1})
bnds=tuple((0,1) for x in range(noa))    #权重在0-1之间
opts=sco.minimize(min_sharpe,noa*[1./noa,],method='SLSQP',bounds=bnds,constraints=cons)             
opts
opts['x'].round(3)   #可以得到最优组合权重向量
statistics(opts['x']).round(3)  #可以得到sharpe最大的组合3个统计数据



#方差最小的投资组合
def min_variance(weights):
    return statistics(weights)[1]
optv=sco.minimize(min_variance,noa*[1./noa,],method='SLSQP',bounds=bnds,constraints=cons)
optv
opts['x'].round(3)            #方差最小的最优组合权重向量及组合的统计数据
statistics(opts['x']).round(3)    #得到预期收益率、波动率和夏普指数



#画出有效组合前沿
def min_variance(weights):
    return statistics(weights)[1]
target_returns=np.linspace(0.0,0.5,50)
target_variance=[]
for tar in target_returns:
   cons=({'type':'eq','fun':lambda
           x:statistics(x)[0]-tar},{'type':'eq','fun':lambda x:np.sum(x)-1})
   res=sco.minimize(min_variance,noa*[1./noa,],method='SLSQP',bounds=bnds,
constraints=cons)
   target_variance.append(res['fun'])
target_variance=np.array(target_variance) 

plt.figure(figsize=(12,6))
plt.scatter(port_variance,port_returns,
           c=port_returns/port_variance,marker='o')
#圆圈o：蒙特卡洛模拟随机产生的组合
plt.scatter(target_variance,target_returns,
           c=target_returns/target_variance,marker='x')
#叉号x：有效边界
plt.plot(statistics(opts['x'])[1],statistics(opts['x'])[0],'r*',markersize=15.0)
#红星：标记最高SHARPE组合
plt.plot(statistics(optv['x'])[1],statistics(optv['x'])[0],'y*',markersize=15.0)
#黄星：标记最小方差组合
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')