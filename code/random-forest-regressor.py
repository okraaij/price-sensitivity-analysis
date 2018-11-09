#######################################################################
#   
#   University of Edinburgh Business School
#   MSc Business Analytics
#   Industrial Analytics
#
#   A demand analysis for designing a new pricing strategy based on increased manufacturing costs and market competition
#
#   Please read attached 'Report' file for the analysis and more information
#
#   Copyright© of this project is with the authors
#
#######################################################################

# Import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import cross_val_score
from statsmodels.stats.diagnostic import het_breuschpagan

%matplotlib inline
sns.set(style="white", font_scale=0.9)

# Read dataset and select predictor (X) and target (y)
dataset = pd.read_csv('datasetv2.csv', sep=";")
dataset = pd.DataFrame(dataset, columns=['demand_Maa','own_price','compe_price','inc_per_capita','pro_exp','Annual_Production_Of_Mustard_Seeds'])
y = np.log(dataset['demand_Maa'])
X = np.log(dataset.drop('demand_Maa', axis=1))

# Set up parameters for GridSearch
#param_grid = {"n_estimators": [200, 500, 750], "max_depth": [1,2,3,4,5,6], "max_features": [1, 2, 3, 4], "min_samples_leaf": [1,2,3,4,10], "bootstrap": [True, False]}

# Fit Random Forest Regressor and apply GridSearch to find best hyperparameters
#model = RandomForestRegressor(random_state=0)
#grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
#grid.fit(X, y)

# Output best scores and parameters
print(grid.best_score_)
print(grid.best_params_)

#old
#regressor = RandomForestRegressor(random_state=0, n_estimators=500, max_depth=100, max_features=3, 
                                  #min_samples_leaf=1, bootstrap=True)

# Fit Random Forest Regressor according to best hyperparameters
regressor = RandomForestRegressor(random_state=0, n_estimators=500, max_depth=3, max_features=4, 
                                  min_samples_leaf=1, bootstrap=True)
regressor.fit(X, y)

# Obtain R2 squared and adjusted R-squared
r2 = regressor.score(X,y)
RAdjusted = 1-(((1-r2)*len(dataset['demand_Maa'])/(len(dataset['demand_Maa'])-5-1)))

# Apply 10-fold cross validation
maescores = cross_val_score(regressor, X, y, scoring='neg_mean_absolute_error', cv=10, n_jobs=-1)

# Obtain AIC and BIC value
y_hat = regressor.predict(X)
residuals = y - y_hat
res = het_breuschpagan(residuals, X)
sse = sum(residuals**2)
AIC = 2*4 - 2*np.log(sse)
BIC = 54*np.log(sse/54) + 4*np.log(54)

# Print scores
#print("The Mean Absolute Error of the Random Forest Regressor is " + str(abs(np.mean(maescores))))
print("The R2 squared of the Random Forest Regressor is " + str(r2))
print("The adjusted R2 squared of the Random Forest Regressor is " + str(RAdjusted))
print("The AIC score of the Random Forest Regressor is " + str(AIC))
print("The BIC score of the Random Forest Regressor " + str(BIC))
print("The p-value from the Breuschpagan test is " + str(res))
 
# Plot feature importance
feature_import = pd.DataFrame(data=regressor.feature_importances_, index=['own_price','compe_price','inc_per_capita','pro_exp','Annual_Prod_MSeeds'], columns=['values'])
feature_import.sort_values(['values'], ascending=False, inplace=True)
feature_import.transpose()
feature_import.reset_index(level=0, inplace=True)
sns.barplot(x='index', y='values', data=feature_import, palette='deep')
plt.show()