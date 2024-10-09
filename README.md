# Project Background

Data from the superstore was downloaded from the [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final?resource=download). The Superstore has collected data since 2014 and had an overall growth trajectory from 2014 to 2017. The insights in this report aim to propel the Superstore into further growth and financial success.

- Insights are provided based on profit and sales metrics.
- The pandas queries used to analyze the data can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/superstore_analysis.py)
- The code powering the dashboard can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/main.py)

# Data Structure

The data consists of one table `Store Records` with the following structure:

<div style="text-align: center;">
  <img src="data/entity_relationship_diagram1.png" alt="Superstore Data Structure" height="600" width="400" />
  <img src="data/entity_relationship_diagram2.png" alt="Second Image" height="600" width="400" /> 
</div>

# Executive Summary

**Overview of Findings**

In 2017, the Superstore had its best year in terms of sales and profits. The store has seen year over year growth and is doing well in the New York and California markets. From 2016 to 2017, the store saw a 14% increaes in profits and a 20% increase in sales revenue. Nearly 70% of customers who made a purchase have come back to make another purchase. Overall, health for the Superstore is in the green.

Unfortunately, the store is not doing well in the states of Texas and Illinois. Year after year, these are states where profits are consistently negative. Texas in particular generates a larage amount of sales, and those sales amount to negative profits.

Products in the furniture segment tend to do poorly in terms of profit and when compared to other segments. In 2014, it accounted for 11% of profits, but by 2017, that number had dropped to 3%, meanwhile it's consistently accounted for about 30% of sales annually.

![Superstore Dashboard](data/superstore.png)

