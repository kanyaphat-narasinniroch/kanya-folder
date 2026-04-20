#import
import pandas as pd
import numpy as np

customers = pd.read_csv('data/customers.csv')
products = pd.read_csv('data/products.csv')
sales_transac = pd.read_csv('data/sales_transactions.csv')

#f.write == writing text file
#dtypes == type of all data
#Last Lines == .Tails()
#Columns == columns
#### First (5) Lines == .Head ####

#################################### 5 DataFrame  ###############################
print("-"*15," First 5 DataFrame of CUSTOMERS","-"*15)
print(customers.head())

print("-"*15," 5 DataFrame of PRODUCT ","-"*15)
print(products.head())

print("-"*15," 5 DataFrame of SALES_TRANSACTIONS ","-"*15)
print(sales_transac.head())

#################################### CUSTOMERS ###############################
print("-"*15," First 5 DataFrame of CUSTOMERS","-"*15)
print(customers.head())
print(customers.dtypes)
print(customers.isnull().sum())
#หารูปแบบวันที่
#bef = customers['join_date'].isnull().sum()
#par = pd.to_datetime(customers['join_date'], errors='coerce')
#aft = par.isnull().sum()
#invalid_dates = aft - befw
#print(f"Invalid Date : {invalid_dates} Rows")

customers['c_date'] = pd.to_datetime(customers['join_date'], errors='coerce')
invalid_c_date = customers[
                           (customers["c_date"].isna()) |
                           (customers["c_date"] < '2000-01-01') |
                           (customers["c_date"] > '2000-03-23')
                        ].shape[0]

print(f"Invalid Date : {invalid_c_date}")

#################################### PRODUCT ###############################

print("-"*15," 5 DataFrame of PRODUCT ","-"*15)
print(products.head())
print(products.dtypes)
print(products.isnull().sum())
#Date
products['p_date'] = pd.to_datetime(products['introduced_date'], errors='coerce',dayfirst=True)
invalid_p_date = products[
                           (products["p_date"].isna()) |
                           (products["p_date"] < '2000-01-01') |
                           (products["p_date"] > '2000-03-23')
                        ].shape[0]
print(f"Invalid Date Product: {invalid_p_date}")

############################# SALES_TRANSACTIONS #################################

print("-"*15," 5 DataFrame of SALES_TRANSACTIONS ","-"*15)
print(sales_transac.head())
print(sales_transac.dtypes)
print(sales_transac.isnull().sum())
#นับจำนวนที่ติดลบ
negtv_co_pri = (sales_transac['price'] < 0).sum()
negtv_qt_pri = (sales_transac['quantity'] < 0).sum()
negtv_dc_pri = (sales_transac['discount_amount'] < 0).sum()
print("co : ", negtv_co_pri)
print("qt : ", negtv_qt_pri)
print("dc : ", negtv_dc_pri)

#Date
sales_transac['s_date'] = pd.to_datetime(sales_transac['date'], errors='coerce',dayfirst=True)
invalid_s_date = sales_transac[
                           (sales_transac["s_date"].isna()) |
                           (sales_transac["s_date"] < '2000-01-01') |
                           (sales_transac["s_date"] > '2000-03-23')
                        ].shape[0]
print(f"Invalid Date sales_transac : {invalid_s_date}")

###########################################################################

valid_pd_id = set(products['product_id'].dropna().astype(int))
valid_cus_id = set(customers['customer_id'])
not_match_pd = (~sales_transac['product_id'].isin(valid_pd_id)).sum()
not_match_cus = (~sales_transac['customer_id'].isin(valid_cus_id)).sum()
print(f"มีใน sales ไม่มีใน cus : {not_match_cus}")
print(f"มีใน sales ไม่มีใน pd : {not_match_pd}")

format_issues = (
      (customers['first_name'] != customers['first_name'].str.strip()) |
      (customers['last_name'] != customers['last_name'].str.strip())
      ).sum()
print(f"จำนวนชื่อและนามสกุลที่รูปแบบผิด : {format_issues} รายการ")

# def check(df, column_name, valid_values=['TRUE', 'FALSE']):
#     if column_name in df.columns:
#         # ใช้ ~ คือ "ไม่" (NOT) และ .isin() เพื่อเช็คว่าอยู่ในกลุ่มที่ยอมรับไหม
#         invalid_mask = ~df[column_name].fillna('').astype(str).isin(valid_values)
#         return invalid_mask.sum()
#     else:
#         print(f"Warning: Column '{column_name}' not found.")
#         return 0 

# # วิธีใช้งาน
# churned_v = check(customers, 'churned')
# print(f"จำนวน churned นอกเหนือจาก T,F: {churned_v} รายการ")


### Gender Checking ###
gender_v = 0
if 'gender' in customers.columns:
      gender_v = (~customers['gender'].fillna('').isin(['M','F'])).sum()
print(f"จำนวนเพศนอกเหนือจาก M,F : {gender_v} รายการ")

### churned Checking ###
churned_v = 0
if 'churned' in customers.columns:
      churned_v = (~customers['churned'].fillna('').isin(['True', 'False'])).sum()
print(f"จำนวน churned เหนือจาก T,F : {churned_v} รายการ")

### phone Checking ###
phones = customers['phone_number']
missing = phones.isnull().sum()
format = phones.dropna().astype(str).str.contains(r'[() \-]', regex=True).sum()
garb = phones.dropna().astype(str).str.contains(r'[a-zA-Z!@#$%^&*|{}\[\]<>~]', regex=True).sum()
print(f"NaN:         {missing}")    # 40
print(f"Formatting:  {format}") # 50  (มี space/dash/วงเล็บ)
print(f"Garbage:     {garb}")    # 42  (ตัวอักษร/อักขระแปลก)
print(f"รวมต้องแก้:  {missing+format+garb}")  

# ตรวจภาษาไทย (\u0E00-\u0E7F = ช่วง Unicode ภาษาไทย)
thai_first = customers['first_name'].dropna().astype(str) \
             .str.contains(r'[\u0E00-\u0E7F]', regex=True).sum()
thai_last  = customers['last_name'].dropna().astype(str) \
             .str.contains(r'[\u0E00-\u0E7F]', regex=True).sum()

print(f"first_name มีภาษาไทย: {thai_first} rows")  # 0
print(f"last_name  มีภาษาไทย: {thai_last} rows")   # 0

### Active Checking ###
active_v = 0
if 'active' in products.columns:
      active_v = (~products['active'].fillna('').isin(['TRUE','FALSE'])).sum()
print(f"จำนวน Active นอกเหนือจาก TRUE FALSE : {active_v} รายการ")

### seasonal Checking ###
seasonal_v = 0
if 'seasonal' in products.columns:
      seasonal_v = (~products['seasonal'].fillna('').isin(['TRUE','FALSE'])).sum()
print(f"จำนวน seasonal นอกเหนือจาก TRUE FALSE : {seasonal_v} รายการ")

### seasonal Checking ###
payment_v = 0
if 'payment_method' in sales_transac.columns:
      payment_v = (~sales_transac['payment_method'].fillna('').isin(['Credit Card','Mobile Pay', 'Cash'])).sum()
print(f"จำนวน payment_method นอกเหนือจาก 'Credit Card','Mobile Pay', 'Cash' : {payment_v} รายการ")

###########################################################################

def write(df,name,file):
        f.write(f"{name}\n")
        f.write(df.head().to_string())
        f.write("\n++ TYPES ++\n")
        f.write(df.dtypes.to_string())
        f.write("\n++ MISSING DATA ++\n")
        f.write(df.isnull().sum().to_string())
        f.write("\n")
        f.write("="*250)

with open("output/Session1_DataExploration.txt",
          'w', encoding='utf8') as f:
    
    write(sales_transac,"DataFrame Of sales_transac's",f)
    #CUSTOMERS
    #f.write("* 5 DataFrame of CUSTOMERS\n")
    #f.write(customers.head().to_string())
    #f.write("\n++TYPES\n")
    #f.write(customers.dtypes.to_string())
    #f.write("\n")
    #f.write("\n++MISSING DATA\n")
    #f.write(customers.isnull().sum().to_string())
    #f.write("\n")
    #f.write("="*250)

    #PRODUCT
    #f.write("\n* 5 DataFrame of PRODUCT\n")
    #f.write(products.head().to_string())
    #f.write("\n++TYPES\n")
    #f.write(products.dtypes.to_string())
    #f.write("\n")
    #f.write("\n++MISSING DATA\n")
    #f.write(products.isnull().sum().to_string())
    #f.write("\n")
    #f.write("="*250)

#     ##SALES_TRANSACTIONS
#     f.write("\n* 5 DataFrame of SALES_TRANSACTIONS\n")
#     f.write(sales_transac.head().to_string())
#     f.write("\n++TYPES\n")
#     f.write(sales_transac.dtypes.to_string())
#     f.write("\n")
#     f.write("\n++MISSING DATA\n")
#     f.write(sales_transac.isnull().sum().to_string())
#     f.write("\n")
#     f.write("="*250)
#     f.write("\n")
    f.write("\n")
    f.write(str(not_match_cus))
    f.write("\n")
    f.write(str(not_match_pd))






