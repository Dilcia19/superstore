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
    'profit_pct_change_recent':profit_pct_change_recent, 
    'sales_pct_change_recent':sales_pct_change_recent
    }

    return data_dict



