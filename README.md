# Assignment3(Portfolio Construction)
Basic Thoughts
==
I learned Markowitz's portfolio theory from the class named Investment Science, so I want to select several stocks to practice and visualize the model.

Data Source
==
Considering the expected return and volatility of stocks, We select hs300, Pingan(601318), Youzu(002174), BOE(000725). We make use of tushare to import data during the period from 2018 to 2020.

Data Processing
==
Monte Carlo
-
I use Monte Carlo method to produce a lot of weights of assets, and then plot it.
![image](https://user-images.githubusercontent.com/80868998/118300181-3b12e700-b514-11eb-8789-f87178523b5e.png)

I also cacluate mean, variance, coviarance.

Portfolio Optimization
==
1:I choose the sharpe ratio to get the first portfolio construction.

2:I also get the portfolio with minimum varaiance.

Data Visiualization
==
I use red star to show the portfolio of the biggest sharpe ratio

I use yellow star to represent the portfolio of the minimum variance

I use x to represent the efficent frontier.

![image](https://user-images.githubusercontent.com/80868998/118302001-46671200-b516-11eb-9ff4-bd6d83b6938b.png)
