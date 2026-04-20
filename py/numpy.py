import numpy as np
sale = np.array([3500, 4500, 2000, 6000, 3000, 10000, 8000])
np.array(list)

#vat = price * 0.07
com = sale * 0.10
after_com = sale - com
after_bo = after_com + 500
after_vat = after_bo * 0.07

print("Sum :", after_vat.sum())
print("Max :", after_vat.max())
print("Min :", after_vat.min())
print("Average :", after_vat.mean())