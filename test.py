from datetime import datetime
import pandas as pd

data_type = {

    '_CustomerID' : str
}

sales_data = pd.read_csv('sales_data.csv', dtype= data_type, parse_dates= ['OrderDate'] ) 

df = sales_data.copy()

df['Revenue'] = (df['Unit Price'] - (df['Unit Price'] * df['Discount Applied']) - df['Unit Cost']) * df['Order Quantity']

## ! print(df.dtypes) 

columns = ['OrderNumber', '_CustomerID', 'OrderDate', 'Revenue']

df_dateset = df[columns]

today_date = pd.to_datetime('2021-01-01')

rfm_dataset = df_dateset.groupby('_CustomerID').agg({
    'OrderDate': lambda v: (today_date - v.max()).days, 
    'OrderNumber': 'count',
    'Revenue' : 'sum'
}
)

rfm_dataset.rename(
    columns = {
        'OrderDate' : 'Recency',
        'OrderNumber' : 'Frequency',
        'Revenue' : 'Monetary'
    },
    inplace = True
)

r = pd.qcut(rfm_dataset['Recency'], q=5, labels=range(5, 0, -1))

f = pd.qcut(rfm_dataset['Frequency'], q=5, labels=range(1, 6))

m = pd.qcut(rfm_dataset['Monetary'], q=5, labels=range(1, 6)) 

rfm = rfm_dataset.assign(R = r.values, F = f.values, M = m.values)
rfm['rfm_group'] = rfm[['R', 'F', 'M']].apply(lambda v: '-'.join(v.astype(str)), axis = 1)
rfm['rfm_score_total'] = rfm[['R', 'F', 'M']].sum(axis=1)  

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Get the value counts of the rfm_score_total column
rfm_score_counts = rfm['rfm_score_total'].value_counts()

# Create the bar chart
plt.figure(figsize=(8, 6))  # Set the figure size (width, height) in inches
plt.bar(rfm_score_counts.index, rfm_score_counts.values)  # Use index for x-axis labels, values for bar heights

# Set chart title and labels
plt.title('RFM Score Distribution (Value Counts)')
plt.xlabel('RFM Score (Total)')
plt.ylabel('Number of Customers')

# Rotate x-axis labels if many scores
if len(rfm_score_counts) > 10:  # Adjust the threshold as needed
    plt.xticks(rotation=45)

# Display the chart
plt.grid(axis='y')
plt.tight_layout()
plt.show()

