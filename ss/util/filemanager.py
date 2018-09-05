# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:29:28 2018

@author: Satoru
"""

import pandas as pd
import configparser as cp

class CSV:
    
    def get_csv(path):
        # engineの指定がないと日本語ファイルが読み込めない
        return pd.read_csv(path, encoding="cp932", engine="python")
    
    def export_csv(path, data_frame):
        pass

class INI:
    def get_ini(path):
        return cp.SafeConfigParser().read(path)
        pass