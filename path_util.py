"""
Utility about path
"""

import sys


def get_package_top():
    """top level package path to which tha code belongs"""
    re = sys.path[1]
    # avoid changing path when debugging pyCharm
    if sys.path[0].find(re) == 0:
        re = sys.path[2]
    return re
