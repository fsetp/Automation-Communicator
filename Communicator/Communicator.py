################################################################################
#
# coding:utf-8
import serial
import tkinter as tk
import tkinter.scrolledtext
import time
from datetime import datetime

from time import sleep
from tkinter import ttk

########################################
#
ser = None
loopFlg = 0

########################################
#
ComChText	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
BaudText	= ['9600', '115200']
DacChText	= ['0', '1']

########################################
#
def dac_command_text(ch, value):
	return 'dac ' + str(ch) + ' ' + str(value)

#def stateForOpen():

########################################
#
def Open_clicked():
	global ser

	btnOpen['state'] = tk.DISABLED		# Open
	btnClose['state'] = tk.NORMAL		# Close
	btnInit['state'] = tk.NORMAL		# Init
	btnExit['state'] = tk.DISABLED		# Exit
	cbDacCh['state'] = tk.DISABLED		# 
	dacValue['state'] = tk.DISABLED		# 
	btnDac['state'] = tk.NORMAL			# Dac
	btnScale['state'] = tk.NORMAL		# 
	btnScaleZero['state'] = tk.NORMAL	# 
	btnAmeter['state'] = tk.NORMAL		# 
	btnLoop['state'] = tk.NORMAL		# Loop
	btnStop['state'] = tk.DISABLED		# Stop
	txtDacCh['state'] = tk.NORMAL		# 
	txtMvStep['state'] = tk.NORMAL		# 
	txtMvFrom['state'] = tk.NORMAL		# 
	txtMvTo['state'] = tk.NORMAL		# 
	txtRecive.delete('1.0',tk.END)		# 

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())
		print('connecting ...', com, baud)
		ser = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')

	except:
		print('connecting error.')
		txtRecive.insert(tk.END,'Device Error')
		btnOpen['state'] = tk.NORMAL		# Open
		btnClose['state'] = tk.DISABLED		# Close
		btnInit['state'] = tk.DISABLED		# Init
		btnExit['state'] = tk.NORMAL		# Exit
		cbDacCh['state'] = tk.DISABLED		# 
		dacValue['state'] = tk.DISABLED		# 
		btnDac['state'] = tk.DISABLED		# Dac
		btnScale['state'] = tk.DISABLED		# 
		btnScaleZero['state'] = tk.DISABLED	# 
		btnAmeter['state'] = tk.DISABLED	# 
		btnLoop['state'] = tk.DISABLED		# Loop
		btnStop['state'] = tk.DISABLED		# Stop
		txtDacCh['state'] = tk.DISABLED		# 
		txtMvStep['state'] = tk.DISABLED	# 
		txtMvFrom['state'] = tk.DISABLED	# 
		txtMvTo['state'] = tk.DISABLED		# 

########################################
#
def Close_clicked():
	global ser
	btnOpen['state'] = tk.NORMAL		# Open
	btnClose['state'] = tk.DISABLED		# Close
	btnInit['state'] = tk.NORMAL		# Init
	btnExit['state'] = tk.NORMAL		# Exit
	cbDacCh['state'] = tk.NORMAL		# 
	dacValue['state'] = tk.NORMAL		# 
	btnDac['state'] = tk.DISABLED		# Dac
	btnScale['state'] = tk.DISABLED		# 
	btnScaleZero['state'] = tk.DISABLED	# 
	btnAmeter['state'] = tk.DISABLED	# 
	btnLoop['state'] = tk.DISABLED		# Loop
	btnStop['state'] = tk.DISABLED		# Stop
	txtDacCh['state'] = tk.DISABLED		# 
	txtMvStep['state'] = tk.DISABLED	# 
	txtMvFrom['state'] = tk.DISABLED	# 
	txtMvTo['state'] = tk.DISABLED		# 
	ser.close()



#	pre-process
#	wait second
#	post-process
#
#
#

IntervalMs = 100
WaitSecNum = 5
WaitItvMs = 50
DacValue = 0

########################################
#
def PreProcess():
	global IntervalMs
	global WaitSecNum
	global WaitItvMs
	global DacValue

	print('Pre Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	# set current
	#
	DacCh = txtDacCh.get()
	DacValue = txtMvFrom.get()
	dac_text = dac_command_text(DacCh, DacValue) + '\r\n'
	ser.write(dac_text.encode('shift-jis'))
	print(dac_text)

	# make wait count
	WaitItvMs = WaitSecNum * 1000 / IntervalMs

	return True

########################################
#
def WaitSecond():
	global WaitItvMs

#	print('Wait Second')
	WaitItvMs -= 1
	if (WaitItvMs > 0):
		return False

	return True

########################################
#
def PostProcess():

	print('Post Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	ser.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	ser.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	return True

########################################
#
ItvFuncList = [PreProcess, WaitSecond, PostProcess]
idxFunc = 0

########################################
#
def interval_work():
	global loopFlg
	global idxFunc
	global ser

	func = ItvFuncList[idxFunc]
	if (func()):
		idxFunc += 1
		if (idxFunc >= len(ItvFuncList)):
			idxFunc = 0

#	txtRecive.see('end')
	if (loopFlg == 1):
		root.after(IntervalMs, interval_work)

########################################
#
def Init_clicked():
	ser.write('init\r\n'.encode('shift-jis'))
	print('init')
	sleep(0.1)
	txtRcv = ser.read(256)
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def Exit_clicked():

	root.destroy()

########################################
#
def DAC_clicked():
	global ser
	global cbDacCh
	global dacValue

	ch		= cbDacCh.get()
	value	= dacValue.get()

	text = dac_command_text(ch, value) + '\r\n'

	ser.write(text.encode('shift-jis'))
	print('dac ' + ch + ' ' + value)
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def SCALE_clicked():
	global ser
	ser.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def ZERO_clicked():
	global ser
	ser.write("scale zero\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def AMETER_clicked():
	global ser
	ser.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	text = str(txtRcv)
	text = text.replace('\r\n', '')
#	text = text.replace('\n', '')
#	value = float(text)
	print(text)


########################################
#
def Loop_clicked():
	global loopFlg
	loopFlg = 1 
	btnExit['state'] = tk.DISABLED
	btnStop['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

	interval_work()

########################################
#
def Stop_clicked():
	global loopFlg
	loopFlg = 0
	btnExit['state'] = tk.NORMAL
	btnStop['state'] = tk.DISABLED

########################################
#
root = tk.Tk()
#root.geometry('430x320')
root.geometry('440x370')
root.title('Communicator Tool for Atom Shell')

row_idx = 0
col_idx = 0

########################################
#
labelCom = tk.Label(root, text = ' COM :')
labelCom.grid(row = row_idx, column = 0, sticky = tk.E)

cbDevCom = ttk.Combobox(root, width = 4, values = ComChText)
cbDevCom.current(4)
cbDevCom.grid(row = row_idx, column = 1)

########################################
#
labelBaud = tk.Label(root, text = ' Baud :')
labelBaud.grid(row = row_idx, column = 2, sticky = tk.E)

cbDevBaud = ttk.Combobox(root, width = 10, values = BaudText)
cbDevBaud.current(1)
cbDevBaud.grid(row = row_idx, column = 3)

row_idx += 1
########################################
# Open
btnOpen = tk.Button(master = root, text = 'Open', command = Open_clicked, width = 10)
btnOpen.grid(row = row_idx, column = 0, padx = 10, pady = 3 )

########################################
# Close
btnClose = tk.Button(master = root, text = 'Close', command = Close_clicked, state = tk.DISABLED, width = 10)
btnClose.grid(row = row_idx, column = 1, pady = 3)

########################################
# Init
btnInit = tk.Button(master = root, text = 'Init', command = Init_clicked, state = tk.DISABLED, width = 10)
btnInit.grid(row = row_idx, column = 2, pady = 3)

########################################
# Exit
btnExit = tk.Button(master=root, text='Exit' , command = Exit_clicked, width = 10)
btnExit.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1

########################################
# Dac
label_ch = tk.Label(root, text = 'Ch : ')
label_ch.grid(row = row_idx, column = 0, sticky = tk.E, pady = 10)

cbDacCh = ttk.Combobox(root, width = 1, value = DacChText, state = tk.DISABLED)
cbDacCh.set(DacChText[0])
cbDacCh.grid(row = row_idx, column = 1, sticky = tk.W)

label_dac = tk.Label(root, text = 'DAC(mV) : ')
label_dac.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

dacValue = ttk.Entry(root, width = 6, state = tk.DISABLED)
dacValue.delete(0, tk.END)
dacValue.insert(tk.END, '3000')
dacValue.grid(row = row_idx, column = 3, sticky = tk.W)

btnDac = tk.Button(master = root, text = 'DAC', command = DAC_clicked, state = tk.DISABLED, width = 10)
btnDac.grid(row = row_idx, column = 4, pady = 3)


row_idx += 1
########################################
#
btnScale = tk.Button(master = root, text = 'SCALE', command = SCALE_clicked, state = tk.DISABLED, width = 10)
btnScale.grid(row = row_idx, column = 0, pady = 3)

########################################
#
btnScaleZero = tk.Button(master = root, text = 'ZERO', command = ZERO_clicked, state = tk.DISABLED, width = 10)
btnScaleZero.grid(row = row_idx, column = 1, pady = 3)

row_idx += 1

########################################
#
btnAmeter = tk.Button(master = root, text = 'AMETER', command = AMETER_clicked, state = tk.DISABLED, width = 10)
btnAmeter.grid(row = row_idx, column = 1)

row_idx += 1
########################################
#
labelCh = tk.Label(root, text = 'DAC Ch:')
labelCh.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtDacCh = ttk.Entry(root, width = 4, state = tk.DISABLED)
txtDacCh.delete(0, tk.END)
txtDacCh.insert(tk.END, '0')
txtDacCh.grid(row = row_idx, column = 1, sticky = tk.W)

labelMvStep = tk.Label(root, text = 'mV Step :')
labelMvStep.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvStep = ttk.Entry(root, width = 10, state = tk.DISABLED)
txtMvStep.delete(0, tk.END)
txtMvStep.insert(tk.END, '2')
txtMvStep.grid(row = row_idx, column = 3, sticky = tk.W)

########################################
# Loop
btnLoop = tk.Button(master = root, text = 'LOOP', command = Loop_clicked, state = tk.DISABLED, width = 10)
btnLoop.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1 

labelMvFrom = tk.Label(root, text = 'mV from :')
labelMvFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtMvFrom = ttk.Entry(root, width = 10, state = tk.DISABLED)
txtMvFrom.delete(0, tk.END)
txtMvFrom.insert(tk.END, '0')
txtMvFrom.grid(row = row_idx, column = 1, sticky = tk.W)

labelMvTo = tk.Label(root, text = 'mV to :')
labelMvTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvTo = ttk.Entry(root, width = 10, state = tk.DISABLED)
txtMvTo.delete(0, tk.END)
txtMvTo.insert(tk.END, '1000')
txtMvTo.grid(row = row_idx, column = 3, sticky = tk.W)

########################################
# Stop
btnStop = tk.Button(master = root, text = 'STOP', command = Stop_clicked, state = tk.DISABLED, width = 10)
btnStop.grid(row = row_idx, column = 4)

row_idx += 1
########################################
#
#txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 52, height = 13)
txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 56, height = 10)
txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10,pady = 10)

root.mainloop()

