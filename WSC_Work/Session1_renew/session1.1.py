import pandas as pd

# Loop import
files = [
    'data/customers.csv',
    'data/products.csv',
    'data/sales_transactions.csv'
]

dfs = {}

report = ""

for fe in files:
    dfs[fe] = pd.read_csv(fe)

# print(dfs)

for name, df in dfs.items():
    print(f"\n{name} HEAD :")
    print(df.head())

for name, df in dfs.items(): #ดูข้อมูลข้างใน

    report += "\nInconsistancy and Anomolies :\n"
    report += f"### File : {name}\n"
    report += "Preview Head :\n"
    report += df.head().to_string()
    report += "\n"
    report += "Data Types :\n"

    report += "\n".join([
        f"- {c}: {t}" for c, t in df.dtypes.items() #ดูไทป์ข้อมูล
    ])
#ประกาศออกมา
#print(report)

# หาเวลาที่เกินกำหนด
    d_cols = [
    c for c in df.columns
    if 'date' in c.lower()
    ]
    
    if d_cols:
        d_mask = pd.concat([
            df[c].notna() & (
                pd.to_datetime(df[c], errors='coerce', format = 'mixed').isna() | 
                ~pd.to_datetime(df[c], errors='coerce', format = 'mixed').dt.year.between(2010, 2025)
            )
            for c in d_cols
        ], axis = 1 ).any(axis = 1)
    else:
        d_mask = [False] * len(df)
# print(d_mask)

# หาตัวเลขที่ติดลบ
    n_cols = [
    c for c in ['quantity', 'price', 'cost']
    
    if c in df.columns 
    ]

    if n_cols:
        n_mask = pd.concat([
            pd.to_numeric(
                df[c].astype(str).str.replace('$',''), errors='coerce'
            ) < 0

            for  c in n_cols
        ], axis=1).any(axis = 1)
    else:
        n_mask = [False] * len(df)

    if name == 'data/sales_transactions.csv':
        id_mask = (
            ~df['customer_id'].isin(
                dfs['data/customers.csv']['customer_id']
            ) |
            ~df['product_id'].isin(
                dfs['data/products.csv']['product_id']
            )
        )
    else:
        id_mask = [False] * len(df)

#print(n_mask)

    if name == 'data/customers.csv':
        fname_mask = (
            df['first_name'].str.contains(r'^\s|\s$|s{2,}', na = False) |
            df['last_name'].str.contains(r'^\s|\s$|s{2,}', na = False) |
            df['email'].str.contains(r'[A-Z]', na = False) |
            df['phone_number'].str.contains(r'[\-\(\)]', na = False) 
        )
    elif name == 'data/products.csv':
        fname_mask = (
            df['product_name'].str.contains(r'^\s|\s$|s{2,}', na = False) |
            df['ingredients'].str.contains(r'^\s|\s$|s{2,}', na = False)
        )
    else:
        fname_mask = [False] * len(df)

    if name == 'data/customers.csv':
        unp_mask = (
            ( ~df['gender'].isin(['M','F']) & df['gender'].notna() ) |
            ( ~df['membership_status'].str.capitalize().isin(['Basic','Gold','Silver']) & df['membership_status'].notna() ) |
            (  df['preferred_category'].notna() ) |
            ( ~df['churned'].isin(['FALSE','TRUE']) & df['churned'].notna() ) 
            
        )
    elif name == 'data/sales_transactions.csv':
        unp_mask = (
            ( ~df['payment_method'].isin(['Credit Card', 'Cash', 'Mobile Pay']) & df['payment_method'].notna() ) |
            ( ~df['channel'].isin(['Online', 'In-store']) & df['channel'].notna() ) 
        )
    elif name == 'data/products.csv':
        unp_mask = (
            ( ~df['category'].isin(['Tarte', 'Bread', 'Pastry', 'Viennoiserie', 'N/A']) & df['category'].notna() ) |
            ( ~df['seasonal'].isin(['FALSE','TRUE']) & df['seasonal'].notna() ) |
            ( ~df['active'].isin(['FALSE','TRUE']) & df['active'].notna() ) 
        )
    else:
        unp_mask = [False] * len(df)

    # print(f"ERROR :\n{ername_mask}, \nPrice : \n{unp_mask}")
    report += "\n"
    report += "/"*50
    report += f"\nInvalid Dates : {sum(d_mask)}\n"
    report += f"Negative Values : {sum(n_mask)}\n"
    report += f"Invalid ID's: {sum(id_mask)}\n"
    report += f"Unexpected Values: {sum(unp_mask)}\n"
    report += f"Formatting Issues: {sum(fname_mask)}\n"
    report += "*"*50

with open('Session1_DataExploration.txt','w',encoding='utf-8') as f:
    f.write(report.strip())