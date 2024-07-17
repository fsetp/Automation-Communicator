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
g_bOpen			= False

########################################
#
ComChText	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
BaudText	= ['9600', '115200']
DacChText	= ['0', '1']

MethodText	= ['-', 'Normal', 'Dither', '4 points']		# cbDacMethod
METHOD_NONE		= 0
METHOD_NORMAL	= 1
METHOD_DITHER	= 2
METHOD_4POINTS	= 3

########################################
# widget globals
cbDevCom			= None
cbDevBaud			= None
btnOpen				= None
btnClose			= None
btnFile				= None
btnInit				= None
btnExit				= None
cbDacCh				= None
dacValue			= None
btnDac				= None
btnScale			= None
btnScaleZero		= None
btnAmeter			= None
btnSequence			= None
cbDacMethod			= None
btnStop				= None
txtMvStep			= None
txtWaitMs			= None
txtMvFrom			= None
txtMvTo				= None
txtMvCenter			= None
txtLevel			= None
txtFreq				= None
btnDitherOn			= None
btnDitherReflect	= None
btnDitherOff		= None
txtRecive			= None
txtLoopTimes		= None
txtRemainSec		= None
txtScale			= None
txtCurrent			= None

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
	global txtLoopTimes
	global txtRecive

	btnOpen['state']			= tk.DISABLED	# Open
	btnClose['state']			= tk.NORMAL		# Close
	btnFile['state']			= tk.NORMAL		#
	btnInit['state']			= tk.NORMAL		# Init
	btnExit['state']			= tk.NORMAL		# Exit
	cbDacCh['state']			= 'readonly'	# 
	dacValue['state']			= tk.NORMAL		# 
	btnDac['state']				= tk.NORMAL		# Dac
	btnScale['state']			= tk.NORMAL		# 
	btnScaleZero['state']		= tk.NORMAL		# 
	btnAmeter['state']			= tk.NORMAL		# 
	btnSequence['state']		= tk.DISABLED	#
	cbDacMethod['state']		= 'readonly'	#
	btnStop['state']			= tk.DISABLED	# Stop
	txtMvStep['state']			= tk.DISABLED	# 
	txtWaitMs['state']			= tk.DISABLED	#
	txtMvFrom['state']			= tk.DISABLED	# 
	txtMvTo['state']			= tk.DISABLED	# 
	txtMvCenter['state']		= tk.NORMAL		# 
	txtLevel['state']			= tk.NORMAL		# 
	txtFreq['state']			= tk.NORMAL		# 
	btnDitherOn['state']		= tk.NORMAL		#
	btnDitherReflect['state']	= tk.DISABLED	#
	btnDitherOff['state']		= tk.DISABLED	#
	txtLoopTimes['state']		= tk.DISABLED	#
	txtUpBottom['state']		= tk.DISABLED	#
	txtUpTop['state']			= tk.DISABLED	#
	txtDownTop['state']			= tk.DISABLED	#
	txtDownBottom['state']		= tk.DISABLED	#
	txtRecive['state']			= tk.NORMAL		#

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
	global txtLoopTimes
	global btnDitherOff

	btnOpen['state']			= tk.NORMAL		# Open
	btnClose['state']			= tk.DISABLED	# Close
	btnFile['state']			= tk.DISABLED	#
	btnInit['state']			= tk.DISABLED	# Init
	btnExit['state']			= tk.NORMAL		# Exit
	cbDacCh['state']			= tk.DISABLED	# 
	dacValue['state']			= tk.DISABLED	# 
	btnDac['state']				= tk.DISABLED	# Dac
	btnScale['state']			= tk.DISABLED	# 
	btnScaleZero['state']		= tk.DISABLED	# 
	btnAmeter['state']			= tk.DISABLED	# 
	btnSequence['state']		= tk.DISABLED	#
	cbDacMethod['state']		= tk.DISABLED	#
	btnStop['state']			= tk.DISABLED	# Stop
	txtMvStep['state']			= tk.DISABLED	# 
	txtWaitMs['state']			= tk.DISABLED	#
	txtMvFrom['state']			= tk.DISABLED	# 
	txtMvTo['state']			= tk.DISABLED	# 
	txtMvCenter['state']		= tk.DISABLED	# 
	txtLevel['state']			= tk.DISABLED	# 
	txtFreq['state']			= tk.DISABLED	# 
	btnDitherOn['state']		= tk.DISABLED	#
	btnDitherReflect['state']	= tk.DISABLED	#
	btnDitherOff['state']		= tk.DISABLED	#
	txtLoopTimes['state']		= tk.DISABLED	#
	txtUpBottom['state']		= tk.DISABLED	#
	txtUpTop['state']			= tk.DISABLED	#
	txtDownTop['state']			= tk.DISABLED	#
	txtDownBottom['state']		= tk.DISABLED	#
	txtRecive['state']			= tk.DISABLED	#

########################################
#
def Open_clicked():
	global g_serial
	global g_bOpen
	global cbDevCom
	global cbDevBaud
	global txtRecive

	EnableWidget()

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())

		print('connecting ...', com, baud)
		g_serial = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')
		txtRecive.delete('1.0',tk.END)
		txtRecive.insert(tk.END,'Connected\r\n')
		g_bOpen = True

	except:
		print('connecting error.')
		txtRecive.delete('1.0',tk.END)
		txtRecive.insert(tk.END,'Connecting Error\r\n')
		g_bOpen = False
		DisableWidget()

########################################
#
def Close_clicked():
	global g_serial
	global g_bOpen

	if (g_bOpen):
		DisableWidget()
		g_serial.close()
		g_bOpen = False
		print('connecting closed.')
		txtRecive.delete('1.0',tk.END)
		txtRecive.insert(tk.END,'Closed\r\n')

########################################
#
def writeCsvData(time, idx, dac, current, load):
	global g_DataFileName
	global txtRecive

	csvLineData	= []

	csvLineData.append(time)
	csvLineData.append(idx)
	csvLineData.append(dac)
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
	global cbDacMethod

	# current time
	time = datetime.now()
	timetext = time.strftime('%y%m%d%H%M%S')

	fTyp = [("csv file", "*.csv")]
	iniDir = os.path.abspath(os.path.dirname(__file__))

	# None
	if (cbDacMethod.current() == METHOD_NONE):
		pass

	# normal selected
	elif (cbDacMethod.current() == METHOD_NORMAL):
		iniFile = 'normal_' + timetext + '.csv'

	# dither selected
	elif (cbDacMethod.current() == METHOD_DITHER):
		iniFile = 'dither_' + timetext + '.csv'

	# 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):
		iniFile = 'fourpoints_' + timetext + '.csv'

	#
	file_name = tk.filedialog.asksaveasfilename(filetypes = fTyp, initialdir = iniDir, initialfile = iniFile, defaultextension = 'csv')
	g_DataFileName = file_name

	# csv header text
	if (g_DataFileName != ''):
		writeCsvData('Time', 'Index', 'Dac', 'Current', 'Load')

########################################
#	pre-process
#	wait second
#	post-process
#
g_IntervalMs	= int(100)	# 100 ms
g_WaitMs		= 0
g_WaitItvMs		= 0
g_DacValue		= 0
g_DacDir		= True		# true:increase

g_DitherCh		= 0
g_DitherLevel	= 0
g_DitherHz		= 0

g_nLoopTimes	= 0
g_nLoopIndex	= 0
g_nRemainSec	= 0

g_FourPoints	= None
g_FourPointsIdx	= 0

########################################
#
def SetDacValue(ch, value):
	global g_serial

	dac_text = dac_command_text(ch, value) + '\r\n'
	g_serial.write(dac_text.encode('shift-jis'))
	text = dac_text[:-2]
	print(text)

########################################
#
def InitProcess():
	global g_DacValue
	global g_WaitMs
	global g_DacDir

	global g_DitherCh
	global g_DitherLevel
	global g_DitherHz
	global cbDacCh
	global cbDacMethod
	global txtMvCenter
	global txtLevel
	global txtFreq
	global txtRecive
	global txtMvFrom
	global txtMvTo
	global txtMvStep
	global txtWaitMs
	global txtLoopTimes
	global txtUpBottom
	global txtUpTop
	global txtDownTop
	global txtDownBottom

	global g_nLoopIndex
	global txtRemainSec

	global g_nLoopTimes
	global g_nRemainSec

	global g_FourPoints
	global g_FourPointsIdx

	print('Init')

	#
	nFrom  = int(txtMvFrom.get())
	nTo    = int(txtMvTo.get())
	nStep  = int(txtMvStep.get())
	nTimes = 0

	# loop times
	g_nLoopIndex = 0
	g_nLoopTimes = int(txtLoopTimes.get())
	if (g_nLoopTimes < 1):
		g_nLoopTimes = 1

	# if none selected
	if (cbDacMethod.current() == METHOD_NONE):
		pass

	# if normal selected
	elif (cbDacMethod.current() == METHOD_NORMAL):
		g_DacDir	= True;
		g_DacValue	= int(txtMvFrom.get())
		g_WaitMs	= int(txtWaitMs.get())

		if (nStep > 0):
			nTimes = int(((nTo - nFrom) / nStep) * 2 * g_nLoopTimes + g_nLoopTimes)	# rising and falling
		else:
			nTimes = g_nLoopTimes

	# if dither selected
	elif (cbDacMethod.current() == METHOD_DITHER):
		g_DacDir		= True;
		g_DacValue		= int(txtMvFrom.get())
		g_WaitMs		= int(txtWaitMs.get())
		g_DitherCh		= int(cbDacCh.get())
		g_DitherLevel	= int(txtLevel.get())
		g_DitherHz		= int(txtFreq.get())

		if (nStep > 0):
			nTimes = int(((nTo - nFrom) / nStep) * 2 * g_nLoopTimes + g_nLoopTimes)	# rising and falling
		else:
			nTimes = g_nLoopTimes

		DitherReflect(g_DitherCh, g_DacValue, g_DitherLevel, g_DitherHz)
		DitherOn()

	# if 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):
		pt1 = int(txtUpBottom.get())
		pt2 = int(txtUpTop.get())
		pt3 = int(txtDownTop.get())
		pt4 = int(txtDownBottom.get())
		g_FourPoints	= [pt1, pt2, pt3, pt4]
		g_FourPointsIdx = 0		# 0 to len(g_FourPoints) - 1
		g_DacValue		= g_FourPoints[g_FourPointsIdx]
		g_WaitMs		= int(txtWaitMs.get())

		nTimes = g_nLoopTimes * len(g_FourPoints)

	#
	nTotalWaitMs = int(nTimes * g_WaitMs)
	text = 'Times : ' + str(nTimes) + '\r\n'
	txtRecive.insert(tk.END,text.encode('ascii'))
	text = 'Total Sec : ' + str(int(nTotalWaitMs / 1000)) + '\r\n'
	txtRecive.insert(tk.END,text.encode('ascii'))

	print(str(g_nLoopIndex) + ' / ' + str(g_nLoopTimes))

	# remain sec
	g_nRemainSec = int(nTotalWaitMs / 1000)
	text = str(g_nRemainSec) + ' sec'
	txtRemainSec['text'] = text

########################################
#
def PreProcess():
	global g_IntervalMs
	global g_WaitItvMs
	global g_WaitMs
	global g_DacValue
	global cbDacCh
	global txtRecive
	global txtRemainSec
	global cbDacMethod
	global g_nRemainSec
	global g_DitherCh
	global g_DitherLevel
	global g_DitherHz

	global g_FourPoints
	global g_FourPointsIdx

	print('Pre Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	print(timetext)

	# if none selected
	if (cbDacMethod.current() == METHOD_NONE):
		pass

	# if normal selected
	elif (cbDacMethod.current() == METHOD_NORMAL):

		# set value
		#
		DacCh = cbDacCh.get()
		SetDacValue(DacCh, g_DacValue)

	# if dither selected
	elif (cbDacMethod.current() == METHOD_DITHER):

		DitherReflect(g_DitherCh, g_DacValue, g_DitherLevel, g_DitherHz)

	# if 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):

		# set value
		#
		DacCh = cbDacCh.get()
		SetDacValue(DacCh, g_DacValue)

	# make wait count
	g_WaitItvMs = g_WaitMs / g_IntervalMs

	# Remain sec
	text = str(g_nRemainSec) + ' sec'
	txtRemainSec['text'] = text

#	print(text + '\r\n')
	print(text)

	# subdtruct remain sec
	g_nRemainSec -= int(g_WaitMs / 1000)

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
	global g_serial
	global g_DacValue
	global g_DacDir
	global g_loopFlg
	global g_DataFileName
	global cbDacCh
	global cbDacMethod
	global txtMvFrom
	global txtMvTo
	global txtMvStep
	global txtRecive
	global g_nLoopTimes
	global g_nLoopIndex
	global g_nRemainSec
	global txtRemainSec

	global g_FourPoints
	global g_FourPointsIdx

	print('Post Process')

	# current time
	time = datetime.now()
	timetext = time.strftime('%Y/%m/%d %H:%M:%S')
	csvtimetext = time.strftime('%H:%M:%S:%f')
	print(timetext)
	print(csvtimetext)

	# current value
	g_serial.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvCurrent = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcvCurrent.decode('ascii'))
	current = txtRcvCurrent[:-2]
	current = str(current, 'utf-8')
	text = current + ' mV'
	print(text)
	txtCurrent['text'] = text

	# scale value (load)
	g_serial.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcvScale = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcvScale.decode('ascii'))
	scale = txtRcvScale[:-2]
	scale = str(scale, 'utf-8')
	text = scale + ' g'
	print(text)
	txtScale['text'] = text

#	txtRecive.see('end')

	# save to csv
	writeCsvData(csvtimetext, g_nLoopIndex, g_DacValue, float(current), float(scale))

	# if none selected
	if (cbDacMethod.current() == METHOD_NONE):
		pass

	# if normal or dither selected
	elif (cbDacMethod.current() == METHOD_NORMAL or cbDacMethod.current() == METHOD_DITHER):

		# not increase
		nStep  = int(txtMvStep.get())
		if (nStep == 0):
			g_nLoopTimes -= 1

			# loop final
			if (g_nLoopTimes == 0):

				# loop end, clear file mame
				g_loopFlg		= 0
				g_DataFileName	= None

				# Remain sec
				text = str(g_nRemainSec) + ' sec'
				txtRemainSec['text'] = text

				print(text + '\r\n')

				# if normal selected
				if (cbDacMethod.current() == METHOD_NORMAL):
					DacCh = cbDacCh.get()
					SetDacValue(DacCh, 0)

				# if dither selected
				elif (cbDacMethod.current() == METHOD_DITHER):
					DitherOff()

				#
				selectMethod()

			# loop continue (start from loop top)
			else:
				g_nLoopIndex += 1

		# rise up
		elif (g_DacDir):
			# under 'To' value
			nTo = int(txtMvTo.get())
			if (g_DacValue < nTo):

				# increment dac value
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
			# over 'From' value (still continue loop)
			nFrom = int(txtMvFrom.get())
			if (g_DacValue > nFrom):

				# decrement dac value
				g_DacValue -= int(txtMvStep.get())
				print('dac : ' + str(g_DacValue) + ' mV')

			# reach at 'From' value (loop end)
			else:
				g_nLoopTimes -= 1

				# loop final
				if (g_nLoopTimes == 0):

					# loop end, clear file mame
					g_loopFlg		= 0
					g_DataFileName	= None

					# Remain sec
					text = str(g_nRemainSec) + ' sec'
					txtRemainSec['text'] = text

					print(text + '\r\n')

					# if normal selected
					if (cbDacMethod.current() == METHOD_NORMAL):
						DacCh = cbDacCh.get()
						SetDacValue(DacCh, 0)

					# if dither selected
					elif (cbDacMethod.current() == METHOD_DITHER):
						DitherOff()

					#
					selectMethod()

				# loop continue (start from loop top)
				else:
					g_DacDir	= True;
					g_DacValue	= int(txtMvFrom.get())
					g_nLoopIndex += 1

	# if 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):
		#
		g_FourPointsIdx += 1
		if (g_FourPointsIdx >= len(g_FourPoints)):
			g_FourPointsIdx = 0
			g_nLoopTimes -= 1

			# loop final
			if (g_nLoopTimes == 0):

				# loop end, clear file mame
				g_loopFlg		= 0
				g_DataFileName	= None

				DacCh = cbDacCh.get()
				SetDacValue(DacCh, 0)

				# Remain sec
				text = str(g_nRemainSec) + ' sec'
				txtRemainSec['text'] = text
				print(text + '\r\n')

				#
				selectMethod()

		# set next dac
		g_DacValue = g_FourPoints[g_FourPointsIdx]

		pass

	return True

########################################
#
ItvFuncList = [PreProcess, WaitSecond, PostProcess]
g_idxFunc = 0

########################################
#
def interval_work():
	global g_loopFlg
	global g_idxFunc
	global g_serial
	global g_DacValue
	global g_root
	global btnSequence
	global btnStop
	global g_IntervalMs

	func = ItvFuncList[g_idxFunc]
	if (func()):
		# increment func index
		g_idxFunc += 1
		if (g_idxFunc >= len(ItvFuncList)):
			g_idxFunc = 0

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

	Close_clicked()

	g_root.destroy()

########################################
#
def DAC_clicked():
	global cbDacCh
	global dacValue

	ch		= cbDacCh.get()
	value	= dacValue.get()

	SetDacValue(ch, value)

	print('dac ' + ch + ' ' + value)

########################################
#
def SCALE_clicked():
	global g_serial
	global txtScale
	global txtRecive

	g_serial.write("scale\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	text = txtRcv[:-2]
	text = str(text, 'utf-8')
	text = text + ' g'
	print(text)
	txtScale['text'] = text

########################################
#
def ZERO_clicked():
	global g_serial

	g_serial.write("scale zero\r\n".encode('shift-jis'))

########################################
#
def AMETER_clicked():
	global g_serial
	global txtCurrent
	global txtRecive

	g_serial.write("current\r\n".encode('shift-jis'))
	sleep(0.1)
	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))
	text = txtRcv[:-2]
	text = str(text, 'utf-8')
	text = text + ' mA'
	print(text)
	txtCurrent['text'] = text

########################################
#
def selectMethod():
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

	# Loop not selected
	if (idx == METHOD_NONE):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.NORMAL
		dacValue['state']		= tk.NORMAL

		txtMvCenter['state']	= tk.NORMAL
		txtLevel['state']		= tk.NORMAL
		txtFreq['state']		= tk.NORMAL

		txtMvStep['state']		= tk.DISABLED
		btnSequence['state']	= tk.DISABLED
		txtWaitMs['state']		= tk.DISABLED
		txtMvFrom['state']		= tk.DISABLED
		txtMvTo['state']		= tk.DISABLED
		txtLoopTimes['state']	= tk.DISABLED
		txtUpBottom['state']	= tk.DISABLED	#
		txtUpTop['state']		= tk.DISABLED	#
		txtDownTop['state']		= tk.DISABLED	#
		txtDownBottom['state']	= tk.DISABLED	#

	# Normal loop selected
	elif (idx == METHOD_NORMAL):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.DISABLED
		txtFreq['state']		= tk.DISABLED

		txtMvStep['state']		= tk.NORMAL
		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.NORMAL
		txtMvTo['state']		= tk.NORMAL
		txtLoopTimes['state']	= tk.NORMAL
		txtUpBottom['state']	= tk.DISABLED
		txtUpTop['state']		= tk.DISABLED
		txtDownTop['state']		= tk.DISABLED
		txtDownBottom['state']	= tk.DISABLED

	# dither loop selected
	elif (idx == METHOD_DITHER):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.NORMAL
		txtFreq['state']		= tk.NORMAL

		txtMvStep['state']		= tk.NORMAL
		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.NORMAL
		txtMvTo['state']		= tk.NORMAL
		txtLoopTimes['state']	= tk.NORMAL
		txtUpBottom['state']	= tk.DISABLED
		txtUpTop['state']		= tk.DISABLED
		txtDownTop['state']		= tk.DISABLED
		txtDownBottom['state']	= tk.DISABLED

	# 4 points loop selected
	elif (idx == METHOD_4POINTS):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.DISABLED
		txtFreq['state']		= tk.DISABLED

		txtMvStep['state']		= tk.DISABLED
		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.DISABLED
		txtMvTo['state']		= tk.DISABLED
		txtLoopTimes['state']	= tk.NORMAL
		txtUpBottom['state']	= tk.NORMAL
		txtUpTop['state']		= tk.NORMAL
		txtDownTop['state']		= tk.NORMAL
		txtDownBottom['state']	= tk.NORMAL

########################################
# Combobox Selected
def select_combo(event):

	print(event)
	selectMethod()

########################################
#
def Sequence_clicked():
	global g_loopFlg
	global g_DataFileName
	global txtRecive
	global btnSequence
	global btnStop

#	print(type(g_DataFileName))
#	print(g_DataFileName)

	#
	if (g_DataFileName == None or g_DataFileName ==""):
		File_clicked()

		if (g_DataFileName ==""):
			return

	InitProcess()

	g_loopFlg = 1 
	interval_work()

	cbDacMethod['state']	= tk.DISABLED
	cbDacCh['state']		= tk.DISABLED
	btnDac['state']			= tk.DISABLED
	dacValue['state']		= tk.DISABLED

	txtMvCenter['state']	= tk.DISABLED
	txtLevel['state']		= tk.DISABLED
	txtFreq['state']		= tk.DISABLED

	txtMvStep['state']		= tk.DISABLED
	btnSequence['state']	= tk.DISABLED
	txtWaitMs['state']		= tk.DISABLED
	txtMvFrom['state']		= tk.DISABLED
	txtMvTo['state']		= tk.DISABLED
	txtLoopTimes['state']	= tk.DISABLED
	txtUpBottom['state']	= tk.DISABLED
	txtUpTop['state']		= tk.DISABLED
	txtDownTop['state']		= tk.DISABLED
	txtDownBottom['state']	= tk.DISABLED

	btnSequence['state'] = tk.DISABLED
	btnStop['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

########################################
#
def Stop_clicked():
	global g_loopFlg
	global g_DataFileName
	global btnSequence
	global btnStop
	global cbDacMethod

	g_loopFlg = 0
	g_DataFileName = None

	# if dither selected
	if (cbDacMethod.current() == METHOD_DITHER):
		DitherOff()

	selectMethod()

	btnSequence['state'] =  tk.NORMAL
	btnStop['state'] = tk.DISABLED

########################################
#
def dither_command_text(ch, mv, level, hz):
	return 'dither ' + str(ch) + ' ' + str(mv) + ' ' + str(level) + ' ' + str(hz)

########################################
#
def DitherReflect(ch, mv, level, hz):
	global g_serial

	text = dither_command_text(ch, mv, level, hz) + '\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('dither ' + str(ch) + ' ' + str(mv) + ' ' + str(level) + ' ' + str(hz))

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

	text = 'idle start\r\n'

	g_serial.write(text.encode('shift-jis'))
	print('idle start')

	sleep(0.1)
	txtRcv = g_serial.readline()
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))

	reply = txtRcv[:-2]
	reply = str(reply, 'utf-8')
	print(reply)

########################################
#
def DitherOn_clicked():
	global btnDitherOn
	global btnDitherReflect
	global btnDitherOff

	DitherReflect_clicked()

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
#	txtRecive.insert(tk.END,txtRcv.decode('ascii'))

	reply = txtRcv[:-2]
	reply = str(reply, 'utf-8')
	print(reply)

########################################
#
def DitherOff_clicked():
	global btnDitherOn
	global btnDitherReflect
	global btnDitherOff

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
	global txtLoopTimes
	global txtRemainSec
	global txtCurrent
	global txtScale
	global txtUpBottom
	global txtUpTop
	global txtDownTop
	global txtDownBottom

	global txtRecive

	########################################
	#
	g_root = tk.Tk()
	g_root.geometry('434x450')
	g_root.title('Communicator Tool for Atom Shell Ver 1.00')

	row_idx = 0
	col_idx = 0

	########################################
	# serial com
	labelCom = tk.Label(g_root, text = ' COM : ')
	labelCom.grid(row = row_idx, column = 0, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevCom = ttk.Combobox(g_root, width = 2, values = ComChText, state = 'readonly')
	cbDevCom.current(4)
	cbDevCom.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	########################################
	# baud rate
	labelBaud = tk.Label(g_root, text = ' Baud : ')
	labelBaud.grid(row = row_idx, column = 2, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevBaud = ttk.Combobox(g_root, width = 8, values = BaudText, state = 'readonly')
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
	btnAmeter = tk.Button(master = g_root, text = 'CURRENT', command = AMETER_clicked, state = tk.DISABLED, width = 10)
	btnAmeter.grid(row = row_idx, column = 2, padx = 2, pady = 3)

	########################################
	# Dac Method
	labelMethod = tk.Label(g_root, text = 'Method : ')
	labelMethod.grid(row = row_idx, column = 3, sticky = tk.E, pady = 3)

	cbDacMethod = ttk.Combobox(g_root, width = 8, value = MethodText, state = tk.DISABLED)
	cbDacMethod.set(MethodText[0])
	cbDacMethod.grid(row = row_idx, column = 4, sticky = tk.W)
	cbDacMethod.bind('<<ComboboxSelected>>', select_combo)

	row_idx += 1

	########################################
	# Scale
	labelScale = tk.Label(g_root, text = 'Scale : ')
	labelScale.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtScale = tk.Label(g_root, text = '0 g')
	txtScale.grid(row = row_idx, column = 1, sticky = tk.W, pady = 3)

	########################################
	# Current
	labelCurrent = tk.Label(g_root, text = 'Current : ')
	labelCurrent.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtCurrent = tk.Label(g_root, text = '0 mA')
	txtCurrent.grid(row = row_idx, column = 3, sticky = tk.W, pady = 3)

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
	# Dither Off
	btnDitherOff = tk.Button(master = g_root, text = 'Dither Off', command = DitherOff_clicked, state = tk.DISABLED, width = 10)
	btnDitherOff.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	# Down Top
	labelDownTop = tk.Label(g_root, text = 'Down Top : ')
	labelDownTop.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtDownTop = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtDownTop.delete(0, tk.END)
	txtDownTop.insert(tk.END, '200')
	txtDownTop.grid(row = row_idx, column = 1, sticky = tk.W)
	txtDownTop['state'] = tk.DISABLED

	########################################
	# Up Top
	labelUpTop = tk.Label(g_root, text = 'Up Top : ')
	labelUpTop.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtUpTop = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtUpTop.delete(0, tk.END)
	txtUpTop.insert(tk.END, '220')
	txtUpTop.grid(row = row_idx, column = 3, sticky = tk.W)
	txtUpTop['state'] = tk.DISABLED

	row_idx += 1

	########################################
	# Down Bottom
	labelDownBottom = tk.Label(g_root, text = 'Down Bottom : ')
	labelDownBottom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtDownBottom = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtDownBottom.delete(0, tk.END)
	txtDownBottom.insert(tk.END, '180')
	txtDownBottom.grid(row = row_idx, column = 1, sticky = tk.W)
	txtDownBottom['state'] = tk.DISABLED

	########################################
	# Up Bottom
	labelUpBottom = tk.Label(g_root, text = 'Up Bottom : ')
	labelUpBottom.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtUpBottom = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtUpBottom.delete(0, tk.END)
	txtUpBottom.insert(tk.END, '200')
	txtUpBottom.grid(row = row_idx, column = 3, sticky = tk.W)
	txtUpBottom['state'] = tk.DISABLED

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
	# from mV
	labelMvFrom = tk.Label(g_root, text = 'mV from : ')
	labelMvFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtMvFrom = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvFrom.delete(0, tk.END)
	txtMvFrom.insert(tk.END, '100')
	txtMvFrom.grid(row = row_idx, column = 1, sticky = tk.W)
	txtMvFrom['state'] = tk.DISABLED

	########################################
	# to mV
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
	border4 = ttk.Separator(g_root, orient = 'horizontal')
	border4.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# Loop Times
	labelLoopTimes = tk.Label(g_root, text = 'Loop Times : ')
	labelLoopTimes.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtLoopTimes = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtLoopTimes.delete(0, tk.END)
	txtLoopTimes.insert(tk.END, '1')
	txtLoopTimes.grid(row = row_idx, column = 1, sticky = tk.W)
	txtLoopTimes['state'] = tk.DISABLED

	########################################
	# Remain Sec
	labelRemaimSec = tk.Label(g_root, text = 'Remain : ')
	labelRemaimSec.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtRemainSec = tk.Label(g_root, text = '0 sec')
	txtRemainSec.grid(row = row_idx, column = 3, sticky = tk.W, pady = 3)

	row_idx += 1

	########################################
	#
	#txtRecive = tkinter.scrolledtext.ScrolledText(g_root , width = 52, height = 13)
	txtRecive = tkinter.scrolledtext.ScrolledText(g_root , width = 56, height = 5)
	txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10, pady = 10)

	########################################
	#
	g_root.mainloop()

################################################################################
if __name__ == "__main__":
	main()
