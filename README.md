# Boston Housing Dataset

![alt text](Flowchart.jpg)

## Description

Take a look at Boston, a city full of knowledge and economic strength, where finding a home can be quite challenging. Known for its rich history and academic presence, Boston’s real estate market is as complex as a game of chess.

To better understand this complexity, we can examine the Boston Assessment 2021 dataset, which holds a wealth of information. It contains 177,091 individual records, each contributing to the overall picture of Boston’s housing market. With 63 columns of data, it offers a detailed view of the many factors that influence this dynamic market.

In short, Boston’s housing market is more than just a collection of properties; it’s a lively ecosystem that mirrors the city’s past, present, and future. It’s a market that requires patience, offers rewards, and continues to attract those who want to call this historic city home.

## Setup:

Here’s a refined version:

1. Download the CSV file from the following URL: [Boston Property Assessment Data](https://data.boston.gov/dataset/property-assessment/resource/c4b7331e-e213-45a5-adda-052e4dd31d41).

2. Upload the `boston_housing.csv` file to Amazon S3.

3. Create an AWS RDS MySQL database.

4. Install the MySQL Workbench application on Windows and connect it to your AWS RDS MySQL instance.

5. Create a schema and table in the database with the same column names as those in the CSV file.

6. Use the “Server” menu in MySQL Workbench to import data directly from your CSV file into the table.

7. Connect to the AWS RDS MySQL instance using the following variables:
   a. `DBHostname`
   b. `Port`
   c. `DBUsername`
   d. `Region`
   e. `ssl_ca`

8. Create the following MySQL procedures:
   a. `get_building_attributes`
   b. `get_building_att_and_area`

9. Run the following commands to launch the Bokeh server for EDA files:

   ```bash
   python -m bokeh serve --show EDA.py
   python -m bokeh serve --show EDA_2.py
   ```

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
