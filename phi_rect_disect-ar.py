import wx, itertools, math

phi = (math.sqrt(5) - 1) / 2

class paintPanel(wx.Panel):
	def disectRect(self, weight, l, t, r, b, weightacc=None):
		w, h = r - l, b - t
		if len(weight) == 1:
			return [(l, t, w, h)], abs(w / h - 1.0)
		else:
			weightAcc = list(itertools.accumulate(weight)) if weightacc is None else weightacc
			wtSum = weightAcc[-1]
			tarSplit = min(w, h) / max(w, h) * phi * wtSum
			idxSplit = min(min(enumerate(weightAcc), key=lambda x: abs(x[1] - tarSplit))[0] + 1,  len(weight) - 1)
			wtSplit = weightAcc[idxSplit - 1]
			s, v = [[0, 0], [0, 0]], [[0, 0], [0, 0]]
			for i in range(2):
				if i == 0:
					pos = l + w * wtSplit // wtSum
					rectl, rectr = (l, t, pos, b), (pos, t, r, b)
				else:
					pos = t + h * wtSplit // wtSum
					rectl, rectr = (l, t, r, pos), (l, pos, r, b)
				s[i][0], v[i][0] = self.disectRect(weight[:idxSplit], *rectl, weightAcc[:idxSplit])
				s[i][1], v[i][1] = self.disectRect(weight[idxSplit:], *rectr, [x - wtSplit for x in weightAcc[idxSplit:]])
			sv = [sum(x) for x in v]
			return itertools.chain(*s[0 if sv[0] < sv[1] else 1]), min(sv)
	
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
		s, v = self.disectRect(self.weights, 10, 10, w - 20, h - 20)
		for x in s:
			print('Draw: l={}, t={}, w={}, h={}'.format(*x))
			dc.DrawRectangle(*x)

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
