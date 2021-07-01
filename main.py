# Explained the whole app line by line
# If you find any value this do upvote/give a star.

import pandas as pd
import numpy as np
import requests
import json
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

#Adding Logo and Page Name
st.set_page_config(page_title='Stocks Daily',
                   page_icon='📈')

# Initialising the start date and the end date(i.e today).
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Setting the title of the App
st.title("Stocks Daily 📈")
st.write("This app let's you to generate a **live time-series** forecast of FAAMG stocks, **predict** the future price of them(upto 7 years) and also lets you **convert the currecy** as per your needs.")
st.markdown("""The forecasting library used is Facebook's **[Prophet](https://facebook.github.io/prophet/)**.""")
st.markdown("![Gif](https://miro.medium.com/max/620/0*dunTLlei47QWR7NR.gif)")

st.subheader("What Are Stocks? 💲")

with st.beta_expander("Defining Stock Market"):
    st.markdown("The stock market is a market that enables the seamless exchange of buying and selling of company stocks. Every Stock Exchange has its own Stock Index value. The index is the average value that is calculated by combining several stocks. This helps in representing the entire stock market and predicting the market’s movement over time. The stock market can have a huge impact on people and the country’s economy as a whole. Therefore, predicting the stock trends in an efficient manner can minimize the risk of loss and maximize profit.")

with st.beta_expander("Machine learning in stock market"):
    st.markdown("Stock and financial markets tend to be unpredictable and even illogical, just like the outcome of the Brexit vote or the last US elections. Due to these characteristics, financial data should be necessarily possessing a rather turbulent structure which often makes it hard to find reliable patterns. Modeling turbulent structures requires machine learning algorithms capable of finding hidden structures within the data and predict how they will affect them in the future. The most efficient methodology to achieve this is Machine Learning.")
    st.markdown("**Machine learning has the potential to ease the whole process by analyzing large chunks of data, spotting significant patterns and generating a single output that navigates traders towards a particular decision based on predicted asset prices.**")

st.subheader("Know About FAAMG 💸")
with st.beta_expander("What Are FAAMG Stocks?"):
    st.markdown("In finance, “FAAMG” is an acronym that refers to the stocks of five prominent American technology companies: Facebook (FB), Amazon (AMZN), Apple (AAPL), Microsoft (MSFT); and Alphabet's Google (GOOG)")

with st.beta_expander("Understanding FAAMG Stocks"):
    st.markdown('Approximately 3,000 companies (mostly tech companies) trade on the NASDAQ, and the Nasdaq Composite Index, which indicates how the tech sector is faring in the economy. Facebook (FB), Amazon (AMZN), Apple (AAPL), Microsoft (MSFT), and Alphabet (GOOG) accounted for 55% of the NASDAQ’s year-to-date (YTD) gains as of June 9, 2017.')
    st.markdown("FAAMG are termed growth stocks, mostly due to their year-over-year (YOY) steady and consistent increase in the earnings they generate, which translates into increasing stock prices. Retail and institutional investors buy into these stocks directly or indirectly through mutual funds, hedge funds, or exchange traded funds (ETFs) in a bid to make a profit when the share prices of the tech firms go up.")

# Initialising Stock Names.
stocks = ('FB','AMZN', 'AAPL', 'MSFT', 'GOOG')

st.subheader("Let's Jump Straight To Modelling ‍💻")
# A box in streamlit where we can select stocks
selected_stock = st.selectbox('Select Ticker For Prediction', stocks)

# A slider in streamlit which is used to set how many years you want to predict
n_years = st.slider('Select How Many Years You Want To Predict:', 1, 7)

# 1 year=365 days so if n_years then n_years*365 days.
period = n_years * 365

# st.cache runs the function and stores the result in a local cache.
# Then, next time the cached function is called,
# if none of these components changed,
# Streamlit will just skip executing the function altogether
# and, instead, return the output previously stored in the cache.
@st.cache
#ticker is the stock name
def load_data(ticker):
    #Downloading the data from start to today of the selected stock.
    data = yf.download(ticker, START, TODAY)
    #resetting the index.
    data.reset_index(inplace=True)
    return data

#Shows the text in the app
data_load_state = st.text('Loading data...')


#Calling the load_data function
data = load_data(selected_stock)

#When loading done then shows this text
data_load_state.text('Loading data... Done ✅!')

#This is a subheader
st.subheader('Here Is The Raw Data 🔧')
#Outputs the tail of the dataset
st.write(data.tail())

st.markdown("**Current Open Price in USD:**")
st.write(data.iloc[-1,1])
st.markdown("**Current Close Price in USD:**")
st.write(data.iloc[-1,4])

with st.beta_expander("Explaining The Raw Dataset"):
    st.markdown('In stock trading, the `High` and `Low` refer to the maximum and minimum prices in a given time period. `Open` and `Close` are the prices at which a stock began and ended trading in the same period. `Volume` is the total amount of trading activity. Adjusted values factor in corporate actions such as dividends, stock splits, and new share issuance.')

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    #Plots the stock_open feature
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    # Plots the stock_close feature
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    #Adding a slider that will help you in zooming in and out of graph
    st.subheader('Plotting The Raw Data 👨🏻‍🔧')
    fig.layout.update(xaxis_title="Date", yaxis_title="Price in $", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

    # fig3 = go.Figure(data=[go.Candlestick(x=data['Date'],
    #                                      open=data['Open'],
    #                                      high=data['High'],
    #                                      low=data['Low'],
    #                                      close=data['Close'],
    #                                      name="stock_close")])
    #
    # fig3.layout.update(xaxis_title="Date", yaxis_title="Price in $")
    # st.plotly_chart(fig3)


# Calling the above function
plot_raw_data()

# This is a button to run the prediction
start_execution = st.button('Click Here To Predict 🚀')
st.markdown("Note : Could take some time(30sec-2min) to predict as the model is training and fitting the data in real time. Thanks for having patience.")

if start_execution:
    #Displays GIF when loading
    gif_runner = st.image('https://aws1.discourse-cdn.com/business7/uploads/streamlit/original/2X/2/247a8220ebe0d7e99dbbd31a2c227dde7767fbe1.gif')
    # Predict forecast with Prophet.
    # The features are "Data" and "Close" price.
    df_train = data[['Date', 'Close']]
    # Renaming the features as per Prophet needs.
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    # Daily Seasonality is a characteristic of a time series in which the
    # data experiences regular and predictable changes that recur everyday.
    # Any predictable fluctuation or pattern that recurs or repeats over a
    # one-day period is said to be daily seasonal.
    m = Prophet(daily_seasonality=True)
    # fitting the data
    m.fit(df_train)
    # Make dataframe with future dates for forecasting
    # periods:Int number of periods to forecast forward.
    future = m.make_future_dataframe(periods=period)
    # forecast is the predicted dataset
    forecast = m.predict(future)

    # Adding subheader
    st.subheader('Forecast Data 🔮')
    # Shows the last 5 values
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    with st.beta_expander("Explaining The Features"):
        st.markdown("`ds` -> Dates")
        st.markdown("`yhat` -> Forecast Data")
        st.markdown("`yhat_lower` and `yhat_upper` -> Lowermost and uppermost uncertainty intervals")

    # Plotting the forecast data
    if n_years==1:
        st.subheader(f'Result of the Forecast upto {n_years} year ⚙️')
    else:
        st.subheader(f'Result of the Forecast upto {n_years} years ⚙️')


    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1,use_container_width=True)
    fig1.layout.update(xaxis_title="Date", yaxis_title="Price in $", xaxis_rangeslider_visible=True)
    st.markdown("The date column is now labeled as **ds** and the values columns as **y**")

    # Plotting additional forecast data
    st.subheader("Forecast Components 🛠")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
    st.write("The forecast and component visualizations show that Prophet was able to accurately model the underlying trend in the data, while also accurately modeling daily, weekly and yearly seasonality.")

    # Removes The GIF after loading
    gif_runner.empty()




# This is the part of converting the currency
st.subheader("Convert Your Currency ⚖️")
st.image("https://cdn.dribbble.com/users/22930/screenshots/1923847/money.gif",width=340)
st.markdown("**Input Option**")

def currency_converter():
    url = "https://free.currconv.com/api/v7/currencies?apiKey=73373685ba13d7df49a0"
    # Make a request to a web page, and return the status code
    response = requests.get(url)
    
    # response.content returns the content of the response, in bytesl
    status_get = response.content
    
    # decoding the bytes from utf-8 to string
    status_get = status_get.decode('utf-8')
    
    # parsing and stored the json string to python dictionary
    status_json = json.loads(status_get)
    
    # making an array for storing currency
    all_currencies = []
    for i in status_json["results"]:
        all_currencies.append(i)
    number = st.number_input('Input the Value')
    # rounding the input to 2 digit place
    number = round(number,2)
    # selecting the currency to convert
    option = st.selectbox('', all_currencies, key=1)
    # filling values
    value = st.empty()
    # Selecting the currency to convert to
    option2 = st.selectbox('', all_currencies, key=2)

    left_column, right_column = st.beta_columns(2)
    pressed = left_column.button('Convert 💱')
    if pressed:
        # This is used for conversion
        sta = str(option)+"_"+str(option2)
        
        url = "https://free.currconv.com/api/v7/convert?q="+sta+"&compact=ultra&apiKey=73373685ba13d7df49a0"
        response = requests.get(url)
        status_get = response.content
        status_get = status_get.decode('utf-8')
        status_json = json.loads(status_get)
        
        # if the value is valid then -> number * 1 unit of input currency = output currency.
        value.success(status_json[sta] * number)
        
        # here we display 1 unit of input currency = how much unit of output currency
        converter = "1 "+option+" = "+str(status_json[sta])+" "+option2
        st.write(converter)


currency_converter()


with st.beta_expander("Credits 💎"):
    st.subheader("Author:")
    st.image("https://avatars.githubusercontent.com/u/52373756?s=400&u=f3b4f3403656c3f61c6b378f1028803bd9e81031&v=4")
    st.markdown(""" App Made By **[Koustav Banerjee](https://www.linkedin.com/in/koding-senpai/)**""")
    st.markdown("""**[Source code](https://github.com/Kens3i/Stocks-Daily)**""")
    st.markdown("""
    * **Python libraries:** streamlit, pandas, datetime, yfinance, fbprophet, plotly, requests, json
    * **Data source(For Currency):** [currencyconverterapi.com](https://www.currencyconverterapi.com/)
    """)
