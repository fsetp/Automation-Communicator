################################################################################
#
# coding:utf-8
import os
import csv
import serial
import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
import time
from datetime import datetime

from time import sleep
from tkinter import ttk

########################################
#
g_serial		= None
g_loopFlg		= 0
g_DataFileName	= None

########################################
#
ComChText	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
BaudText	= ['9600', '115200']
DacChText	= ['0', '1']
MethodText	= ['Normal', 'Dither']

########################################
#
def dac_command_text(ch, value):
	return 'dac ' + str(ch) + ' ' + str(value)

########################################
#
def EnableWidget():
	btnOpen['state'] = tk.DISABLED			# Open
	btnClose['state'] = tk.NORMAL			# Close
	btnFile['state'] = tk.NORMAL			#
	btnInit['state'] = tk.NORMAL			# Init
	btnExit['state'] = tk.DISABLED			# Exit
	cbDacCh['state'] = tk.NORMAL			# 
	dacValue['state'] = tk.NORMAL			# 
	btnDac['state'] = tk.NORMAL				# Dac
	btnScale['state'] = tk.NORMAL			# 
	btnScaleZero['state'] = tk.NORMAL		# 
	btnAmeter['state'] = tk.NORMAL			# 
	btnSequence['state'] = tk.NORMAL		#
	cbDacMethod['state'] = tk.NORMAL		#
	btnStop['state'] = tk.DISABLED			# Stop
	cbDacCh2['state'] = tk.NORMAL			# 
	txtMvStep['state'] = tk.NORMAL			# 
	txtWaitMs['state'] = tk.NORMAL			#
	txtMvFrom['state'] = tk.NORMAL			# 
	txtMvTo['state'] = tk.NORMAL			# 
	cbDacCh3['state'] = tk.NORMAL			# 
	txtMvCenter['state'] = tk.NORMAL		# 
	txtLevel['state'] = tk.NORMAL			# 
	txtFreq['state'] = tk.NORMAL			# 
#	txtRecive.delete('1.0',tk.END)			# 
	btnDitherOn['state'] = tk.NORMAL		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#

########################################
#
def DisableWidget():
	btnOpen['state'] = tk.NORMAL			# Open
	btnClose['state'] = tk.DISABLED			# Close
	btnFile['state'] = tk.DISABLED			#
	btnInit['state'] = tk.DISABLED			# Init
	btnExit['state'] = tk.NORMAL			# Exit
	cbDacCh['state'] = tk.DISABLED			# 
	dacValue['state'] = tk.DISABLED			# 
	btnDac['state'] = tk.DISABLED			# Dac
	btnScale['state'] = tk.DISABLED			# 
	btnScaleZero['state'] = tk.DISABLED		# 
	btnAmeter['state'] = tk.DISABLED		# 
	btnSequence['state'] = tk.DISABLED		#
	cbDacMethod['state'] = tk.DISABLED		#
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
def Open_clicked():
	global g_serial

	EnableWidget()

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())
		print('connecting ...', com, baud)
		g_serial = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')

	except:
		print('connecting error.')
		txtRecive.insert(tk.END,'Device Error')
		DisableWidget()

########################################
#
def Close_clicked():
	global g_serial

	DisableWidget()
	g_serial.close()

########################################
#
def writeData(time, current, load):
	global g_DataFileName

	csvLineData	= []

	csvLineData.append(time)
	csvLineData.append(current)
	csvLineData.append(load)
	print(csvLineData)

	try:
		f = open(g_DataFileName, 'a', encoding='utf-8', newline='')
		dataWriter = csv.writer(f)
		dataWriter.writerow(csvLineData)
		f.close()

	except:
		print('csv write error.')
		txtRecive.insert(tk.END,'csv write error')

########################################
#
def File_clicked():
	global g_DataFileName

	# current time
	time = datetime.now()
	timetext = time.strftime('%y%m%d%H%M%S')

	fTyp = [("csv file", "*.csv")]
	iniDir = os.path.abspath(os.path.dirname(__file__))
	iniFile = 'data_' + timetext + '.csv'
	file_name = tk.filedialog.asksaveasfilename(filetypes = fTyp, initialdir = iniDir, initialfile = iniFile, defaultextension = 'csv')
	g_DataFileName = file_name
	if (g_DataFileName != ''):
#		timetext = time.strftime('%H:%M:%S.%f')
		writeData('Time', 'Current', 'Load')
#		writeData(timetext, '0.1', '1.0')

########################################
#	pre-process
#	wait second
#	post-process
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

	# if normal selected
	if (cbDacMethod.current() == 0):

		# set current
		#
		DacCh = cbDacCh2.get()
		dac_text = dac_command_text(DacCh, g_DacValue) + '\r\n'
		g_serial.write(dac_text.encode('shift-jis'))
		print(dac_text)

	# if dither selected
	else:
		pass

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

	g_serial.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvScale = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcvScale.decode('ascii'))
	print(type(txtRcvScale))
#	txtRcvScale.replace('\r', '')
#	txtRcvScale.replace('\n', '')

	scale = str(txtRcvScale, 'utf-8')
#	scale.strip()
	print(scale)

	g_serial.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvCurrent = g_serial.readline()
	txtRecive.insert(tk.END,txtRcvCurrent.decode('ascii'))
	current = str(txtRcvCurrent, 'utf-8')
	current.replace('\r', '')
	current.replace('\n', '')
	print(current)

	# current time
	time = datetime.now()
	timetext = time.strftime('%H:%M:%S.%f')

	print(type(scale))
	print(type(current))

	writeData(timetext, scale, current)


	# rise up
	if (g_DacDir):
		# under 'To' value
		nTo = int(txtMvTo.get())
		if (g_DacValue < nTo):
			g_DacValue += int(txtMvStep.get())
			print('dac : ' + str(g_DacValue))

			# arrive at top
			if (g_DacValue == nTo):
				if (g_DacDir):
					g_DacDir = False

		# reach at top
		else:
			if (g_DacDir):
				g_DacDir = False

	# fall down
	else:
		# over 'From' value
		nFrom = int(txtMvFrom.get())
		if (g_DacValue > nFrom):
			g_DacValue -= int(txtMvStep.get())
			print('dac : ' + str(g_DacValue))

		# reach at 'From' value
		else:

			# if normal selecter
			if (cbDacMethod.current() == 1):
				g_loopFlg = 0

			# if dither selected
			else:
				pass

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
	global g_serial
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

	g_serial.write('init\r\n'.encode('shift-jis'))
	print('init')
	sleep(0.1)
	txtRcv = g_serial.read(256)
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def Exit_clicked():

	root.destroy()

########################################
#
def DAC_clicked():
	global g_serial
	global cbDacCh
	global dacValue

	ch		= cbDacCh.get()
	value	= dacValue.get()

	text = dac_command_text(ch, value) + '\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('dac ' + ch + ' ' + value)
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def SCALE_clicked():
	global g_serial
	g_serial.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def ZERO_clicked():
	global g_serial
	g_serial.write("scale zero\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def AMETER_clicked():
	global g_serial
	g_serial.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = g_serial.readline()
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

	btnSequence['state'] = tk.DISABLED
	btnStop['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

	InitProcess()

	# if normal selected
	if (cbDacMethod.current() == 0):
		g_loopFlg = 1 
		interval_work()

	# if dither selected
	else:
		pass

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
	global g_serial
	global cbDacCh3
	global txtMvCenter
	global txtLevel
	global txtFreq

	ch		= cbDacCh3.get()
	mv		= txtMvCenter.get()
	level	= txtLevel.get()
	hz		= txtFreq.get()

	text = dither_command_text(ch, mv, level, hz) + '\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('dither ' + ch + ' ' + mv + ' ' + level + ' ' + hz)
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

########################################
#
def DitherOn_clicked():
	global g_serial

	DitherReflect_clicked()

	text = 'idle start\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('idle start')
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	btnDitherOn['state'] = tk.DISABLED		#
	btnDitherReflect['state'] = tk.NORMAL	#
	btnDitherOff['state'] = tk.NORMAL		#

########################################
#
def DitherOff_clicked():
	global g_serial

	text = 'idle stop\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('idle stop')
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	print(txtRcv)

	btnDitherOn['state'] = tk.NORMAL		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#

########################################
#
root = tk.Tk()
#root.geometry('430x320')
root.geometry('440x500')
root.title('Communicator Tool for Atom Shell')

row_idx = 0
col_idx = 0

########################################
# serial com
labelCom = tk.Label(root, text = ' COM : ')
labelCom.grid(row = row_idx, column = 0, sticky = tk.E)

cbDevCom = ttk.Combobox(root, width = 2, values = ComChText)
cbDevCom.current(3)
cbDevCom.grid(row = row_idx, column = 1)

########################################
# baud rate
labelBaud = tk.Label(root, text = ' Baud : ')
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
# File
btnFile = tk.Button(master = root, text = 'File', command = File_clicked, state = tk.NORMAL, width = 10)
btnFile.grid(row = row_idx, column = 2, pady = 3)

########################################
# Init
btnInit = tk.Button(master = root, text = 'Init', command = Init_clicked, state = tk.DISABLED, width = 10)
btnInit.grid(row = row_idx, column = 3, pady = 3)

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
# scale
btnScale = tk.Button(master = root, text = 'SCALE', command = SCALE_clicked, state = tk.DISABLED, width = 10)
btnScale.grid(row = row_idx, column = 0, pady = 3)

########################################
# scale zero
btnScaleZero = tk.Button(master = root, text = 'ZERO', command = ZERO_clicked, state = tk.DISABLED, width = 10)
btnScaleZero.grid(row = row_idx, column = 1, pady = 3)

row_idx += 1

########################################
# ameter
btnAmeter = tk.Button(master = root, text = 'AMETER', command = AMETER_clicked, state = tk.DISABLED, width = 10)
btnAmeter.grid(row = row_idx, column = 1)

row_idx += 1
########################################
# dac
labelCh2 = tk.Label(root, text = 'DAC Ch : ')
labelCh2.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

cbDacCh2 = ttk.Combobox(root, width = 1, value = DacChText, state = tk.DISABLED)
cbDacCh2.set(DacChText[0])
cbDacCh2.grid(row = row_idx, column = 1, sticky = tk.W)

########################################
# mv step
labelMvStep = tk.Label(root, text = 'mV Step : ')
labelMvStep.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvStep = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtMvStep.delete(0, tk.END)
txtMvStep.insert(tk.END, '2')
txtMvStep.grid(row = row_idx, column = 3, sticky = tk.W)
txtMvStep['state'] = tk.DISABLED

########################################
# Sequence
btnSequence = tk.Button(master = root, text = 'SEQUENCE', command = Sequence_clicked, state = tk.DISABLED, width = 10)
btnSequence.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1 

########################################
#
labelMethod = tk.Label(root, text = 'Method : ')
labelMethod.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

cbDacMethod = ttk.Combobox(root, width = 8, value = MethodText, state = tk.DISABLED)
cbDacMethod.set(MethodText[0])
cbDacMethod.grid(row = row_idx, column = 1, sticky = tk.W)

########################################
# wait ms
labelWaitMs = tk.Label(root, text = 'Wait ms : ')
labelWaitMs.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtWaitMs = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtWaitMs.delete(0, tk.END)
txtWaitMs.insert(tk.END, '5000')
txtWaitMs.grid(row = row_idx, column = 3, sticky = tk.W)
txtWaitMs['state'] = tk.DISABLED

row_idx += 1 

########################################
#
labelMvFrom = tk.Label(root, text = 'mV from : ')
labelMvFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtMvFrom = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtMvFrom.delete(0, tk.END)
txtMvFrom.insert(tk.END, '0')
txtMvFrom.grid(row = row_idx, column = 1, sticky = tk.W)
txtMvFrom['state'] = tk.DISABLED

########################################
#
labelMvTo = tk.Label(root, text = 'mV to : ')
labelMvTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvTo = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtMvTo.delete(0, tk.END)
txtMvTo.insert(tk.END, '1000')
txtMvTo.grid(row = row_idx, column = 3, sticky = tk.W)
txtMvTo['state'] = tk.DISABLED

########################################
# Stop
btnStop = tk.Button(master = root, text = 'STOP', command = Stop_clicked, state = tk.DISABLED, width = 10)
btnStop.grid(row = row_idx, column = 4)

row_idx += 1

########################################
#
labelCh3 = tk.Label(root, text = 'DAC Ch : ')
labelCh3.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

cbDacCh3 = ttk.Combobox(root, width = 1, value = DacChText, state = tk.DISABLED)
cbDacCh3.set(DacChText[0])
cbDacCh3.grid(row = row_idx, column = 1, sticky = tk.W)

########################################
#
labelMvCenter = tk.Label(root, text = 'mV (center) : ')
labelMvCenter.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtMvCenter = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtMvCenter.delete(0, tk.END)
txtMvCenter.insert(tk.END, '1000')
txtMvCenter.grid(row = row_idx, column = 3, sticky = tk.W)
txtMvCenter['state'] = tk.DISABLED

########################################
#
btnDitherOn = tk.Button(master = root, text = 'Dither On', command = DitherOn_clicked, state = tk.DISABLED, width = 10)
btnDitherOn.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1

########################################
#
labelLevel = tk.Label(root, text = 'Level (%) : ')
labelLevel.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtLevel = ttk.Entry(root, width = 6, state = tk.NORMAL)
txtLevel.delete(0, tk.END)
txtLevel.insert(tk.END, '10')
txtLevel.grid(row = row_idx, column = 1, sticky = tk.W)
txtLevel['state'] = tk.DISABLED

########################################
#
labelFreq = tk.Label(root, text = 'Frequency (Hz) : ')
labelFreq.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

txtFreq = ttk.Entry(root, width = 8, state = tk.NORMAL)
txtFreq.delete(0, tk.END)
txtFreq.insert(tk.END, '1000')
txtFreq.grid(row = row_idx, column = 3, sticky = tk.W)
txtFreq['state'] = tk.DISABLED

########################################
#
btnDitherReflect = tk.Button(master = root, text = 'Reflect', command = DitherReflect_clicked, state = tk.DISABLED, width = 10)
btnDitherReflect.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1

########################################
#
btnDitherOff = tk.Button(master = root, text = 'Dither Off', command = DitherOff_clicked, state = tk.DISABLED, width = 10)
btnDitherOff.grid(row = row_idx, column = 4, pady = 3)

row_idx += 1
########################################
#
#txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 52, height = 13)
txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 56, height = 10)
txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10,pady = 10)

root.mainloop()

