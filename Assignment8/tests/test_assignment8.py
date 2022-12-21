import unittest
import pandas as pd
import assignment8
from gradescope_utils.autograder_utils.decorators import (number, visibility,
                                                          weight)


class Testassignment8(unittest.TestCase):

    def setUp(self):
        self.assignment8 = assignment8

    @weight(10)
    @visibility('visible')
    @number("ex1")
    def test_ex1(self):
        self.assignment8.ex1()
        result_from_file = pd.read_csv('ex1.tsv')
        expected_from_file = pd.read_csv('ex1_solution.tsv')
        assert result_from_file.equals(expected_from_file) == True

    @weight(10)
    @visibility('visible')
    @number("ex2")
    def test_ex2(self):
        self.assignment8.ex2()
        result_from_file = pd.read_csv('ex2.tsv')
        expected_from_file = pd.read_csv('ex2_solution.tsv')
        assert result_from_file.equals(expected_from_file) == True

    @weight(10)
    @visibility('visible')
    @number("ex3")
    def test_ex3(self):
        self.assignment8.ex3()
        result_from_file = pd.read_csv('ex3.tsv')
        expected_from_file = pd.read_csv('ex3_solution.tsv')
        assert result_from_file.equals(expected_from_file) == True

    @weight(10)
    @visibility('visible')
    @number("ex4")
    def test_ex4(self):
        self.assignment8.ex4()
        result_from_file = pd.read_csv('ex4.tsv')
        expected_from_file = pd.read_csv('ex4_solution.tsv')
        assert result_from_file.equals(expected_from_file) == True
