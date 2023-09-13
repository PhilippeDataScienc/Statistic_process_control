import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


class StatisticProcessControl:
    """
    A class used to assess the capability of a process variable taken from a csv file

    ...

    Attributes
    ----------
    path : str
        the path of the csv file containing the variable
    signal : str
        the name of the signal to be processes (default = "mean_ir_pwr")

    Methods
    -------
    csv_to_df()
        transform the csv file into a panda DataFrame

    print_columns()
        Help user to see the column name of the csv file

    normality_test()
        Normality test (Shapiro) for the signal variable

    plot_graph()
        plot a series of graphs representing the data distribution

    calcul_cpk()
        Calcul le Cp et le Cpk du signal

    """
    def __init__(self, path: str, signal: str = "mean_ir_pwr"):
        self.path = path  # csv path
        self.signal = signal  # name of the column to be analyzed in the csv file

    def csv_to_df(self) -> pd.DataFrame:
        """
        transform the csv file into a panda DataFrame
        :return: Dataframe with layers in column 1 and signal in column 2, or return empty dataframe if error detected
        """
        try:
            csv = pd.read_csv(self.path)
            return csv[['layer', self.signal]]
        except KeyError:
            print(f"{self.signal} not in index, please choose a correct signal: see print_column() method")
            csv = pd.DataFrame()
            return csv
        except FileNotFoundError:
            print(f"file not found in the path {self.path}. Please provide a correct path")
            csv = pd.DataFrame()
            return csv

    def print_columns(self) -> list:
        """
        Help user to see the column name of the csv file
        :return: print a list of the column names
        """
        csv = pd.read_csv(self.path)
        print(csv.columns)
        return list(csv.columns)

    def normality_test(self) -> int:
        """
        Normality test (Shapiro) for the signal variable
        :return: 1 with normal message (95%) if normality, otherwise 0 with message
        """
        if len(self.csv_to_df()) == 0:
            return 0
        else:
            try:
                data = self.csv_to_df()
                result = stats.shapiro(data[self.signal])
                if result[1] <= 0.05:
                    print("distribution non normale")
                    return 0
                else:
                    print("la distribution est normale avec un degré de confiance de 95%")
                    return 1
            except TypeError:
                print(f"{self.signal} not in index, please choose a correct signal: see print_column() method")
                return 0

    def plot_graph(self) -> plt:
        """
        plot a series of graphs representing the data distribution
        :return: an histogram with a mean, and a scatter graph with the mean
        """
        data = self.csv_to_df()
        fig = plt.figure()
        ax = fig.subplot_mosaic("""A
        B""")
        ax['A'].hist(data[self.signal], alpha=0.5)
        ax['A'].axvline(np.mean(data[self.signal]), color='r', linestyle='dashed')
        ax['B'].scatter(data["layer"], data[self.signal], alpha=0.5)
        ax['B'].axhline(np.mean(data[self.signal]), color='r', linestyle='dashed')
        plt.show()

    def get_cpk(self, lsl: float = -1, usl: float = 1) -> tuple:
        """
        Computation of the designated signal Cp and Cpk
        lsl : float, lower specification limit of the variable (default = -1)
        usl : float, upper specification limit of the variable (default = 1)
        :return: Cp and Cpk for the given signal if there is a normal distribution, None otherwise
        """
        normality_check = self.normality_test()
        if normality_check == 0:
            print("Non normal signal distribution. Cpk computation not done")
            return None, None
        else:
            data = self.csv_to_df()
            mu = np.mean(data[self.signal])
            sigma = np.std(data[self.signal])
            cp = (usl - lsl) / (6 * sigma)
            cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))
            print(f"Cp={cp:.3f}, Cpk={cpk:.3f}")
            return cp, cpk
