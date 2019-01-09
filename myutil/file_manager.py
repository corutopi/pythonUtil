# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:29:41 2018

@author: water
"""

import os

import pandas as pd


class CSV:
    """
    docstr_test
    """
    
    @classmethod
    def get_file(cls, path) -> pd.DataFrame:
        if os.path.isfile(path):
            return pd.read_csv(path, encoding="shift_jis", engine="python")
#            return pd.read_csv(path, encoding="cp932", engine="python")
        else:
            return None
    
    @classmethod
    def export_file(cls, path, df: pd.DataFrame):
        df.to_csv(path, index=None, encoding="shift_jis")


if __name__ == "__main__":
    pd.set_option("display.width", 80)
    pd.set_option("display.max_colwidth", 50)
    pd.set_option("display.max_rows", 20)
    pd.set_option("display.unicode.east_asian_width", True)
    
    df = CSV.get_file("my_test_mini.csv")
    print(df)
    df = CSV.get_file("my_test_mini_lack.csv")
    print(df)
    df = df.fillna("aaa")
    print(df)
    CSV.export_file("export.csv", df)
    pass