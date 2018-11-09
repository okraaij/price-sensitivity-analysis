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

# Importing the libraries
import numpy as np
import pandas
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
import xlsxwriter
import math
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Importing the data
DataExcel = pandas.read_excel('IndustrialData.xlsx')

# Setting the variables Names
IndVariable = "own_price"
IndVariable2 = 'compe_price'
IndVariable3 = 'inc_per_capita'
IndVariable4 = 'pro_exp'
IndVariable5 = 'Annual_Production_Of_Mustard_Seeds'
TargetVariable = 'demand_Maa'

# Recording values to keep
LastOwnPrice = DataExcel[IndVariable][53]
LastPriceComp = DataExcel[IndVariable2][53]
LastIncomeCapita = DataExcel[IndVariable3][53]
LastProExp = DataExcel[IndVariable4][53]
LastAnnualProd = 8.0

# Reorganizing the data
Predictors = DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]]
Target = DataExcel[TargetVariable]

# Transforming the dataset
Scaler = StandardScaler()
Scaler.fit(Predictors)
StandardizedData = Scaler.transform(Predictors)
PrincipalComponent = PCA(n_components=4)
PrincipalComponent.fit(StandardizedData)
PCAData = PrincipalComponent.transform(StandardizedData)
Predictors = pandas.DataFrame(data = PCAData, columns = ['PC1', 'PC2', 'PC3', 'PC4'])
# print("Variance Achieved: " + str(round(sum(PrincipalComponent.explained_variance_ratio_)*100,2)))

# Regression Tree
RegressionTree = DecisionTreeRegressor(max_depth=5, min_samples_split=2, min_samples_leaf=1, max_features=None)
RegressionTree.fit(Predictors, Target)

# Random Forest
RandomForest = RandomForestRegressor(random_state=0, n_estimators=500, max_depth=100, max_features=3, min_samples_leaf=1, bootstrap=True)
RandomForest.fit(Predictors, Target)

# Multiple Regression
PredictorsMR = sm.add_constant(Predictors)
MultipleRegression = sm.OLS(Target, PredictorsMR).fit()

# Creating the excel file
Workbook = xlsxwriter.Workbook("PCA - 8Production - 0Increase 23032018.xlsx")
Worksheet = Workbook.add_worksheet("Prediction")

# Adding the headers
Worksheet.write(0, 0, 'Own_Price')
Worksheet.write(0, 1, 'Demand Regression Tree')
Worksheet.write(0, 2, 'Demand Random Forest')
Worksheet.write(0, 3, 'Demand Multiple Regression')
LineExcel = 1

# Setting the initial values
InitialPrice = LastOwnPrice - 10
FirstPrice = InitialPrice
CompetitionPrice = LastPriceComp

# Values to be predicted Machine Learning
FuturePredictors = pandas.DataFrame(DataExcel[[IndVariable, IndVariable2, IndVariable3, IndVariable4, IndVariable5]])
FuturePredictors['compe_price'] = CompetitionPrice
FuturePredictors['inc_per_capita'] = LastIncomeCapita
FuturePredictors['pro_exp'] = LastProExp
FuturePredictors['Annual_Production_Of_Mustard_Seeds'] = LastAnnualProd

# Setting the different prices
for i in range(0, len(FuturePredictors['own_price'])):
    FuturePredictors['own_price'][i] = InitialPrice
    InitialPrice +=1

# Transforming the future predictions data
FutureStandardized = Scaler.transform(FuturePredictors)
FutureComponents = PrincipalComponent.transform(FutureStandardized)

# Predictions
FinalPredictionTree = RegressionTree.predict(FutureComponents)
FinalPredictionRan = RandomForest.predict(FutureComponents)
FutureComponents = sm.add_constant(FutureComponents)
FinalPredictionMR = MultipleRegression.predict(FutureComponents)

# Saving in excel file
for i in range(0, len(FinalPredictionTree)):
    Worksheet.write(i + 1, 0, FirstPrice)
    Worksheet.write(i + 1, 1, FinalPredictionTree[i])
    Worksheet.write(i + 1, 2, FinalPredictionRan[i])
    Worksheet.write(i + 1, 3, FinalPredictionMR[i])
    FirstPrice += 1

# Closing the excel file
Workbook.close()