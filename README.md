# Project Background

**Overview:** The goal of the super store analysis is to analyze the distribution of sales and profits between the years 2014-2017. The analysis and dashboard provides data to inform stakeholders on which products to promote and discontinue; in addition, highlights markets that are performing well and ones that are not.

- Insights are provided based on profit and sales metrics.
- The live dashboard can be found [here.](https://superstore-bi-analysis.streamlit.app)
- The pandas queries used to analyze the data can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/superstore_analysis.py)
- The code powering the dashboard can be found [here.](https://github.com/Dilcia19/superstore_analysis/blob/main/scripts/main.py)

**Data Source:** Data from the superstore was downloaded from the [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final?resource=download). The Superstore has collected data since 2014 and had an overall growth trajectory from 2014 to 2017. The insights in this report aim to propel the Superstore into further growth and financial success.

**Tools:** Data cleaning and analysis were done with pandas. The dashboard was built with streamlit, a python framework that allows data analysts to build interactive dashboards without the need for directly building out having to develop the front-end with HTML, CSS and Javascript. The live dashboard is deployed on streamlit cloud.



# Data Structure

The data consists of one table `Store Records` with the following structure:

<div style="text-align: center;">
  <img src="data/entity_relationship_diagram1.png" alt="Superstore Data Structure" height="400" />
  <img src="data/entity_relationship_diagram2.png" alt="Second Image" height="400" /> 
</div>

# Executive Summary

**Overview of Findings**

In 2017, the Superstore had its best year in terms of sales and profits. The store has seen year over year growth and is doing well in the New York and California markets. From 2016 to 2017, the store saw a 14% increase in profits and a 20% increase in sales revenue. 

Nearly 40% of customers who made a purchase have come back to make another purchase. Overall, health for the Superstore is in the green. Unfortunately, the store is not doing well in the states of Texas and Illinois and has poor profit margins in the furniiture segment.

![Superstore Dashboard](data/superstore.png)

**Key Findings**

Great Markets:
- Year after year, California and New York outperform the rest of the markets in terms of sales and profits. 
- In 2017, California had $146,000 in sales and brought in $29,000 in profits. 
- New York had $93,000 in sales and brought in $24,000 in profits. These markets should continue to be invested in heavily.

Great Category:
- The technology and office supplies categories bring in the highest profits. 
- In 2017, both categories together accounted for 71% of the sales, but accounted for 97% of the profit. Investing further in either or both of these categories can yield great results.

Great Products:
- The `Canon imageCLASS 2200 Advanced Copier` consistently brought in high profits for the past 2 years.
- Copiers in general, are a good product to invest in, they generate high profits even with low volume.
- Each year, there is at least one copier on the list for top 5 products profitable products.
- Copiers in general have a healthy profit margin. In the most recent year, the `Canon imageCLASS 2200 Advanced Copier` had a profit margin of 44%.

Troublesome Markets:
- Year after year, Texas and Illinois profits were consistently negative. In 2014, Texas had a net profit of -$9,000 and has remained negative, although the loss in profits fluctuate significantly year to year.
- Illinois had a net profit of -$2,000 in 2014, but by 2017, that number had dropped to -$6,000.

Troublesome Category:
- In 2014, the furniture category accounted for 11% of Superstore profits, but by 2017, that number had dropped to 3%.
- Meanwhile the furniture category consistently accounted for about 30% of sales annually.

Trouble Products:
- `Cubify CubeX 3D Printer`, a machines sold by the Superstore, have consistently lost the superstore money. 
- The two versions of this product: `Cubify CubeX 3D Printer Double Head Print` and `Cubify CubeX 3D Printer Triple Head Print` have appeared on the list of biggest profit losers 3 out of 4 years of operation.
- It is likely time to drop this product. 
- The profit margin for the `Cubify CubeX 3D Printer` is -48%, and generally a bad investment for inventory.


