import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import timedelta, datetime

# Initialize Faker and set locale to en_US
fake = Faker('en_US')

# Define the number of days and sales per day
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 6, 30)
total_days = (end_date - start_date).days + 1

# Define the range of sales per day
min_sales_per_day = 100
max_sales_per_day = 200

# Define possible medicines
medicines = [
    {'id': 301, 'name': 'Lipitor', 'price': 25.00},
    {'id': 302, 'name': 'Amoxicillin', 'price': 15.00},
    {'id': 303, 'name': 'Metformin', 'price': 10.00},
    {'id': 304, 'name': 'Ibuprofen', 'price': 5.00},
    {'id': 305, 'name': 'Zoloft', 'price': 20.00},
    {'id': 306, 'name': 'Amlodipine', 'price': 12.00},
    {'id': 307, 'name': 'Metoprolol', 'price': 11.00},
    {'id': 308, 'name': 'Albuterol', 'price': 18.00},
    {'id': 309, 'name': 'Omeprazole', 'price': 14.00},
    {'id': 310, 'name': 'Losartan', 'price': 13.00},
    {'id': 311, 'name': 'Levothyroxine', 'price': 17.00},
    {'id': 312, 'name': 'Gabapentin', 'price': 19.00},
    {'id': 313, 'name': 'Lisinopril', 'price': 8.00},
    {'id': 314, 'name': 'Atorvastatin', 'price': 21.00},
    {'id': 315, 'name': 'Simvastatin', 'price': 22.00},
    {'id': 316, 'name': 'Tramadol', 'price': 24.00},
    {'id': 317, 'name': 'Prednisone', 'price': 23.00},
    {'id': 318, 'name': 'Azithromycin', 'price': 16.00},
    {'id': 319, 'name': 'Clonazepam', 'price': 28.00},
    {'id': 320, 'name': 'Citalopram', 'price': 27.00},
    {'id': 321, 'name': 'Doxycycline', 'price': 26.00},
    {'id': 322, 'name': 'Furosemide', 'price': 9.00},
    {'id': 323, 'name': 'Hydrochlorothiazide', 'price': 7.00},
    {'id': 324, 'name': 'Warfarin', 'price': 6.00},
    {'id': 325, 'name': 'Tamsulosin', 'price': 29.00},
]

# Define possible payment methods and insurance providers
payment_methods = ['cash', 'credit card', 'insurance']
insurance_providers = ['Aetna', 'Blue Cross', 'Cigna', 'United Healthcare', None]

# Define store locations
store_locations = ['New York', 'Los Angeles', 'Chicago', 'Boston', 'Miami']

# Function to generate sales data
def generate_sales_data(start_date, total_days, min_sales_per_day, max_sales_per_day):
    sales_data = []
    sale_id = 1
    
    for day in range(total_days):
        sale_date = start_date + timedelta(days=day)
        sales_per_day = random.randint(min_sales_per_day, max_sales_per_day)
        
        for _ in range(sales_per_day):
            customer_id = fake.random_int(min=100, max=999)
            prescription_id = fake.random_int(min=200, max=299)
            medicine = random.choice(medicines)
            quantity_sold = fake.random_int(min=1, max=5)
            total_price = round(medicine['price'] * quantity_sold, 2)
            pharmacist_id = fake.random_int(min=400, max=499)
            payment_method = random.choice(payment_methods)
            insurance_provider = random.choice(insurance_providers) if payment_method == 'insurance' else None
            store_location = random.choice(store_locations)
            
            sales_data.append([
                sale_id, sale_date, customer_id, prescription_id, medicine['id'],
                medicine['name'], quantity_sold, medicine['price'], total_price,
                pharmacist_id, payment_method, insurance_provider, store_location
            ])
            
            sale_id += 1
            
    return sales_data

# Generate the sales data
sales_data = generate_sales_data(start_date, total_days, min_sales_per_day, max_sales_per_day)

# Create a DataFrame
columns = [
    'sale_id', 'sale_date', 'customer_id', 'prescription_id', 'medicine_id',
    'medicine_name', 'quantity_sold', 'unit_price', 'total_price',
    'pharmacist_id', 'payment_method', 'insurance_provider', 'store_location'
]
sales_df = pd.DataFrame(sales_data, columns=columns)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('../../../genieai.db')
cursor = conn.cursor()

# Create the sales table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        sale_date DATE,
        customer_id INTEGER,
        prescription_id INTEGER,
        medicine_id INTEGER,
        medicine_name TEXT,
        quantity_sold INTEGER,
        unit_price REAL,
        total_price REAL,
        pharmacist_id INTEGER,
        payment_method TEXT,
        insurance_provider TEXT,
        store_location TEXT
    )
''')

# Insert the sales data into the sales table
sales_df.to_sql('sales', conn, if_exists='append', index=False)

# Commit the transaction and close the connection
conn.commit()
conn.close()

# Display the DataFrame
print(sales_df)