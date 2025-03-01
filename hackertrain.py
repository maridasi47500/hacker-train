import time
import numpy as np
from smbus2 import SMBus

# Function to read data from an I2C wheel sensor
def read_wheel_sensor(bus, address, register):
    try:
        # Read 2 bytes from the specified register
        data = bus.read_word_data(address, register)
        # Convert data to rotations per second (this will depend on your sensor)
        rotations_per_sec = data / 1000.0  # Example conversion
        return rotations_per_sec
    except Exception as e:
        print(f"Error reading from sensor: {e}")
        return None

# Function to calculate the speed in mph
def calculate_speed(rotations_per_sec, wheel_diameter):
    circumference = np.pi * wheel_diameter  # Circumference in meters
    speed_m_per_s = rotations_per_sec * circumference  # Speed in meters per second
    speed_mph = speed_m_per_s * 2.237  # Convert to mph
    return speed_mph

# Function to activate the braking system
def activate_brake():
    print("Simulated brake activated to slow down the train.")
    return True

# Function to accelerate the train
def accelerate_train(bus, address, register, target_speed_mph, current_speed_mph):
    if current_speed_mph < target_speed_mph:
        # Send signal to accelerate
        print("Simulated acceleration to increase train speed.")
        # Example: write to the register to increase speed (replace with actual implementation)
        bus.write_byte_data(address, register, 0x01)
        return True
    return False

# Parameters for I2C communication
wheel_diameter = 0.8  # Diameter of the train wheel in meters
sampling_interval = 1  # Time between sensor readings in seconds
i2c_sensor_address = 0x40  # I2C address of the wheel sensor (example)
i2c_sensor_register = 0x00  # Register to read from (example)
speed_control_address = 0x41  # I2C address of the speed control system (example)
speed_control_register = 0x01  # Register to control speed (example)
speed_threshold = 80  # Speed threshold in mph
target_speed_mph = 100  # Desired speed in mph

# Initialize the I2C bus
bus = SMBus(1)

while True:
    rotations_per_sec = read_wheel_sensor(bus, i2c_sensor_address, i2c_sensor_register)
    if rotations_per_sec is not None:
        speed = calculate_speed(rotations_per_sec, wheel_diameter)
        
        if speed < 80:
            speed_category = "Below 80 mph"
        elif 80 <= speed < 100:
            speed_category = "80-100 mph"
        else:
            speed_category = "Above 100 mph"
        
        print(f"Train speed: {speed:.2f} mph | Category: {speed_category}")
        
        if speed > speed_threshold:
            brake_activated = activate_brake()
            if brake_activated:
                print("Brake activated to slow down the train.")
        else:
            accelerate_train(bus, speed_control_address, speed_control_register, target_speed_mph, speed)
    
    time.sleep(sampling_interval)
