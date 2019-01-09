import wx.grid
import pandas as pd


class PandasGridTable(wx.grid.GridTableBase):
    def __init__(self, df=None):
        super().__init__()
        self.df: pd.DataFrame = None
        if df is not None:
            self.df = df

    def set_data(self, df: pd.DataFrame):
        self.df = df

    def GetColLabelValue(self, col):
        return self.df.columns[col]

    def GetRowLabelValue(self, row):
        return str(self.df.index[row])

    def GetNumberCols(self):
        return len(self.df.columns)

    def GetNumberRows(self):
        return len(self.df)

    def IsEmptyCell(self, row, col):
        try:
            return not self.df.iat[row, col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.df.iat[row, col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        try:
            self.df.iat[row, col] = value
        except IndexError:
            pass


if __name__ == '__main__':
    def main():
        from myutil.file_manager import CSV
        import os
        import sys
        # read csv
        root_dir = sys.path[1]
        df = CSV.get_file(os.path.join(root_dir, 'SampleCSV', 'my_test.csv'))
        print(df)
        # create wx.window
        import wx
        app = wx.App()
        f = wx.Frame(None)
        g = wx.grid.Grid(f)
        t = PandasGridTable(df)
        g.SetTable(t)
        g.AutoSize()
        f.Show()
        app.MainLoop()
        pass
    main()
