import pandas as pd

def profit_delta(store_records):

    profit_delta = store_records[['order_id','profit','year']].groupby('year').agg({'profit':'sum','order_id':'first'}).reset_index()
    profits_2017 = int(profit_delta['profit'].iloc[3])
    profits_2016 = int(profit_delta['profit'].iloc[2])
    profits_2014 = int(profit_delta['profit'].iloc[0])

    profit_pct_change = (profits_2017 - profits_2014)/profits_2014 * 100

    profit_pct_change_recent = (profits_2017 - profits_2016)/profits_2016 * 100
    profit_pct_change_recent = round(profit_pct_change_recent, 2)

    sales_delta = (
        store_records.filter(['order_id', 'sales', 'year'])
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
    retention_rate = store_records[['customer_id','year','product_id']].groupby(['year','customer_id']).agg('count').reset_index()
    retention_rate_pv = pd.pivot(retention_rate, index='customer_id', columns='year', values='product_id').reset_index()
    retention_rate_pv2 = retention_rate_pv.dropna(axis=0)

    # and 772 repeat customers who have purchased from the store more than once
    retention_rate_pv = retention_rate_pv.fillna(0)
    retention_rate_pv['single_purchase_customer'] = retention_rate_pv[retention_rate_pv == 0].count(axis=1).gt(2)
    repeat_customers = retention_rate_pv[retention_rate_pv['single_purchase_customer'] == False]

    repeat_customers_ls = list(repeat_customers['customer_id'].unique())

    # what % of purchases are repeated (customerID)
    ## make sure I didn't count unique orders without grouping
    df_repeat_customers = store_records[store_records['customer_id'].isin(repeat_customers_ls)]
    df_repeat_customers = df_repeat_customers[['order_id','customer_id', 'product_id']]
    df_repeat_customers = df_repeat_customers.groupby(['customer_id', 'order_id']).agg('count').reset_index()

    # after grouping, we have to subtract number of unique customers from unique orders
    # unique orders is counting all orders
    # for the purposes of calculating % of repeat orders, we can't count the first order
    # hence, deleting one order for each customer or the number of unique customers removed from total unique orders
    number_of_repeat_orders = len(df_repeat_customers['order_id'].unique()) - len(df_repeat_customers['customer_id'].unique())
    number_of_unique_customers = len(df_repeat_customers['customer_id'].unique())
    pct_repeated_orders = (number_of_repeat_orders - number_of_unique_customers) / store_records['order_id'].nunique()
    pct_repeated_orders = round(pct_repeated_orders, 2) * 100

    not_first_order = number_of_repeat_orders - number_of_unique_customers

    return pct_repeated_orders, not_first_order





