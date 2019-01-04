#!/usr/bin/python

""""""

import wx
import os
import sqlite3

class MainFrame(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.path = wx.TextCtrl(self)
        self.choice_path_btn = wx.Button(self, -1, '...', size=(30, 25))
        self.table = wx.ComboBox(self, style=wx.CB_READONLY)
        self.table_info = wx.ListCtrl(self, style=wx.LC_REPORT)
        si = wx.BoxSizer(wx.HORIZONTAL)
        si.Add(self.path, 1, wx.EXPAND)
        si.Add((20, 1))
        si.Add(self.choice_path_btn, 0, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 20))
        sizer.Add(si, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(self.table, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(self.table_info, 1, wx.EXPAND)
        sizer.Add((1, 20))
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add((20, 1))
        s.Add(sizer, 1, wx.EXPAND)
        s.Add((20, 1))
        self.SetSizer(s)
        self.path.Bind(wx.EVT_TEXT, self.onText)
        self.choice_path_btn.Bind(wx.EVT_BUTTON, self.onBtn)
        self.table.Bind(wx.EVT_COMBOBOX, self.onSelect)

    def onText(self, event=0):
        if os.path.exists(self.path.GetValue()):
            self.updateComboBox()

    def updateComboBox(self):
        self.table.Clear()
        self.table.Set(self.getTables())

    def getTables(self):
        with sqlite3.connect(self.path.GetValue()) as con:
            cur = con.cursor()
            cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
            data = [table[0] for table in cur.fetchall()]
        return data

    def onBtn(self, event=0):
        path =  wx.FileSelector('Select Database')
        if path:
            self.path.SetValue(path)

    def onSelect(self, event=0):
        self.table_info.ClearAll()
        table = self.table.GetStringSelection()
        with sqlite3.connect(self.path.GetValue()) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('SELECT * FROM %s' %(table,))
            data = cur.fetchall()
        for col in data[0].keys():
            self.table_info.AppendColumn(col)
        for row in data:
            row = dict(row)
            self.table_info.Append([i for _, i in row.items()])
        self.table_info.Layout()

def main():
    app = wx.App()
    fr = wx.Frame(None, size=(800, 600))
    MainFrame(fr)
    fr.Center()
    fr.Show()
    app.MainLoop()
    '''
    with sqlite3.connect('db.sqlite3') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
        for table in cur.fetchall():
            print('\nTABLE %s' %(table[0]))
            cur.execute('SELECT * FROM %s' %(table[0],))
            for row in cur.fetchall():
                print(dict(row))
                '''
    return True

if __name__ == '__main__':
    main()
