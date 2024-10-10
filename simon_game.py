
from machine import Pin, PWM
import time
import random
import tm1637




class SimonGame:
    
    tm = tm1637.TM1637(clk=Pin(17), dio=Pin(16))
    
    # Define the pin for the passive buzzer
    buzzer = Pin(0, Pin.OUT)

    # PWM for generating tones
    pwm = PWM(buzzer)

    color_list = [1, 2, 3, 4]
    random_list = []
    player_list = []
    turn_index = -1
    game_running = True
    player_running = True
    score = 0
    
    # Define the frequencies for each color
    colors_tones = {
        "red": 440,    # A4
        "blue": 494,   # B4
        "yellow": 523, # C5
        "green": 587   # D5
    }

    def __init__(self, 
                button_red_pin,
                button_green_pin,
                button_yellow_pin,
                button_blue_pin,
                led_red_pin,
                led_green_pin,
                led_yellow_pin,
                led_blue_pin,
                led_blink_interval=1):

        self.button_red = Pin(button_red_pin, Pin.IN, Pin.PULL_UP)
        self.button_green = Pin(button_green_pin, Pin.IN, Pin.PULL_UP)
        self.button_yellow = Pin(button_yellow_pin, Pin.IN, Pin.PULL_UP)
        self.button_blue = Pin(button_blue_pin, Pin.IN, Pin.PULL_UP)

        self.led_red = Pin(led_red_pin, Pin.OUT)
        self.led_green = Pin(led_green_pin, Pin.OUT)
        self.led_yellow = Pin(led_yellow_pin, Pin.OUT)
        self.led_blue = Pin(led_blue_pin, Pin.OUT)

        self.led_blink_interval = led_blink_interval
        
        self.tm.brightness(4)

        self._show_text("PLAy", 1)


    # Function to play a tone
    def _play_tone(self, frequency, duration):
        self.pwm.freq(frequency)
        self.pwm.duty_u16(512)  # Set duty cycle to 50%
        time.sleep(duration)
        self.pwm.duty_u16(0)  # Turn off the buzzer
        

    def _show_score(self):
        score = "{:04}".format(SimonGame.score)
        self.tm.write([0, 0, 0, 0])
        self.tm.show(score, False)
        
        
    def _show_text(self, text, duration: int):
        self.tm.write([0, 0, 0, 0])
        self.tm.show(f"{text}", False)
        time.sleep(duration)

    #Chose random coloe from list of colors
    def chose_color(self):
        choice = random.choice(SimonGame.color_list)
        return choice


    
    def play_led(self, led_num, led_blink_interval):
        pause = led_blink_interval

        if led_num == 1:
            self.led_red.value(1)
            self._play_tone(SimonGame.colors_tones["red"], 0.5)
            time.sleep(pause)
            self.led_red.value(0)
            time.sleep(pause)
        elif led_num == 2:
            self.led_green.value(1)
            self._play_tone(SimonGame.colors_tones["green"], 0.5)
            time.sleep(pause)
            self.led_green.value(0)
            time.sleep(pause)
        elif led_num == 3:
            self.led_yellow.value(1)
            self._play_tone(SimonGame.colors_tones["yellow"], 0.5)
            time.sleep(pause)
            self.led_yellow.value(0)
            time.sleep(pause)
        elif led_num == 4:
            self.led_blue.value(1)
            self._play_tone(SimonGame.colors_tones["blue"], 0.5)
            time.sleep(pause)
            self.led_blue.value(0)
            time.sleep(pause)




    def pc_turn(self):
        self._show_text(" PC ", 1)
        self._show_score()
        for i in SimonGame.random_list:
            self.play_led(i, self.led_blink_interval)

        SimonGame.player_running = True


    def player_turn(self):
        self._show_text("PL 1", 1)
        self._show_score()
        while SimonGame.player_running:
   
            if not self.button_red.value():
                SimonGame.player_list.append(1)
                SimonGame.turn_index += 1
                self.led_red.value(1)
                self._play_tone(SimonGame.colors_tones["red"], 0.5)
                time.sleep(0.5)
                self.led_red.value(0)
                self.check_lose()
            elif not self.button_green.value():
                SimonGame.player_list.append(2)
                SimonGame.turn_index += 1
                self.led_green.value(1)
                self._play_tone(SimonGame.colors_tones["green"], 0.5)
                time.sleep(0.5)
                self.led_green.value(0)
                self.check_lose()
            elif not self.button_yellow.value():
                SimonGame.player_list.append(3)
                SimonGame.turn_index += 1
                self.led_yellow.value(1)
                self._play_tone(SimonGame.colors_tones["yellow"], 0.5)
                time.sleep(0.5)
                self.led_yellow.value(0)
                self.check_lose()
            elif not self.button_blue.value():
                SimonGame.player_list.append(4)
                SimonGame.turn_index += 1
                self.led_blue.value(1)
                self._play_tone(SimonGame.colors_tones["blue"], 0.5)
                time.sleep(0.5)
                self.led_blue.value(0)
                self.check_lose()


    
    def new_game(self):
        self._show_score()
        for i in range(2):
            c = self.chose_color()
            SimonGame.random_list.append(c)


    def play_game(self):
        self.new_game()

        while SimonGame.game_running:
            self.pc_turn()
            self.player_turn()


    def check_lose(self):
        if len(SimonGame.player_list) > (len(SimonGame.random_list)):
            SimonGame.player_running = False
            self.game_over()
        elif SimonGame.random_list[SimonGame.turn_index] != SimonGame.player_list[SimonGame.turn_index]:
            SimonGame.player_running = False
            self.game_over()
        elif SimonGame.player_list == SimonGame.random_list:
            SimonGame.player_running = False
            SimonGame.score = (len(SimonGame.random_list)- 1) * 10
            print((len(SimonGame.random_list)- 1) * 10)
            c = self.chose_color()
            SimonGame.random_list.append(c)
            self._reset_var()


    def game_over(self):
        self._show_text("OvEr", 1)
        SimonGame.random_list = []
        SimonGame.score = 0 
        self._reset_var()
        self.play_game()


    def _reset_var(self):
        SimonGame.player_list = []
        SimonGame.turn_index =-1

