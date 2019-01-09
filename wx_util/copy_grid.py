"""my util wx grid
@todo enable 'return' operation
@todo enable 'all select' operation
@
"""

import wx
import wx.grid

KEY_CODE_C = ord('C')
KEY_CODE_D = ord('D')
KEY_CODE_V = ord('V')
KEY_CODE_Z = ord('Z')
KEY_CODE_BS = 8
KEY_CODE_DL = 46
KEY_CODE_DL_EX = 127


class CPGrid(wx.grid.Grid):

    def __init__(self, parent):
        super().__init__(parent)
        '''
        if use EVT_KEY_DOWN event, default key operation (like cursor key: move
        select cell, shift + space key: select) would be disabled.
        '''
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
        pass

    def on_key(self, event: wx.KeyEvent):
        """key push events controller
        can use following shortcut keys
            Ctrl + C    : copy selected cell
            Ctrl + V    : paste text data
            Delete      : delete all selected cells data
        ... and more. coming soon?
        :param event:
        :return:
        """
        # print(event.GetKeyCode())
        if event.ControlDown() and event.GetKeyCode() == KEY_CODE_C:
            self.copy()
            print('Do Copy!')
        if event.ControlDown() and event.GetKeyCode() == KEY_CODE_V:
            print('Do Paste!')
            self.paste()
        if event.ControlDown() and event.GetKeyCode() == KEY_CODE_Z:
            print('Undo!')
        if event.GetKeyCode() == KEY_CODE_BS and \
                event.GetKeyCode() == KEY_CODE_D:
            print('Cell Delete!')
        if event.GetKeyCode() == wx.WXK_DELETE:
            self.delete()
            print('Range Delete!')
            return  # not cell activate if delete key pushed
        # do other default events
        event.DoAllowNextEvent()

    def copy(self):
        """copy selected range to text.
        like this.
        [cell]\t[cell]\t[cell]\t......\r\n
        [cell]\t[cell]\t[cell]\t......\r\n
        ......
        [cell]\t[cell]\t[cell]\t......\r\n
        @todo raise error if multiple range cell selected
        :return: None
        """
        # get copy target range
        row_start, col_start, rows, cols = self._select_range()
        # transform cell data to test
        copy_text = ''
        for r in range(rows):
            for c in range(cols):
                copy_text += str(self.GetCellValue(row_start + r,
                                                   col_start + c))
                if c < cols:
                    copy_text += '\t'
            copy_text += '\r\n'
        print(copy_text)
        # set clipboard
        clipboard = wx.TextDataObject()
        clipboard.SetText(copy_text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            # @todo call error
            pass

    def paste(self):
        """paste text data to selected range.
        text data format like this.
        [cell]\t[cell]\t[cell]\t......\r\n
        [cell]\t[cell]\t[cell]\t......\r\n
        ......
        [cell]\t[cell]\t[cell]\t......\r\n
        @todo repeat paste when selected rows/cols is multiple of data rows/cols
        @todo raise error or based on first cell if multiple range cell selected
        :return: None
        """
        # get copy target range
        row_start, col_start, rows, cols = self._select_range()
        # make paste data
        clipboard = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(clipboard)
            wx.TheClipboard.Close()
        else:
            # @todo call error
            pass
        paste_texts = []
        tmp_line = clipboard.GetText().splitlines()
        for r in range(len(tmp_line)):
            paste_texts.append(tmp_line[r].split('\t'))
        # check can paste data to range
        # paste
        for r in range(rows if rows < len(paste_texts) else len(paste_texts)):
            for c in range(cols if cols < len(paste_texts[r])
                           else len(paste_texts[r])):
                self.SetCellValue(row_start + r, col_start + c,
                                  paste_texts[r][c])

    def delete(self):
        """delete all selected cells data.
        :return:
        """
        # @todo implement
        row_start, col_start, rows, cols = self._select_range()
        for r in range(rows):
            for c in range(cols):
                self.SetCellValue(row_start + r, col_start + c,
                                  "")
        pass

    def _push_delete(self, key_code):
        """Determine whether the pressed key is a delete key.
        Since the code of the delete key may be different depending on the
        keyboard, let's separate it into another method.
        -> can solve to use wx.WXK_DELETE

        :param key_code: get '.GetKeyCode()'
        :return: is 'delete key' then True
        """

    def _select_range(self):
        if len(self.GetSelectionBlockTopLeft()) == 0:
            row_start = self.GetGridCursorRow()
            col_start = self.GetGridCursorCol()
            row_end = row_start
            col_end = col_start
        else:
            row_start = self.GetSelectionBlockTopLeft()[0][0]
            col_start = self.GetSelectionBlockTopLeft()[0][1]
            row_end = self.GetSelectionBlockBottomRight()[0][0]
            col_end = self.GetSelectionBlockBottomRight()[0][1]
        rows = row_end - row_start + 1
        cols = col_end - col_start + 1
        return row_start, col_start, rows, cols
        pass


if __name__ == '__main__':
    import wx

    print('Hello World')
    app = wx.App()
    f = wx.Frame(None)
    f.SetSize(1000, 500)
    p = wx.Panel(f)
    s = wx.BoxSizer(wx.HORIZONTAL)
    g = CPGrid(p)
    g.CreateGrid(10, 10)
    s.Add(g)
    p.SetSizer(s)
    f.Show()
    app.MainLoop()
    pass
