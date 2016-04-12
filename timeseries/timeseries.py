### START ###

""" 
Apply a ARIMA model on a CSV timeseries file.
Fit a linear model and provide descriptive statistics.
Preliminary functions to detrend, transform, and fit lags (ACF/PACF).
Visualize a fitted ARIMA plot with out-of-sample predictions on timeseries. 
"""

# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as datetime 
import os
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from sklearn import linear_model

# Seaborne graph template
sns.set(style='ticks', palette='Set2')
sns.despine()

# Get the directory
print('Where is the main directory?')
main_dir = input()
os.chdir(main_dir)

# Specify CSV file, format time and Y variable
print('What is the CSV filename? (with extension)')
csv_file = input()
data = pd.read_csv(csv_file)
headers = data.columns.values
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
print(data.head(1))
print('What is the time variable? (e.g. Years/month/year)')
index = input()
print('What is the time variable format? (e.g. %Y,%m, %Y-%m)')
frmt = input()
print('What header is the main Y variable? (e.g. 0, 1, 2?)')
Y = int(input())
print('What is the name of the main Y variable?')
Y_name = input()

ts = pd.read_csv(csv_file, parse_dates='Year', index_col=index,date_parser=dateparse)
ts.reset_index(inplace=True)
ts.dropna(inplace=True)
ts[headers[0]] = pd.to_datetime(ts[headers[0]], format=frmt)
ts = ts.set_index(headers[0])
timeseries = ts[headers[Y]] # make sure Y is in header 1

# Create new file
folder = csv_file.replace(".csv", "")
path = (main_dir + folder + "/")
if not os.path.exists(path):
	os.makedirs(path)
os.chdir(path)	

# Data description 
def desc_stat(data):
	print ('\nData Types: \n\n',data.dtypes)
	print ('\nHead: \n\n' ,ts.head())
	print ('\nBasic Statistics: \n\n' ,data.describe().round(2))

# Linear Model
def linear(data):
	# Regression
	x = []
	y = []
	for i in range(len(data)):
		x.append(i)
	for p in data[headers[1]]: 
		y.append(p)
	x = np.array(x)
	y = np.array(y)
	x = x.reshape(-1, 1)
	y = y.reshape(-1, 1)
	x_line = np.column_stack((x, x**2)) 
	x_cons = sm.add_constant(x_line) 
	model = sm.OLS(y, x_cons)
	results = model.fit()
	print (results.summary())
	print ('Coefficients: ', results.params) # Save to pfd
	print ('Standard errors: ', results.bse)
	print ('R2: ', results.rsquared)
	# Plot
	prstd, iv_l, iv_u = wls_prediction_std(results)
	fig, ax = plt.subplots()
	title = "Linear Regression" ,headers[1]
	plt.title(title)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.get_xaxis().tick_bottom()    
	ax.get_yaxis().tick_left()  
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
	                labelbottom="on", left="off", right="off", labelleft="on")
	ax.plot(x, y, label="data")
	ax.plot(x, results.fittedvalues, 'r--.', label="OLS")
	ax.plot(x, iv_u, 'c--')
	ax.plot(x, iv_l, 'c--')
	ax.legend(loc='best')
	plt.savefig('linear.png', bbox_inches="tight")

def stationarity(timeseries):
	#Determing rolling statistics
	rol_mean = timeseries.rolling(window=12).mean()
	rol_std = timeseries.rolling(window=12).std()
	#Plot rolling statistics:
	fig, ax = plt.subplots()
	plt.grid(color='grey', which='major', axis='y', linestyle='--')
	plt.plot(timeseries, color='blue', label='Original', linewidth=1.25)
	plt.plot(rol_mean, color='red', label='Rolling Mean', linewidth=1.25)
	plt.plot(rol_std, color='black', label = 'Rolling Std', linewidth=1.25)
	plt.legend(loc='best')
	title = headers[1], data[index].iloc[0], '-' ,data[index].iloc[-1]
	plt.title(title)
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
		            labelbottom="on", left="off", right="off", labelleft="on")
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.xaxis.set_ticks_position('bottom') 
	fig.title = ('stationarity.png')
	fig.savefig(fig.title, bbox_inches="tight")
	#Perform Dickey-Fuller test:
	print ('Results of Dickey-Fuller Test:\n')
	df_test = adfuller(timeseries, autolag='AIC')
	df_output = pd.Series(df_test[0:4], index=['Test Statistic','p-value','#Lags Used','No. of Observations Used'])
	for key,value in df_test[4].items():
	    df_output['Critical Value (%s)'%key] = value
	print (df_output.round(3))

# Transform to Log
def log_trans(ts):
	ts_log = np.log(ts)
	fig, ax = plt.subplots()
	plt.grid(color='grey', which='major', axis='y', linestyle='--')
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.get_xaxis().tick_bottom()    
	ax.get_yaxis().tick_left()    
	plt.yticks(fontsize=14)
	plt.xticks(fontsize=14)  
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
	                labelbottom="on", left="off", right="off", labelleft="on")
	plt.xlabel("Year", fontsize=14)
	plt.title("Log Transformation", fontsize=15) 
	for n in enumerate(ts_log.columns):
		plt.plot(ts_log[n[1]], label=n[1], linewidth=1.25)
	plt.legend(loc='best')
	plt.tight_layout()
	fig.savefig('log_trans.png', bbox_inches="tight")

# Difference to remove trend
def differencing(timeseries):
	diff_ts = timeseries - timeseries.shift()
	diff_ts.dropna(inplace=True)
	stationarity(diff_ts)

# Decomposition plot
def decomp(ts):
	decomposition = seasonal_decompose(ts[Y_name])
	fig = decomposition.plot() 
	plt.tight_layout()
	fig.savefig('decomp.png', bbox_inches="tight")
	trend = decomposition.trend
	seasonal = decomposition.seasonal
	resid = decomposition.resid

# ACF and PACF for Lags
def corrfunc(timeseries):
	diff_ts = timeseries - timeseries.shift()
	diff_ts.dropna(inplace=True)
	ts_acf = acf(diff_ts, nlags=20)
	ts_pacf = pacf(diff_ts, nlags=20, method='ols')
	#Plot ACF and PACF:
	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(211)
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
		                labelbottom="on", left="on", right="off", labelleft="on")
	fig = sm.graphics.tsa.plot_acf(timeseries.values.squeeze(), lags=20, ax=ax1)
	plt.title('ACF', fontsize=15)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(timeseries, lags=20, ax=ax2)
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
		                labelbottom="on", left="on", right="off", labelleft="on")
	plt.xlabel("Lags", fontsize=14) 
	plt.title('PACF', fontsize=15)
	plt.tight_layout()
	fig.savefig('corrfunc.png', bbox_inches="tight")

# ARIMA Model
def ARMA(timeseries):
	# Input how many lags
	print ('\nHow many AR lags?')
	p = int(input())
	print ('\nHow many MA lags?')
	q = int(input())
	print ('\nDifferenced? Y/N')
	d = 1 if input() == 'Y' else 0
	arma_mod = sm.tsa.ARIMA(timeseries, order=(p, d, q))
	arma_res = arma_mod.fit(trend='nc', disp=-1)
	print (arma_res.summary())
	# Plot ARIMA w/ predictions
	fig, ax = plt.subplots()
	ax = timeseries.ix[1:].plot(ax=ax)
	plt.tick_params(axis="both", which="both", bottom="on", top="off",    
		                labelbottom="on", left="on", right="off", labelleft="on")
	print('When would you like to start forecast? DD-MM-YYY')
	pred_start = (input())
	print('When would you like to stop forecast? DD-MM-YYY (e.g. one year ahead)')
	pred_end = (input())
	arma_res.plot_predict(start=pred_start, end=pred_end, dynamic=False, ax=ax, plot_insample=False)	
	plt.xlabel("Year", fontsize=14) 
	plt.title('ARIMA', fontsize=15)
	plt.tight_layout()
	fig.savefig('arma.png', bbox_inches="tight")

# PROGRAM 
desc_stat(data)
linear(data)
stationarity(timeseries)
log_trans(ts)
differencing(timeseries)
decomp(ts)
corrfunc(timeseries)
ARMA(timeseries)

### END ###



