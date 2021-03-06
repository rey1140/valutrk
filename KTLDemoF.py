import streamlit as st 
import plotly.express as px 
import pandas as pd 
#import cufflinks as cf 
import seaborn  as sns 
import numpy as np 
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
#from scipy import stats 
#import base64
#from PIL import Image
#import json
#import urllib.request
#import hashlib

html_temp = """
        <body style="background-color:blue;">
        <div style="background-color:blue;padding:16px">
        <h2 style="color:white;text-align:center;">ValuTrk Data Analysis </h2>
        </div>
        </body>
    """
st.markdown(html_temp, unsafe_allow_html=True)

#Title
#st.title("VALUTRK Data Analysis Demo")

#Sidebar
st.sidebar.subheader("Spend report")

#Setup
uploaded_file = st.sidebar.file_uploader(
	label="Upload Files 200mb max size:CSV ",
	type=['csv','xlsx'])


global df 
if uploaded_file is not None:
	file_details = {"filename":uploaded_file.name, "filetype":uploaded_file.type,"filesize":uploaded_file.size}
	st.write(file_details)
	f_name = file_details["filename"]
	print(uploaded_file)
	print("Hello")
	try:
		df = pd.read_csv(uploaded_file)
		st.write(f_name)
		if  f_name == "EtsySoldOrders2020.csv":
			df[['Kyear','Kmonth','Kday']]=df['Sale Date'].str.split('-',expand=True)
			df['Sale Date'] = pd.to_datetime(df['Sale Date'])
			df['Day of Week'] = df['Sale Date'].dt.day_name()
			df = pd.melt(df, id_vars=['Order total','Day of Week','Delivery Country','Kmonth'], 
				value_vars=['Discount Amount','Delivery Discount','Delivery','Sales tax'],var_name = ['Expense'])
	
		elif	f_name == "ChitChat Export.csv":
				df[['Kyear','Kmonth','Kday']]=df['ship_date'].str.split('-',expand=True)
				df['ship_date'] = pd.to_datetime(df['ship_date'])
				df['Day of Week'] = df['ship_date'].dt.day_name()
				df = pd.melt(df, id_vars=['purchase_amount','carrier','weight','postage_type','return_country_code','Day of Week','Kmonth'], 
					value_vars=['delivery_fee','insurance_fee','postage_fee','federal_tax','provincial_tax'],
					var_name = 'Logistic_Type',value_name='Shipment Fees')
	
		elif	f_name == "EtsyListingsDownload.csv":
				df[['Kyear','Kmonth','Kday']]=df['Sale Date'].str.split('-',expand=True)
				df['Sale Date'] = pd.to_datetime(df['Sale Date'])
				df['Day of Week'] = df['Sale Date'].dt.day_name()
				df = pd.melt(df, id_vars=['Delivery City','Delivery State','Delivery Country','Order Value','Order total','Order Net','value','Day of Week','Kmonth'], 
					value_vars=['Order Value','Delivery','Sales Tax','Discount Amount','Delivery Discount'],
					var_name = 'Calculated Total',value_name='Other Expense')



	except Exception as e:
		print(e)
		df = pd.read_excel(uploaded_file)





	global numeric_columns
	try:
#	df = pd.melt(df, id_vars=['Order total','Day of Week','Delivery Country','Kmonth'], value_vars=['Discount Amount','Delivery Discount','Delivery','Sales tax'])
		st.write(df)
#	numeric_columns = list(df.select_dtypes(['float','int']).columns)
		numeric_columns = list(df.columns)
	except Exception as e:
		print(e)
		st.write("Please upload file to the application.")

#add a select widget to teh side bar
chart_select = st.sidebar.selectbox(
	label = "Select the chart type",
	options = ['Scatterplots','Violinplots','Barplots','Boxplots','Lineplots','Jointplots','lmplot','Forecasting']
	)



if chart_select == 'Scatterplots':
	st.sidebar.subheader("Settings:x=Order total y=value Delivery County")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		sns.relplot(x=x_values, y=y_values, hue = Z_values,data=df,height = 8, aspect = 1.3)
		plt.title("Keeteelee Scatter Plot Expense Breakdown by Delivery Country")
		st.pyplot()
	except Exception as e:
		print(e)

if chart_select == 'Violinplots':
	st.sidebar.subheader("Settings:x=DayofWeek y=Order total z=Delivery Country ")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		sns.catplot(x=x_values, y=y_values, hue = Z_values,data=df,kind='violin',Legend = True, height=8,aspect=1.3)
		plt.title("Keeteelee Violin Plot Order Total by Country with distribution-line")
		st.pyplot()
	except Exception as e:
		print(e)

if chart_select == 'Barplots':
	st.sidebar.subheader("Settings:x=DayofWeek y=Order total z Delivery Country")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		plt.figure(figsize=(12,8))
		sns.barplot(x=x_values, y=y_values, hue = Z_values,data=df)
		plt.title("Keeteelee BarPlot Order Total by Country with mean-line")
		st.pyplot()
	except Exception as e:
		print(e)


if chart_select == 'Boxplots':
	st.sidebar.subheader("Settings:x=DayofWeek y=Order total z Delivery Country")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		plt.figure(figsize = (12,8))
		sns.boxplot(x=x_values, y=y_values, hue = Z_values,data=df)
		plt.title("Keeteelee BoxPlot Order Total by Country with mean-line")
		st.pyplot()
	except Exception as e:
		print(e)


if chart_select == 'Jointplots':
	st.sidebar.subheader("Settings:x=Order total y=value z=Delivery Country")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		sns.jointplot(x=x_values, y=y_values,data=df, kind = 'reg',height = 10)
		#plt.title("Keeteelee JointPlot Order Total by Country with mean-line")
		st.pyplot()
	except Exception as e:
		print(e)


if chart_select == 'lmplot':
	st.sidebar.subheader("Settings:x=Order total y=value z=Delivery Country")
	try:
		x_values = st.sidebar.selectbox('X axis',options=numeric_columns)
		y_values = st.sidebar.selectbox('Y axis',options=numeric_columns)
		Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)

		st.set_option('deprecation.showPyplotGlobalUse', False)
		sns.lmplot(x=x_values, y=y_values, hue = Z_values,data=df, markers=['o','^'])
		plt.title("Keeteelee LMPlot Order Total by Country with mean-line")
		st.pyplot()
	except Exception as e:
		print(e)

if chart_select == 'Forecasting':
	st.sidebar.subheader("Settings:")
	try:
		X = df.iloc[:, :-1].values
		y = df.iloc[:, -1].values
		#X = st.sidebar.multiselect('Features',options = feature_columns)
		#y = st.sidebar.selectbox('Label', options = label_columns)
		# Z_values = st.sidebar.selectbox('Z category', options=numeric_columns)
		
		print(X)
		# Encoding categorical data		
		from sklearn.compose import ColumnTransformer
		from sklearn.preprocessing import OneHotEncoder
		ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3])], remainder='passthrough')
		X = np.array(ct.fit_transform(X))
		print(X)
		st.subheader("R&D Spend(3) vs Administrative Spend(4) vs Marketing Spend(5)")
		st.line_chart(X)
		# Splitting the dataset into the Training set and Test set
		from sklearn.model_selection import train_test_split
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

		# Training the Multiple Linear Regression model on the Training set
		from sklearn.linear_model import LinearRegression
		regressor = LinearRegression()
		regressor.fit(X_train, y_train)

		# Predicting the Test set results
		y_pred = regressor.predict(X_test)
		np.set_printoptions(precision=2)
		dfF = np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1)
		st.write(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))
		st.subheader("Yearly Profit Prediction(1) vs Actual (0)")
		st.line_chart(dfF)
	
		
	except Exception as e:
		print(e)








