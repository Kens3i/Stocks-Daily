# Stocks-Daily
## Web-App Developed with Streamlit & FB Prophet 📈

![](https://media.giphy.com/media/S4178TW2Rm1LW/giphy.gif)

## Table of Contents

1.  [Overview](#Overview)
    
2.  [Motivation](#Motivation)
    
3.  [Libraries Used](#Libraries-Used)
    
4.  [Workflow](#Workflow)
5.  [Screesnshots](#Screesnshots)
6. [FAQs](#FAQs)

## Overview

This app let's you to generate a **live time-series** forecast of FAAMG stocks, **predict** the future price of them(upto 7 years) and also lets you **convert the currecy** as per your needs. Click [here](https://share.streamlit.io/kens3i/stocks-daily/main/main.py) to visit the website !

## Motivation

I was very curious about how stock markets work and how people became rich by investing in the right stocks (For Ex:Warrren Buffet) at the right time. For newbies like me who couldn't predict the stock prices based on so many data that is present on the internet I created this app to let people see the trends and growth the stock market get if someone invests for a long time. Also this app gave me a solid idea how the time series forecasting works and how the prediction of the prices occurs.

## Libraries-Used

-   `yfinance`
-   `fbprophet`
-   `plotly`
-   `streamlit`
-   `datetime`
-   `pandas`
-   `requests`

## Workflow

- **Selecting** a ticker(stock symbol) .
- **Extracting** the stocks data of the selected ticker from `yfinance` library.
- Selecting how many years the user wants to **predict**.
- **Ploting** the raw data and  giving an overview of the dataset.
- Clicking the prediction button and getting the **forecast data** along with daily,weekly and yearly trends.
- As the prices are in `USD` the user can see how much does `USD` compares with their local currency and can find an **estimate price**.
- To do the currency conversion I used **Rates API** which is a free service for current and historical foreign exchange rates built on top of data published by [European Central Bank.](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

## Screenshots
![](https://github.com/Kens3i/Stocks-Daily/blob/main/gifs/Stock%20intro.gif)
![](https://github.com/Kens3i/Stocks-Daily/blob/main/gifs/Stocks%20SS%20predict.gif)
![](https://github.com/Kens3i/Stocks-Daily/blob/main/gifs/SS%20Currency.gif)


## Challenges I Faced

- I just knew a little bit of HTML and CSS which was not sufficient to make this project, thankfully streamlit saved me.
- Took me some time just to know how the `fbprophet` library actually works.
- It took me some more time to tune the model to give the best prediction, tested each hyperparameters manually one by one !
- Didn't knew much about stock markets so spend some time studying the basics of the stock market.
- Had some deployment issues so I had to manually select all the libraries in requirements.txt.

## FAQs

### Why Time-Series Forecasting ?
The common trend towards the stock market among the society is that it is highly risky for investment or not suitable for trade so most of the people are not even interested. The seasonal variance and steady flow of any index will help both existing and new investors to understand and make a decision to invest in the stock/share market.

To solve these types of problems, the time series analysis will be the best tool for forecasting the trend or even future. The trend chart will provide adequate guidance for the investor.

### What is a Stock Market?
A stock or share (also known as a company’s “[equity](https://www.investopedia.com/terms/e/equity.asp)”) is a financial instrument that represents ownership in a company or corporation and represents a proportionate claim on its [assets](https://www.investopedia.com/terms/a/asset.asp) (what it owns) and [earnings](https://www.investopedia.com/terms/e/earnings.asp) (what it generates in profits). — [Investopedia](https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp)

### Why Apply ML In Stock Market?
Stock prices are not randomly generated values instead they can be treated as a discrete-time series model which is based on a set of well-defined numerical data items collected at successive points at regular intervals of time.Machine learning has the potential to ease the whole process by analyzing large chunks of data, spotting significant patterns and generating a single output that navigates traders towards a particular decision based on predicted asset prices.

### What are FAAMG Stocks?
FAAMG is an abbreviation coined by Goldman Sachs for five top-performing tech stocks in the market, namely, Facebook, Amazon, Apple, Microsoft, and Alphabet’s Google.
FAAMG are termed [growth stocks](https://www.investopedia.com/terms/g/growthstock.asp), mostly due to their year-over-year (YOY) steady and consistent increase in the earnings they generate, which translates into increasing stock prices.

### Why FB Prophet ?
Facebook developed an open sourcing Prophet, a forecasting tool available in both Python and R. It provides intuitive parameters which are easy to tune. Even someone who lacks deep expertise in time-series forecasting models can use this to generate meaningful predictions for a variety of problems in business scenarios.

**Highlights** of Facebook Prophet

-   Very fast, since it’s built in [Stan](https://mc-stan.org/users/documentation/), a programming language for statistical inference written in C++.
-   An additive regression model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects: 
	1. A piecewise linear or logistic growth curve trend. Prophet automatically detects changes in trends by selecting changepoints from the data 
	2. A yearly seasonal component modeled using Fourier series 
	3. A weekly seasonal component using dummy variables 
	4. A user-provided list of important holidays.
-   Robust to missing data and shifts in the trend, and typically handles outliers .
-   Easy procedure to tweak and adjust forecast while adding domain knowledge or business insights.

### Why Streamlit ?

A few of the **advantages** of using Streamlit tools like Dash and Flask:

-   It embraces Python scripting; No HTML knowledge is needed!
-   Less code is needed to create a beautiful application
-   No callbacks are needed since widgets are treated as variables
-   Data caching simplifies and speeds up computation pipelines.


### Thankyou For Spending Your Precious Time Going Through This Project!
### If You Find Any Value In This Project Or Gained Something New Please Do Give A ⭐.
