def Cal_Sale(total):
    if total <= 3000:
        commit = 0
    elif total <= 5000:
        commit = total * 0.1
    elif total <= 8000:
        commit = total * 0.15
    else:
        commit = total * 0.2
    return commit  

name = input("Enter your name: ")
total_sales = float(input("Enter your total sales: "))

commission = Cal_Sale(total_sales)

# result
print(f"Salesperson: ", name)
print(f"Total Sales: {total_sales:,.2f}")
print(f"Commission Earned: {commission:,.2f}")
print(f"Total Earned: ", total_sales + commission)