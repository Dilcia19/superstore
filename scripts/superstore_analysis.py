import pandas as pd

def profit_delta(store_records):

    profit_delta = (
        store_records
        .filter(['order_id', 'profit', 'year'])
        .groupby('year')
        .agg(
            {'profit':'sum',
            'order_id':'first'}
        )
        .reset_index()
    )

    profits_2017 = int(profit_delta['profit'].iloc[3])
    profits_2016 = int(profit_delta['profit'].iloc[2])
    profits_2014 = int(profit_delta['profit'].iloc[0])

    profit_pct_change = (profits_2017 - profits_2014)/profits_2014 * 100

    profit_pct_change_recent = (profits_2017 - profits_2016)/profits_2016 * 100
    profit_pct_change_recent = round(profit_pct_change_recent, 2)

    sales_delta = (
        store_records
        .filter(['order_id', 'sales', 'year'])
        .groupby('year')
        .agg(
            {'sales':'sum',
            'order_id':'first'}
        )
        .reset_index()
        .assign(
            sales_previous_year = lambda x: x.sales.shift(1)
        )
        .assign(
            sales_delta = lambda x: (x.sales - x.sales_previous_year) / x.sales_previous_year * 100
        )
    )
    
    sales_2017 = int(sales_delta['sales'].iloc[3])
    sales_2016 = int(sales_delta['sales'].iloc[2])
    sales_2014 = int(sales_delta['sales'].iloc[0])

    sales_pct_change = (sales_2017 - sales_2014)/sales_2014 * 100
    sales_pct_change = round(sales_pct_change, 2)
    
    sales_pct_change_recent = (sales_2017 - sales_2016)/sales_2016 * 100
    sales_pct_change_recent = round(sales_pct_change_recent, 2)

    data_dict = {
    'profits_2017':profits_2017,
    'profit_pct_change_recent':profit_pct_change_recent, 
    'sales_2017':sales_2017,
    'sales_pct_change_recent':sales_pct_change_recent
    }

    return data_dict


def repeat_customers(store_records):
    # retention rate - ie, how many of those customers have come back
    # we have about 300 repeat customers that purchase every year out of 793 unique customers

    retention_rate = (
        store_records
        .filter(['order_id', 'customer_id', 'year'])
        .groupby(['customer_id', 'year'])
        .agg(
            {'order_id':'count'}
        )
        .reset_index()
    )

    retention_rate_pv = (
        retention_rate
        .pivot(
            index='customer_id', 
            columns='year', 
            values='order_id')
        .reset_index()
        .dropna(axis=0)
        .fillna(0)
    )

    # and 772 repeat customers who have purchased from the store more than once
    retention_rate_pv['single_purchase_customer'] = retention_rate_pv[retention_rate_pv == 0].count(axis=1).gt(2)
    # df for customers who made more than one purchase
    repeat_customers = retention_rate_pv[retention_rate_pv['single_purchase_customer'] == False]
    # list of customers who made more than one purchase
    repeat_customers_ls = list(repeat_customers['customer_id'].unique())

    # what % of purchases are repeated (customerID)
    ## make sure I didn't count unique orders without grouping
    df_repeat_customers = (
        store_records
        .query("customer_id in @repeat_customers_ls")
        .filter(['order_id','customer_id', 'product_id'])
        .groupby(['customer_id', 'order_id']) # orders may have multiple rows b/c they have multiple products + don't want to double-count
        .agg('count')
        .reset_index()
    )

    # after grouping, we have to subtract number of unique customers from unique orders
    # unique orders is counting all orders
    # for the purposes of calculating % of repeat orders, we can't count the first order
    # hence, deleting one order for each customer or the number of unique customers removed from total unique orders

    number_of_repeat_orders = len(df_repeat_customers['order_id'].unique()) - len(df_repeat_customers['customer_id'].unique())
    number_of_unique_customers = len(df_repeat_customers['customer_id'].unique())
    
    pct_repeated_orders = (number_of_repeat_orders - number_of_unique_customers) / store_records['order_id'].nunique()
    pct_repeated_orders = round(pct_repeated_orders, 2) * 100

    # not_first_order = number_of_repeat_orders - number_of_unique_customers

    return pct_repeated_orders

def top_sub_categories_profit(df_filtered):

    top_5_sub_category_year = (
        df_filtered
        .filter(['product_id', 'profit', 'product_name',
                 'category','sub_category'])
        .groupby(['sub_category'])
        .agg(
            {'profit':'sum'}
        )
        .rename(columns={'product_id':'product_id_count'})
        .sort_values(by='profit', ascending=False)
        .reset_index()
        .filter(['sub_category', 'profit'])
        .assign(profit=lambda x: x.profit.round(0))
        .iloc[0:5]
    )

    return top_5_sub_category_year

def top_sub_categories_sales(df_filtered):

    top_5_sub_category_syear = (
        df_filtered
        .filter(['product_id', 'sales', 'product_name',
                 'profit','category','sub_category'])
        .groupby(['sub_category'])
        .agg(
            {'sales':'sum',
             'profit':'sum'}
        )
        .rename(columns={'product_id':'product_id_count'})
        .sort_values(by='sales', ascending=False)
        .reset_index()
        .filter(['sub_category', 'sales', 'profit'])
        .assign(sales=lambda x: x.sales.round(0))
        .assign(profit=lambda x: x.profit.round(0))
        .iloc[0:5]
    )

    return top_5_sub_category_syear


def profits_by_state(df_filtered):

    gp_states_profit = (
        df_filtered
        .filter(['state', 'profit'])
        .groupby(['state'])
        .agg(
            {'profit':'sum'}
        )
        .reset_index()
        .assign(profit=lambda x: x.profit.round(0))
    )

    return gp_states_profit

def sales_by_state(df_filtered):

    gp_states_sales = (
        df_filtered
        .filter(['state', 'sales'])
        .groupby(['state'])
        .agg(
            {'sales':'sum'}
        )
        .reset_index()
        .assign(sales=lambda x: x.sales.round(0))
    )

    return gp_states_sales

def high_profit_products(df_filtered):

    high_low_profit_products = (
        df_filtered
        .filter(['product_id', 'profit', 'product_name',
                 'category','sub_category'])
        .groupby(['product_id'])
        .agg(
            {'profit':'sum',
            'product_name':'first',
            'category':'first',
            'sub_category':'first'}
        )
        .reset_index()
        .assign(profit=lambda x: x.profit.round(0))
    )

    top_5_high_profit = (
        high_low_profit_products
        .sort_values(by='profit', ascending=False)
        .iloc[0:5]
    )

    bottom_5_low_profit = (
        high_low_profit_products
        .sort_values(by='profit', ascending=True)
        .iloc[0:5]
    )

    return top_5_high_profit, bottom_5_low_profit

def high_profit_categories(df_filtered):

    top_5_high_profit_categories = (
        df_filtered
        .filter(['category','profit'])
        .groupby(['category'])
        .agg(
            {'profit':'sum'}
        )
        .reset_index()
        .sort_values(by='profit', ascending=False)
        .assign(total_year_profit=lambda x: x.profit.sum())
        .assign(category_profit_pct=lambda x: (x.profit / x.total_year_profit) * 100)
        .assign(category_profit_pct=lambda x: x.category_profit_pct.round(0))
        .rename(columns={'category_profit_pct':'distribution of profit'})
        .iloc[0:5]
    )

    return top_5_high_profit_categories

def high_sales_categories(df_filtered):

    top_5_high_sales_categories = (
        df_filtered
        .filter(['category','sales'])
        .groupby(['category'])
        .agg(
            {'sales':'sum'}
        )
        .reset_index()
        .sort_values(by='sales', ascending=False)
        .assign(total_year_sales=lambda x: x.sales.sum())
        .assign(category_sales_pct=lambda x: (x.sales / x.total_year_sales) * 100)
        .assign(category_sales_pct=lambda x: x.category_sales_pct.round(0))
        .rename(columns={'category_sales_pct':'distribution of sales'})
        .iloc[0:5]
    )

    return top_5_high_sales_categories

def high_profit_segments(df_filtered):

    high_profit_segments = (
        df_filtered
        .filter(['segment','profit'])
        .groupby(['segment'])
        .agg(
            {'profit':'sum'}
        )
        .reset_index()
        .sort_values(by='profit', ascending=False)
        .assign(total_year_profit=lambda x: x.profit.sum())
        .assign(segment_profit_pct=lambda x: (x.profit / x.total_year_profit) * 100)
        .assign(segment_profit_pct=lambda x: x.segment_profit_pct.round(0))
        .rename(columns={'segment_profit_pct':'percent of profit'})
        .iloc[0:5]
    )

    return high_profit_segments





