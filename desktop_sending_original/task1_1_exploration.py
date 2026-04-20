import pandas as pd
import numpy as np
import os

# ── โหลดไฟล์ CSV ───────────────────────────────────────────
customers = pd.read_csv('data/customers.csv')
products  = pd.read_csv('data/products.csv')
sales     = pd.read_csv('data/sales_transactions.csv')

# ── ฟังก์ชันช่วยงาน ─────────────────────────────────────────
def count_invalid_dates(series):
    before = series.isnull().sum()
    after  = pd.to_datetime(series, errors='coerce').isnull().sum()
    return int(after - before)

def count_extra_spaces(df, cols):
    total = 0
    for col in cols:
        if col in df.columns:
            mask = (
                df[col].dropna().astype(str).str.strip()
                != df[col].dropna().astype(str)
            )
            total += int(mask.sum())
    return total

# ── เริ่มสร้างรายงาน ─────────────────────────────────────────
lines = []

def section(title):
    lines.append("")
    lines.append("=" * 60)
    lines.append(title)
    lines.append("=" * 60)

def sub(title):
    lines.append("")
    lines.append(f"--- {title} ---")

# ════════════════════════════════════════════
#  FILE: customers.csv
# ════════════════════════════════════════════
section("FILE: customers.csv")

# 5 แถวแรก
sub("5 แถวแรก")
lines.append(customers.head().to_string())

# Data Types
sub("Data Types")
for col, dtype in customers.dtypes.items():
    lines.append(f"  {col}: {dtype}")

# Missing Values
sub("Missing Values")
for col, n in customers.isnull().sum().items():
    lines.append(f"  {col}: {n} missing")

# Inconsistencies and Anomalies
sub("Inconsistencies and Anomalies")

# Invalid Dates
lines.append(f"  Invalid Dates (join_date):          {count_invalid_dates(customers['join_date'])} rows")
lines.append(f"  Invalid Dates (last_purchase_date): {count_invalid_dates(customers['last_purchase_date'])} rows")

# Negative Values
lines.append(f"  Negative Values (age):           {int((customers['age'] < 0).sum())} rows")
lines.append(f"  Negative Values (total_spending): {int((customers['total_spending'] < 0).sum())} rows")

# Invalid IDs
lines.append(f"  Invalid IDs: N/A (customers is the reference file)")

# Unexpected Values
expected_gender = {'M', 'F'}
bad_gender = int(customers['gender'].notna().sum()) - int(customers[customers['gender'].notna()]['gender'].isin(expected_gender).sum())
lines.append(f"  Unexpected gender values: {bad_gender} rows")
lines.append(f"    Found: {customers['gender'].dropna().unique().tolist()}")

expected_mem = {'Basic', 'Silver', 'Gold'}
bad_mem = int((~customers['membership_status'].isin(expected_mem)).sum())
lines.append(f"  Unexpected membership_status: {bad_mem} rows")
lines.append(f"    Found: {customers['membership_status'].unique().tolist()}")

expected_churn = {'True', 'False'}
bad_churn = int((~customers['churned'].isin(expected_churn)).sum())
lines.append(f"  Unexpected churned values: {bad_churn} rows")
lines.append(f"    Found: {customers['churned'].unique().tolist()}")

expected_pref = {'Pastries', 'Bread', 'Tarte', 'Macaron'}
bad_pref = int(customers['preferred_category'].notna().sum()) - int(
    customers[customers['preferred_category'].notna()]['preferred_category'].str.strip().isin(expected_pref).sum()
)
lines.append(f"  Unexpected preferred_category: {bad_pref} rows")

# Formatting Issues
fmt = count_extra_spaces(customers, ['first_name','last_name','gender','membership_status','preferred_category'])
lines.append(f"  Formatting Issues (extra spaces): {fmt} rows")

# ════════════════════════════════════════════
#  FILE: products.csv
# ════════════════════════════════════════════
section("FILE: products.csv")

sub("5 แถวแรก")
lines.append(products.head().to_string())

sub("Data Types")
for col, dtype in products.dtypes.items():
    lines.append(f"  {col}: {dtype}")

sub("Missing Values")
for col, n in products.isnull().sum().items():
    lines.append(f"  {col}: {n} missing")

sub("Inconsistencies and Anomalies")

lines.append(f"  Invalid Dates (introduced_date): {count_invalid_dates(products['introduced_date'])} rows")

products['_date_parsed'] = pd.to_datetime(products['introduced_date'], errors='coerce')
future = int((products['_date_parsed'] > pd.Timestamp.today()).sum())
lines.append(f"  Future Dates  (introduced_date): {future} rows")
products.drop(columns=['_date_parsed'], inplace=True)

products['_price_num'] = pd.to_numeric(products['price'], errors='coerce')
products['_cost_num']  = pd.to_numeric(products['cost'],  errors='coerce')
lines.append(f"  Negative Values (price): {int((products['_price_num'] < 0).sum())} rows")
lines.append(f"  Negative Values (cost):  {int((products['_cost_num']  < 0).sum())} rows")
products.drop(columns=['_price_num','_cost_num'], inplace=True)

lines.append(f"  Invalid IDs: N/A (products is the reference file)")

expected_cat = {'Pastries', 'Bread', 'Tarte'}
bad_cat = int(products['category'].notna().sum()) - int(
    products[products['category'].notna()]['category'].str.strip().isin(expected_cat).sum()
)
lines.append(f"  Unexpected category values: {bad_cat} rows")
lines.append(f"    Found: {products['category'].dropna().unique().tolist()}")

expected_active = {'True', 'False'}
bad_active = int(products['active'].notna().sum()) - int(
    products[products['active'].notna()]['active'].astype(str).isin(expected_active).sum()
)
lines.append(f"  Unexpected active values: {bad_active} rows")
lines.append(f"    Found: {products['active'].dropna().unique().tolist()}")

fmt_p = count_extra_spaces(products, ['product_name','category','ingredients'])
lines.append(f"  Formatting Issues (extra spaces): {fmt_p} rows")

# ════════════════════════════════════════════
#  FILE: sales_transactions.csv
# ════════════════════════════════════════════
section("FILE: sales_transactions.csv")

sub("5 แถวแรก")
lines.append(sales.head().to_string())

sub("Data Types")
for col, dtype in sales.dtypes.items():
    lines.append(f"  {col}: {dtype}")

sub("Missing Values")
for col, n in sales.isnull().sum().items():
    lines.append(f"  {col}: {n} missing")

sub("Inconsistencies and Anomalies")

lines.append(f"  Invalid Dates (date):          {count_invalid_dates(sales['date'])} rows")
lines.append(f"  Negative Values (quantity):    {int((sales['quantity'] < 0).sum())} rows")
lines.append(f"  Negative Values (price):       {int((sales['price'] < 0).sum())} rows")
lines.append(f"  Negative Values (discount_amount): {int((sales['discount_amount'] < 0).sum())} rows")

valid_pids = set(products['product_id'].dropna().astype(int))
valid_cids = set(customers['customer_id'])
lines.append(f"  Invalid product_id  (not in products.csv):  {int((~sales['product_id'].isin(valid_pids)).sum())} rows")
lines.append(f"  Invalid customer_id (not in customers.csv): {int((~sales['customer_id'].isin(valid_cids)).sum())} rows")

expected_pay = {'Credit Card', 'Mobile Pay', 'Cash'}
bad_pay = int((~sales['payment_method'].isin(expected_pay)).sum())
lines.append(f"  Unexpected payment_method: {bad_pay} rows")
lines.append(f"    Found: {sales['payment_method'].unique().tolist()}")

expected_ch = {'Online', 'In-store'}
bad_ch = int((~sales['channel'].isin(expected_ch)).sum())
lines.append(f"  Unexpected channel: {bad_ch} rows")
lines.append(f"    Found: {sales['channel'].unique().tolist()}")

fmt_s = count_extra_spaces(sales, ['payment_method','channel'])
lines.append(f"  Formatting Issues (extra spaces): {fmt_s} rows")

# ── บันทึกไฟล์ ───────────────────────────────────────────────
lines.append("")
lines.append("=" * 60)
lines.append("END OF REPORT")
lines.append("=" * 60)

os.makedirs('output', exist_ok=True)
with open('output/Session1_DataExploration.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("✓ บันทึกไฟล์ Session1_DataExploration.txt สำเร็จ")
