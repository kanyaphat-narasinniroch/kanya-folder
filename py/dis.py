#Program5
def Cal_Discount(total):
    if total <= 500:
        discount = 0
    elif total <= 1000:
        discount = total * 0.05
    elif total <= 3000:
        discount = total * 0.1
    elif total <= 5000:
        discount = total * 0.15
    else:
        discount = total * 0.2
    return discount  

name = input("Enter your name: ")
total_am = float(input("Enter your Total Amount: "))


disc = Cal_Discount(total_am)


# result
print(f"Customer: ", name)
print(f"Total Amount: {total_am:,.2f}")
print(f"Discount Earned: {disc:,.2f}")
print(f"Total Amount After Discount: ", total_am - disc)