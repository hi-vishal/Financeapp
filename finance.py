import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews as SN

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
startdate = st.sidebar.date_input('Start Date')
enddate = st.sidebar.date_input("End Date")

data = yf.download(ticker,startdate,enddate)
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricingData, fundamentalData , news = st.tabs(["Pricing Data","Fundamental Data","Top News"])

with pricingData:
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annualReturn = data2['% Change'].mean()*252*100
    st.write('Annual Return is ',annualReturn,'%')
    stddev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stddev*100,'%')
    st.write('Risk Adj. Return is ', annualReturn/(stddev*100))


with fundamentalData:
    key = 'GFOTR7HSM71L8S2Y'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balanceSheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balanceSheet.T[2:]
    bs.columns = list(balanceSheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    incomeStatement = fd.get_income_statement_annual(ticker)[0]
    is1 = incomeStatement.T[2:]
    is1.columns = list(balanceSheet.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cashFlow = fd.get_cash_flow_annual(ticker)[0]
    cf = cashFlow.T[2:]
    cf.columns = list(cashFlow.T.iloc[0])
    st.write(cf)

with news:
    st.header(f"News of {ticker}")
    sn = SN(ticker, save_news=False)
    dfNews = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(dfNews['published'][i])
        st.write(dfNews['title'][i])
        st.write(dfNews['summary'][i])
        titleSentiment = dfNews['sentiment_title'][i]
        st.write(f"Title Sentiments {titleSentiment}")
        newsSentiment = dfNews['sentiment_summary'][i]
        st.write(f"News Sentiments {newsSentiment}")

