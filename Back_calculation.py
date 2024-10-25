import warnings
warnings.filterwarnings('ignore')
import numpy as np
from scipy.optimize import fsolve

def back_calculation(y, f, y0, params):

    # Initialize the array to store the concentrations
    conc_c = np.zeros_like(y)



    # Define the function to find the root
    def f_zero(x, y, **kwargs):
        return f(x, **kwargs) - y

    # Loop through each OD reading and find the corresponding concentration
    for i, y_val in enumerate(y):
        # Define the shifted function for root finding
        shifted_fcurve = lambda x: f_zero(x, y_val, **params)
        
        # Find the root using fsolve
        conc_c[i] = fsolve(shifted_fcurve, y0)[0]


    return conc_c

