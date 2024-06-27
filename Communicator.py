# COM/USB-CDC Access Sample for DMM				Ver1.00
# 対象機種はGDMシリーズ、DLシリーズです。
# 本サンプルはWindowsでのみ動作確認となります。
# WindowsがCOMポートとして認識するI/Fが利用できます。
# Linux系の場合はポート名がttyS,ttyUSB,ttyACMなどになります。
# USB-CDCの場合はボーレートは9600を指定します。
# PySerialモジュールを使用します。
# GUI表示はTkinterを使用しています。
# DMMの測定レンジがAutoの場合は測定できない場合があります。
# 測定に必要な時間をインターバルに指定してください。

# coding:utf-8
import serial		   # pyserialモジュール
import tkinter as tk	# tkモジュール
import tkinter.scrolledtext
import time

from time import sleep
from tkinter import ttk


instr = None
Baud = ['9600', '115200']
loopFlg = 0

Ch_Text = ['0', '1']

########################################
#
def Open_clicked():
	global instr

	btn1['state'] = tk.DISABLED		# Open
	btn2['state'] = tk.NORMAL		# Close
	btn3['state'] = tk.DISABLED		# Init
	btn4['state'] = tk.DISABLED		# Exit
	btnDac['state'] = tk.NORMAL		# Exit
	btn5['state'] = tk.NORMAL		# 
	btn6['state'] = tk.NORMAL		# 
	btn7['state'] = tk.NORMAL		# 
	btn8['state'] = tk.NORMAL		# 
	btn9['state'] = tk.NORMAL		# Loop
	btn10['state'] = tk.DISABLED	# Stop
	txtRecive.delete('1.0',tk.END)

	try:
		com = 'COM' + txtPort.get()
		print(type(com))
		print(com)
		baud = int(cbDevBaud.get())
		print(type(baud))
		print(baud)
#		instr = serial.Serial(com, baud, timeout = 1)
		instr = serial.Serial('COM3', 115200, timeout = 1)
		print('Serial')
		instr.port = 'COM' + txtPort.get()		#Windows COMポート指定 Device Managerで確認
		print('Port')
#		instr.port = 'ttyS'  + txtPort.get()	 #Linux 標準COMポート　dmesgで確認
#		instr.port = 'ttyUSB'  + txtPort.get()   #Linux USB変換ポート　dmesgで確認
#		instr.port = 'ttyACM'  + txtPort.get()   #Linux USB変換ポート　dmesgで確認

#		instr.baudrate = cbDevBaud.get()	 # ボーレート指定
#		instr.timeout = 0.5				 # タイムアウト指定

#		instr.open()
#		print('Open')
		instr.write("*cls\n".encode("utf-8"))
		instr.write("*idn?\n".encode("utf-8"))
		print('Write')
		sleep(0.1)
		txtRcv = instr.read(256)
		txtRecive.insert(tk.END,txtRcv.decode('ascii'))

	except:
		txtRecive.insert(tk.END,'Device Error')
		btn1['state'] = tk.NORMAL		# Open
		btn2['state'] = tk.DISABLED		# Close
		btn3['state'] = tk.DISABLED		# Init
		btn4['state'] = tk.NORMAL		# Exit
		btn5['state'] = tk.DISABLED		# 
		btn6['state'] = tk.DISABLED		# 
		btn7['state'] = tk.DISABLED		# 
		btn8['state'] = tk.DISABLED		# 
		btn9['state'] = tk.DISABLED		# Loop
		btn10['state'] = tk.DISABLED	# Stop

########################################
#
def Close_clicked():
	global instr
	instr.write("syst:loc\n".encode("utf-8"))
	btn1['state'] = tk.NORMAL		# Open
	btn2['state'] = tk.DISABLED		# Close
	btn3['state'] = tk.NORMAL		# Init
	btn4['state'] = tk.NORMAL		# Exit
	btn5['state'] = tk.DISABLED		# 
	btn6['state'] = tk.DISABLED		# 
	btn7['state'] = tk.DISABLED		# 
	btn8['state'] = tk.DISABLED		# 
	btn9['state'] = tk.DISABLED		# Loop
	btn10['state'] = tk.DISABLED	# Stop
	instr.close()

########################################
#
def interval_work():							# インターバルで行う処理を記述
	global loopFlg
	global instr
	
	instr.write("read?\n".encode("utf-8"))
	sleep(0.1)
	txtRcv = instr.read(256)
	txtRecive.insert(tk.END,time.ctime() + '   ,' + txtRcv.decode('ascii').replace('\r','')  )
	txtRecive.see('end')
	if (loopFlg == 1):
		root.after(1000, interval_work)			  # インターバルの時間(ms)を指定

########################################
#
def Init_clicked():
	pass
	
########################################
#
def Exit_clicked():

	root.destroy()

########################################
#
def Loop_clicked():
	global loopFlg
	loopFlg = 1 
	btn4['state'] = tk.DISABLED
	btn5['state'] = tk.NORMAL
	txtRecive.delete('1.0',tk.END)

	interval_work()

########################################
#
def Stop_clicked():
	global loopFlg
	loopFlg = 0
	btn4['state'] = tk.NORMAL
	btn5['state'] = tk.DISABLED


########################################
#
def DAC_clicked():
	global instr
	instr.write(":conf:volt:dc max\n".encode("utf-8"))

########################################
#
def ACV_clicked():
	global instr
	instr.write(":conf:volt:ac max\n".encode("utf-8"))

########################################
#
def DCI_clicked():
	global instr
	instr.write(":conf:curr:dc max\n".encode("utf-8"))

########################################
#
def ACI_clicked():
	global instr
	instr.write(":conf:curr:ac max\n".encode("utf-8"))

########################################
#
root = tk.Tk()
root.geometry('430x320')
root.title('Communicator Tool for Atom Shell')

row_idx = 0
col_idx = 0

########################################
#
label1 = tk.Label(root, text = 'COM Port:')
label1.grid(row = row_idx, column = 0, sticky = tk.E, pady = 3)

txtPort = ttk.Entry(root, width = 4 )
txtPort.delete(0, tk.END)
txtPort.insert(tk.END, '3')
txtPort.grid(row = row_idx, column = 1, sticky = tk.W)

########################################
#
label2 = tk.Label(root, text = ' Baud :')
label2.grid(row = row_idx, column = 2, sticky = tk.E)

cbDevBaud = ttk.Combobox(root, width = 10, value = Baud)
cbDevBaud.set(Baud[1])
cbDevBaud.grid(row = row_idx, column = 3)

row_idx += 1
########################################
# Open
btn1 = tk.Button(master = root, text = 'Open', command = Open_clicked, width = 10)
btn1.grid(row = row_idx, column = 0, pady = 3 )

########################################
# Close
btn2 = tk.Button(master = root, text = 'Close', command = Close_clicked, state = tk.DISABLED, width = 10)
btn2.grid(row = row_idx, column = 1)

########################################
# Init
btn3 = tk.Button(master = root, text = 'Init', command = Init_clicked, state = tk.DISABLED, width = 10)
btn3.grid(row = row_idx, column = 2)

########################################
# Exi
btn4 = tk.Button(master=root, text='Exit' , command = Exit_clicked, width = 10)
btn4.grid(row = row_idx, column = 4)

row_idx += 1

label_ch = tk.Label(root, text = 'Ch:')
label_ch.grid(row = row_idx, column = 0, sticky = tk.E, pady = 10)

cbDacCh = ttk.Combobox(root, width = 1, value = Ch_Text)
cbDacCh.set(Ch_Text[0])
cbDacCh.grid(row = row_idx, column = 1, sticky = tk.W)

label_dac = tk.Label(root, text = 'DAC(mV):')
label_dac.grid(row = row_idx, column = 2, sticky = tk.E, pady = 3)

dacValue = ttk.Entry(root, width = 6 )
dacValue.delete(0, tk.END)
dacValue.insert(tk.END, '3000')
dacValue.grid(row = row_idx, column = 3, sticky = tk.W)

btnDac = tk.Button(master = root, text = 'DAC', command = DAC_clicked, state = tk.DISABLED, width = 10)
btnDac.grid(row = row_idx, column = 4, pady = 3)


row_idx += 1
########################################
#
btn5 = tk.Button(master = root, text = 'DAC', command = DAC_clicked, state = tk.DISABLED, width = 10)
btn5.grid(row = row_idx, column = 0, pady = 3)

########################################
#
btn6 = tk.Button(master = root, text = 'ACV', command = ACV_clicked, state = tk.DISABLED, width = 10)
btn6.grid(row = row_idx, column = 1)

########################################
#
btn7 = tk.Button(master = root, text = 'DCI', command = DCI_clicked, state = tk.DISABLED, width = 10)
btn7.grid(row = row_idx, column = 2)

########################################
#
btn8 = tk.Button(master = root, text = 'ACI', command = ACI_clicked, state = tk.DISABLED ,width = 10)
btn8.grid(row = row_idx, column = 3)

row_idx += 1
########################################
# Loop
btn9 = tk.Button(master = root, text = 'LOOP', command = Loop_clicked, state = tk.DISABLED, width = 10)
btn9.grid(row = row_idx, column = 0, pady = 3)

########################################
# Stop
btn10 = tk.Button(master = root, text = 'STOP', command = Stop_clicked, state = tk.DISABLED, width = 10)
btn10.grid(row = row_idx, column = 1)

row_idx += 1
########################################
#
txtRecive = tkinter.scrolledtext.ScrolledText(root , width = 52, height = 13)
txtRecive.grid(row = row_idx , column = 0, columnspan = 5 ,padx = 10,pady = 10)

root.mainloop()

