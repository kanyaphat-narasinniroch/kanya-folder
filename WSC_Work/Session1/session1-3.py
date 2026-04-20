#import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt;
from matplotlib.backends.backend_pdf \
import PdfPages

df = pd.read_csv('output/sales_transactions_cleaned.csv')
df = df.assign(
    date=lambda x: pd.to_datetime(x['date']).dt.strftime('%Y-%m')
    )

price = pd.to_numeric(
    df['price'].astype(str).str.replace('$',''),
    errors='coerce')

quantity = pd.to_numeric(
    df['quantity'],
    errors='coerce').fillna(0)

discount = pd.to_numeric(
    df['discount_amount'],
    errors='coerce').fillna('0')

df['revenue'] = (price * quantity) - discount

m_stats = df.groupby('date').agg(
    rev = ('revenue', 'sum'),
    ts = ('transaction_id', 'nunique')
)

# รายได้ต่อวัน
m_stats = m_stats.assign(
    aov = lambda x: x['rev'] / x['ts']
)

# เรียง
m_stats = m_stats.sort_index()
m_stats = m_stats.reset_index()

# หา top 3
top3 = m_stats.nlargest(3, 'rev')
top3 = top3[['date', 'rev']]
top3 = top3.assign(
    rev = lambda x: x['rev'].apply(lambda v: f"${v:,.2f}")
)

# สร้าง pdf
with PdfPages('Session1_SalesTrends.pdf') as pdf:
    # figsize คือ กว้าง*ยาว
    # ax = axis
    fig, ax = plt.subplots(3, 1, figsize = (10, 12))
    fig.tight_layout(pad = 6.0)

    # ข้อมูลที่่แสดง
    plots = [
        ('rev', 'red', 'Total Sale Revenue'),
        ('ts', 'blue', 'Number of transactions per month'),
        ('aov', 'green', 'Average order value per month')
    ]
    
    # loop สร้างกราฟ
    for i, (col, c, title) in enumerate(plots):
        ax[i].plot(
            m_stats['date'],
            m_stats[col],
            marker = 'o',
            color = c
        )
        ax[i].set_title(title, weight = 'bold', )
        ax[i].tick_params(axis = 'x', rotation = 45 )
        ax[i].grid(ls = '--')

    pdf.savefig(fig, bbox_inches = 'tight')
    plt.close()
    # จบ พาร์ทสร้าง pdf

    # เขียนอะไรสักอย่างลงตาราง
    fig, ax = plt.subplots(figsize = (6, 2))
    ax.axis('off') #เอามุมออก

    table = ax.table(
        cellText = top3.values, 
        # ตัวหนังสือข้างใน col
        colLabels = ['Month', 'Total Sale Revenue'],
        loc = 'center',
        cellLoc = 'center',
        colColours = ['xkcd:sky blue', 'xkcd:electric purple']
    )

    table.scale(1,2)
    ax.set_title('Top 3 Month', weight = 'bold')

    pdf.savefig(fig, bbox_inches = 'tight')
    plt.close()
    # จบ พาร์ทสร้าง ตาราง