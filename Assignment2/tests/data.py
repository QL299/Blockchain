import unittest
from data.profitability import calculate_profit

class DataTest(unittest.TestCase):

    def check_approx_equality(self, n1, n2):
        """ Check that two values are within 1% of each other (to allow for minor differences in arithmetic). """
        self.assertTrue(abs(n1 - n2) / float(abs(n1 + n2 + .00001) / 2) < .01)

    def test_profitability(self):
        hashrate_per_miner = 14000000000000
        self.check_approx_equality(calculate_profit(float(1590896927258), hashrate_per_miner, 5, 10000, 33.0, 2.0), 17525)
        self.check_approx_equality(calculate_profit(float(1590896927258), hashrate_per_miner, 1, 9000, 12.5, 1.0), 597)
        self.check_approx_equality(calculate_profit(float(1590896927258), 3 * hashrate_per_miner, 5, 9000, 12.5, 1.5), 13442)
        self.check_approx_equality(calculate_profit(float(1590896927258), hashrate_per_miner, 1, 50000, 12.5, 1.0), 3319)
        self.check_approx_equality(calculate_profit(float(1590896927258), hashrate_per_miner, 1, 9000, 0.0, 1.0), 0)
        self.check_approx_equality(calculate_profit(float(1590896927258), hashrate_per_miner, 3, 9000, 10.0, 0.0), 0)
        self.check_approx_equality(calculate_profit(float(2590896927258), hashrate_per_miner, 20, 12000, 10.0, 0.0), 0)
        self.check_approx_equality(calculate_profit(float(0), 0, 0, 0, 0.0, 0.0), 0)

if __name__ == '__main__':
    unittest.main()


