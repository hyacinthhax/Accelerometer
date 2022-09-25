import os
import smbus
import math
import time

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
tmp_out_1 = 0x41
tmp_out_2 = 0x42

def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h << 8) + l
	return value

def read_word_2c(reg):
	val = read_word(reg)
	if (val >= 0x8000):
		return -((65535 -val) + 1)
	else:
		return val

def dist(a, b):
	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x, y, z):
	radians = math.atan2(x, dist(x,y))
	return -math.degrees(radians)

def get_x_rotation(x, y, z):
	radians = math.atan2(y, dist(y,z))
	return math.degrees(radians)

def get_temp():
	raw_temp = read_word(tmp_out_1)
	actual_temp = (raw_temp/340) + 36.53
	return actual_temp


while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	time.sleep(1)
	print(get_temp())
	bus = smbus.SMBus(1)
	address = 0x68
	bus.write_byte_data(address, power_mgmt_1, 0X00)

	print("Gyro:  \n")
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

	print(f"GyroX:  {gyro_xout}")
	print(f"GyroY:  {gyro_yout}")
	print(f"GyroZ:  {gyro_zout}")

	print("\nAccelerometer:  \n")

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)

	scaledX = accel_xout / 16384.0
	scaledY = accel_yout / 16384.0
	scaledZ = accel_zout / 16384.0

	print("AccelX:  ", ("%6d" % accel_xout), "ScaledX:  ", scaledX)
	print("AccelY:  ", ("%6d" % accel_yout), "ScaledY:  ", scaledY)
	print("AccelZ:  ", ("%6d" % accel_zout), "ScaledZ:  ", scaledZ)

	print("\nXRotation:  ", get_x_rotation(scaledX, scaledY, scaledZ))
	print("YRotation:  ", get_y_rotation(scaledX, scaledY, scaledZ))

