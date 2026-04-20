import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')

# 1. โหลดข้อมูลดิบ
c, s = pd.read_csv('customers.csv'), pd.read_csv('sales_transactions.csv')

# 2. เติมค่าว่างอายุ, จัดฟอร์แมตเบอร์โทร (เพิ่มการดักจับค่าว่างเปล่าและ 00), เติมโปรโมชัน
c['age'] = c['age'].fillna(c['age'].median())
c['phone_number'] = c['phone_number'].fillna('0').astype(str).str.replace(r'[^0-9+]', '', regex=True).replace(['', '00'], '0')
s['promotion_id'] = s['promotion_id'].fillna(0)

# 3. สร้างฟังก์ชันจิ๋ว (เพิ่ม .fillna() เพื่ออุดรูรั่ววันที่ก่อนแปลงค่า)
dt_fix = lambda x: pd.to_datetime(x.fillna('2024-01-01'), errors='coerce', format='mixed').dt.normalize() + pd.to_timedelta(np.random.randint(32400, 61201, len(x)), unit='s')

# เรียกใช้ฟังก์ชันจิ๋วทีละตัว (เขียนแยกบรรทัดเพื่อให้อ่านง่ายและไม่เกิด Error)
c['join_date'] = dt_fix(c['join_date'])
c['last_purchase_date'] = dt_fix(c['last_purchase_date'])
s['date'] = dt_fix(s['date'])

# 4. ส่งออกไฟล์ CSV ทันที
c.to_csv('customers_cleaned.csv3', index=False)
s.to_csv('sales_transactions_cleaned.csv', index=False)
print("✅ คลีนข้อมูลแบบย่อขั้นสุดเสร็จสมบูรณ์!")