import pandas as pd, warnings; warnings.filterwarnings('ignore')

dfs = {f:pd.read_csv(f) for f in ['customers.csv', 'products.csv', 'sales_transactions.csv']}
# ดึงข้อมูล 3 ตาราง
[ display(d.head()) for d in dfs.values() ]
# เป็นค่าว่างรอข้อมูลมาใส่
report = ""


# ....c = ... check
# ....m = ....mask
for name, df in dfs.items():
    # col = column \\ typ = types
    report += f"\n########## File: {name} #########\nData Types:\n" + "\n".join([f"-{col}:{typ}" for col, typ in df.dtypes.items()]) + "\n\nInconsistencies Or Anomalies:\n"
    
    # find column that has "date" in it
    dc = [col for col in df.columns if 'date' in col.lower()]
    
    # concat คือ ฟังก์ชันสำหรับ "เชื่อม" หรือ "รวม" อ็อบเจ็กต์ Pandas (DataFrame หรือ Series) ตั้งแต่ 2 ชุดขึ้นไปเข้าด้วยกันตามแกนที่กำหนด (Axis)
    ############################################################################# Date Time Checking #####################################################################################
    dm = pd.concat([pd.to_datetime(df [col], errors='coerce').pipe(lambda s: s.isna() | ~s.dt.year.between(2010, 2025)) for col in dc ], axis = 1).any(axis = 1) if dc else [0] * len (df)

    # find column that has 'quantity', 'price', 'cost' in it
    nc = [col for col in ['quantity', 'price', 'cost'] if col in df.columns]

    ############################################################################ Negative Number Checking #####################################################################################
    nm = pd.concat([pd.to_numeric(df[col].astype(str).str.replace('$','', regex = False), errors = 'coerce') < 0 for col in nc], axis = 1).any(axis = 1) if nc else [0] * len(df)

    # find column that has ID in it if null = 0
    idm = (~df.customer_id.isin(dfs['customers.csv'].customer_id) | ~df.product_id.isin(dfs['products.csv'].product_id)) if name == 'sales_transactions.csv' else [0] * len(df)
    
    ############################################################################ Unexpected Checking #####################################################################################
    um = (
        (~df.gender.isin(['M','F']) |
         ~df.membership_status.str.title().isin(['Basic','Silver','Gold']) |
         ~df.churned.isin(['TRUE','FALSE']))
        if name == 'customers.csv'
        
        else
        (~df.category.isin(['Pastries','Bread','Tarte','Viennoiserie']) |
         ~df.seasonal.isin(['TRUE','FALSE']) |
         ~df.active.isin(['TRUE','FALSE']) )
        if name == 'products.csv'
        
        else
        (~df.payment_method.isin(['Credit Card','Mobile Pay','Cash']) |
         ~df.channel.isin(['Online','In-store']))

        if name == 'sales_transactions.csv' else [0]*len(df))
    ############################################################################ Formatting Issues Checking #####################################################################################
    fm = (
        (df.first_name.str.contains(r'^\s|\s$|[ก-๙]') |
        df.last_name.str.contains(r'^\s|\s$|[ก-๙]') |
        df.email.str.contains(r'^\s|\s$|[A-Z]|[ก-๙]'))
        if name == 'customers.csv'
        
        else
        (df.product_name.str.contains(r'^\s|\s$|[ก-๙]') |
        df.ingredients.str.contains(r'^\s|\s$|[ก-๙]') |
        df.ingredients.isna() |
        df.price.astype(str).str.contains('\$') |
        df.cost.astype(str).str.contains('\$') ) 
        if name == 'products.csv' else [0]*len(df))
    ############################################################################ Reporting #####################################################################################
    report += f" Invalid Dates : {sum(dm)}\n\
    Negative Values : {sum(nm)}\n\
    Invalid IDs : {sum(idm)}\n\
    Unexpected Values : {sum(um)}\n\
    Formatting Issues : {sum(fm)}\n\
    \n" + "="*60 + "\n"

print(report)
open('output/Session1_DataExploration.txt', 'w', encoding='utf-8').write(report.strip())
    