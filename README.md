# Boston Housing Dataset

![alt text](Flowchart.jpg)

## Description

Take a look at Boston, a city full of knowledge and economic strength, where finding a home can be quite challenging. Known for its rich history and academic presence, Boston’s real estate market is as complex as a game of chess.

To better understand this complexity, we can examine the Boston Assessment 2022 dataset, which holds a wealth of information. It contains 168,116 individual records, each contributing to the overall picture of Boston’s housing market. With 56 columns of data, it offers a detailed view of the many factors that influence this dynamic market.

In short, Boston’s housing market is more than just a collection of properties; it’s a lively ecosystem that mirrors the city’s past, present, and future. It’s a market that requires patience, offers rewards, and continues to attract those who want to call this historic city home.


## EDA

![alt text](Dashboard.png)

![alt text](Dashboard2.png)


## Predictive Analytics
    1. Linear Regression
    2. Random Forest
    3. LightGBM Regression
    4. Ridge Regression
    5. Lasso Regression

The analysis focused on key real estate features, carefully selected using `Variance Inflation Factor` (VIF) to minimize multicollinearity while capturing diverse property aspects. These included kitchen details, location, building type, exterior condition, bathroom style, HVAC systems, and property tax. This comprehensive yet non-redundant set of features was then used in predictive modeling. The `LightGBM` model emerged as the top performer, achieving an impressive `80.87%` accuracy in predicting the target variable, demonstrating its effectiveness for this particular dataset.
