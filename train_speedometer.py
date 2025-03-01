import RPi.GPIO as GPIO
import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

class TrainSpeedometer:
    def __init__(self, sensor_pin, coefficient_conversion):
        self.sensor_pin = sensor_pin
        self.coefficient_conversion = coefficient_conversion
        self.pulse_count = 0
        self.start_time = time.time()
        
        # Configuration des GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        GPIO.add_event_detect(self.sensor_pin, GPIO.RISING, callback=self.count_pulses)
        
        # Configuration de l'écran LCD
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.display.begin()
        self.display.clear()
        self.display.display()
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        
    def count_pulses(self, channel):
        self.pulse_count += 1
        
    def freinage(self):
        print("Freinage du train...")
        
    def maintenir_vitesse(self):
        print("Maintien de la vitesse actuelle du train...")
        
    def afficher_vitesse(self, speed_mph):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.draw.text((0, 0), f"Vitesse: {speed_mph:.2f} mph", font=self.font, fill=255)
        self.display.image(self.image)
        self.display.display()
        
    def run(self):
        try:
            while True:
                time.sleep(1)
                end_time = time.time()
                elapsed_time = end_time - self.start_time
                rpm = (self.pulse_count / elapsed_time) * 60
                speed_mph = rpm * self.coefficient_conversion * 0.621371
                self.pulse_count = 0
                self.start_time = end_time
                
                print(f"Vitesse actuelle du train: {speed_mph:.2f} mph")
                self.afficher_vitesse(speed_mph)
                
                if speed_mph < 49.71:  # Correspond à 80 km/h
                    print("Vitesse en dessous de 49.71 mph")
                    # Code pour contrôler la vitesse à moins de 49.71 mph
                elif 49.71 <= speed_mph <= 62.14:  # Correspond à 80-100 km/h
                    print("Vitesse entre 49.71 et 62.14 mph")
                    self.maintenir_vitesse()
                else:
                    print("Vitesse au-dessus de 62.14 mph")
                    self.freinage()
                    
        except KeyboardInterrupt:
            GPIO.cleanup()
            
# Utilisation de la classe
train_speedometer = TrainSpeedometer(sensor_pin=17, coefficient_conversion=0.05)
train_speedometer.run()
