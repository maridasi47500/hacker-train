import time
import numpy as np

# Mock functions to simulate sensor readings and actions
def read_wheel_sensor(bus, address, register):
    # Simulate sensor data as random rotations per second
    rotations_per_sec = np.random.uniform(0, 2)  # Example: range from 0 to 2 rotations per second
    return rotations_per_sec

def calculate_speed(rotations_per_sec, wheel_diameter):
    circumference = np.pi * wheel_diameter  # Circumference in meters
    speed_m_per_s = rotations_per_sec * circumference  # Speed in meters per second
    speed_mph = speed_m_per_s * 2.237  # Convert to mph
    return speed_mph

def activate_brake():
    print("Simulated brake activated to slow down the train.")
    return True

class Speedometer:
    def __init__(self, target_speed_mph):
        self.target_speed_mph = target_speed_mph
        self.current_speed = 0
    
    def ChangeDutyCycle(self, speed):
        self.current_speed = speed * self.target_speed_mph / 100
        print(f"Current speed: {self.current_speed:.2f} mph")

# Motor speed control with user input
def motor_speed_control():
    print("Train is departing the station...")
    
    target_speed_mph = 100  # Desired speed in mph
    speedometer = Speedometer(target_speed_mph)  # Create Speedometer object

    while True:
        try:
            while True:
                # User input to set motor speed
                input_str = input("SBC_Speed = ")
                try:
                    speed = int(input_str)
                    if 0 <= speed <= 100:
                        # Use the Speedometer class to change duty cycle
                        speedometer.ChangeDutyCycle(speed)
                    else:
                        print("Please enter a value between 0 and 100.")
                except ValueError:
                    print("Please enter a valid integer.")
                
                # Simulate speed changes and arrival process
                if speedometer.current_speed < target_speed_mph:
                    print("Accelerating...")
                if speedometer.current_speed == target_speed_mph:
                    print("Train has reached 100 mph. Maintaining speed for a few seconds...")
                    time.sleep(5)  # Maintain speed for 5 seconds
                    break
        
        except KeyboardInterrupt:
            break

    # Arrival
    print("Train is arriving at the station. Slowing down...")
    while speedometer.current_speed > 0:
        speedometer.current_speed -= 10  # Simulate deceleration
        print(f"Decelerating... Current speed: {speedometer.current_speed:.2f} mph")
        if speedometer.current_speed <= 0:
            speedometer.current_speed = 0
            activate_brake()
        time.sleep(1)

    print("Train has arrived at the station and come to a complete stop.")
    print("Exiting motor speed control...")
    
    # Cleanup (simulated)
    print("PWM stopped and GPIO cleaned up (simulated).")

# Run the motor speed control
motor_speed_control()
