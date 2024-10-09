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

def top_sub_categories_profit(df_filtered):

    top_5_sub_category_year = df_filtered[['product_id', 'profit', 'product_name','category','sub_category']].groupby(['sub_category']).agg({'profit':'sum'}).rename(columns={'product_id':'product_id_count'}).sort_values(by='profit', ascending=False).reset_index()
    top_5_sub_category_year = top_5_sub_category_year[['sub_category', 'profit']]
    top_5_sub_category_year['profit'] = top_5_sub_category_year['profit'].round(0)
    top_5_sub_category_year = top_5_sub_category_year.iloc[0:5]


    return top_5_sub_category_year

def top_sub_categories_sales(df_filtered):

    top_5_sub_category_syear = df_filtered[['product_id', 'sales', 'product_name','category','sub_category']].groupby(['sub_category']).agg({'sales':'sum'}).rename(columns={'product_id':'product_id_count'}).sort_values(by='sales', ascending=False).reset_index()
    top_5_sub_category_syear = top_5_sub_category_syear[['sub_category', 'sales']]
    top_5_sub_category_syear['sales'] = top_5_sub_category_syear['sales'].round(0)
    top_5_sub_category_syear = top_5_sub_category_syear.iloc[0:5]

    return top_5_sub_category_syear


def profits_by_state(df_filtered):

    gp_states_profit = df_filtered[['state','profit']].groupby('state').agg({'profit':'sum'}).reset_index()
    gp_states_profit['profit'] = gp_states_profit['profit'].round(0)
    return gp_states_profit

def sales_by_state(df_filtered):

    gp_states_sales = df_filtered[['state','sales']].groupby('state').agg({'sales':'sum'}).reset_index()
    gp_states_sales['sales'] = gp_states_sales['sales'].round(0)
    return gp_states_sales

def high_profit_products(df_filtered):
    
    high_profit_products = df_filtered[['product_id','product_name','profit','category','sub_category']].groupby(['product_id']).agg({'profit':'sum','product_name':'first','category':'first','sub_category':'first'}).reset_index()
    high_profit_products['profit'] = high_profit_products['profit'].round(0)
    high_profit_products = high_profit_products.sort_values(by='profit', ascending=False)
    high_profit_products['total_year_profit'] = high_profit_products['profit'].sum()
    high_profit_products['product_profit_pct'] = high_profit_products['profit'] / high_profit_products['total_year_profit']
    high_profit_products = high_profit_products.drop(columns=['total_year_profit', 'product_profit_pct'])
    top_5_high_profit = high_profit_products.iloc[0:5]

    return top_5_high_profit

def high_profit_categories(df_filtered):
    
    high_profit_categories = df_filtered[['category','profit']].groupby('category').agg({'profit':'sum'}).reset_index()
    high_profit_categories = high_profit_categories.sort_values(by='profit', ascending=False)
    high_profit_categories['total_year_profit'] = high_profit_categories['profit'].sum()
    high_profit_categories['category_profit_pct'] = (high_profit_categories['profit'] / high_profit_categories['total_year_profit']) * 100
    high_profit_categories['category_profit_pct'] = high_profit_categories['category_profit_pct'].round(0)
    high_profit_categories = high_profit_categories.rename(columns={'category_profit_pct':'percent of profit'})
    top_5_high_profit_categories = high_profit_categories.iloc[0:5]

    return top_5_high_profit_categories

def high_sales_categories(df_filtered):
    
    high_sales_categories = df_filtered[['category','sales']].groupby('category').agg({'sales':'sum'}).reset_index()
    high_sales_categories = high_sales_categories.sort_values(by='sales', ascending=False)
    high_sales_categories['total_year_sales'] = high_sales_categories['sales'].sum()
    high_sales_categories['category_sales_pct'] = (high_sales_categories['sales'] / high_sales_categories['total_year_sales']) * 100
    high_sales_categories['category_sales_pct'] = high_sales_categories['category_sales_pct'].round(0)
    high_sales_categories = high_sales_categories.rename(columns={'category_sales_pct':'percent of sales'})
    top_5_high_profit_categories = high_sales_categories.iloc[0:5]

    return top_5_high_profit_categories

def high_profit_segments(df_filtered):

    high_profit_segments = df_filtered[['segment','profit']].groupby('segment').agg({'profit':'sum'}).reset_index()
    high_profit_segments = high_profit_segments.sort_values(by='profit', ascending=False)
    high_profit_segments['total_year_profit'] = high_profit_segments['profit'].sum()
    high_profit_segments['segment_profit_pct'] = (high_profit_segments['profit'] / high_profit_segments['total_year_profit']) * 100
    high_profit_segments['segment_profit_pct'] = high_profit_segments['segment_profit_pct'].round(0)
    high_profit_segments = high_profit_segments.rename(columns={'segment_profit_pct':'percent of profit'})
    high_profit_segments = high_profit_segments.iloc[0:5]

    return high_profit_segments





