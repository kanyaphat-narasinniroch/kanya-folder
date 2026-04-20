import pandas as pd
import numpy as np

customers = pd.read_csv('D:/WSC S1 Practice/RS/customers.csv')
products = pd.read_csv('D:/WSC S1 Practice/RS/products.csv')
sales = pd.read_csv('D:/WSC S1 Practice/RS/sales_transactions.csv')

# Combine Name
customers['full_name'] = (
    customers['first_name'].fillna('').str.strip() + ' ' +
    customers['last_name'].fillna('').str.strip()
).str.strip()

# TOP 5 ROWS
print("=== TOP 5 ROWS ===")
print("\nCustomers:\n", customers.head())
print("\nProducts:\n", products.head())
print("\nSales:\n", sales.head())

# CHECK DATA TYPES
print("\n=== DATA TYPES ===")
print("\nCustomers:\n", customers.dtypes)
print("\nProducts:\n", products.dtypes)
print("\nSales:\n", sales.dtypes)

# NON-NUMERIC COLUMNS
print("\n=== NON-NUMERIC COLUMNS ===")

non_numeric_customers = customers.select_dtypes(exclude=[np.number]).columns
non_numeric_products = products.select_dtypes(exclude=[np.number]).columns
non_numeric_sales = sales.select_dtypes(exclude=[np.number]).columns

print("\nCustomers:", list(non_numeric_customers))
print("Products:", list(non_numeric_products))
print("Sales:", list(non_numeric_sales))

# MISSING VALUES
print("\n=== MISSING VALUES ===")
print("\nCustomers:\n", customers.isnull().sum())
print("\nProducts:\n", products.isnull().sum())
print("\nSales:\n", sales.isnull().sum())

# SALES DATE
sales['date_parsed'] = pd.to_datetime(sales['date'], errors='coerce')

invalid_sales_dates = sales[
    (sales['date_parsed'].isna()) |
    (sales['date_parsed'] < '2000-01-01') |
    (sales['date_parsed'] > '2025-12-31')
].shape[0]


# CUSTOMERS - JOIN DATE
customers['join_date_parsed'] = pd.to_datetime(
    customers['join_date'],
    errors='coerce',
    dayfirst=True
)

invalid_join_dates = customers[
    (customers['join_date_parsed'].isna()) |
    (customers['join_date_parsed'] < '2000-01-01') |
    (customers['join_date_parsed'] > '2025-12-31')
].shape[0]


# CUSTOMERS - LAST PURCHASE DATE
customers['last_purchase_date_parsed'] = pd.to_datetime(
    customers['last_purchase_date'], errors='coerce'
)

invalid_last_purchase_dates = customers[
    (customers['last_purchase_date_parsed'].isna()) |
    (customers['last_purchase_date_parsed'] < '2000-01-01') |
    (customers['last_purchase_date_parsed'] > '2025-12-31')
].shape[0]

# Date Products
products['introduced_date_parsed'] = pd.to_datetime(
    products['introduced_date'], errors='coerce'
)

invalid_products_dates = products[
    (products['introduced_date_parsed'].isna()) |
    (products['introduced_date_parsed'] < '2000-01-01') |
    (products['introduced_date_parsed'] > '2025-12-31')
].shape[0]

total_invalid_dates = (
    invalid_sales_dates +
    invalid_join_dates +
    invalid_last_purchase_dates +
    invalid_products_dates
)

print("\nInvalid Dates:", total_invalid_dates)


# Sum Negative
negative_qty = (sales['quantity'] < 0).sum()
negative_price = (sales['price'] < 0).sum()

# Invalid IDs
invalid_product_ids = (~sales['product_id'].isin(products['product_id'])).sum()
invalid_customer_ids = (~sales['customer_id'].isin(customers['customer_id'])).sum()

# Formatting Name
format_issues = (
    (customers['first_name'] != customers['first_name'].str.strip()) |
    (customers['last_name'] != customers['last_name'].str.strip())
).sum()

negative_values = sales[
    (sales['quantity'] < 0) |
    (sales['price'] < 0)
].shape[0]

unexpected_values = 0

if 'gender' in customers.columns:
    unexpected_values += (~customers['gender'].fillna('').isin(['M', 'F'])).sum()

if 'active' in products.columns:
    unexpected_values += (~products['active'].fillna('').isin(['True', 'False'])).sum()

if 'seasonal' in products.columns:
    unexpected_values += (~products['seasonal'].fillna('').isin(['True', 'False'])).sum()

if 'payment_method' in sales.columns:
    unexpected_values += (~sales['payment_method'].fillna('').isin(['Credit Card', 'Mobile Pay', 'Cash'])).sum()

print("Unexpected Values:", unexpected_values)

format_issues = 0

for df in [customers, products, sales]:
    for col in df.select_dtypes(include=['object', 'string']).columns:
        format_issues += (df[col] != df[col].str.strip()).sum()
        format_issues += df[col].str.contains(r'\s{2,}', na=False).sum()

print("Formatting Issues:", format_issues)

# PRINT RESULT
print("\n=== DATA QUALITY ISSUES ===")
print("Negative Values:", negative_values)
print("Invalid Dates:", total_invalid_dates)
print("Negative Quantity Rows:", negative_qty)
print("Negative Price Rows:", negative_price)
print("Invalid Product IDs:", invalid_product_ids)
print("Invalid Customer IDs:", invalid_customer_ids)
print("Formatting Issues :", format_issues)
print("Unexpected Values:", unexpected_values)

with open("D:/WSC S1 Practice/RS/Session1_DataExploration.txt",
          'w', encoding='utf-8') as f:

    f.write("=== FIRST 5 ROWS ===\n")
    
    f.write("\nCustomers:\n")
    f.write(customers.head().to_string())
    
    f.write("\n\nProducts:\n")
    f.write(products.head().to_string())
    
    f.write("\n\nSales:\n")
    f.write(sales.head().to_string())

    f.write("\n\n=== DATA TYPES ===\n")
    
    f.write("\nCustomers:\n")
    f.write(customers.dtypes.to_string())
    
    f.write("\n\nProducts:\n")
    f.write(products.dtypes.to_string())
    
    f.write("\n\nSales:\n")
    f.write(sales.dtypes.to_string())

    f.write("\n\n=== NON-NUMERIC COLUMNS ===\n")
    
    f.write("\nCustomers:\n")
    f.write(", ".join(non_numeric_customers))
    
    f.write("\n\nProducts:\n")
    f.write(", ".join(non_numeric_products))
    
    f.write("\n\nSales:\n")
    f.write(", ".join(non_numeric_sales))

    f.write("\n\n=== MISSING VALUES ===\n")
    
    f.write("\nCustomers:\n")
    f.write(customers.isnull().sum().to_string())
    
    f.write("\n\nProducts:\n")
    f.write(products.isnull().sum().to_string())
    
    f.write("\n\nSales:\n")
    f.write(sales.isnull().sum().to_string())

    f.write("\n\n=== DATA QUALITY ISSUES ===\n")
    f.write(f"Formatting Issues: {format_issues}\n")
    f.write(f"Unexpected Values: {unexpected_values}\n")
    f.write(f"Negative Values: {negative_values}\n")
    f.write(f"Invalid Dates: {total_invalid_dates}\n")
    f.write(f"Negative Quantity Rows: {negative_qty}\n")
    f.write(f"Negative Price Rows: {negative_price}\n")
    f.write(f"Invalid Product IDs: {invalid_product_ids}\n")
    f.write(f"Invalid Customer IDs: {invalid_customer_ids}\n")
    f.write(f"Formatting Issues : {format_issues}\n")
