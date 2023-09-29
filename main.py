import wx
import wx.xrc
import compiler
import io


class Window ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
						  size=wx.Size(486, 327), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		bSizer1 = wx.BoxSizer(wx.VERTICAL)

		bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

		self.edit = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, -1), wx.TE_MULTILINE)
		bSizer2.Add(self.edit, 1, wx.ALL | wx.EXPAND, 5)

		self.lexer_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
									  wx.TE_MULTILINE | wx.TE_READONLY)
		bSizer2.Add(self.lexer_text, 1, wx.ALL | wx.EXPAND, 5)

		bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

		self.button = wx.ToggleButton(self, wx.ID_ANY, u"Convert", wx.DefaultPosition, wx.DefaultSize, 0)
		self.button.SetValue(True)
		bSizer1.Add(self.button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

		self.SetSizer(bSizer1)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.button.Bind(wx.EVT_TOGGLEBUTTON, self.click)
		self.Show(True)

	def __del__( self ):
		pass

	def click(self, parent):
		compiler.input_stream = io.StringIO(self.edit.GetValue())
		lex = compiler.Lexer()
		res = ""
		while lex.symbol != compiler.Lexer.EOF:
			lex.next_token()
			if lex.symbol == compiler.Lexer.ID or lex.symbol == compiler.Lexer.NUM or lex.symbol == compiler.Lexer.REAL:
				res += "(" + compiler.decrypt[lex.symbol] + "," + str(lex.value) + ")\n"
			else:
				res += "(" + compiler.decrypt[lex.symbol] + ")\n"
		self.lexer_text.SetValue(res)


if __name__ == "__main__":
	app = wx.App()
	wnd = Window(None)
	app.MainLoop()
