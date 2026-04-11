# -*- coding: utf-8 -*-

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import os
import glob
merged_df=pd.read_csv("/content/drive/MyDrive/ESDA/econ/outlier_removed_merged")
merged_df.head()

import numpy as np
import statsmodels.api as sm

# Suppose df has:
#   'Date' - a datetime column (format: dd.mm.yyyy or similar)
#   'Price' - the electricity price

# 1) Parse and set date if not already done
merged_df['Datum von'] = pd.to_datetime(merged_df['Datum von'], format='%d.%m.%Y')

# 2) Identify seasonal patterns
#    - day of week (Monday=0, Sunday=6)
#    - month (January=1, December=12)
merged_df['DayOfWeek'] = merged_df['Datum von'].dt.dayofweek  # 0=Monday, ..., 6=Sunday
merged_df['Month'] = merged_df['Datum von'].dt.month         # 1=January, ..., 12=December
merged_df['Year'] = merged_df['Datum von'].dt.year        # 1=January, ..., 12=December
# 3) Create dummy variables
#    To avoid the dummy variable trap, drop the first category in each set
day_dummies = pd.get_dummies(merged_df['DayOfWeek'], prefix='Day', drop_first=True)
month_dummies = pd.get_dummies(merged_df['Month'], prefix='Month', drop_first=True)
year_dummies = pd.get_dummies(merged_df['Year'], prefix='Year', drop_first=True)
# 4) Combine dummies into your design matrix (X)
#    You could also include other regressors if you want
X = pd.concat([day_dummies,month_dummies,year_dummies], axis=1)
# X = sm.add_constant(X)  # add an intercept term

y = merged_df['Deutschland/Luxemburg [€/MWh] Berechnete Auflösungen']

# 5) Regress Price on the seasonality dummies
model = sm.OLS(y, X).fit()

# 6) Get the residuals: these are your seasonally adjusted prices
merged_df['Price_Adjusted'] = model.resid

# 7) Check or plot the residuals
print(merged_df['Price_Adjusted'].head())

# 8) (Optional) Run ADF on the adjusted series
from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(merged_df['Price_Adjusted'])
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])
print("Test Critical Values: :", adf_result[4])

from matplotlib import pyplot
import matplotlib.pyplot as plt


# Plot the data with years on the x-axis
plt.figure(figsize=(14, 6))
plt.plot(merged_df['Datum von'],merged_df['Price_Adjusted'])
plt.xlabel('Year')
plt.ylabel('Wind Power Generation(MW)')
plt.title('Daily Wind Generation Total Seasonality Adjusted')
plt.grid(True)
plt.show()

df_wind=pd.read_csv("/content/drive/MyDrive/ESDA/econ/daily_wind_generation_total.csv")
df_wind.head()

# 2) Identify seasonal patterns
#    - day of week (Monday=0, Sunday=6)
#    - month (January=1, December=12)

df_wind['Date'] = pd.to_datetime(df_wind['date'], format='%Y-%m-%d')
df_wind.set_index('Date', inplace=True)
df_wind['Month'] = df_wind.index.month            # e.g. 1 to 12
df_wind['DayOfWeek'] = df_wind.index.dayofweek    # Monday=0 ... Sunday=6

# 3) Create dummy variables
#    To avoid the dummy variable trap, drop the first category in each set
day_dummies = pd.get_dummies(df_wind['DayOfWeek'], prefix='Day', drop_first=True)
month_dummies = pd.get_dummies(df_wind['Month'], prefix='Month', drop_first=True)

# 4) Combine dummies into your design matrix (X)
#    You could also include other regressors if you want
X = pd.concat([day_dummies,month_dummies], axis=1)
# X = sm.add_constant(X)  # add an intercept term

y = df_wind['Wind Total']

# 5) Regress Price on the seasonality dummies
model = sm.OLS(y, X).fit()

# 6) Get the residuals: these are your seasonally adjusted prices
df_wind['wind_Adjusted'] = model.resid

# 7) Check or plot the residuals
print(df_wind['wind_Adjusted'].head())

# 8) (Optional) Run ADF on the adjusted series
from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(df_wind['wind_Adjusted'])
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])
print("Test Critical Values: :", adf_result[4])

# Plot the data with years on the x-axis
plt.figure(figsize=(14, 6))
plt.plot(df_wind['wind_Adjusted'])
plt.xlabel('Year')
plt.ylabel('Wind Power Generation(MW)')
plt.title('Daily Wind Generation Total Seasonality Adjusted')
plt.grid(True)
plt.show()

# df_wind.head()
merged_df['wind_Adjusted']=df_wind['wind_Adjusted'].values
merged_df.head()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX



# Separate the dependent (endog) variable and the exogenous (exog) variable
endog = merged_df['Price_Adjusted'][0:730]
exog = merged_df['wind_Adjusted'] [0:730] # if you have multiple exogenous vars, include them here

# ----------------------------------------------------------------------------
# 2) Determine the best AR lag p by minimizing AIC
#    We fix d=0 and q=0, so it's effectively an AR(p) with exogenous regressors
# ----------------------------------------------------------------------------
p_candidates = range(1, 14)  # for example, try p from 1 to 13

best_p = None
best_aic = float('inf')
best_model = None

for p in p_candidates:
    try:
        # Fit ARMAX as SARIMAX with order=(p,0,0)
        model = SARIMAX(endog=endog, exog=exog, order=(p, 0, 0),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        results = model.fit(disp=False)

        if results.aic < best_aic:
            best_aic = results.aic
            best_p = p
            best_model = results
    except Exception as e:
        # If the model fails to converge for some p, just skip it
        print(f"Warning: AR({p}) model failed to fit.\nError: {e}")
        continue

print(f"Best AR lag (p) according to AIC is: {best_p}")
print(f"Best AIC: {best_aic:.2f}")

# ----------------------------------------------------------------------------
# 3) Final Model with p=7 (assuming that's indeed the best)
# ----------------------------------------------------------------------------
print("\nSummary of the best ARMAX model:")
print(best_model.summary())

# ----------------------------------------------------------------------------
# 4) Diagnostics: Fitted values, Residuals, Plots
# ----------------------------------------------------------------------------
merged_df['Fitted'] = best_model.fittedvalues
merged_df['Residuals'] = best_model.resid

# # Plot actual Price vs. Fitted
# df[['Price', 'Fitted']].plot()
# plt.title(f'AR({best_p}) Model: Actual vs Fitted Electricity Prices')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.show()

# # Histogram of residuals
# df['Residuals'].plot(kind='hist', bins=30)
# plt.title('Histogram of Residuals')
# plt.show()

# Autocorrelation of residuals can be further checked with statsmodels ACF/PACF:
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(merged_df['Residuals'].dropna())
plt.title('ACF of Residuals')
plt.show()

plot_pacf(merged_df['Residuals'].dropna())
plt.title('PACF of Residuals')
plt.show()
