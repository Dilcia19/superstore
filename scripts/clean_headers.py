import pandas as pd

superstore = pd.read_csv('../data/sample_superstore.csv')

superstore.columns = superstore.columns.str.reaplace(' ','_')
superstore.columns = superstore.columns.str.lower()

superstore.to_csv('../data/sample_superstore_updated.csv', index=False)