# Kupresanin Project Repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)

<!-- tocstop -->

## Project Charter 

**Vision**:  
To take it to the man.  
In other words, for gambling purposes, help the user to consistently beat the MLB over / under runs totals wagers.  

**Mission**:  
Each day, the user can pull the runs total predictions for the slate of MLB games.  
These predictions can be used to make educated bets.

**Success Criteria**:  

**Statistical Criteria**:  
Mean Square Error, from the regression, boosted tree, or random forest final model.  
The model will produce a numerical prediction, "Total Runs Scored" for each MLB game today.  
Hope to keep MSE (test) under 1 run, but not sure at this point.  

**Business Criteria**:  
To win at sports gambling, the bettor needs to win more than 55 percent of wagers placed.  
From deployment through the end of the 2019 MLB regular season, I will use the model and track a running total of wagers won.  

**Example**:  
Say on April 10, there are three MLB games scheduled:  
Pirates vs. Cubs, runs total = 7.5  
Indians vs. Tigers, runs total = 7.0  
Rays vs. White Sox, runs total = 8.5

![example](mlb.png)

The above "runs total" values are set by the bookie before the game is played.  
The gambler can bet UNDER if he thinks the game will have fewer runs than the above values.  
The gambler can bet OVER if she thinks the game will have more runs than the above values.  

The user accesses the model early in the day and the predictions are:  
Pirates vs. Cubs, predicted runs = 7.9  
Indians vs. Tigers, predicted runs = 6.4  
Rays vs. White Sox, predicted runs = 9.9  

The best betting opportunity for April 10 is the bet the OVER 8.5 on Rays vs. White Sox.  

If the game has 9 or more runs, the gambler wins.  
If the game has 8 or fewer runs, the gambler loses.  
Bets pay even money, so a $100 bet wins $100.  

The reason the gambler must win more than 55 percent of wagers is the bookie charges a commission to make the wager.  


## Backlog

**Themes**:  
  
1.  A working app that meets the MSiA criteria.  
2.  Enough modeling predictive power to take it to the man.  
3.  Testing / Logging / QA crash course.  

**Epics**:  
  
1.1.  Source data from baseball statistics API.  
1.2.  Build predictive models based on local data.  
1.3.  Successfully migrate data from API to cloud database.  
1.4.  Automate continuous daily data collection.  
1.5.  Develop web app for user to obtain daily predictions.  

2.1.  Upon functionality, begin to track if predictions can beat the bookie.  
2.2.  Additional variables can be entered into modeling, but keeping it simple to start:  

Available variables (per day):  
Matchup variables (location, stadium, surface, time, etc...)  
Weather variables (temperature, wind, cloud coverage, etc...)  
Matchup variables (starting pitcher record / runs given up / history and team record)  

3.1.  Develop these skills from scratch (no experience on any of them).  

**Stories**:  

1.1.a.  Learn how to pull API data (website already selected and required variables available).  
1.1.b.  Learn where to put API data.  
1.1.c.  Revisit manipulating / cleaning / transforming data in Python.  

1.2.a.  Develop models using Scikit-Learn - likely regression, boosted tree, and random forest.  
1.2.b.  Determine reasonable strategy for train / test split.  
1.2.c.  















