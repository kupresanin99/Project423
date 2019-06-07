# Developer: Joe Kupresanin
# QA: Max Holiber

Instructions to run app in another environment at the bottom of this page. 

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Instructions](#Instructions)

<!-- tocstop -->

## Project Charter 

**Vision**:  
With legalized sports betting, there is a market for selling predictive services to gamblers.  
Main point:  help the bettor consistently beat the MLB over / under runs totals offered by the bookie.  

For each baseball game, the bookie sets an OVER / UNDER line for total runs scored (example below).  
The bettor can wager on OVER if s/he thinks more runs will be scored than the bookie's line.  
Likewise, the bettor can wager on UNDER if s/he thinks fewer runs will be scored than the bookie's line.  

Bets pay even money (less a 10 percent commission), so the bettor must win 55 percent of bets to break even.  


**Mission**:  
Each day, the bettor can pull from the web app the runs total predictions for the slate of today's MLB games.  
These predictions can be used to make educated bets.  

**Success Criteria**:  

**Statistical Criteria**:  
Root mean square error, from the regression, boosted tree, or random forest final model.  
The model will produce a numerical prediction, "Total Runs Scored" for each MLB game today.  
Hope to keep RMSE (test) under 1 run, but not sure at this point.  

**Business Criteria**:  
To win at sports gambling, the bettor needs to win more than 55 percent of wagers placed.  
From deployment through the end of the 2019 MLB regular season, I will use the model and track a running total of wagers won.  
If the app can beat the bookie over the course of the remainder of the baseball season, we will consider it a success.  

**Example Scenario**:  
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

The best betting opportunity for April 10 is to bet the OVER 8.5 on Rays vs. White Sox.  

If the game has 9 or more runs, the gambler wins.  
If the game has 8 or fewer runs, the gambler loses.  
Bets pay even money, so a $100 bet wins $100.  

The reason the gambler must win more than 55 percent of wagers is the bookie charges a commission to make the wager.  


## Backlog

**Removed on June 6**
- Check the other branches if needed.


## Instructions

**0. Connect to your EC2 instance on AWS**

	It is suggested that the graders switch to a t2.2XL instance for this project.
	Training on t2.2XL should take ~ 10 minutes.  
	Training on micro might take ~ 10 hours.  
	All other steps running smoothly on micro, for what it's worth.  

**1. Clone the master branch of this GitHub repo.  In terminal, cd into project directory.**

**2. Create a conda environment, my_env = name of your new environment**
	
	conda create --name my_env python=3.7
	conda activate my_env
	pip install -r requirements.txt

**3.  Move three data files from Joe's S3 bucket to your S3 bucket**

	1.  From the terminal, set your AWS environment variable:
		a.  export AWS_ACCESS_KEY_ID=
		b.  export AWS_SECRET_ACCESS_KEY=
	
	2.  From the terminal, edit the config.py and update the following:
		(Remove kupebaseball and replace with destination S3 bucket)
		(Yes, please change them both)
		a. my_bucket = "" 
		b. DEST_BUCKET = "" 
		
	3.  Run `python s3.py` in the terminal from the project directory  
	
	4.  Navigate to S3 to see if three files have been transferred to your bucket:
		a.  "model_data"
		b.  "predictions.csv"
		c.  "results.csv"
		
**4. Initialize the database in RDS**

	1.  Set your MYSQL environment variables by running the following commands in the terminal:
		export MYSQL_USER="" 
		export MYSQL_PASSWORD=""
		export MYSQL_HOST="" 
		export MYSQL_PORT=""
	
	2.  Run `python Create_RDS_DB.py` to create the MySQL database in RDS
		Populated tables Predictions and Reports will exist with MLB model results from the 2019 season
	
**5. Create the webpage**

	1.  Run `python app.py` to create the public-facing webpage.
	2.  Visit the IPv4 Public IP found on the EC2 console. Add ":3000" to your IP address to view the page.
	3.  The graders should see gambling predictions through June 10th on this page.  
	
**6. Train the model for today's games**

	1.  Your EC2 instance should be switched to t2.2XL - (10 minutes training time)
	2.  If the EC2 instance is micro, it might take 10 hours.  
	3.  If you switch EC2 to 2XL, be sure to switch back so you are not charged more than a few pennies.  
	4.  Run `python main_menu.py` from the command line.  
	5.  Select option 1 for Admin Mode.
	6.  Select option 1 for API pull (enter today's date).
		a.  The API credentials are coded into the config.py file (throwaway account).
		b.  For ease, the program uses those credentials (since you are grading 46 projects). 
		c.  I realize these should be exported in EC2 and the graders should have their own keys.  
	7.  Select option 2 to run today's model (enter today's date) (about 10 minutes on 2XL).
	8.  Upon training completion, you must enter the gambling lines manually.
		a.  You can just make up numbers here - it doesn't affect the predictions.
		b.  If you'd like to input actual lines, I used http://www.vegasinsider.com/mlb/scoreboard/
		c.  Entering the gambling lines has no impact on the predictions "customers" can view on the web.
	9.  Once gambling lines are input, the website will be updated with today's predictions.  
	10.  Before training and entering lines, the graders will see results through 6/10 on my webpage. 
	11.  After training and enter lines, graders will see one additional day of predictions on the web.  
	
**Notes**

	1.  I found some CSS a few weeks ago to make my html table look pretty.  Forgot the source.  
	2.  All other code is original.  
	3.  Logging and testing made it to the icebox.  ¯\_(ツ)_/¯
	4.  The model is repeatable on any given day - seeding with datetime.now().day().  
	5.  At this point, predictions are available publicly to the customer on the webpage.
	6.  At this point, reports are available privately to the developer on EC2.  