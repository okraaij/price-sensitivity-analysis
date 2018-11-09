# Price sensitivity analysis

An implementation of a price sensitivity analysis for a fictional oil company that explores the most significant price/demand driving factors and subsequently uses price elasticities to explore the maximum level of price increase possible without losing demand

## Overview

- This repository contains a price sensitivity analysis as part of a project for the MSc Business Analytics at the University of Edinburgh. 
- This project focused on:
  1. What are the most significant demand driving factors for the product? (feature selection)
  2. What is the optimal pricing response/strategy for the company without them compromising their revenues?
- The approach taken:
  - Question 1:
    - Regression Trees (with 10-fold cross-validation), a Random Forest Regressor (with 10-fold cross-validation and hyperparameter tuning using GridSearch) and Multiple Regression (Backward Stepwise Selection, for both log-log and standard data)
    - Multiple Regression was also used to estimate the demand function for the log-log model
  - Question 2:
    - Use the coefficients from the Multiple Regression demand function to analyse the price elasticity of demand
    - Apply Principle Component Analysis (PCA) due to the strong multicollinearity observed in the data and hereby remove strongly correlated predictors
    - Use a new Multiple Regression model to explore the effects of various scenarios on demand and revenue by prediction:
      - Increase or no increase (6% / 0%) of competitors's price
      - Various level of production (6.3 / 5.5 / 8.0 million tonnes) 
      - Various percentual changes in price (0.0% / 3.3% / 5.5% / 6.6%)
- The [implementation](/code/) is provided for the following predictive models:
  - [Regression Tree](/code/regression-tree.py) (Python)
  - [Random Forest Regressor](/code/random-forest-regressor.py) (Python)
  - [Multiple Regression](/code/multiple-regression.R) (R)
  - [Principle Component Analysis and predicting the various scenarios](/code/pca-and-prediction.py) (Python)
