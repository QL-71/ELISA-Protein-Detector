import inspect
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from scipy.optimize import curve_fit, least_squares
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize

def insulin_curve_fit3(con_x, od_y, f, methods, initial_guess):
    # Define the objective function to minimize
    def objective(params):
        model_prediction = f(con_x, *params)
        residuals = od_y - model_prediction
        return np.sum(residuals**2)

    if methods == 'Levenberg-Marquardt':
        popt, pcov = curve_fit(f, con_x, od_y, p0=initial_guess, ftol=1.49012e-16, maxfev=100000)
    elif methods == 'BFGS':
        initial_guess = [0.5, 0.5, 0.5, 0.5, 0.5]  #Example initial guess
        result = minimize(objective, initial_guess, method=methods, tol=1e-16)

        # Extract the fitted parameters
        popt = result.x
    elif methods == 'Nonlinear-Least-Square':
        #Using Least_Squares for Nonlinear Least Squares Fitting
        result = least_squares(lambda params: f(con_x, *params) - od_y, initial_guess)
        popt = result.x
    else:
        # Perform the optimization
        result = minimize(objective, initial_guess, method = methods, jac = None, tol=1e-16)
        
        # Extract the fitted parameters
        popt = result.x
    
    # Calculate the goodness-of-fit
    model_prediction = f(con_x, *popt)
    residuals = od_y - model_prediction
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((od_y - np.mean(od_y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Prepare the result
    fitresult = {
        "Prediction": model_prediction,
        'params': popt,
        'residuals': residuals,
        'r_squared': r_squared
    }
    
    return fitresult

def plot_graph(con_x, od_y, model_prediction):

    # Plot the data and the curve fit
    plt.figure(figsize=(8, 6))
    plt.scatter(con_x, od_y, label='Data', marker='.')
    plt.plot(con_x, model_prediction, 'r-', label='Curve Fit')
    plt.xlabel('Concentration')
    plt.ylabel('OD')
    plt.title('Insulin Concentration Curve Fit')
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_graph2(con_x, od_y, model_prediction):
    # Set style using seaborn
    sns.set(style="whitegrid")

    # Plot the data and the curve fit
    plt.figure(figsize=(10, 6))

    # Plot data points
    plt.scatter(con_x, od_y, label='Data', color='blue', marker='.', alpha=0.6)

    # Plot curve fit line
    plt.plot(con_x, model_prediction, color='red', linestyle='-', linewidth=2, label='Curve Fit')

    # Add labels and title
    plt.xlabel('Concentration', fontsize=14)
    plt.ylabel('OD', fontsize=14)
    plt.title('Insulin Concentration Curve Fit', fontsize=16)

    # Add legend
    plt.legend(loc='upper left', fontsize=12)

    # Add grid
    plt.grid(True)

    # Add interactive features
    plt.tight_layout()
    plt.show()

