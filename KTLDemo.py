import streamlit as st 
import plotly.express as px 
import pandas as pd 
#import cufflinks as cf 
import seaborn  as sns 
import numpy as np 
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
#from scipy import stats 



#Title
st.title("Keeteelee Studio Data Analysis")

#Sidebar
st.sidebar.subheader("Spend report")

#Setup
uploaded_file = st.sidebar.file_uploader(
	label="Upload Files 200mb max size:EtsySoldOrders2020.csv ",
	type=['csv','xlsx'])


global df 
if uploaded_file is not None:
	print(uploaded_file)
	print("Hello")
	try:
		df = pd.read_csv(uploaded_file)
		#if uploaded_file == "EtsySoldOrders2020.csv":
		df[['Kyear','Kmonth','Kday']]=df['Sale Date'].str.split('-',expand=True)
		df['Sale Date'] = pd.to_datetime(df['Sale Date'])
		df['Day of Week'] = df['Sale Date'].dt.day_name()
		df = pd.melt(df, id_vars=['Order total','Day of Week','Delivery Country','Kmonth'], value_vars=['Discount Amount','Delivery Discount','Delivery','Sales tax'])
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
	options = ['Scatterplots','Violinplots','Barplots','Boxplots','Lineplots','Jointplots','lmplot']
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
