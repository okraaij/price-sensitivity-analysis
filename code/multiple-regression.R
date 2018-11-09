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

library(car)
library(stargazer)
library(readxl)

IndustrialData <- read_excel("~/Downloads/IndustrialData.xlsx", 
                             col_types = c("blank", "numeric", "numeric", 
                                           "numeric", "numeric", "numeric", 
                                           "numeric"))
View(IndustrialData)

# Transform the amended dataset by taking natural logs of the predictor and dependent variable
IndustrialData_Log <- log(IndustrialData)

# Load all predictors in demand function and print a summary
lm.fit = lm(demand_Maa ~ .*., data = IndustrialData)
stargazer(lm.fit, type="text")

# Remove one predictor per iteration (largest p-value)
lm.fit1 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds, data = IndustrialData)
lm.fit2 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustardplt_Seeds-compe_price:inc_per_capita,
             data = IndustrialData)
lm.fit3 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp,
             data = IndustrialData)
lm.fit4 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp,
             data = IndustrialData)
lm.fit5 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita,
             data = IndustrialData)
lm.fit6 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds,
             data = IndustrialData)
lm.fit7 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds-inc_per_capita:pro_exp,
             data = IndustrialData)
lm.fit8 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds-inc_per_capita:pro_exp-pro_exp:Annual_Production_Of_Mustard_Seeds,
             data = IndustrialData)
lm.fit9 = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds-inc_per_capita:pro_exp-pro_exp:Annual_Production_Of_Mustard_Seeds-compe_price:Annual_Production_Of_Mustard_Seeds,
             data = IndustrialData)

# Final version of the log-log demand function, with all predictors being statistically and practically significant
Transformed = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds-inc_per_capita:pro_exp-pro_exp:Annual_Production_Of_Mustard_Seeds-compe_price:Annual_Production_Of_Mustard_Seeds-Annual_Production_Of_Mustard_Seeds,
              data = IndustrialData_Log)

# Final version of the demand function without a log-log transformation, with all predictors being statistically and practically significant
Non_Transformed = lm(demand_Maa ~ .*.-own_price:Annual_Production_Of_Mustard_Seeds-compe_price:inc_per_capita-own_price:pro_exp-compe_price:pro_exp-own_price:inc_per_capita-inc_per_capita:Annual_Production_Of_Mustard_Seeds-inc_per_capita:pro_exp-pro_exp:Annual_Production_Of_Mustard_Seeds-compe_price:Annual_Production_Of_Mustard_Seeds-Annual_Production_Of_Mustard_Seeds,
              data = IndustrialData)

# Compare the two models
stargazer(Transformed, Non_Transformed, type="text")

