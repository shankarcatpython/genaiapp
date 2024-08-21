import sqlite3
import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest
import json

# Connect to the SQLite database containing the sales data
conn = sqlite3.connect('../../../genieai.db')

# Load the sales data into a DataFrame
sales_df = pd.read_sql_query("SELECT * FROM sales", conn)

# Get total record count from the sales table
total_record_count = len(sales_df)
print(f'Total record count in the sales table: {total_record_count}')

# Close the connection to the pharmacy database
conn.commit()
conn.close()

# Function to detect anomalies using Isolation Forest for multiple features
def detect_anomalies(data, features):
    model = IsolationForest(contamination=0.01)  # Lowering the contamination rate to 1%
    data['anomaly'] = model.fit_predict(data[features])
    anomalies = data[data['anomaly'] == -1].copy()  # Create a copy to avoid SettingWithCopyWarning
    return anomalies.index.tolist(), anomalies

# Detect anomalies in the 'total_price' and 'quantity_sold' features
features = ['total_price', 'quantity_sold']
anomaly_indices, anomalies_df = detect_anomalies(sales_df, features)

# Calculate statistical metrics for the features
metrics = {}
for feature in features:
    metrics[feature] = {
        'mean': sales_df[feature].mean(),
        'median': sales_df[feature].median(),
        'std_dev': sales_df[feature].std(),
        'min_value': float(sales_df[feature].min()),  # Ensure float conversion
        'max_value': float(sales_df[feature].max())   # Ensure float conversion
    }
    # Print the calculated metrics for each feature
    print(f"Metrics for {feature}:")
    print(f"  Mean: {metrics[feature]['mean']}")
    print(f"  Median: {metrics[feature]['median']}")
    print(f"  Std Dev: {metrics[feature]['std_dev']}")
    print(f"  Min Value: {metrics[feature]['min_value']}")
    print(f"  Max Value: {metrics[feature]['max_value']}")

anomaly_count = len(anomaly_indices)
print(f'Anomalies count: {anomaly_count}')

# Add reasons for anomalies using .loc to avoid SettingWithCopyWarning
anomalies_df.loc[:, 'reason'] = anomalies_df.apply(lambda row: f"total_price: {row['total_price']} (mean: {metrics['total_price']['mean']}, std_dev: {metrics['total_price']['std_dev']}); quantity_sold: {row['quantity_sold']} (mean: {metrics['quantity_sold']['mean']}, std_dev: {metrics['quantity_sold']['std_dev']})", axis=1)

# Convert the anomaly data to JSON format with reasons
anomalies_json = anomalies_df[[
    'sale_id', 'sale_date', 'customer_id', 'prescription_id', 'medicine_id',
    'medicine_name', 'quantity_sold', 'unit_price', 'total_price', 'pharmacist_id',
    'payment_method', 'insurance_provider', 'reason'
]].to_json(orient='records')

# Insert the anomaly results into the meta table
meta_conn = sqlite3.connect('../../../genieai.db')
cur = meta_conn.cursor()

# Create the anomalymeta table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS anomaly (
    table_name    TEXT,
    analysis_date TEXT,
    feature_name  TEXT,
    mean          REAL,
    median        REAL,
    std_dev       REAL,
    min_value     REAL,
    max_value     REAL,
    anomaly_count INTEGER,
    anomalies     TEXT
)
''')

# Insert the meta information into the anomalymeta table for each feature
for feature in features:
    mean_value = float(metrics[feature]['mean'])
    median_value = float(metrics[feature]['median'])
    std_dev_value = float(metrics[feature]['std_dev'])
    min_value = float(metrics[feature]['min_value'])
    max_value = float(metrics[feature]['max_value'])

    cur.execute('''
    INSERT INTO anomaly (
        table_name, analysis_date, feature_name, mean, median, std_dev, min_value, max_value, anomaly_count, anomalies
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'sales', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), feature,
        mean_value, median_value, std_dev_value, min_value, max_value, anomaly_count,
        anomalies_json
    ))

# Commit the transaction and close the connection to the meta database
meta_conn.commit()
meta_conn.close()

print(f'Anomalies detected and meta information inserted into anomalymeta table.')