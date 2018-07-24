# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 21:52:49 2018

@author: Satoru
"""

from datetime import datetime

class Log:
    _instance = None
    
    log_file = "text.txt"
    logging_mode = ""
    logging_style = ""
    
    # constracter
    def __init__(self):
        pass
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        ## initialize #########
        pass
        #######################
        return cls._instance





def _export_logFile(message):
    f = open(Log.log_file, 'a')
    f.writelines(str(datetime.now()) + " " + message + "\n")
    f.writelines(str(datetime.now()) + " " + message + "\n")
    f.close()
    pass


if __name__ == "__main__":
    _export_logFile("hogehoge")
    pass