# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 00:56:00 2018

@author: water
"""

import pandas as pd


def compress_columns(df: pd.DataFrame,
                     target_columns: list,
                     new_columns_name: str,
                     new_datas_name: str):
    """複数の列を「単一化(*)」する
    *:ここでは,同じ種別にまとめられるが別々にされている複数の列を一つにまとめることと.
    
    具体的には以下のような動作になる.
    ----------
    before df:
               name   age contory      3      4      5
        0     Jolno  15.0   Italy  False  False   True
        1    Koichi  17.0   Japan  False   True   True
        2  RisaRisa   NaN   Japan  False  False  False
        
    thisfunc(df, [3, 4, 5], "part", "is_appeared"):
               name   age contory  part  is_appeared
        0     Jolno  15.0   Italy     3        False
        1    Koichi  17.0   Japan     3        False
        2  RisaRisa   NaN   Japan     3        False
        3     Jolno  15.0   Italy     4        False
        4    Koichi  17.0   Japan     4         True
        5  RisaRisa   NaN   Japan     4        False
        6     Jolno  15.0   Italy     5         True
        7    Koichi  17.0   Japan     5         True
        8  RisaRisa   NaN   Japan     5        False
    
    index は新規作成される.
    単一化した列はdfの最後に追加される.単一化された元の列は削除される.
    
    Parameters
    ----------
    df :
        target DataFrame
    target_columns :
        commpressed columns as list
    new_columns_name :
        new column name that commpressed column name data
    new_datas_name :
        commpressed datas name
    
    Returns
    -------
    commpressed pandas.DataFrame
    """
    # initialize
    list_target_columns = list(target_columns)
    df_result = None  # return value
    
    # process
    for target_column in list_target_columns:
        list_drop = list_target_columns.copy()
        list_drop.remove(target_column)
        
        df_tmp = df.drop(list_drop, axis=1)
        df_tmp[new_columns_name] = target_column
        df_tmp = df_tmp.rename(columns={target_column: new_datas_name})
        
        if df_result is None:
            df_result = df_tmp
        else:
            df_result = pd.concat([df_result, df_tmp])
    
    # Orderliness
    columns_tmp = list(df_result.columns)
    columns_tmp.remove(new_columns_name)
    columns_tmp.remove(new_datas_name)
    columns_tmp.append(new_columns_name)
    columns_tmp.append(new_datas_name)
    df_result = df_result[columns_tmp]
    df_result = df_result.reset_index(drop=True)
    
    return df_result


def amplify_column(df: pd.DataFrame,
                   name_column: str,
                   value_column: str):
    """指定した列を「増幅(*)」する
    *:ここでは,1列で定義されている複数の属性とそれに付随する値を属性ごとの列に分割すること.
    
    具体的には以下のような動作になる.
    ----------
    before df:
               name   age contory  part  is_appeared
        0     Jolno  15.0   Italy     3          NaN
        1    Koichi  17.0   Japan     3        False
        2  RisaRisa   NaN   Japan     3        False
        3     Jolno  15.0   Italy     4        False
        4    Koichi  17.0   Japan     4         True
        5  RisaRisa   NaN   Japan     4        False
        6     Jolno  15.0   Italy     5         True
        7    Koichi  17.0   Japan     5         True
        8  RisaRisa   NaN   Japan     5        False
        
    thisfunc(df, "part", "is_appeared"):
               name   age contory      3      4      5
        0     Jolno  15.0   Italy    NaN  False   True
        1    Koichi  17.0   Japan  False   True   True
        2  RisaRisa   NaN   Japan  False  False  False
    
    index は新規作成される.
    増幅した列はdfの最後に追加される.増幅前の列は削除される.
    
    Parameters
    ----------
    df :
        target DataFrame
    name_column :
        attribute column name to be amplicied
    value_column :
        value column name to be amplicied
    
    Returns
    -------
    amplified pandas.DataFrame
    """
    # initialize
    df_result = None  # return value
    
    # process
    list_names = df[name_column]
    list_names = list(list_names[list_names.duplicated()==False])
    for name in list_names:
        df_tmp = df[df[name_column]==name]
        df_tmp = df_tmp.drop(name_column, axis=1)
        df_tmp = df_tmp.rename(columns={value_column: name})
        
        if df_result is None:
            df_result = df_tmp
        else:
            df_result = pd.merge(df_result, df_tmp, how="outer")
    
    # orderliness
    df_result = df_result.reset_index(drop=True)
    
    return df_result


def get_duplicated_frame(df: pd.DataFrame,
                         key_columns: list):
    """指定した列内の組み合わせ毎にDataFrameを分割して返すジェネレーター
    
    Parameters
    ----------
    df :
        target DataFrame
    key_columns :
        target column name list
    
    Returns
    -------
    amplified pandas.DataFrame
    
    Raise
    -----
    Exception :
        * If 'kye_columns' is not list-like
    """
    # initialize
    key_col = None
    key_cols = None
    if not isinstance(key_columns, list):
        raise Exception("key_columns only accepts ""list"" type")
    else:
        key_col = key_columns[0]
        if len(key_columns) > 0:
            key_cols = key_columns.copy()
            key_cols.remove(key_col)
    
    df_key_list = df[key_col]
    df_key_list = df_key_list[df_key_list.duplicated()==False]
    list_keys = list(df_key_list)
    for l in list_keys:
        df_tmp = df[df[key_col]==l]
        if not key_cols is None:
            yield df_tmp
        else:
            df_result = get_duplicated_frame(df_tmp, key_cols)
            yield df_result


if __name__ == "__main__":
    def main():
        df = pd.DataFrame([["Jolno", 15, "Italy", False, False, True],
                           ["Koichi", 17, "Japan", False, True, True],
                           ["RisaRisa", None, "Japan", False, False, False]],
                          columns=["name", "age", "contory", 3, 4, 5])
        print("before...")
        print(df)
        print()
        print()
        df = compress_columns(df, df.columns[3:6], "part", "is_appeared")
        print("after...")
        print(df)
        print()
        print()

        df = df.drop(5).reset_index(drop=True)
        df = amplify_column(df, "part", "is_appeared")
        print("and revers...")
        print(df)
        print()
        print()

        for i in get_duplicated_frame(df, ["contory"]):
            print(i)
    main()
    pass






