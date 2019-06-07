# Modeling methodology

# Each day, 49 randomly selected random forest models are selected.
# The best one (based on lowest CV R-Sq) is selected and the day's baseball predictions are scored.

# Since predicting baseball scores is nearly impossible, I've taken this as the "best" we can do.
# 49 models takes about 10 minutes on EC2 2XL instance

tree_start = 200
tree_stop = 3000
tree_jump = 10
max_features = ['auto', 'sqrt']
depth_start = 10
depth_stop = 110
depth_num = 11
min_samples_split = [2, 3, 5, 7, 9, 11]
min_samples_leaf = [1, 2, 3, 4, 5]
n_iter = 49
cross_val = 5
verbose = 0
n_jobs = -1
