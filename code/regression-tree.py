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

import numpy as np
import pandas
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
from sklearn.cross_validation import cross_val_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model
import statsmodels.api as sm
import math
from statsmodels.stats.diagnostic import het_breuschpagan

# Create the dataset
rng = np.random.RandomState(1)

# Import the data
DataExcel = pandas.read_excel('IndustrialData.xlsx')
DataExcel['inc_per_capita'] = np.log(DataExcel['inc_per_capita'])
DataExcel['own_price'] = np.log(DataExcel['own_price'])
DataExcel['compe_price'] = np.log(DataExcel['compe_price'])
DataExcel['pro_exp'] = np.log(DataExcel['pro_exp'])
DataExcel['Annual_Production_Of_Mustard_Seeds'] = np.log(DataExcel['Annual_Production_Of_Mustard_Seeds'])
DataExcel['demand_Maa'] = np.log(DataExcel['demand_Maa'])
IndVariable = "own_price"
IndVariable2 = 'compe_price'
IndVariable3 = 'inc_per_capita'
IndVariable4 = 'pro_exp'
IndVariable5 = 'Annual_Production_Of_Mustard_Seeds'
MaxDepth = 5

# SecondRegressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),n_estimators=300, random_state=rng)
SecondRegressor = DecisionTreeRegressor(max_depth=MaxDepth, min_samples_split=2, min_samples_leaf=1, max_features=None)
SecondRegressor.fit(DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]], DataExcel['demand_Maa'])

# # Visualizing the decision tree
# graph = Source(tree.export_graphviz(SecondRegressor, out_file=None, feature_names=[IndVariable,IndVariable2, IndVariable3, IndVariable4]))
# graph.format = 'png'
# graph.render('dtree_render2',view=True)

# Cross Validation Checkings
Scores = abs(cross_val_score(SecondRegressor, DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]], DataExcel['demand_Maa'], scoring="r2", cv=10))
y_actual = DataExcel['demand_Maa']
y_pred = SecondRegressor.predict(DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]])
Residuals = abs(y_actual - y_pred)

print("MSE Average:" + str(np.mean(Scores)))
print("The new score is: " + str(SecondRegressor.score(DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]],DataExcel['demand_Maa'])))
print("Average demands:"  + str(np.mean(DataExcel['demand_Maa'])))
print("Percentage MSE: " + str(np.mean(Scores)/np.mean(DataExcel['demand_Maa'])))
print("-----------------------------------------------")
print(SecondRegressor.feature_importances_*100)
print("-----------------------------------------------")
r2 = r2_score(y_true=y_actual,y_pred=y_pred)
print("The R Squared is: " + str(r2))
AIC, BIC = AICCalc(y_actual, y_pred, 5)
print("The AIC is: " + str(AIC))
print("The BIC is: " + str(BIC))
print("-----------------------------------------------")
Res, lm_pvalue, fvalue, pvalue = het_breuschpagan(Residuals, DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]])
print("P Value of the Test: " + str(pvalue))
print("-----------------------------------------------")
# Computing the adjusted R squared
RAdjusted = 1-(((1-r2)*len(DataExcel['demand_Maa'])/(len(DataExcel['demand_Maa'])-5-1)))
print("The adjusted R squared is: " + str(RAdjusted))


def AICCalc (Y_Actual, Y_Predicted, N_Variables):
    res = Y_Actual - Y_Predicted
    SSE = sum(res**2)
    AIC = 2*N_Variables - 2*math.log(SSE)
    BIC = len(Y_Actual)*math.log(SSE/len(Y_Actual)) + N_Variables*math.log(len(Y_Actual))
    return AIC, BIC