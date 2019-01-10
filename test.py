# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:21:48 2018

@author: Satoru
"""

from myutil.file_manager import CSV

if __name__ == "__main__":
    s = "カレンダー.csv"
    
    print(CSV.get_file(s))
    
    pass