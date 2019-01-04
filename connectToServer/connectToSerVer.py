#!/usr/bin/python

""""""

import wx
import socket
import os

class MainFrame(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.server_name = wx.TextCtrl(self)
        self.domain = wx.TextCtrl(self, -1, 'reactorcenter.dnri.vn')
        self.connect_btn = wx.Button(self, -1, 'Connect')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 20))
        sizer.Add(wx.StaticText(self, -1, 'Server Name'))
        sizer.Add(self.server_name, 0, wx.EXPAND)
        sizer.Add((1, 20))
        sizer.Add(wx.StaticText(self, -1, 'Domain'))
        sizer.Add(self.domain, 0, wx.EXPAND)
        sizer.Add((1, 1), 1)
        sizer.Add(self.connect_btn, 0, wx.CENTER)
        sizer.Add((1, 20))
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add((20, 1))
        s.Add(sizer, 1, wx.EXPAND)
        s.Add((20, 1))
        self.SetSizer(s)
        self.server_name.SetFocus()
        self.connect_btn.Enable(False)
        self.server_name.Bind(wx.EVT_TEXT, self.onText)
        self.connect_btn.Bind(wx.EVT_BUTTON, self.onBtn)

    def onText(self, event=0):
        if self.server_name.GetValue():
            self.connect_btn.Enable()
        else:
            self.connect_btn.Enable(False)

    def onBtn(self, event=0):
        try:
            server = ['\n', socket.gethostbyname(self.server_name.GetValue()), ' ', self.domain.GetValue(), '\n']
            file_path = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
            print(file_path, os.path.exists(file_path))
            wx.MessageBox('Server IP: %s' %(server[1]), 'Info')
            with open(file_path, 'a+') as f:
                f.seek(0)
                for line in f.read().split('\n'):
                    print(line)
                    if server[1] in line and server[3] in line:
                        break
                else:
                    f.write(''.join(server))
            wx.MessageBox('Connected!', 'Successfully')
        except:
            wx.MessageBox('Can not connect to server', 'Error', style=wx.ICON_ERROR)
        self.server_name.SetValue('')

def main():
    app = wx.App()
    fr = wx.Frame(None, title='Connect To Server')
    MainFrame(fr)
    fr.Show()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
