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
g_DataFileName	= None
g_bOpen			= False

g_bLoopFlg		= False

########################################
#	pre-process
#	wait second
#	post-process
#
g_IntervalMs	= int(100)	# 100 ms
g_WaitMs		= 0
g_WaitItvMs		= 0
g_LoopDir		= True		# true:increase
g_LoopValue		= 0

g_From			= 0
g_To			= 0
g_Step			= 0
g_Times			= 0

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
ComChText	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
BaudText	= ['9600', '115200']
DacChText	= ['0', '1']
PwmChText	= ['0', '1', '2']
PwmMoveText	= ['CW', 'CCW', 'STOP', 'BRAKE', 'STAND BY']

MethodText	= ['-', 'Normal Dac', 'Dither Dac', '4 points', 'PWM Dac']		# cbDacMethod
METHOD_NONE		= 0
METHOD_NORMAL	= 1
METHOD_DITHER	= 2
METHOD_4POINTS	= 3
METHOD_PWM		= 4

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
def SetDacValue(ch, value):
	global g_serial

	dac_text = dac_command_text(ch, value) + '\r\n'
	g_serial.write(dac_text.encode('shift-jis'))
	text = dac_text[:-2]
	print(text)

########################################
#
def SetPwmValue(ch, duty):
	global g_serial

	pwm_text	= 'pwm ' + str(ch) + ' ' + str(duty) + '\r\n'
	g_serial.write(pwm_text.encode('shift-jis'))
	text = pwm_text[:-2]
	print(text)

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
	global cbPwmCh
	global dutyValue
	global btnDuty
	global btnDutyCw
	global btnDutyCcw
	global btnDutyStop
	global btnDutyBrake
	global btnDutyStandby
	global txtPwmStep
	global cbPwmMove
	global txtPwmFrom
	global txtPwmTo

	btnOpen['state']			= tk.DISABLED	# Open
	btnClose['state']			= tk.NORMAL		# Close
	btnFile['state']			= tk.NORMAL		#
	btnInit['state']			= tk.NORMAL		# Init
	btnExit['state']			= tk.NORMAL		# Exit
	btnScale['state']			= tk.NORMAL		# 
	btnScaleZero['state']		= tk.NORMAL		# 
	cbDacMethod['state']		= 'readonly'	#
	btnAmeter['state']			= tk.NORMAL		# 
	cbDacCh['state']			= 'readonly'	# 
	dacValue['state']			= tk.NORMAL		# 
	btnDac['state']				= tk.NORMAL		# Dac

	cbPwmCh['state']			= 'readonly'	# 
	dutyValue['state']			= tk.NORMAL		#
	btnDuty['state']			= tk.NORMAL		#
	btnDutyCw['state']			= tk.NORMAL		#
	btnDutyCcw['state']			= tk.NORMAL		#
	btnDutyStop['state']		= tk.NORMAL		#
	btnDutyBrake['state']		= tk.NORMAL		#
	btnDutyStandby['state']		= tk.NORMAL		#

	btnDitherReflect['state']	= tk.DISABLED	#
	btnDitherOn['state']		= tk.NORMAL		#
	btnDitherOff['state']		= tk.DISABLED	#
	btnSequence['state']		= tk.DISABLED	#
	btnStop['state']			= tk.DISABLED	# Stop
	txtMvStep['state']			= tk.DISABLED	# 
	txtWaitMs['state']			= tk.DISABLED	#
	txtMvFrom['state']			= tk.DISABLED	# 
	txtMvTo['state']			= tk.DISABLED	# 
	txtMvCenter['state']		= tk.NORMAL		# 
	txtLevel['state']			= tk.NORMAL		# 
	txtFreq['state']			= tk.NORMAL		# 
	txtLoopTimes['state']		= tk.DISABLED	#
	txtUpBottom['state']		= tk.DISABLED	#
	txtUpTop['state']			= tk.DISABLED	#
	txtDownTop['state']			= tk.DISABLED	#
	txtDownBottom['state']		= tk.DISABLED	#
	txtPwmStep['state']			= tk.DISABLED	#
	cbPwmMove['state']			= tk.DISABLED	#
	txtPwmFrom['state']			= tk.DISABLED	#
	txtPwmTo['state']			= tk.DISABLED	#
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
	global cbPwmCh
	global dutyValue
	global btnDuty
	global btnDutyCw
	global btnDutyCcw
	global btnDutyStop
	global btnDutyBrake
	global btnDutyStandby
	global txtPwmStep
	global cbPwmMove
	global txtPwmFrom
	global txtPwmTo

	btnOpen['state']			= tk.NORMAL		# Open
	btnClose['state']			= tk.DISABLED	# Close
	btnFile['state']			= tk.DISABLED	#
	btnInit['state']			= tk.DISABLED	# Init
	btnExit['state']			= tk.NORMAL		# Exit
	cbDacCh['state']			= tk.DISABLED	# 
	dacValue['state']			= tk.DISABLED	# 
	btnDac['state']				= tk.DISABLED	# Dac

	cbPwmCh['state']			= 'readonly'	# 
	dutyValue['state']			= tk.DISABLED	#
	btnDuty['state']			= tk.DISABLED	#
	btnDutyCw['state']			= tk.DISABLED	#
	btnDutyCcw['state']			= tk.DISABLED	#
	btnDutyStop['state']		= tk.DISABLED	#
	btnDutyBrake['state']		= tk.DISABLED	#
	btnDutyStandby['state']		= tk.DISABLED	#

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
	txtPwmStep['state']			= tk.DISABLED	#
	cbPwmMove['state']			= tk.DISABLED	#
	txtPwmFrom['state']			= tk.DISABLED	#
	txtPwmTo['state']			= tk.DISABLED	#
	txtRecive['state']			= tk.DISABLED	#

########################################
#
def Open_clicked():
	global g_serial
	global g_bOpen
	global cbDevCom
	global cbDevBaud
	global txtRecive

	try:
		com = 'COM' + cbDevCom.get()
		baud = int(cbDevBaud.get())

		print('connecting ...', com, baud)
		g_serial = serial.Serial(com, baud, timeout = 0.5)
		print('connecting succeeded.')
		txtRecive.delete('1.0',tk.END)
		txtRecive.insert(tk.END,'Connected\r\n')
		g_bOpen = True

		for i in range(50):
			sleep(0.1)
			txtRcv = g_serial.readline()
			if(len(txtRcv) == 0):
				break
			text = txtRcv[:-2]
			print(text)

		EnableWidget()

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

	# pwm selected
	elif (cbDacMethod.current() == METHOD_PWM):
		iniFile = 'pwm_' + timetext + '.csv'

	#
	file_name = tk.filedialog.asksaveasfilename(filetypes = fTyp, initialdir = iniDir, initialfile = iniFile, defaultextension = 'csv')
	g_DataFileName = file_name

	# csv header text
	if (g_DataFileName != ''):
		writeCsvData('Time', 'Index', 'Dac', 'Current', 'Load')

########################################
#
def InitProcess():
	global g_From
	global g_To
	global g_Step
	global g_Times
	global g_WaitMs

	global g_LoopCh
	global g_LoopDir
	global g_LoopValue
	global g_DitherCh
	global g_DitherLevel
	global g_DitherHz
	global cbDacCh
	global cbPwmCh
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
	g_From  = 0
	g_To    = 0
	g_Step  = 0
	g_Times = 0

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
		g_From  = int(txtMvFrom.get())
		g_To    = int(txtMvTo.get())
		g_Step  = int(txtMvStep.get())
		g_Times = 0

		g_LoopCh	= int(cbDacCh.get())
		g_LoopDir	= True
		g_LoopValue	= g_From
		g_WaitMs	= int(txtWaitMs.get())

		if (g_Step > 0):
			g_Times = int(((g_To - g_From) / g_Step) * 2 * g_nLoopTimes + g_nLoopTimes)	# rising and falling
		else:
			g_Times = g_nLoopTimes

	# if dither selected
	elif (cbDacMethod.current() == METHOD_DITHER):
		g_From  = int(txtMvFrom.get())
		g_To    = int(txtMvTo.get())
		g_Step  = int(txtMvStep.get())
		g_Times = 0

		g_LoopCh		= int(cbDacCh.get())
		g_LoopDir		= True
		g_LoopValue		= g_From
		g_WaitMs		= int(txtWaitMs.get())
		g_DitherCh		= int(cbDacCh.get())
		g_DitherLevel	= int(txtLevel.get())
		g_DitherHz		= int(txtFreq.get())

		if (g_Step > 0):
			g_Times = int(((g_To - g_From) / g_Step) * 2 * g_nLoopTimes + g_nLoopTimes)	# rising and falling
		else:
			g_Times = g_nLoopTimes

		DitherReflect(g_LoopCh, g_LoopValue, g_DitherLevel, g_DitherHz)
		DitherOn()

	# if 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):
		pt1 = int(txtUpBottom.get())
		pt2 = int(txtUpTop.get())
		pt3 = int(txtDownTop.get())
		pt4 = int(txtDownTop.get())
		g_FourPoints = [pt1, pt2, pt3, pt4]
		g_FourPointsIdx = 0		# 0 to len(g_FourPoints) - 1
		g_LoopValue		= g_FourPoints[g_FourPointsIdx]
		g_WaitMs		= int(txtWaitMs.get())

		g_Times = g_nLoopTimes * len(g_FourPoints)

	# if pwm selected
	elif (cbDacMethod.current() == METHOD_PWM):
		g_From  = int(txtPwmFrom.get())
		g_To    = int(txtPwmTo.get())
		g_Step  = int(txtPwmStep.get())
		g_Times = 0

		g_LoopCh	= int(cbPwmCh.get())
		g_LoopDir	= True
		g_LoopValue	= g_From
		g_WaitMs	= int(txtWaitMs.get())

		if (g_Step > 0):
			g_Times = int(((g_To - g_From) / g_Step) * 2 * g_nLoopTimes + g_nLoopTimes)	# rising and falling
		else:
			g_Times = g_nLoopTimes

	#
	nTotalWaitMs = int(g_Times * g_WaitMs)
	text = 'Times : ' + str(g_Times) + '\r\n'
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
	global g_LoopCh
	global g_LoopValue
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
		SetDacValue(g_LoopCh, g_LoopValue)

	# if dither selected
	elif (cbDacMethod.current() == METHOD_DITHER):

		DitherReflect(g_LoopCh, g_LoopValue, g_DitherLevel, g_DitherHz)

	# if 4 points selected
	elif (cbDacMethod.current() == METHOD_4POINTS):

		# set value
		#
		SetDacValue(g_LoopCh, g_LoopValue)

	# if pwm selected
	elif (cbDacMethod.current() == METHOD_PWM):

		# set value
		#
		SetPwmValue(g_LoopCh, g_LoopValue)

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
def getScaleVakue():
	global g_serial
	global txtRecive

	bError = True
	while (bError == True):
		g_serial.write("scale\r\n".encode('shift-jis'))
		sleep(0.1)
		txtRcv = g_serial.readline()
		txtRecive.insert(tk.END,txtRcv.decode('ascii'))
		text = txtRcv[:-2]
		text = str(text, 'utf-8')
		if (text != '-nan'):
			bError = False

	return text

########################################
#
def PostProcess():
	global g_serial

	global g_From
	global g_To
	global g_Step
	global g_Times
	global g_WaitMs

	global g_LoopCh
	global g_LoopDir
	global g_LoopValue
	global g_bLoopFlg
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
	current = txtRcvCurrent[:-2]
	current = str(current, 'utf-8')
	text = current + ' mV'
	print(text)
	txtCurrent['text'] = text

	# scale value (load)
	scale = getScaleVakue()

	text = scale + ' g'
	print(text)
	txtScale['text'] = text

	# save to csv
	writeCsvData(csvtimetext, g_nLoopIndex, g_LoopValue, float(current), float(scale))

	# if none selected
	if (cbDacMethod.current() == METHOD_NONE):
		pass

	# if normal or dither selected
	elif (cbDacMethod.current() == METHOD_NORMAL or cbDacMethod.current() == METHOD_DITHER or METHOD_PWM):

		# not increase
		if (g_Step == 0):
			g_nLoopTimes -= 1

			# loop final
			if (g_nLoopTimes == 0):

				# loop end, clear file mame
				g_bLoopFlg		= False
				g_DataFileName	= None

				# Remain sec
				text = str(g_nRemainSec) + ' sec'
				txtRemainSec['text'] = text

				print(text + '\r\n')

				# if normal selected
				if (cbDacMethod.current() == METHOD_NORMAL):
					SetDacValue(g_LoopCh, 0)

				# if dither selected
				elif (cbDacMethod.current() == METHOD_DITHER):
					DitherOff()

				# if pwm selected
				elif (cbDacMethod.current() == METHOD_PWM):
					SetPwmValue(g_LoopCh, 0)
					# STOP Action needed

				#
				selectMethod()

			# loop continue (start from loop top)
			else:
				g_nLoopIndex += 1

		# rise up
		elif (g_LoopDir):
			# under 'To' value
			if (g_LoopValue < g_To):

				# increment dac value
				g_LoopValue += g_Step
				print('value : ' + str(g_LoopValue) + ' mV')

				# arrive at top
				if (g_LoopValue == g_To):
					if (g_LoopDir):
						g_LoopDir = False

			# reach at top
			else:
				if (g_LoopDir):
					g_LoopDir = False

		# fall down
		else:
			# over 'From' value (still continue loop)
			if (g_LoopValue > g_From):

				# decrement dac value
				g_LoopValue -= g_Step
				print('value : ' + str(g_LoopValue) + ' mV')

			# reach at 'From' value (loop end)
			else:
				g_nLoopTimes -= 1

				# loop final
				if (g_nLoopTimes == 0):

					# loop end, clear file mame
					g_bLoopFlg		= False
					g_DataFileName	= None

					# Remain sec
					text = str(g_nRemainSec) + ' sec'
					txtRemainSec['text'] = text

					print(text + '\r\n')

					# if normal selected
					if (cbDacMethod.current() == METHOD_NORMAL):
						SetDacValue(g_LoopCh, 0)

					# if dither selected
					elif (cbDacMethod.current() == METHOD_DITHER):
						DitherOff()

					# if pwm selected
					elif (cbDacMethod.current() == METHOD_PWM):
						SetPwmValue(g_LoopCh, 0)
						# STOP Action needed

					#
					selectMethod()

				# loop continue (start from loop top)
				else:
					g_LoopDir	= True;
					g_LoopValue	= g_From
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
				g_bLoopFlg		= False
				g_DataFileName	= None

				SetDacValue(g_LoopCh, 0)

				# Remain sec
				text = str(g_nRemainSec) + ' sec'
				txtRemainSec['text'] = text
				print(text + '\r\n')

				#
				selectMethod()

		# set next dac
		g_LoopValue = g_FourPoints[g_FourPointsIdx]


	# if normal or dither selected
	elif (cbDacMethod.current() == METHOD_NORMAL or cbDacMethod.current() == METHOD_DITHER):

		# not increase
		if (g_Step == 0):
			g_nLoopTimes -= 1

			# loop final
			if (g_nLoopTimes == 0):

				# loop end, clear file mame
				g_bLoopFlg		= False
				g_DataFileName	= None

				# Remain sec
				text = str(g_nRemainSec) + ' sec'
				txtRemainSec['text'] = text

				print(text + '\r\n')

				# if normal selected
				if (cbDacMethod.current() == METHOD_NORMAL):
					SetDacValue(g_LoopCh, 0)

				# if dither selected
				elif (cbDacMethod.current() == METHOD_DITHER):
					DitherOff()

				# if pwm selected
				elif (cbDacMethod.current() == METHOD_PWM):
					SetPwmValue(g_LoopCh, 0)
					# STOP Action needed

				#
				selectMethod()

			# loop continue (start from loop top)
			else:
				g_nLoopIndex += 1

		# rise up
		elif (g_LoopDir):
			# under 'To' value
			if (g_LoopValue < g_To):

				# increment dac value
				g_LoopValue += g_Step
				print('value : ' + str(g_LoopValue) + ' mV')

				# arrive at top
				if (g_LoopValue == g_To):
					if (g_LoopDir):
						g_LoopDir = False

			# reach at top
			else:
				if (g_LoopDir):
					g_LoopDir = False

		# fall down
		else:
			# over 'From' value (still continue loop)
			if (g_LoopValue > g_From):

				# decrement dac value
				g_LoopValue -= g_Step
				print('value : ' + str(g_LoopValue) + ' mV')

			# reach at 'From' value (loop end)
			else:
				g_nLoopTimes -= 1

				# loop final
				if (g_nLoopTimes == 0):

					# loop end, clear file mame
					g_bLoopFlg		= False
					g_DataFileName	= None

					# Remain sec
					text = str(g_nRemainSec) + ' sec'
					txtRemainSec['text'] = text

					print(text + '\r\n')

					# if normal selected
					if (cbDacMethod.current() == METHOD_NORMAL):
						SetDacValue(g_LoopCh, 0)

					# if dither selected
					elif (cbDacMethod.current() == METHOD_DITHER):
						DitherOff()

					# if pwm selected
					elif (cbDacMethod.current() == METHOD_PWM):
						SetPwmValue(g_LoopCh, 0)
						# STOP Action needed

					#
					selectMethod()

				# loop continue (start from loop top)
				else:
					g_LoopDir	= True
					g_LoopValue	= g_From
					g_nLoopIndex += 1

	return True

########################################
#
ItvFuncList = [PreProcess, WaitSecond, PostProcess]
g_idxFunc = 0

########################################
#
def interval_work():
	global g_bLoopFlg
	global g_idxFunc
	global g_serial
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

	if (g_bLoopFlg == True):
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
def PwmDuty_clicked():
	global g_serial
	global cbPwmCh
	global dutyValue

	ch			= cbPwmCh.get()
	duty		= int(dutyValue.get())

	SetPwmValue(ch, duty)

########################################
#
def PwmCw_clicked():
	global g_serial

	g_serial.write("pwm cw\r\n".encode('shift-jis'))
	print('pwm cw')

########################################
#
def PwmCcw_clicked():
	global g_serial

	g_serial.write("pwm ccw\r\n".encode('shift-jis'))
	print('pwm ccw')

########################################
#
def PwmStop_clicked():
	global g_serial

	g_serial.write("pwm stop\r\n".encode('shift-jis'))
	print('pwm stop')

########################################
#
def PwmBrake_clicked():
	global g_serial

	g_serial.write("pwm brake\r\n".encode('shift-jis'))
	print('pwm brake')

########################################
#
def PwmStandby_clicked():
	global g_serial

	g_serial.write("pwm standby\r\n".encode('shift-jis'))
	print('pwm standby')

########################################
#
def SCALE_clicked():
	global txtScale

	text = getScaleVakue()

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

	global cbPwmCh
	global dutyValue
	global btnDuty
	global btnDutyCw
	global btnDutyCcw
	global btnDutyStop
	global btnDutyBrake
	global btnDutyStandby

	global txtMvCenter
	global txtLevel
	global txtFreq
	global cbDacMethod
	global txtMvStep
	global btnSequence
	global txtWaitMs
	global txtMvFrom
	global txtMvTo
	global txtPwmStep
	global cbPwmMove
	global txtPwmFrom
	global txtPwmTo

	idx = cbDacMethod.current()

	# Loop not selected
	if (idx == METHOD_NONE):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.NORMAL
		dacValue['state']		= tk.NORMAL

		cbPwmCh['state']		= tk.NORMAL		# 
		dutyValue['state']		= tk.NORMAL		#
		btnDuty['state']		= tk.NORMAL		#
		btnDutyCw['state']		= tk.NORMAL		#
		btnDutyCcw['state']		= tk.NORMAL		#
		btnDutyStop['state']	= tk.NORMAL		#
		btnDutyBrake['state']	= tk.NORMAL		#
		btnDutyStandby['state']	= tk.NORMAL		#

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
		txtPwmStep['state']		= tk.DISABLED
		cbPwmMove['state']		= tk.DISABLED
		txtPwmFrom['state']		= tk.DISABLED
		txtPwmTo['state']		= tk.DISABLED

	# Normal loop selected
	elif (idx == METHOD_NORMAL):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		cbPwmCh['state']		= tk.NORMAL
		dutyValue['state']		= tk.DISABLED
		btnDuty['state']		= tk.DISABLED
		btnDutyCw['state']		= tk.DISABLED
		btnDutyCcw['state']		= tk.DISABLED
		btnDutyStop['state']	= tk.DISABLED
		btnDutyBrake['state']	= tk.DISABLED
		btnDutyStandby['state']	= tk.DISABLED

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
		txtPwmStep['state']		= tk.DISABLED
		cbPwmMove['state']		= tk.DISABLED
		txtPwmFrom['state']		= tk.DISABLED
		txtPwmTo['state']		= tk.DISABLED

	# dither loop selected
	elif (idx == METHOD_DITHER):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		cbPwmCh['state']		= tk.NORMAL
		dutyValue['state']		= tk.DISABLED
		btnDuty['state']		= tk.DISABLED
		btnDutyCw['state']		= tk.DISABLED
		btnDutyCcw['state']		= tk.DISABLED
		btnDutyStop['state']	= tk.DISABLED
		btnDutyBrake['state']	= tk.DISABLED
		btnDutyStandby['state']	= tk.DISABLED

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
		txtPwmStep['state']		= tk.DISABLED
		cbPwmMove['state']		= tk.DISABLED
		txtPwmFrom['state']		= tk.DISABLED
		txtPwmTo['state']		= tk.DISABLED

	# 4 points loop selected
	elif (idx == METHOD_4POINTS):

		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		cbPwmCh['state']		= tk.NORMAL
		dutyValue['state']		= tk.DISABLED
		btnDuty['state']		= tk.DISABLED
		btnDutyCw['state']		= tk.DISABLED
		btnDutyCcw['state']		= tk.DISABLED
		btnDutyStop['state']	= tk.DISABLED
		btnDutyBrake['state']	= tk.DISABLED
		btnDutyStandby['state']	= tk.DISABLED

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
		txtPwmStep['state']		= tk.DISABLED
		cbPwmMove['state']		= tk.DISABLED
		txtPwmFrom['state']		= tk.DISABLED
		txtPwmTo['state']		= tk.DISABLED

	# pwm loop selected
	elif (idx == METHOD_PWM):
		cbDacMethod['state']	= tk.NORMAL
		cbDacCh['state']		= tk.NORMAL
		btnDac['state']			= tk.DISABLED
		dacValue['state']		= tk.DISABLED

		cbPwmCh['state']		= tk.NORMAL
		dutyValue['state']		= tk.DISABLED
		btnDuty['state']		= tk.DISABLED
		btnDutyCw['state']		= tk.DISABLED
		btnDutyCcw['state']		= tk.DISABLED
		btnDutyStop['state']	= tk.DISABLED
		btnDutyBrake['state']	= tk.DISABLED
		btnDutyStandby['state']	= tk.DISABLED

		txtMvCenter['state']	= tk.DISABLED
		txtLevel['state']		= tk.DISABLED
		txtFreq['state']		= tk.DISABLED

		txtMvStep['state']		= tk.DISABLED
		btnSequence['state']	= tk.NORMAL
		txtWaitMs['state']		= tk.NORMAL
		txtMvFrom['state']		= tk.DISABLED
		txtMvTo['state']		= tk.DISABLED
		txtLoopTimes['state']	= tk.NORMAL
		txtUpBottom['state']	= tk.DISABLED
		txtUpTop['state']		= tk.DISABLED
		txtDownTop['state']		= tk.DISABLED
		txtDownBottom['state']	= tk.DISABLED
		txtPwmStep['state']		= tk.NORMAL
		cbPwmMove['state']		= 'readonly'
		txtPwmFrom['state']		= tk.NORMAL
		txtPwmTo['state']		= tk.NORMAL
		pass

########################################
# Combobox Selected
def select_combo(event):

	print(event)
	selectMethod()

########################################
#
def Sequence_clicked():
	global g_bLoopFlg
	global g_DataFileName
	global txtRecive
	global btnSequence
	global btnStop
	global cbPwmCh

#	print(type(g_DataFileName))
#	print(g_DataFileName)

	#
	if (g_DataFileName == None or g_DataFileName ==""):
		File_clicked()

		if (g_DataFileName ==""):
			return

	InitProcess()

	g_bLoopFlg = True
	interval_work()

	cbDacMethod['state']	= tk.DISABLED
	cbDacCh['state']		= tk.DISABLED
	btnDac['state']			= tk.DISABLED
	dacValue['state']		= tk.DISABLED

	cbPwmCh['state']		= tk.DISABLED

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

	btnSequence['state']	= tk.DISABLED
	btnStop['state']		= tk.NORMAL
	txtRecive.delete('1.0',tk.END)

########################################
#
def Stop_clicked():
	global g_bLoopFlg
	global g_DataFileName
	global btnSequence
	global btnStop
	global cbDacMethod
	global cbPwmCh

	g_bLoopFlg		= False
	g_DataFileName	= None

	# if dither selected
	if (cbDacMethod.current() == METHOD_DITHER):
		DitherOff()

	selectMethod()

	btnSequence['state']	= tk.NORMAL
	btnStop['state']		= tk.DISABLED
	cbPwmCh['state']		= tk.NORMAL

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

	btnDitherOn['state']		= tk.DISABLED	#
	btnDitherReflect['state']	= tk.NORMAL		#
	btnDitherOff['state']		= tk.NORMAL		#

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
	global cbPwmCh
	global dutyValue
	global btnDuty
	global btnDutyCw
	global btnDutyCcw
	global btnDutyStop
	global btnDutyBrake
	global btnDutyStandby
	global txtPwmStep
	global cbPwmMove
	global txtPwmFrom
	global txtPwmTo

	global txtRecive

	########################################
	#
	g_root = tk.Tk()
	g_root.geometry('456x580')
	g_root.title('Communicator Tool for Atom Shell')

	row_idx = 0
	col_idx = 0

	########################################
	# serial com
	labelCom = tk.Label(g_root, text = ' COM : ')
	labelCom.grid(row = row_idx, column = 0, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevCom = ttk.Combobox(g_root, width = 2, values = ComChText, state = 'readonly')
	cbDevCom.current(4)
	cbDevCom.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	#---------------------------------------
	# baud rate
	labelBaud = tk.Label(g_root, text = ' Baud : ')
	labelBaud.grid(row = row_idx, column = 2, padx = 2, pady = 3)#, sticky = tk.E)

	cbDevBaud = ttk.Combobox(g_root, width = 8, values = BaudText, state = 'readonly')
	cbDevBaud.current(1)
	cbDevBaud.grid(row = row_idx, column = 3, padx = 2, pady = 3 )

	row_idx += 1

	#---------------------------------------
	# Open
	btnOpen = tk.Button(master = g_root, text = 'Open', command = Open_clicked, width = 10)
	btnOpen.grid(row = row_idx, column = 0, padx = 2, pady = 3)

	#---------------------------------------
	# Close
	btnClose = tk.Button(master = g_root, text = 'Close', command = Close_clicked, state = tk.DISABLED, width = 10)
	btnClose.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	#---------------------------------------
	# File
	btnFile = tk.Button(master = g_root, text = 'File', command = File_clicked, state = tk.NORMAL, width = 10)
	btnFile.grid(row = row_idx, column = 2, padx = 2, pady = 3)

	#---------------------------------------
	# Init
	btnInit = tk.Button(master = g_root, text = 'Init', command = Init_clicked, state = tk.DISABLED, width = 10)
	btnInit.grid(row = row_idx, column = 3, padx = 2, pady = 3)

	#---------------------------------------
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

	#---------------------------------------
	# scale zero
	btnScaleZero = tk.Button(master = g_root, text = 'ZERO', command = ZERO_clicked, state = tk.DISABLED, width = 10)
	btnScaleZero.grid(row = row_idx, column = 1, padx = 2, pady = 3)

	#---------------------------------------
	# ameter
	btnAmeter = tk.Button(master = g_root, text = 'CURRENT', command = AMETER_clicked, state = tk.DISABLED, width = 10)
	btnAmeter.grid(row = row_idx, column = 2, padx = 2, pady = 3)

	#---------------------------------------
	# Dac Method
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

	#---------------------------------------
	# Dac Value
	label_dac = tk.Label(g_root, text = 'Dac(mV) : ')
	label_dac.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	dacValue = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	dacValue.delete(0, tk.END)
	dacValue.insert(tk.END, '1000')
	dacValue.grid(row = row_idx, column = 3, sticky = tk.W)
	dacValue['state'] = tk.DISABLED

	#---------------------------------------
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
	# Pwm Ch
	labelPwmCh = tk.Label(g_root, text = 'Pwm Ch : ')
	labelPwmCh.grid(row = row_idx, column = 0, sticky = tk.E, pady = 10)

	cbPwmCh = ttk.Combobox(g_root, width = 1, value = PwmChText, state = tk.DISABLED)
	cbPwmCh.set(PwmChText[2])
	cbPwmCh.grid(row = row_idx, column = 1, sticky = tk.W)

	#---------------------------------------
	# Pwm Duty
	label_duty = tk.Label(g_root, text = 'Pwm Duty(0 - 255) : ')
	label_duty.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	dutyValue = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	dutyValue.delete(0, tk.END)
	dutyValue.insert(tk.END, '0')
	dutyValue.grid(row = row_idx, column = 3, sticky = tk.W)
	dutyValue['state'] = tk.DISABLED

	#---------------------------------------
	# Pwm Duty button
	btnDuty = tk.Button(master = g_root, text = 'Duty', command = PwmDuty_clicked, state = tk.DISABLED, width = 10)
	btnDuty.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	# CW Duty button
	btnDutyCw = tk.Button(master = g_root, text = 'CW', command = PwmCw_clicked, state = tk.DISABLED, width = 10)
	btnDutyCw.grid(row = row_idx, column = 0, pady = 3)

	#---------------------------------------
	# CCW Duty button
	btnDutyCcw = tk.Button(master = g_root, text = 'CCW', command = PwmCcw_clicked, state = tk.DISABLED, width = 10)
	btnDutyCcw.grid(row = row_idx, column = 1, pady = 3)

	#---------------------------------------
	# STOP Duty button
	btnDutyStop = tk.Button(master = g_root, text = 'STOP', command = PwmStop_clicked, state = tk.DISABLED, width = 10)
	btnDutyStop.grid(row = row_idx, column = 2, pady = 3)

	#---------------------------------------
	# BRAKE Duty button
	btnDutyBrake = tk.Button(master = g_root, text = 'BRAKE', command = PwmBrake_clicked, state = tk.DISABLED, width = 10)
	btnDutyBrake.grid(row = row_idx, column = 3, pady = 3)

	#---------------------------------------
	# STANDBY Duty button
	btnDutyStandby = tk.Button(master = g_root, text = 'STANDBY', command = PwmStandby_clicked, state = tk.DISABLED, width = 10)
	btnDutyStandby.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	#
	border3 = ttk.Separator(g_root, orient = 'horizontal')
	border3.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
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

	#---------------------------------------
	# Reflect
	btnDitherReflect = tk.Button(master = g_root, text = 'Reflect', command = DitherReflect_clicked, state = tk.DISABLED, width = 10)
	btnDitherReflect.grid(row = row_idx, column = 3, pady = 3)

	#---------------------------------------
	# Dither On
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

	#---------------------------------------
	# Frequency
	labelFreq = tk.Label(g_root, text = 'Frequency (Hz) : ')
	labelFreq.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtFreq = ttk.Entry(g_root, width = 8, state = tk.NORMAL)
	txtFreq.delete(0, tk.END)
	txtFreq.insert(tk.END, '200')
	txtFreq.grid(row = row_idx, column = 3, sticky = tk.W)
	txtFreq['state'] = tk.DISABLED

	#---------------------------------------
	# Dither Off
	btnDitherOff = tk.Button(master = g_root, text = 'Dither Off', command = DitherOff_clicked, state = tk.DISABLED, width = 10)
	btnDitherOff.grid(row = row_idx, column = 4, pady = 3)

	row_idx += 1

	########################################
	#
	border4 = ttk.Separator(g_root, orient = 'horizontal')
	border4.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
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

	#---------------------------------------
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

	#---------------------------------------
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
	border5 = ttk.Separator(g_root, orient = 'horizontal')
	border5.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
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

	#---------------------------------------
	# wait ms
	labelWaitMs = tk.Label(g_root, text = 'Wait ms : ')
	labelWaitMs.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtWaitMs = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtWaitMs.delete(0, tk.END)
	txtWaitMs.insert(tk.END, '1000')
	txtWaitMs.grid(row = row_idx, column = 3, sticky = tk.W)
	txtWaitMs['state'] = tk.DISABLED

	#---------------------------------------
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

	#---------------------------------------
	# to mV
	labelMvTo = tk.Label(g_root, text = 'mV to : ')
	labelMvTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtMvTo = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtMvTo.delete(0, tk.END)
	txtMvTo.insert(tk.END, '300')
	txtMvTo.grid(row = row_idx, column = 3, sticky = tk.W)
	txtMvTo['state'] = tk.DISABLED

	#---------------------------------------
	# Stop
	btnStop = tk.Button(master = g_root, text = 'STOP', command = Stop_clicked, state = tk.DISABLED, width = 10)
	btnStop.grid(row = row_idx, column = 4)

	row_idx += 1

	########################################
	#
	border6 = ttk.Separator(g_root, orient = 'horizontal')
	border6.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# pwm step
	labelPwmStep = tk.Label(g_root, text = 'PWM Step : ')
	labelPwmStep.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtPwmStep = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtPwmStep.delete(0, tk.END)
	txtPwmStep.insert(tk.END, '2')
	txtPwmStep.grid(row = row_idx, column = 1, sticky = tk.W)
	txtPwmStep['state'] = tk.DISABLED

	#---------------------------------------
	# Pwm Move
	labelPwmMove = tk.Label(g_root, text = 'Pwm Move : ')
	labelPwmMove.grid(row = row_idx, column = 2, sticky = tk.E, pady = 10)

	cbPwmMove = ttk.Combobox(g_root, width = 6, value = PwmMoveText, state = tk.DISABLED)
	cbPwmMove.set(PwmMoveText[2])
	cbPwmMove.grid(row = row_idx, column = 3, sticky = tk.W)

	row_idx += 1

	########################################
	# from pwm
	labelPwmFrom = tk.Label(g_root, text = 'PWM from : ')
	labelPwmFrom.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtPwmFrom = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtPwmFrom.delete(0, tk.END)
	txtPwmFrom.insert(tk.END, '100')
	txtPwmFrom.grid(row = row_idx, column = 1, sticky = tk.W)
	txtPwmFrom['state'] = tk.DISABLED

	#---------------------------------------
	# to pwm
	labelPwmTo = tk.Label(g_root, text = 'PWM to : ')
	labelPwmTo.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtPwmTo = ttk.Entry(g_root, width = 6, state = tk.NORMAL)
	txtPwmTo.delete(0, tk.END)
	txtPwmTo.insert(tk.END, '300')
	txtPwmTo.grid(row = row_idx, column = 3, sticky = tk.W)
	txtPwmTo['state'] = tk.DISABLED

	row_idx += 1

	########################################
	#
	border7 = ttk.Separator(g_root, orient = 'horizontal')
	border7.grid(row = row_idx, column = 2, pady = 3, sticky = 'ew')
	row_idx += 1

	########################################
	# Scale
	labelScale = tk.Label(g_root, text = 'Scale : ')
	labelScale.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

	txtScale = tk.Label(g_root, text = '0 g')
	txtScale.grid(row = row_idx, column = 1, sticky = tk.W, pady = 3)

	#---------------------------------------
	# Current
	labelCurrent = tk.Label(g_root, text = 'Current : ')
	labelCurrent.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

	txtCurrent = tk.Label(g_root, text = '0 mA')
	txtCurrent.grid(row = row_idx, column = 3, sticky = tk.W, pady = 3)

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

	#---------------------------------------
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
