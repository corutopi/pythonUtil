import wx.grid
import pandas as pd


class PandasGrid(wx.grid.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_data_frame(self, df: pd.DataFrame):
        """Reflect the contents of the Pandas DataFrame on Grid.
        :param df:
        :return:
        """
        '''Delete all row and col'''
        self.DeleteCols(0, self.GetNumberCols())
        self.DeleteRows(0, self.GetNumberRows())
        '''Make row and col to fit DataFrame'''
        self.AppendCols(len(df.columns))
        self.AppendRows(len(df))
        '''Reflect data on cells'''
        for r in range(len(df.columns)):
            for c in range(len(df)):
                self.SetCellValue(r, c, str(df.iat[r, c]))

    def get_data_frame(self):
        """Return DataFrame that have cells data.
        :return:
        """


if __name__ == '__main__':
    def main():
        import wx
        from myutil.file_manager import CSV
        df = CSV.get_file()
        app = wx.App()
        f = wx.Frame(None)
        g = PandasGrid(f)
        g.CreateGrid(10, 10)
        f.Show()
        app.MainLoop()


    main()
    pass
