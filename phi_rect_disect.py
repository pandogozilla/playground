import wx, itertools, math

phi = (math.sqrt(5) - 1) / 2

class paintPanel(wx.Panel):
	def disectRect(self, dc, weight, l, t, r, b, weightsum=None):
		w, h = r - l, b - t
		if len(weight) == 1:
			print('Draw: l={}, t={}, w={}, h={}'.format(l, t, w, h))
			dc.DrawRectangle(l, t, w, h)
		else:
			lweightsum = list(itertools.accumulate(weight)) if weightsum is None else weightsum
			# normalize
			lweight = [x / lweightsum[-1] for x in weight]
			lweightsum = [x / lweightsum[-1] for x in lweightsum]
			idxSplit = min(min(enumerate(lweightsum), key=lambda x: abs(x[1] - phi))[0] + 1,  len(lweight))
			wtSplit = lweightsum[idxSplit - 1]
			weightsum_rhs = [x - wtSplit for x in lweightsum[idxSplit:]]
			if w >= h:
				pos = l + int(w * wtSplit)
				rectl, rectr = (l, t, pos, b), (pos, t, r, b)
			else:
				pos = t + int(h * wtSplit)
				rectl, rectr = (l, t, r, pos), (l, pos, r, b)
			self.disectRect(dc, lweight[:idxSplit], *rectl, lweightsum[:idxSplit])
			self.disectRect(dc, lweight[idxSplit:], *rectr, weightsum_rhs)
	
	def __init__(self, parent):
		super(paintPanel, self).__init__(parent)
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.SetBackgroundColour(wx.WHITE)
		for x in ['PAINT', 'SIZE']:
			exec('self.Bind(wx.EVT_{}, self.on{})'.format(*([x] * 2)))
		self.weights = [2,4,6,8,10]
		self.weights.sort(reverse=True)
	
	def onSIZE(self, event):
		event.Skip()
		self.Refresh()
	
	def onPAINT(self, event):
		w, h = self.GetClientSize()
		dc = wx.AutoBufferedPaintDC(self)
		dc.Clear()
		print('')
		self.disectRect(dc, self.weights, 10, 10, w - 20, h - 20)

class inputPanel(wx.Panel):
	def __init__(self, parent):
		super(inputPanel, self).__init__(parent)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.txtInput = wx.TextCtrl(self)
		self.txtInput.SetValue('2,4,6,8,10')
		self.btnUpdate = wx.Button(self, label='Update')
		self.btnUpdate.SetDefault()
		self.btnUpdate.Bind(wx.EVT_BUTTON, self.onUpdate)
		self.sizer.Add(self.txtInput, 1, wx.ALIGN_CENTER | wx.EXPAND)
		self.sizer.Add(self.btnUpdate, 0, wx.ALIGN_CENTER)
		self.SetSizer(self.sizer)
		self.Fit()
	
	def onUpdate(self, event):
		try:
			self.rootFrame.paintPanel.weights = list(map(int, self.txtInput.GetValue().split(',')))
			self.rootFrame.paintPanel.weights.sort(reverse=True)
			self.rootFrame.paintPanel.Refresh()
		except:
			print('?')

class mainFrame(wx.Frame):
	def __init__(self):
		super(mainFrame, self).__init__(None)
		self.SetTitle('phi disect')
		self.SetClientSize((500, 600))
		self.splitter = wx.SplitterWindow(self, style=wx.SP_BORDER)
		for x in ['paintPanel', 'inputPanel']:
			exec('self.{} = {}(self.splitter); self.{}.rootFrame = self'.format(*([x] * 3)))
		self.splitter.SplitHorizontally(self.paintPanel, self.inputPanel, -30)
		self.splitter.SetSashGravity(1)

def main():
	app = wx.App(False)
	frame = mainFrame()
	frame.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
