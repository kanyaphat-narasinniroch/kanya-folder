#import
import pandas as pd
import numpy as np
import os

customers = pd.read_csv('data/customers.csv')
sales_transac = pd.read_csv('data/sales_transactions.csv')
#for creating auto folder
os.makedirs('output', exist_ok=True)


# หาค่า median
age_median = customers['age'].median()
print(age_median)
# แทนที่ค่าว่าง (NaN) ด้วยค่า Median
customers['age'] = customers['age'].fillna(age_median)
print(f"Customer's Age :\n{customers['age'].head()}")

print("="*25)

# แทนที่ค่าว่าง (NaN) ด้วย 0
customers['phone_number'] = customers['phone_number'].fillna('0')
print(f"Phone Number :\n{customers['phone_number'].head()}")

print("="*25)

# Clean เบอร์โทร
customers['phone_number'] = (
    customers['phone_number'].astype(str).str.replace(r'[^\d+]','',regex=True)
    .replace('nan','0') 
) 

print("="*25)
# แทนที่ค่าว่าง (NaN) ด้วย 0
sales_transac['promotion_id'] = sales_transac['promotion_id'].fillna('0')
print(f"Promotion :\n{sales_transac['promotion_id'].head()}")


# Random the time
# 1. จัดการค่าว่างให้เป็น '0' และเปลี่ยนเป็น String
# ใช้ fillna ก่อน astype(str) เพื่อไม่ให้เกิดคำว่า 'nan' ในตาราง
customers['phone_number'] = customers['phone_number'].fillna('0').astype(str)

# 2. ใช้ Regex [^\d+] เพื่อลบทุกอย่าง "ยกเว้น" ตัวเลขและเครื่องหมาย +
customers['phone_number'] = customers['phone_number'].str.replace(r'[^\d+]', '', regex=True)

# 3. เช็คผลลัพธ์ทันทีใน Terminal (ไม่ต้องรอไปดูใน Excel)
print("--- ตรวจสอบเบอร์โทรศัพท์ 10 แถวแรก ---")
print(customers['phone_number'].head(10))

# Fixed Random the time function
def time_random(date):
    # Count how many rows we have
    a = len(date)
    
    # Use to_timedelta so we are adding "hours/minutes" as durations
    random_durations = (
        pd.to_timedelta(np.random.randint(9, 17, size=a), unit='h') +
        pd.to_timedelta(np.random.randint(0, 59, size=a), unit='m') +
        pd.to_timedelta(np.random.randint(0, 59, size=a), unit='s')
    )
    
    # Apply only to non-null dates
    mask = date.notna()
    result = date.copy()
    
    # Result = Date (Point in time) + Duration (Timedelta)
    result[mask] = date[mask] + random_durations[mask]
    return result

sales_transac['date'] = pd.to_datetime(sales_transac['date'],errors='coerce')
sales_transac['date'] = time_random(sales_transac['date'])


#creating excel file that's cleaning !!!!! Last part
customers.to_csv('output/customers_cleaned.csv', index=False, encoding='utf-8')
sales_transac.to_csv('output/sales_transactions_cleaned.csv', index=False, encoding='utf-8')