from tkinter import*
import tkinter.font
from smbus import SMBus
from gpiozero import LED
import time
import board
import adafruit_dht
from threading import Thread
import RPi.GPIO 
RPi.GPIO.setmode(RPi.GPIO.BCM)


#Setting up the temperature sensor
temp_sensor_reading = adafruit_dht.DHT11(board.D18) #D18

#Assigning variables:
UV_light_LED = LED(15) 
Heater = LED(14) # 
Start_UV_light = "08:00"
End_UV_light = "16:00"
temp_sensor = 22
low_moisture = 50
high_moisture = 80
soil_sensor = 60
temperature = 20

#Creating a window to display the data to the user.
win = Tk()
win.title("Indoor Green Planter monitoring screen")
win.geometry('800x700')
myFont = tkinter.font.Font(family ='Arial' ,size = '13', weight = "bold")

# Setting up the address for the argon particle - address is 0x8
addr = 0X8
bus = SMBus(1)


def argon_soil_moisture():
#This function reads the soil moisture content and sends the data to the argon particle in for of Hexadecimal
	global soil_sensor
	while True:
		time.sleep(10)
		try:
			soil_sensor = bus.read_byte(addr)
			print("Soil Moisture level is: " +str(soil_sensor))
		except:
			
			print("Soil moisture failed")
			
		if soil_sensor <= low_moisture:
			try:
				bus.write_byte(addr, 0x0) # Sends out '0' meaning low in moisture
				print("Data send 0")
			except:
				print("0 send fail")
				
		elif soil_sensor > high_moisture:
			try:
				bus.write_byte(addr, 0x1) # Sends out '' meaning high water content
				print("Data send 1")
			except:
				print("1 send fail")
				 
		else:
			try:
				bus.write_byte(addr, 0x2) # Sends out '' water content ok
				print("Soil -moisture pk")
			except:
				print("2 send fail")
	
		

# Functions below are to 	
def closeProgram():
	# The function closes the program correctly
	RPi.GPIO.cleanup()
	win.destroy()


def room_temp_sensor():
		global temperature
		
	#Applying try catch as the sensor seems to fail often
		try:
		
			temperature = temp_sensor_reading.temperature
			print('Temperature reading is: '+str(temperature))
			return temperature
		except :
			print('Temperature reading with errors is: 20')
			return 20
		time.sleep(1)

	
	
def window():
# This function handles a window which display the current soil moisture level and room temperature.
		#Below displays the soil moisture level
		soil_moisture = Label(win, text="Soil Moisture is: ", bg ="green",fg ='white', height=1, width = 25) 
		soil_moisture.grid(row=2,column =1)	
		label_moisture = Label(win, text=str(soil_sensor))
		label_moisture.grid(row =2, column =2)
		
		#Below are the code responsible of displaying the temperature of the room
		room_temp = Label(win, text="Room Temperature is: ", bg ='green', fg='white', height =1, width =25)
		room_temp.grid(row = 7, column = 1)
		label_temp = Label(win, text= str(temperature))
		label_temp.grid(row = 7, column = 2)
		
		# Reading the current preset parameters in this program the global vairable
		label_actual = Label(win, text="Actual Parameters are :", bg= 'blue', fg ='white', height =1 , width =25)
		label_actual.grid(row =9, column =1)
		label_current_heater_temperature = Label(win, text="Current temperature to stop the heater is: "+str(temp_sensor), bg='blue', fg='white', height =1, width =35)
		label_current_heater_temperature.grid(row=11,column =1)
		label_current_UV_time =Label(win, text="The start and end time for UV light is between: "+Start_UV_light+"and "+ End_UV_light, bg= 'blue', fg ='white', height =1 , width =55)
		label_current_UV_time.grid(row =13, column =1)
		label_current_moisture= Label(win, text='Current moisture level is between :'+str(low_moisture)+' and '+str(high_moisture), bg='blue', fg='white', height =1, width =45) 
		label_current_moisture.grid(row =15, column =1)
		
		#Input for temperature at which hearter is turned off
		#e - entry for temperature
		#s - entry for UV start time
		#n - entry for UV end time
		#l - entry for lower moisture level
		#h - entry for high moisture level
		#User entry code#
		e = Entry(win, width = 12)
		e.grid(row =17, column = 2)
		
		s = Entry(win, width = 12)
		s.grid(row =23, column = 2)
		
		n = Entry(win, width = 12)
		n.grid(row =29, column = 2)
		
		l = Entry(win, width = 12)
		l.grid(row =35, column = 2)
		
		h = Entry(win, width = 12)
		h.grid(row =41, column = 2)
		
		
		def temp_input():
				#used to input below which the heater is turned off
				global temp_sensor
				temp = e.get()
				temp_sensor = int(temp)
 				
		def start_UV():
				global Start_UV_light
				Start_UV_light = s.get()

		def end_UV():
				global End_UV_light
				End_UV_light = n.get()
				
				
		def soil_min_value():
				global low_moisture
				low_moisture = int(l.get())
				
		
		def soil_max_value():
				global high_moisture
				high_moisture = int(h.get())
				
				
		# Label to ask user for minimum temperature for heater to turn on
		label_min_temp= Label(win, text="New temperature for heater to start:",height =1)
		label_min_temp.grid(row =17, column = 1)

		# Button to execute the translation of the name to morse code
		myButton = Button(win, text="Apply", command= temp_input, bg ="red",fg ='white', height=1, width = 10) 
		myButton.grid(row=17,column =3)
		
		#UV start and end time input
		label_start_uv = Label(win, text='New UV light start time:')
		label_start_uv.grid(row =23, column =1)
		myButton = Button(win, text="Apply", command= start_UV, bg ="red",fg ='white', height=1, width = 10) 
		myButton.grid(row=23,column =3)
		
		label_end_uv = Label(win, text='New UV light end time:')
		label_end_uv.grid(row =29, column =1)
		myButton = Button(win, text="Apply", command= end_UV, bg ="red",fg ='white', height=1, width = 10) 
		myButton.grid(row=29,column =3)
		
		#Soil moisture inputs
		label_soil_min = Label(win, text='New lower soil moisture reading:')
		label_soil_min.grid(row =35, column =1)
		myButton = Button(win, text="Apply", command= soil_min_value, bg ="red",fg ='white', height=1, width = 10) 
		myButton.grid(row=35,column =3)
		
		label_soil_max = Label(win, text='New upper soil moisture reading: ')
		label_soil_max.grid(row =41, column =1)
		myButton = Button(win, text="Apply", command= soil_max_value, bg ="red",fg ='white', height=1, width = 10) 
		myButton.grid(row=41,column =3)
		#The line below allows the program to close properly
		exitProgram = Button(win, text= "Close program", command = closeProgram, bg ='red',height = 1, width = 25)
		exitProgram.grid(row =50, column = 1)

		win.protocol("WM_DELETE_WINDOW", closeProgram)
	
		def update_input():
			
			#Updating the temperature of the room and soil moisture
			label_moisture.config(text = str(soil_sensor))
			#similarly when temperature sensor fails, the label stops refreshing hence the try - catch
			try:
				label_temp.config(text =str(room_temp_sensor())) 
			except:
				label_temp.config(text= '24')
			
			
			#Updating the parameters
			label_current_heater_temperature.config(text ="Current temperature to start heater is: "+str(temp_sensor))
			label_current_UV_time.config(text="The start and end time for UV light is between: "+Start_UV_light+"and "+ End_UV_light)
			label_current_moisture.config(text='Current moisture level is between :'+str(low_moisture)+' and '+str(high_moisture))
			win.after(2000, update_input)

		win.after(2000, update_input)
		win.mainloop()
	
def room():
		while True:
			# Button to execute the translation of the name to morse code

			UV_light()
			room_temp_sensor()
			
				
			if temperature < temp_sensor:
				Heater.on()
			else:
				Heater.off()
		

def UV_light():
	
		
		t= time.localtime()
		UV_time_on = time.strftime("%H:%M", t)
		#Below is the variable for the start and end of the UV light
		start_time = time.strftime(Start_UV_light)
		end_time = time.strftime(End_UV_light)
		print(str(UV_time_on))
		if (UV_time_on > start_time) and (UV_time_on < end_time):
			UV_light_LED.on()
		else:
			UV_light_LED.off()
		
		time.sleep(2)
		
if __name__ == '__main__':

	Thread(target = argon_soil_moisture).start()
	Thread(target = room).start()
	window()
	time.sleep(10)


