
import numpy as np

from sklearn.preprocessing import StandardScaler

input_lst= [1.92630000e+03, 2.74882906e-02, 3.08585808e+02, 3.80237682e+02,
 7.37851738e+05, 6.91044949e+02, 1.01853643e+01, 5.02332899e+00,
 3.50000000e+02 ,1.11900000e+02, 1.98311322e+00]

inp_data_norm=StandardScaler().fit_transform(np.array(input_lst).reshape(-1,1))
lst = inp_data_norm.reshape(1, -1).tolist()
print(lst)