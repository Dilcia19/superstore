import pandas as pd

superstore = pd.read_csv('../data/sample_superstore.csv', encoding='ISO-8859-1')

superstore.columns = superstore.columns.str.replace(' ','_')
superstore.columns = superstore.columns.str.lower()

superstore.to_csv('../data/sample_superstore_updated.csv', index=False)