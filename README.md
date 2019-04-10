# Kupresanin Project Repository

<!-- toc -->

- [Project Charter](#project-charter)

<!-- tocstop -->

## Project Charter 

**Vision**:  
To take it to the man.  
In other words, for gambling purposes, help the user to consistently beat the MLB over / under runs totals wagers.  

**Mission**:  
Each day, the user can pull the runs total predictions for the slate of MLB games.  
These predictions can be used to make educated bets.

**Success criteria**:  

**Statistical Criteria**:  
Mean Square Error, from the regression, boosted tree, or random forest final model.  
The model will produce a numerical prediction, "Total Runs Scored" for each MLB game today.  
Hope to keep MSE (test) under 1 run, but not sure at this point.  

**Business Criteria**:  
To win at sports gambling, the bettor needs to win more than 55 percent of wagers placed.  
From deployment through the end of the 2019 MLB regular season, I will use the model and track a running total of wagers won.  

**Example**:  
Say on April 10, there are three MLB games scheduled:  
Indians vs. White Sox, runs total = 8.5  
Cubs vs. Pirates, runs total = 7.5  
Rockies vs. Reds, runs total = 10.5  

The above "runs total" values are set by the bookie before the game is played.  
The gambler can bet UNDER if he thinks the game will have fewer runs than the above values.  
The gambler can bet OVER if she thinks the game will have more runs than the above values.  

The user runs the model early in the day and the predictions are:  
Indians vs. White Sox, predicted runs = 7.9  
Cubs vs. Pirates, predicted runs = 8.2  
Rockies vs. Reds, predicted runs = 11.9  

The best betting opportunity for April 10 is the bet the OVER on Rockies vs. Reds.  

If the game has 11 or more runs, the gambler wins.  
If the game has 10 or fewer runs, the gambler loses.  
Bets pay even money, so a $100 bet wins $100.  

The reason the gambler must win more than 55 percent of wagers is the bookie charges a commission to make the wager.  



 



