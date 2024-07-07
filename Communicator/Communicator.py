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
g_loopFlg = 0

########################################
#
ComChText	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
BaudText	= ['9600', '115200']
DacChText	= ['0', '1']

########################################
#
def dac_command_text(ch, value):
	return 'dac ' + str(ch) + ' ' + str(value)

########################################
#
def Open_clicked():
	global ser

	btnOpen['state'] = tk.DISABLED			# Open
	btnClose['state'] = tk.NORMAL			# Close
	btnInit['state'] = tk.NORMAL			# Init
	btnExit['state'] = tk.DISABLED			# Exit
	cbDacCh['state'] = tk.NORMAL			# 
	dacValue['state'] = tk.NORMAL			# 
	dacValue.delete(0, tk.END)				
	dacValue.insert(tk.END, '3000')			
	btnDac['state'] = tk.NORMAL				# Dac
	btnScale['state'] = tk.NORMAL			# 
	btnScaleZero['state'] = tk.NORMAL		# 
	btnAmeter['state'] = tk.NORMAL			# 
	btnSequence['state'] = tk.NORMAL		# Loop
	btnStop['state'] = tk.DISABLED			# Stop
	cbDacCh2['state'] = tk.NORMAL			# 
	txtMvStep['state'] = tk.NORMAL			# 
	txtMvStep.delete(0, tk.END)				
	txtMvStep.insert(tk.END, '2')			
	txtWaitMs['state'] = tk.NORMAL			
	txtWaitMs.delete(0, tk.END)				
	txtWaitMs.insert(tk.END, '5000')		
	txtMvFrom['state'] = tk.NORMAL			# 
	txtMvFrom.delete(0, tk.END)				
	txtMvFrom.insert(tk.END, '0')			
	txtMvTo['state'] = tk.NORMAL			# 
	txtMvTo.delete(0, tk.END)				
	txtMvTo.insert(tk.END, '1000')			
	cbDacCh3['state'] = tk.NORMAL			# 
	txtMvCenter['state'] = tk.NORMAL		# 
	txtMvCenter.delete(0, tk.END)			
	txtMvCenter.insert(tk.END, '1000')		
	txtLevel['state'] = tk.NORMAL			# 
	txtLevel.delete(0, tk.END)				
	txtLevel.insert(tk.END, '10')			
	txtFreq['state'] = tk.NORMAL			# 
	txtFreq.delete(0, tk.END)				
	txtFreq.insert(tk.END, '1000')			
	txtRecive.delete('1.0',tk.END)			# 
	btnDitherOn['state'] = tk.NORMAL		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())
		print('connecting ...', com, baud)
		ser = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')

	except:
		print('connecting error.')
		txtRecive.insert(tk.END,'Device Error')
		btnOpen['state'] = tk.NORMAL			# Open
		btnClose['state'] = tk.DISABLED			# Close
		btnInit['state'] = tk.DISABLED			# Init
		btnExit['state'] = tk.NORMAL			# Exit
		cbDacCh['state'] = tk.DISABLED			# 
		dacValue['state'] = tk.DISABLED			# 
		btnDac['state'] = tk.DISABLED			# Dac
		btnScale['state'] = tk.DISABLED			# 
		btnScaleZero['state'] = tk.DISABLED		# 
		btnAmeter['state'] = tk.DISABLED		# 
		btnSequence['state'] = tk.DISABLED		# Loop
		btnStop['state'] = tk.DISABLED			# Stop
		cbDacCh2['state'] = tk.DISABLED			# 
		txtMvStep['state'] = tk.DISABLED		# 
		txtWaitMs['state'] = tk.DISABLED		
		txtMvFrom['state'] = tk.DISABLED		# 
		txtMvTo['state'] = tk.DISABLED			# 
		cbDacCh3['state'] = tk.DISABLED			# 
		txtMvCenter['state'] = tk.DISABLED		# 
		txtLevel['state'] = tk.DISABLED			# 
		txtFreq['state'] = tk.DISABLED			# 
		btnDitherOn['state'] = tk.DISABLED		#
		btnDitherReflect['state'] = tk.DISABLED	#
		btnDitherOff['state'] = tk.DISABLED		#


########################################
#
def Close_clicked():
	global ser
	btnOpen['state'] = tk.NORMAL			# Open
	btnClose['state'] = tk.DISABLED			# Close
	btnInit['state'] = tk.NORMAL			# Init
	btnExit['state'] = tk.NORMAL			# Exit
	cbDacCh['state'] = tk.DISABLED			# 
	dacValue['state'] = tk.DISABLED			# 
	btnDac['state'] = tk.DISABLED			# Dac
	btnScale['state'] = tk.DISABLED			# 
	btnScaleZero['state'] = tk.DISABLED		# 
	btnAmeter['state'] = tk.DISABLED		# 
	btnSequence['state'] = tk.DISABLED		# Loop
	btnStop['state'] = tk.DISABLED			# Stop
	cbDacCh2['state'] = tk.DISABLED			# 
	txtMvStep['state'] = tk.DISABLED		# 
	txtWaitMs['state'] = tk.DISABLED		
	txtMvFrom['state'] = tk.DISABLED		# 
	txtMvTo['state'] = tk.DISABLED			# 
	cbDacCh3['state'] = tk.DISABLED			# 
	txtMvCenter['state'] = tk.DISABLED		# 
	txtLevel['state'] = tk.DISABLED			# 
	txtFreq['state'] = tk.DISABLED			# 
	btnDitherOn['state'] = tk.DISABLED		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#
	ser.close()



#	pre-process
#	wait second
#	post-process
#
#
#

g_IntervalMs	= int(100)
g_WaitMs		= int(5000)
g_WaitItvMs		= int(50)
g_DacValue		= int(0)
g_DacDir		= True;		# true:increase

########################################
#
def InitProcess():
	global g_DacValue
	global g_WaitMs
	global g_DacDir

	g_DacDir	= True;
	g_DacValue	= int(txtMvFrom.get())
	g_WaitMs	= int(txtWaitMs.get())

########################################
#
def PreProcess():
	global g_IntervalMs
	global g_WaitItvMs
	global g_DacValue

	print('Pre Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	# set current
	#
	DacCh = cbDacCh2.get()
	dac_text = dac_command_text(DacCh, g_DacValue) + '\r\n'
	ser.write(dac_text.encode('shift-jis'))
	print(dac_text)

	# make wait count
	g_WaitItvMs = g_WaitMs / g_IntervalMs

	return True

########################################
#
def WaitSecond():
	global g_WaitItvMs

#	print('Wait Second')
	g_WaitItvMs -= 1
	if (g_WaitItvMs > 0):
		return False

	return True

########################################
#
def PostProcess():
	global g_DacValue
	global g_DacDir
	global g_loopFlg

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

	#
	if (g_DacDir):
		nTo = int(txtMvTo.get())
		if (g_DacValue < nTo):
			g_DacValue += int(txtMvStep.get())
			print('dac : ' + str(g_DacValue))

			if (g_DacValue == nTo):
				if (g_DacDir):
					g_DacDir = False

		else:
			if (g_DacDir):
				g_DacDir = False
	else:
		nFrom = int(txtMvFrom.get())
		if (g_DacValue > nFrom):
			g_DacValue -= int(txtMvStep.get())
			print('dac : ' + str(g_DacValue))

		else:
			g_loopFlg = 0

	return True

########################################
#
ItvFuncList = [PreProcess, WaitSecond, PostProcess]
idxFunc = 0

########################################
#
def interval_work():
	global g_loopFlg
	global idxFunc
	global ser
	global g_DacValue

	func = ItvFuncList[idxFunc]
	if (func()):
		idxFunc += 1
		if (idxFunc >= len(ItvFuncList)):
			idxFunc = 0

#	txtRecive.see('end')
	if (g_loopFlg == 1):
		root.after(g_IntervalMs, interval_work)

	else:
		btnSequence['state'] = tk.NORMAL		# Loop
		btnStop['state'] = tk.DISABLED			# Stop

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
def Sequence_clicked():
	global g_loopFlg

	g_loopFlg = 1 
	btnSequence['state'] = tk.DISABLED
	btnStop['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

	InitProcess()

	interval_work()

########################################
#
def Stop_clicked():
	global g_loopFlg
	g_loopFlg = 0
	btnSequence['state'] = tk.NORMAL
	btnStop['state'] = tk.DISABLED

########################################
#
def dither_command_text(ch, mv, level, hz):
	return 'dither ' + str(ch) + ' ' + str(mv) + ' ' + str(level) + ' ' + str(hz)

########################################
#
def DitherReflect_clicked():
	global ser
	global cbDacCh3
	global txtMvCenter
	global txtLevel
	global txtFreq

	ch		= cbDacCh3.get()
	mv		= txtMvCenter.get()
	level	= txtLevel.get()
	hz		= txtFreq.get()

	text = dither_command_text(ch, mv, level, hz) + '\r\n'

	ser.write(text.encode('shift-jis'))
	print('dither ' + ch + ' ' + mv + ' ' + level + ' ' + hz)
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def DitherOn_clicked():

	global ser

	DitherReflect_clicked()

	text = 'idle start\r\n'

	ser.write(text.encode('shift-jis'))
	print('idle start')
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	btnDitherOn['state'] = tk.DISABLED		#
	btnDitherReflect['state'] = tk.NORMAL	#
	btnDitherOff['state'] = tk.NORMAL		#

########################################
#
def DitherOff_clicked():
	text = 'idle stop\r\n'

	ser.write(text.encode('shift-jis'))
	print('idle stop')
	sleep(0.1)
	txtRcv = ser.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	btnDitherOn['state'] = tk.NORMAL		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#

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

cbDevCom = ttk.Combobox(root, width = 2, values = ComChText)
cbDevCom.current(4)
cbDevCom.grid(row = row_idx, column = 1)

########################################
#
labelBaud = tk.Label(root, text = ' Baud :')
labelBaud.grid(row = row_idx, column = 2, sticky = tk.E)

cbDevBaud = ttk.Combobox(root, width = 8, values = BaudText)
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
labelCh = tk.Label(root, text = 'Ch : ')
labelCh.grid(row = row_idx, column = 0, sticky = tk.E, pady = 10)

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
labelCh2 = tk.Label(root, text = 'DAC Ch:')
labelCh2.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

cbDacCh2 = ttk.Combobox(root, width = 1, value = DacChText, state = tk.DISABLED)
cbDacCh2.set(DacChText[0])
cbDacCh2.grid(row = row_idx, column = 1, sticky = tk.W)

labelMvStep = tk.Label(root, text = 'mV Step :')
labelMvStep.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvStep = ttk.Entry(root, width = 6, state = tk.DISABLED)
txtMvStep.delete(0, tk.END)
txtMvStep.insert(tk.END, '2')
txtMvStep.grid(row = row_idx, column = 3, sticky = tk.W)

########################################
# Sequence
btnSequence = tk.Button(master = root, text = 'SEQUENCE', command = Sequence_clicked, state = tk.DISABLED, width = 10)
btnSequence.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1 

labelWaitMs = tk.Label(root, text = 'Wait ms :')
labelWaitMs.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtWaitMs = ttk.Entry(root, width = 6, state = tk.DISABLED)
txtWaitMs.delete(0, tk.END)
txtWaitMs.insert(tk.END, '5000')
txtWaitMs.grid(row = row_idx, column = 3, sticky = tk.W)

row_idx += 1 

labelMvFrom = tk.Label(root, text = 'mV from :')
labelMvFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtMvFrom = ttk.Entry(root, width = 6, state = tk.DISABLED)
txtMvFrom.delete(0, tk.END)
txtMvFrom.insert(tk.END, '0')
txtMvFrom.grid(row = row_idx, column = 1, sticky = tk.W)

labelMvTo = tk.Label(root, text = 'mV to :')
labelMvTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvTo = ttk.Entry(root, width = 6, state = tk.DISABLED)
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
labelCh3 = tk.Label(root, text = 'DAC Ch:')
labelCh3.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

cbDacCh3 = ttk.Combobox(root, width = 1, value = DacChText, state = tk.DISABLED)
cbDacCh3.set(DacChText[0])
cbDacCh3.grid(row = row_idx, column = 1, sticky = tk.W)

labelMvCenter = tk.Label(root, text = 'mV (center) :')
labelMvCenter.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvCenter = ttk.Entry(root, width = 6, state = tk.DISABLED)
txtMvCenter.delete(0, tk.END)
txtMvCenter.insert(tk.END, '1000')
txtMvCenter.grid(row = row_idx, column = 3, sticky = tk.W)

btnDitherOn = tk.Button(master = root, text = 'Dither On', command = DitherOn_clicked, state = tk.DISABLED, width = 10)
btnDitherOn.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1

labelLevel = tk.Label(root, text = 'Level (%) :')
labelLevel.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtLevel = ttk.Entry(root, width = 6, state = tk.DISABLED)
txtLevel.delete(0, tk.END)
txtLevel.insert(tk.END, '10')
txtLevel.grid(row = row_idx, column = 1, sticky = tk.W)

labelFreq = tk.Label(root, text = 'Frequency (Hz) :')
labelFreq.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtFreq = ttk.Entry(root, width = 8, state = tk.DISABLED)
txtFreq.delete(0, tk.END)
txtFreq.insert(tk.END, '1000')
txtFreq.grid(row = row_idx, column = 3, sticky = tk.W)

btnDitherReflect = tk.Button(master = root, text = 'Reflect', command = DitherReflect_clicked, state = tk.DISABLED, width = 10)
btnDitherReflect.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1

btnDitherOff = tk.Button(master = root, text = 'Dither Off', command = DitherOff_clicked, state = tk.DISABLED, width = 10)
btnDitherOff.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1
########################################
#
#txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 52, height = 13)
txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 56, height = 10)
txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10,pady = 10)

root.mainloop()

