# Project Background

Data from the superstore was downloaded from the [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final?resource=download). The Superstore has collected data since 2014 and had an overall growth trajectory from 2014 to 2017. The insights in this report aim to propel the Superstore into further growth and financial success.

- Insights are provided based on profit and sales metrics.
- The pandas queries used to analyze the data can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/superstore_analysis.py)
- The code powering the dashboard can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/main.py)

# Data Structure

The data consists of one table `Store Records` with the following structure:

<p float="center">
  <img src="data/entity_relationship_diagram1.png" alt="Superstore Data Structure" height="400" />
  <img src="data/entity_relationship_diagram2.png" alt="Second Image" height="400" /> 
</p>

- The Super Store was founded at the end of 2013 and started selling products in 2014. 
- The store has seen year over year growth in terms of sales and profits. 
- With the elimination of a few key products and a few unprofitable geographical markets, we will set up the super store to break record profits and sales in the upcoming years

**Super Store Dashboard**



**KPIs: A Brief Look**<br>
If you've had a chance to poke around on the dashboard, you may notice a few things:
1. Profits are increasing overall, but there are states that consistently underperform: Including but not limited to Texas and Illinois
2. Copiers and Phones are consistently in the sub-category of most profitable products
3. From the 3 segments: Technology, Furniture, and Office Supplies - when compared by % of profit they brought each year, Furniture consistently brings in a smaller piece of the pie than the rest
4. Considering that sub-categories within Furniture are rarely in the top 5 most profitable products, or top 5 products with the highest sales revenue, it may be worth re-evaluating if the store needs to sell furniture at all  
5. The data is full of surprises, what will you find?