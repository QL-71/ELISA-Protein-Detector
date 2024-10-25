### Basal Insulin Elisa Curve Fitting Program 📈🔬

This program 🖥️ is designed for conducting curve fitting in Basal Insulin Enzyme-Linked Immunosorbent Assay (Basal Insulin Elisa) 🧪.

- **GUI.py**: Contains the design of the graphical user interface. This serves as the primary interface for user interaction with the program. 💻

- **Fit_Module.py**: Includes the implementation functions for curve fitting and plotting. 📊️

- **Back_calculation.py**: Used to reverse calculate concentration values at low OD values. 📝

- **Model_function.py**: This file defines the method for identifying custom functions 🖌️

- **Basal.exe**: This is the executable file successfully packaged using PyInstaller. Users can directly run it, but ensure it is in the same folder as `Model_function.txt`. It can be packaged using the following command:

  ```
  pyinstaller --onefile --windowed --icon=rock.ico GUI.py
  ```

Tip: Users can simply download and run 'Basal.exe' ,inputting data via the graphical interface, and conducting Basal Insulin Elisa curve fitting. 🚀
