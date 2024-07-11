################################################################################
#
# coding:utf-8
import os
import csv
import serial
import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.ttk as ttk
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

MethodText	= ['-', 'Normal', 'Dither']		# cbDacMethod
METHOD_NONE		= 0
METHOD_NORMAL	= 1
METHOD_DITHER	= 2

cbDevCom = None
cbDevBaud = None
btnOpen = None
btnClose = None
btnFile = None
btnInit = None
btnExit = None
cbDacCh = None
dacValue = None
btnDac = None
btnScale = None
btnScaleZero = None
btnAmeter = None
btnSequence = None
cbDacMethod = None
btnStop = None
txtMvStep = None
txtWaitMs = None
txtMvFrom = None
txtMvTo = None
txtMvCenter = None
txtLevel = None
txtFreq = None
btnDitherOn = None
btnDitherReflect = None
btnDitherOff = None
txtRecive = None


########################################
#
def dac_command_text(ch, value):
	return 'dac ' + str(ch) + ' ' + str(value)

########################################
#
def EnableWidget():
	global btnOpen
	global btnClose
	global btnFile
	global btnInit
	global btnExit
	global cbDacCh
	global dacValue
	global btnDac
	global btnScale
	global btnScaleZero
	global btnAmeter
	global btnSequence
	global cbDacMethod
	global btnStop
	global txtMvStep
	global txtWaitMs
	global txtMvFrom
	global txtMvTo
	global txtMvCenter
	global txtLevel
	global txtFreq
	global btnDitherOn
	global btnDitherReflect
	global btnDitherOff
	global txtRecive

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
	txtMvStep['state'] = tk.DISABLED		# 
	txtWaitMs['state'] = tk.DISABLED		#
	txtMvFrom['state'] = tk.DISABLED		# 
	txtMvTo['state'] = tk.DISABLED			# 
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
	global btnOpen
	global btnClose
	global btnFile
	global btnInit
	global btnExit
	global cbDacCh
	global dacValue
	global btnDac
	global btnScale
	global btnScaleZero
	global btnAmeter
	global btnSequence
	global cbDacMethod
	global btnStop
	global txtMvStep
	global txtWaitMs
	global txtMvFrom
	global txtMvTo
	global txtMvCenter
	global txtLevel
	global txtFreq
	global btnDitherOn
	global btnDitherReflect
	global btnDitherOff

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
	txtMvStep['state'] = tk.DISABLED		# 
	txtWaitMs['state'] = tk.DISABLED		
	txtMvFrom['state'] = tk.DISABLED		# 
	txtMvTo['state'] = tk.DISABLED			# 
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
	global cbDevCom
	global cbDevBaud
	global txtRecive
	
	EnableWidget()

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())
#		com = 'COM4'
#		baud = 115200

		print('connecting ...', com, baud)
		g_serial = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')

	except:
		print('connecting error.')
		txtRecive.insert(tk.END,'Device Error\r\n')
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
	global txtRecive
	
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

	# if normal selected
	if (cbDacMethod.current() == METHOD_NORMAL):
		iniFile = 'normal_' + timetext + '.csv'

	# if dither selected
	else:
		iniFile = 'dither_' + timetext + '.csv'

	file_name = tk.filedialog.asksaveasfilename(filetypes = fTyp, initialdir = iniDir, initialfile = iniFile, defaultextension = 'csv')
	g_DataFileName = file_name

	if (g_DataFileName != ''):
		writeData('Time', 'Current', 'Load')

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

g_DitherCh		= 0
g_DitherMv		= 3000
g_DitherLevel	= 10
g_DitherHz		= 1000

########################################
#
def SetDacValue(ch, value):
	dac_text = dac_command_text(ch, value) + '\r\n'
	g_serial.write(dac_text.encode('shift-jis'))
	text = dac_text[:-2]
	print(text)


g_nTimes = 0
g_nTime  = 0
########################################
#
def InitProcess():
	global g_DacValue
	global g_WaitMs
	global g_DacDir

	global g_DitherCh
	global g_DitherMv
	global g_DitherLevel
	global g_DitherHz
	global cbDacCh
	global txtMvCenter
	global txtLevel
	global txtFreq
	global txtRecive
	
	global g_nTimes
	global g_nTime

	# if normal selected
	if (cbDacMethod.current() == METHOD_NORMAL):

		g_DacDir	= True;
		g_DacValue	= int(txtMvFrom.get())
		g_WaitMs	= int(txtWaitMs.get())

	# if dither selected
	else:
		g_DitherCh		= cbDacCh.get()
		g_DitherMv		= txtMvCenter.get()
		g_DitherLevel	= txtLevel.get()
		g_DitherHz		= txtFreq.get()
		g_WaitMs		= int(txtWaitMs.get())
		DitherReflect(g_DitherCh, g_DitherMv, g_DitherLevel, g_DitherHz)
		DitherOn()

	#
	nFrom  = int(txtMvFrom.get())
	nTo    = int(txtMvTo.get())
	nStep  = int(txtMvStep.get())
	nTimes = (nTo - nFrom) / nStep
	nTotalWaitMs = nTimes * g_WaitMs
	text = 'Times : ' + str(nTimes) + '\r\n'
	txtRecive.insert(tk.END,text.encode('ascii'))
	text = 'Total Sec : ' + str(nTotalWaitMs / 1000) + '\r\n'
	txtRecive.insert(tk.END,text.encode('ascii'))

	g_nTimes = nTimes
	g_nTime  = 0


########################################
#
def PreProcess():
	global g_IntervalMs
	global g_WaitItvMs
	global g_DacValue
	global cbDacCh
	global txtRecive
	
	global g_nTimes
	global g_nTime

	print('Pre Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	# if normal selected
	if (cbDacMethod.current() == METHOD_NORMAL):

		# set value
		#
		DacCh = cbDacCh.get()
		SetDacValue(DacCh, g_DacValue)

	# if dither selected
	else:
		DitherReflect(g_DitherCh, g_DitherMv, g_DitherLevel, g_DitherHz)

	# make wait count
	g_WaitItvMs = g_WaitMs / g_IntervalMs

	#
	text = str(g_nTime) + ' / ' + str(g_nTimes) + '\r\n'
	txtRecive.insert(tk.END,text.encode('ascii'))
	text = text[:-2]
	print(text)
	g_nTime += 1

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
	global g_DataFileName
	global cbDacCh
	global txtRecive
	
	print('Post Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	# current value
	g_serial.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvCurrent = g_serial.readline()
	txtRecive.insert(tk.END,txtRcvCurrent.decode('ascii'))

	current = txtRcvCurrent[:-2]
	current = str(current, 'utf-8')
	print(current + ' mV')

	# scale value (load)
	g_serial.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvScale = g_serial.readline()
	txtRecive.insert(tk.END,txtRcvScale.decode('ascii'))
	scale = txtRcvScale[:-2]
	scale = str(scale, 'utf-8')
	print(scale + ' g')

	# current time
	time = datetime.now()
	timetext = time.strftime('%H:%M:%S.%f')

	# save to csv
	writeData(timetext, current, scale)

	# rise up
	if (g_DacDir):
		# under 'To' value
		nTo = int(txtMvTo.get())
		if (g_DacValue < nTo):
			g_DacValue += int(txtMvStep.get())
			print('dac : ' + str(g_DacValue) + ' mV')

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
			print('dac : ' + str(g_DacValue) + ' mV')

		# reach at 'From' value
		else:

			# loop end, clear file mame
			g_loopFlg		= 0
			g_DataFileName	= None

			# if normal selected
			if (cbDacMethod.current() == METHOD_NORMAL):
				DacCh = cbDacCh.get()
				SetDacValue(DacCh, 0)

			# if dither selected
			else:
				DitherOff()

	# if dither selected
	if (cbDacMethod.current() == METHOD_DITHER):
		g_DitherMv = g_DacValue
		print('dither selected')

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
	global g_root

	func = ItvFuncList[idxFunc]
	if (func()):
		idxFunc += 1
		if (idxFunc >= len(ItvFuncList)):
			idxFunc = 0

#	txtRecive.see('end')
	if (g_loopFlg == 1):
		g_root.after(g_IntervalMs, interval_work)

	else:
		btnSequence['state'] = tk.NORMAL		# Loop
		btnStop['state'] = tk.DISABLED			# Stop

########################################
#
def Init_clicked():
	global g_serial
	global txtRecive

	g_serial.write('init\r\n'.encode('shift-jis'))
	print('init')
	sleep(0.1)
#	txtRcv = g_serial.read(256)
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
#	print(txtRcv)
#	for i in range(3):
	while True:
		txtRcv = g_serial.readline()
		if (txtRcv == b''):
			break
		txtRecive.insert(tk.END,txtRcv.decode('ascii'))
		reply = txtRcv[:-2]
		reply = str(reply, 'utf-8')
		print(reply)

########################################
#
def Exit_clicked():
	global g_root

	g_root.destroy()

########################################
#
def DAC_clicked():
	global g_serial
	global cbDacCh
	global dacValue

	ch		= cbDacCh.get()
	value	= dacValue.get()

	SetDacValue(ch, value)

	print('dac ' + ch + ' ' + value)
#	sleep(0.1)
#	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
#	print(txtRcv)

########################################
#
def SCALE_clicked():
	global g_serial
	global txtRecive
	
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
#	sleep(0.1)
#	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
#	print(txtRcv)

########################################
#
def AMETER_clicked():
	global g_serial
	global txtRecive
	
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
def select_combo(event):
	global cbDacCh
	global dacValue

	global txtMvCenter
	global txtLevel
	global txtFreq
	global cbDacMethod
	global txtMvStep
	global btnSequence
	global txtWaitMs
	global txtMvFrom
	global txtMvTo

	idx = cbDacMethod.current()
	if (idx == METHOD_NONE):

		dacValue['state']		= tk.NORMAL

		txtMvCenter['state']	= tk.NORMAL
		txtLevel['state']		= tk.NORMAL
		txtFreq['state']		= tk.NORMAL

		txtMvStep['state']		= tk.DISABLED
#		btnSequence['state']	= tk.DISABLED
		txtWaitMs['state']		= tk.DISABLED
		txtMvFrom['state']		= tk.DISABLED
		txtMvTo['state']		= tk.DISABLED

	elif (idx == METHOD_NORMAL):
		dacValue['state']		= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.DISABLED
		txtFreq['state']		= tk.DISABLED

		txtMvStep['state']		= tk.NORMAL
#		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.NORMAL
		txtMvTo['state']		= tk.NORMAL

	elif (idx == METHOD_DITHER):
		dacValue['state']		= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.DISABLED
		txtFreq['state']		= tk.DISABLED

		txtMvStep['state']		= tk.NORMAL
#		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.NORMAL
		txtMvTo['state']		= tk.NORMAL

########################################
#
def Sequence_clicked():
	global g_loopFlg
	global g_DataFileName
	global txtRecive
	
	print(type(g_DataFileName))
	print(g_DataFileName)

	#
	if (g_DataFileName == None or g_DataFileName ==""):
		File_clicked()

		if (g_DataFileName ==""):
			return

	btnSequence['state'] = tk.DISABLED
	btnStop['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

	InitProcess()

	# if normal selected
#	if (cbDacMethod.current() == METHOD_NORMAL):
	g_loopFlg = 1 
	interval_work()

	# if dither selected
#	else:
#		DitherReflect_clicked()
#		g_loopFlg = 1 
#		interval_work()

########################################
#
def Stop_clicked():
	global g_loopFlg
	global g_DataFileName

	g_loopFlg = 0
	g_DataFileName = None
	btnSequence['state'] = tk.NORMAL
	btnStop['state'] = tk.DISABLED

########################################
#
def dither_command_text(ch, mv, level, hz):
	return 'dither ' + str(ch) + ' ' + str(mv) + ' ' + str(level) + ' ' + str(hz)

########################################
#
def DitherReflect(ch, mv, level, hz):
	text = dither_command_text(ch, mv, level, hz) + '\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('dither ' + ch + ' ' + mv + ' ' + level + ' ' + hz)
#	sleep(0.1)
#	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
#	print(txtRcv)

########################################
#
def DitherReflect_clicked():
	global g_serial
	global cbDacCh
	global txtMvCenter
	global txtLevel
	global txtFreq

	ch		= cbDacCh.get()
	mv		= txtMvCenter.get()
	level	= txtLevel.get()
	hz		= txtFreq.get()

	DitherReflect(ch, mv, level, hz)

########################################
#
def DitherOn():
	global g_serial
	global txtRecive
	
	DitherReflect_clicked()

	text = 'idle start\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('idle start')

	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))

	reply = txtRcv[:-2]
	reply = str(reply, 'utf-8')
	print(reply)

########################################
#
def DitherOn_clicked():

	DitherOn()

	btnDitherOn['state'] = tk.DISABLED		#
	btnDitherReflect['state'] = tk.NORMAL	#
	btnDitherOff['state'] = tk.NORMAL		#

########################################
#
def DitherOff():

	global g_serial
	global txtRecive

	text = 'idle stop\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('idle stop')
	sleep(0.1)
	txtRcv = g_serial.readline()
	txtRecive.insert(tk.END,txtRcv.decode('ascii'))

	reply = txtRcv[:-2]
	reply = str(reply, 'utf-8')
	print(reply)

########################################
#
def DitherOff_clicked():

	DitherOff()

	btnDitherOn['state'] = tk.NORMAL		#
	btnDitherReflect['state'] = tk.DISABLED	#
	btnDitherOff['state'] = tk.DISABLED		#

################################################################################
#
g_root = None

########################################
#
def main():
	global cbDevCom
	global cbDevBaud
	global g_root
	global btnOpen
	global btnClose
	global btnFile
	global btnInit
	global btnExit
	global cbDacCh
	global dacValue
	global btnDac
	global btnScale
	global btnScaleZero
	global btnAmeter
	global btnSequence
	global cbDacMethod
	global btnStop
	global txtMvStep
	global txtWaitMs
	global txtMvFrom
	global txtMvTo
	global txtMvCenter
	global txtLevel
	global txtFreq
	global btnDitherOn
	global btnDitherReflect
	global btnDitherOff
	global txtRecive
	
	g_root = tk.Tk()
	g_root.geometry('432x440')
	g_root.title('Communicator Tool for Atom Shell')

	row_idx = 0
	col_idx = 0

	########################################
	# serial com
	labelCom = tk.Label(g_root, text = ' COM : ')
	labelCom.grid(row = row_idx, column = 0, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevCom = ttk.Combobox(g_root, width = 2, values = ComChText)
	cbDevCom.current(4)
	cbDevCom.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	########################################
	# baud rate
	labelBaud = tk.Label(g_root, text = ' Baud : ')
	labelBaud.grid(row = row_idx, column = 2, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevBaud = ttk.Combobox(g_root, width = 8, values = BaudText)
	cbDevBaud.current(1)
	cbDevBaud.grid(row = row_idx, column = 3, padx = 2, pady = 3 )

	row_idx += 1
	########################################
	# Open
	btnOpen = tk.Button(master = g_root, text = 'Open', command = Open_clicked, width = 10)
	btnOpen.grid(row = row_idx, column = 0, padx = 2, pady = 3)

	########################################
	# Close
	btnClose = tk.Button(master = g_root, text = 'Close', command = Close_clicked, state = tk.DISABLED, width = 10)
	btnClose.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	########################################
	# File
	btnFile = tk.Button(master = g_root, text = 'File', command = File_clicked, state = tk.NORMAL, width = 10)
	btnFile.grid(row = row_idx, column = 2, padx = 2, pady = 3)

	########################################
	# Init
	btnInit = tk.Button(master = g_root, text = 'Init', command = Init_clicked, state = tk.DISABLED, width = 10)
	btnInit.grid(row = row_idx, column = 3, padx = 2, pady = 3)

	########################################
	# Exit
	btnExit = tk.Button(master=g_root, text='Exit' , command = Exit_clicked, width = 10)
	btnExit.grid(row = row_idx, column = 4, padx = 2, pady = 3)

	row_idx += 1

	########################################
	#
	border0 = ttk.Separator(g_root, orient = 'horizontal')
	border0.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# scale
	btnScale = tk.Button(master = g_root, text = 'SCALE', command = SCALE_clicked, state = tk.DISABLED, width = 10)
	btnScale.grid(row = row_idx, column = 0, padx = 2, pady = 3)

	########################################
	# scale zero
	btnScaleZero = tk.Button(master = g_root, text = 'ZERO', command = ZERO_clicked, state = tk.DISABLED, width = 10)
	btnScaleZero.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	########################################
	# ameter
	btnAmeter = tk.Button(master = g_root, text = 'AMETER', command = AMETER_clicked, state = tk.DISABLED, width = 10)
	btnAmeter.grid(row = row_idx, column = 2, padx = 2, pady = 3)

	########################################
	#
	labelMethod = tk.Label(g_root, text = 'Method : ')
	labelMethod.grid(row = row_idx, column = 3, sticky = tk.E, pady = 3)

	cbDacMethod = ttk.Combobox(g_root, width = 8, value = MethodText, state = tk.DISABLED)
	cbDacMethod.set(MethodText[0])
	cbDacMethod.grid(row = row_idx, column = 4, sticky = tk.W)
	cbDacMethod.bind('<<ComboboxSelected>>', select_combo)

	row_idx += 1

	########################################
	#
	border1 = ttk.Separator(g_root, orient = 'horizontal')
	border1.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# Dac Ch
	labelCh = tk.Label(g_root, text = 'Dac Ch : ')
	labelCh.grid(row = row_idx, column = 0, sticky = tk.E, pady = 10)

	cbDacCh = ttk.Combobox(g_root, width = 1, value = DacChText, state = tk.DISABLED)
	cbDacCh.set(DacChText[0])
	cbDacCh.grid(row = row_idx, column = 1, sticky = tk.W)

	########################################
	# Dac Value
	label_dac = tk.Label(g_root, text = 'Dac(mV) : ')
	label_dac.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	dacValue = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	dacValue.delete(0, tk.END)
	dacValue.insert(tk.END, '1000')
	dacValue.grid(row = row_idx, column = 3, sticky = tk.W)
	dacValue['state'] = tk.DISABLED

	########################################
	# DAC button
	btnDac = tk.Button(master = g_root, text = 'DAC', command = DAC_clicked, state = tk.DISABLED, width = 10)
	btnDac.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	#
	border2 = ttk.Separator(g_root, orient = 'horizontal')
	border2.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# mV Center
	labelMvCenter = tk.Label(g_root, text = 'mV (center) : ')
	labelMvCenter.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtMvCenter = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvCenter.delete(0, tk.END)
	txtMvCenter.insert(tk.END, '200')
	txtMvCenter.grid(row = row_idx, column = 1, sticky = tk.W)
	txtMvCenter['state'] = tk.DISABLED

	########################################
	# Reflect
	btnDitherReflect = tk.Button(master = g_root, text = 'Reflect', command = DitherReflect_clicked, state = tk.DISABLED, width = 10)
	btnDitherReflect.grid(row = row_idx, column = 3, pady = 3)

	########################################
	#
	btnDitherOn = tk.Button(master = g_root, text = 'Dither On', command = DitherOn_clicked, state = tk.DISABLED, width = 10)
	btnDitherOn.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	# Level
	labelLevel = tk.Label(g_root, text = 'Level (%) : ')
	labelLevel.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtLevel = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtLevel.delete(0, tk.END)
	txtLevel.insert(tk.END, '10')
	txtLevel.grid(row = row_idx, column = 1, sticky = tk.W)
	txtLevel['state'] = tk.DISABLED

	########################################
	# Frequency
	labelFreq = tk.Label(g_root, text = 'Frequency (Hz) : ')
	labelFreq.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtFreq = ttk.Entry(g_root, width = 8, state = tk.NORMAL)
	txtFreq.delete(0, tk.END)
	txtFreq.insert(tk.END, '200')
	txtFreq.grid(row = row_idx, column = 3, sticky = tk.W)
	txtFreq['state'] = tk.DISABLED

	########################################
	#
	btnDitherOff = tk.Button(master = g_root, text = 'Dither Off', command = DitherOff_clicked, state = tk.DISABLED, width = 10)
	btnDitherOff.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	#
	border3 = ttk.Separator(g_root, orient = 'horizontal')
	border3.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# mv step
	labelMvStep = tk.Label(g_root, text = 'mV Step : ')
	labelMvStep.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtMvStep = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvStep.delete(0, tk.END)
	txtMvStep.insert(tk.END, '2')
	txtMvStep.grid(row = row_idx, column = 1, sticky = tk.W)
	txtMvStep['state'] = tk.DISABLED

	########################################
	# wait ms
	labelWaitMs = tk.Label(g_root, text = 'Wait ms : ')
	labelWaitMs.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtWaitMs = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtWaitMs.delete(0, tk.END)
	txtWaitMs.insert(tk.END, '1000')
	txtWaitMs.grid(row = row_idx, column = 3, sticky = tk.W)
	txtWaitMs['state'] = tk.DISABLED

	########################################
	# Sequence
	btnSequence = tk.Button(master = g_root, text = 'SEQUENCE', command = Sequence_clicked, state = tk.DISABLED, width = 10)
	btnSequence.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1 

	########################################
	#
	labelMvFrom = tk.Label(g_root, text = 'mV from : ')
	labelMvFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtMvFrom = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvFrom.delete(0, tk.END)
	txtMvFrom.insert(tk.END, '100')
	txtMvFrom.grid(row = row_idx, column = 1, sticky = tk.W)
	txtMvFrom['state'] = tk.DISABLED

	########################################
	#
	labelMvTo = tk.Label(g_root, text = 'mV to : ')
	labelMvTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtMvTo = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvTo.delete(0, tk.END)
	txtMvTo.insert(tk.END, '300')
	txtMvTo.grid(row = row_idx, column = 3, sticky = tk.W)
	txtMvTo['state'] = tk.DISABLED

	########################################
	# Stop
	btnStop = tk.Button(master = g_root, text = 'STOP', command = Stop_clicked, state = tk.DISABLED, width = 10)
	btnStop.grid(row = row_idx, column = 4)

	row_idx += 1

	########################################
	#
	#txtRecive = tkinter.scrolledtext.ScrolledText(g_root , width = 52, height = 13)
	txtRecive = tkinter.scrolledtext.ScrolledText(g_root , width = 56, height = 10)
	txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10,pady = 10)

	g_root.mainloop()

if __name__ == "__main__":
	main()
