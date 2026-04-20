import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')

# --- ส่วนการโหลดข้อมูล ---
dfs = {f: pd.read_csv(f) for f in ['sales_transactions.csv', 'products.csv', 'customers.csv']}

[display(d.head()) for d in dfs.values()]

report = ""

# --- เริ่ม Loop ตรวจสอบข้อมูล ---
for name, df in dfs.items():
    report += f"### File: {name}\nData Types:\n" + "\n".join([f"- {c}: {t}" for c, t in df.dtypes.items()]) + "\n\nInconsistencies:\n"
    
    # ตรวจสอบวันที่
    dc = [c for c in df.columns if 'date' in c.lower()]
    dm = pd.concat([
        pd.to_datetime(df[c], errors='coerce').pipe(lambda s: s.isna() | ~s.dt.year.between(2010, 2025)) 
        for c in dc
    ], axis=1).any(axis=1) if dc else [0]*len(df)
    
    # ตรวจสอบค่าลบ
    nc = [c for c in ['quantity', 'price', 'cost'] if c in df.columns]
    nm = pd.concat([
        pd.to_numeric(df[c].astype(str).str.replace('$', '', regex=False), errors='coerce') < 0 
        for c in nc
    ], axis=1).any(axis=1) if nc else [0]*len(df)
    
    # ตรวจสอบ ID ข้ามตาราง
    im = (
        ~df.customer_id.isin(dfs['customers.csv'].customer_id) | 
        ~df.product_id.isin(dfs['products.csv'].product_id)
    ) if name == 'sales_transactions.csv' else [0]*len(df)
    
    # ตรวจสอบค่าผิดปกติ (Unexpected Values)
    um = (
        ~df.gender.isin(['M','F']) | 
        ~df.membership_status.str.title().isin(['Basic','Silver','Gold'])
    ) if name == 'customers.csv' else (
        ~df.category.isin(['Pastries','Bread','Tarte']) if name == 'products.csv' else [0]*len(df)
    )
    
    # ตรวจสอบรูปแบบ (Formatting Issues)
    fm = (
        df.first_name.str.contains('^\s|\s$') | 
        df.email.str.contains('[A-Z]')
    ) if name == 'customers.csv' else (
        df.price.astype(str).str.contains('\$') 
    )if name == 'products.csv' else [0]*len(df)
    
    # สะสมผลลัพธ์ลงใน Report
    report += f"- Invalid Dates: {sum(dm)}\n- Neg Values: {sum(nm)}\n- Invalid IDs: {sum(im)}\n- Unexpected: {sum(um)}\n- Format Issues: {sum(fm)}\n{'-'*30}\n\n"

# --- ส่งออกไฟล์รายงาน ---
open('Session1_DataExploration.txt', 'w', encoding='utf-8').write(report.strip())

print("✅ Done! Report looks professional.")