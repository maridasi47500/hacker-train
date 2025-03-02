import time
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Mock functions to simulate sensor readings and actions
def read_wheel_sensor():
    rotations_per_sec = np.random.uniform(0.2, 0.5)  # Adjusted for more realistic values
    return rotations_per_sec

def calculate_speed(rotations_per_sec, wheel_diameter):
    circumference = np.pi * wheel_diameter
    speed_m_per_s = rotations_per_sec * circumference
    speed_mph = speed_m_per_s * 2.237
    return speed_mph

def activate_brake():
    console.print("Simulated brake activated to slow down the train.", style="bold red")
    return True

class Speedometer:
    def __init__(self, target_speed_mph):
        self.target_speed_mph = target_speed_mph
        self.current_speed = 0
        self.distance_traveled = 0
        self.time_elapsed = 0

    def ChangeDutyCycle(self, speed):
        self.current_speed = speed * self.target_speed_mph / 100

console = Console()

def motor_speed_control():
    console.print("Train is departing the station...", style="bold green")
    target_speed_mph = 100
    speedometer = Speedometer(target_speed_mph)
    wheel_diameter = 1.0
    start_time = time.time()

    with Live(console=console, auto_refresh=False) as live:
        try:
            while True:
                input_str = input("SBC_Speed = ")
                try:
                    speed = int(input_str)
                    if 0 <= speed <= 100:
                        pass  # Skip changing the duty cycle immediately
                    else:
                        console.print("Please enter a value between 0 and 100.", style="bold red")
                        continue
                except ValueError:
                    console.print("Please enter a valid integer.", style="bold red")
                    continue

                if speedometer.current_speed < speed:
                    # Gradually increase from the current speed to the desired speed
                    while speedometer.current_speed < speed:
                        rotations_per_sec = read_wheel_sensor()
                        real_time_speed = calculate_speed(rotations_per_sec, wheel_diameter)

                        speedometer.current_speed += 0.5  # Simulate realistic gradual speed increase
                        if speedometer.current_speed > speed:
                            speedometer.current_speed = speed
                        speedometer.ChangeDutyCycle(speedometer.current_speed)

                        speedometer.time_elapsed = time.time() - start_time
                        speedometer.distance_traveled += (speedometer.current_speed * 0.1) / 3600  # Convert mph to miles per 0.1 sec

                        table = Table(title="Train Speed Control")
                        table.add_column("Parameter", style="cyan", no_wrap=True)
                        table.add_column("Value", style="magenta")
                        table.add_row("Set Speed (mph)", f"{speedometer.current_speed:.2f}")
                        table.add_row("Real-time Speed (mph)", f"{real_time_speed:.2f}")
                        table.add_row("Distance Traveled (miles)", f"{speedometer.distance_traveled:.2f}")
                        table.add_row("Time Elapsed (seconds)", f"{speedometer.time_elapsed:.2f}")

                        live.update(table, refresh=True)

                        if speedometer.current_speed >= speed:
                            console.print(f"Train has reached {speedometer.current_speed:.2f} mph. Maintaining speed...", style="bold blue")
                            break

                        time.sleep(0.1)

                elif speedometer.current_speed > speed:
                    # Gradually decrease from the current speed to the desired speed
                    console.print("Decelerating...", style="bold yellow")
                    while speedometer.current_speed > speed:
                        speedometer.current_speed -= 0.5
                        if speedometer.current_speed < speed:
                            speedometer.current_speed = speed

                        rotations_per_sec = read_wheel_sensor()
                        real_time_speed = calculate_speed(rotations_per_sec, wheel_diameter)
                        speedometer.distance_traveled += (speedometer.current_speed * 0.1) / 3600  # Convert mph to miles per 0.1 sec
                        speedometer.time_elapsed = time.time() - start_time

                        table = Table(title="Train Speed Control")
                        table.add_column("Parameter", style="cyan", no_wrap=True)
                        table.add_column("Value", style="magenta")
                        table.add_row("Set Speed (mph)", f"{speedometer.current_speed:.2f}")
                        table.add_row("Real-time Speed (mph)", f"{real_time_speed:.2f}")
                        table.add_row("Distance Traveled (miles)", f"{speedometer.distance_traveled:.2f}")
                        table.add_row("Time Elapsed (seconds)", f"{speedometer.time_elapsed:.2f}")

                        live.update(table, refresh=True)
                        time.sleep(0.1)
                    if speed == 0:
                        activate_brake()

        except KeyboardInterrupt:
            pass

    console.print("Train has arrived at the station and come to a complete stop.", style="bold green")
    console.print("Exiting motor speed control...", style="bold magenta")
    console.print("PWM stopped and GPIO cleaned up (simulated).", style="bold magenta")

# Run the motor speed control
motor_speed_control()

