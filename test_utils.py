import unittest
import pandas as pd
import numpy as np
import os
from utils import StatisticProcessControl


class TestCSVToDF(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file for testing
        self.test_csv_path = 'test_data.csv'
        data = {'layer': [1, 2, 3, 4, 5],
                'mean_ir_pwr': [0.5, 0.6, 0.7, 0.8, 0.9]}
        df = pd.DataFrame(data)
        df.to_csv(self.test_csv_path, index=False)

        # Initialize StatisticProcessControl with test data
        self.spc = StatisticProcessControl(self.test_csv_path, signal="mean_ir_pwr")

    def tearDown(self):
        # Clean up the test CSV file
        os.remove(self.test_csv_path)

    def test_csv_to_df_valid_csv(self):
        df = self.spc.csv_to_df()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)

    def test_csv_to_df_invalid_csv(self):
        # Create an invalid non-CSV file for testing
        invalid_csv_path = 'invalid_data.txt'
        with open(invalid_csv_path, 'w') as f:
            f.write("This is not a CSV file.")

        invalid_spc = StatisticProcessControl(invalid_csv_path)
        df = invalid_spc.csv_to_df()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 0)

        # Clean up the invalid file
        os.remove(invalid_csv_path)

    def test_csv_to_df_file_not_found(self):
        invalid_spc = StatisticProcessControl('nonexistent_file.csv')
        df = invalid_spc.csv_to_df()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 0)


class TestNormalityTest(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file with normally distributed data for testing
        self.normal_csv_path = 'normal_data.csv'
        np.random.seed(0)
        normal_data = np.random.normal(loc=0, scale=1, size=100)
        df_normal = pd.DataFrame({'layer': range(1, 101), 'signal': normal_data})
        df_normal.to_csv(self.normal_csv_path, index=False)

        # Create a sample CSV file with non-normally distributed data for testing
        self.non_normal_csv_path = 'non_normal_data.csv'
        non_normal_data = np.random.randint(0, 10, size=100)
        df_non_normal = pd.DataFrame({'layer': range(1, 101), 'signal': non_normal_data})
        df_non_normal.to_csv(self.non_normal_csv_path, index=False)

    def tearDown(self):
        # Clean up the test CSV files
        import os
        os.remove(self.normal_csv_path)
        os.remove(self.non_normal_csv_path)

    def test_normality_test_normal_distribution(self):
        spc_normal = StatisticProcessControl(self.normal_csv_path, signal="signal")
        result = spc_normal.normality_test()
        self.assertEqual(result, 1)

    def test_normality_test_non_normal_distribution(self):
        spc_non_normal = StatisticProcessControl(self.non_normal_csv_path, signal="signal")
        result = spc_non_normal.normality_test()
        self.assertEqual(result, 0)


class TestCalculCpk(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file with normally distributed data for testing
        self.normal_csv_path = 'normal_data.csv'
        np.random.seed(0)
        normal_data = np.random.normal(loc=0, scale=1, size=100)
        df_normal = pd.DataFrame({'layer': range(1, 101), 'signal': normal_data})
        df_normal.to_csv(self.normal_csv_path, index=False)

        # Create a sample CSV file with non-normally distributed data for testing
        self.non_normal_csv_path = 'non_normal_data.csv'
        non_normal_data = np.random.randint(0, 10, size=100)
        df_non_normal = pd.DataFrame({'layer': range(1, 101), 'signal': non_normal_data})
        df_non_normal.to_csv(self.non_normal_csv_path, index=False)

    def tearDown(self):
        # Clean up the test CSV files
        import os
        os.remove(self.normal_csv_path)
        os.remove(self.non_normal_csv_path)

    def test_calcul_cpk_normal_distribution(self):
        spc_normal = StatisticProcessControl(self.normal_csv_path, signal="signal")
        cp, cpk = spc_normal.calcul_cpk()
        self.assertIsNotNone(cp)
        self.assertIsNotNone(cpk)

    def test_calcul_cpk_non_normal_distribution(self):
        spc_non_normal = StatisticProcessControl(self.non_normal_csv_path, signal="signal")
        cp, cpk = spc_non_normal.calcul_cpk()

        # Assert that cp and cpk are None when distribution is non-normal
        self.assertIsNone(cp)
        self.assertIsNone(cpk)


if __name__ == '__main__':
    unittest.main()
