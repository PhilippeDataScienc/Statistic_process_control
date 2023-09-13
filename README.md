# Statistic Process Control (SPC) Documentation

## Introduction

The Statistic Process Control (SPC) class is designed to assess the capability of a process variable extracted from a CSV file. SPC is a statistical method commonly used in quality control and manufacturing to monitor and analyze process data to ensure it remains within specified limits. This documentation provides detailed information on how to use the SPC class, what it does, and identifies potential vulnerabilities in the code.

## Prerequisites

Before using the SPC class, make sure you have the following prerequisites installed on your local machine:

* Python (version 3.6 or later)
* Pandas library
* Matplotlib library
* SciPy library
* NumPy library

You can install these libraries using the following pip commands:

`pip install pandas matplotlib scipy numpy`

## Code Overview

The SPC class consists of the following attributes and methods:

### Attributes
1. **path** (str): The path to the CSV file containing the process variable data.
2. **signal** (str): The name of the signal to be processed. By default, it is set to "mean_ir_pwr."
### Methods
1. **csv_to_df(self) -> pd.DataFrame**
    * Description: Transforms the CSV file into a Pandas DataFrame.
    * Returns: DataFrame with layers in column 1 and the specified signal in column 2, or an empty DataFrame if an error is detected.
2. **print_columns(self) -> list**
    * Description: Helps the user see the column names of the CSV file.
    * Returns: Prints a list of the column names.
3. **normality_test(self) -> int**
    * Description: Performs a normality test (Shapiro-Wilk) for the signal variable.
    * Returns:
      * 1 with a normal message (95% confidence) if the distribution is normal, otherwise 0 with an error message.
4. **plot_graph(self) -> plt**
    * Description: Plots a series of graphs representing the data distribution.
    * Returns: Histogram with a mean line and a scatter graph with the mean line.
5. **get_cpk(self, lsl: float = -1, usl: float = 1) -> tuple**
    * Description: Computes the Cp and Cpk for the specified signal if it has a normal distribution.
    * Parameters:
      * lsl (float): Lower specification limit of the variable (default = -1).
      * usl (float): Upper specification limit of the variable (default = 1).
    * Returns:
      * Cp and Cpk for the given signal if there is a normal distribution, None otherwise.

## How to Use
To use the SPC class on your local machine, follow these steps:

1. Create an instance of the StatisticProcessControl class by providing the path to your CSV file and, if needed, the name of the signal to be processed.

    `spc = StatisticProcessControl("path/to/your/data.csv", "your_signal_column_name")`

2. You can then perform various operations using the class methods:

  * Transform the CSV file into a DataFrame:

    `data_frame = spc.csv_to_df()`
  * Print the column names of the CSV file:

    `spc.print_columns()`
    
  * Check the normality of the signal distribution:

    `spc.normality_test()`

  * Plot data distribution graphs:

    `spc.plot_graph()`
    
  * Calculate Cp and Cpk:

    `cp, cpk = spc.get_cpk(lower_spec_limit, upper_spec_limit)`
    
3. Ensure you have the necessary libraries installed (Pandas, Matplotlib, SciPy, and NumPy).
4. Run your Python script that uses the SPC class.
