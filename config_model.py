# Modeling methodology

# Each day, 49 randomly selected random forest models are selected.
# The best one (based on lowest CV R-Sq) is selected and the day's baseball predictions are scored.

# Since predicting baseball scores is nearly impossible, I've taken this as the "best" we can do.
# 49 models takes about 10 minutes on EC2 2XL instance
# A randomized state has not been set, though should one want the predictions to consistent, this would be needed.

# It is not uncommon for the prediction to be 9.5643 runs, the bookie to have it at 10 runs...
# and for the actual outcome to be 2-1 for 3 runs, or 9-4 for 13 runs, or 11-10 for 21 runs.

# Daily RMSE is about 4.00 runs which means if the prediction is 9.5 runs, outcomes in [1, 17] are not unusual.

# Long story short, if baseball runs were predictable, I'd drop out of MSIA and make $3,000,000 over the summer...
# and retire to Dublin, IE to live a life of wandering the streets, drawing, playing piano, and reading good books.

tree_start = 200
tree_stop = 3000
tree_jump = 10
max_features = ['auto', 'sqrt']
depth_start = 10
depth_stop = 110
depth_num = 11
min_samples_split = [2, 3, 5, 7, 9, 11]
min_samples_leaf = [1, 2, 3, 4, 5]
n_iter = 2
cross_val = 5
verbose = 0
n_jobs = -1
