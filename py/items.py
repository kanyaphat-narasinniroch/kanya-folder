items = ["Lipstick", "Powder", "Mascara", "Eyeliner", "Blush", "Sunscreen", "Serum", "Toner"]

print("1.Select Data")
print("2.Add Data")
print("3.Remove Data")
print("4.Find Data")
print("5.Exit")

menu = int(input("Please Select Menu : "))

if menu == 1:
    print("1. ",items[3])
    print("2. ",items[-1])
    print("3. ",items[0:3])
    print("4. ",items[-3:])
    print("5. ",items[2:5])
    
elif menu == 2:
    add = input("Please Enter Name of Product for ADDING: ")
    items.append(add)
    print("ADD", add, "Success!")
    print(items)
    
elif menu == 3:
    re = input("Please Enter Name of Product for REMOVE: ")
    items.remove(re)
    print("REMOVE", re, "Success!")
    print(items)
    
elif menu == 4:
    fi = input("Please enter Name of Product to Find : ")
    if fi in items:
        print("This Product In Stock !")
    else:
        print("This Product Out Of Stock !")
else:
    print("Thank you for using our service.")
    