# finomena
Kaggle: BNP Paribas Cardif Claims Management

Instructions:
1. Need to have python SciPy stack. Use the following command to get it:
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
2. Need Python 64-bit
3. Run from the command line using 'python trees.py'
4. The train.csv & test.csv file should be in the same directory as the trees.py file

Methodology:

1. Preprocessing of the data was required as it had various alphabetical features
2. All uninitialised entries were set to 0
3. All alphabetical variables were converted to corresponding integers
4. Skipped quite some features as they were non convertible
5. Divided the data into Training and Validation data
6. Tried Decision trees and Random Forest on the data
7. Achieved minimum logloss of .5955 on validation set

TUNING DECISION TREES:
Finding the right depth for decision tree:
Depth, Train Accuracy, 	Validation Accuracy
[[5, 76.632222222222225, 76.431890136096385],
[6, 76.663333333333341, 76.35376834834095],
[7, 76.797777777777782, 76.781382344475972], 
[8, 76.99777777777777, 76.707372229760281],
[9, 77.276666666666671, 76.645697134163896],
[10, 77.733333333333334, 76.563463673368688],
[11, 78.245555555555555, 76.246864849307187],
[12, 78.786666666666676, 76.049504543398712],
[13, 79.468888888888884, 75.342296780560019],
[14, 80.291111111111107, 75.116154763373217]]

TUNING RANDOM FOREST:
FINDING THE RIGHT PARAMETERS FOR RANDOM FOREST
PARAMS: n_estimators, max_depth
N = [10,15,20,25,30]
MD = [5,7,9,11,13,15]
yields N=25, MD=15 as best
Then tried, 
N = [24,25,26]
MD = [14,15,16,17]
which also yielded N=25 and MD=15
