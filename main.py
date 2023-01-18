from tkinter import *
from tkinter import messagebox as msb
import keyboard
import time
import random as r
import threading
#======================
class geometry:
    def __init__(self):
        pass    
    def w(self):
        return self.winfo_screenwidth()-150
    def h(self):
        return 500
    def width(self):
        return self.winfo_screenwidth()
    def height(self):
        return self.winfo_screenheight()
    

class Move:
    def __init__(self):
        pass
    def move(self, speed, key):
        left_object_pos = self.game_frame.coords(self.left_object)
        right_object_pos = self.game_frame.coords(self.right_object)
        if key == "w":
            if left_object_pos[1] > 0:
                self.game_frame.move(self.left_object, 0, -int(speed))
        elif key == "s":
            if left_object_pos[3] < geometry.h(self):
                self.game_frame.move(self.left_object, 0, int(speed))
        elif key == "up":
            if right_object_pos[1] > 0:
                self.game_frame.move(self.right_object, 0, -int(speed))
        elif key == "down":
            if right_object_pos[3] < geometry.h(self):
                self.game_frame.move(self.right_object, 0, int(speed))
    def move_ball(self, x_speed, y_speed):
        stock_pos = self.game_frame.coords(self.ball)
        right_object_pos = self.game_frame.coords(self.right_object)
        left_object_pos = self.game_frame.coords(self.left_object)
        if stock_pos[1] < 0:
            self.y_speed = -y_speed
        if stock_pos[3] > geometry.h(self):
            self.y_speed = -y_speed
        if stock_pos[2] > geometry.w(self)-20 and right_object_pos[1] < stock_pos[3] < right_object_pos[3]:
            self.x_speed = -x_speed
        if stock_pos[0] < 20 and left_object_pos[3] > stock_pos[1] > left_object_pos[1]:
            self.x_speed = -x_speed
        if stock_pos[0] < 0:
            self.x_speed = -x_speed
            self.right_score += 1
            self.game_frame.itemconfig(self.text_r, text = f"{self.right_score}")
        if stock_pos[2] > geometry.w(self):
            self.x_speed = -x_speed
            self.left_score += 1
            self.game_frame.itemconfig(self.text_l, text = f"{self.left_score}")            
        print(stock_pos)
        self.game_frame.move(self.ball, self.x_speed, self.y_speed)
        
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Пинг-понг")
        self.resizable(False, False)
        self.config(bg="#DCDCDC")
        # Geometry
        #============
        self.geometry(
            f"{int(geometry.w(self)/4)}x{int(geometry.h(self))}+{int(geometry.width(self)/2-geometry.w(self)/8)}+{int(geometry.height(self)/2-geometry.h(self)/2)}")
        #============
        self.new_game = Button(self, width=10, height=2, text = "Новая игра", font="Arial 12 bold", command=self.open_game, relief="groove")
        self.new_game.place(x=geometry.w(self)/8-50, y=geometry.h(self)/32)
        self.rules = Button(self, width=10, height=2, text = "Правила", font="Arial 12 bold", command=self.open_setting, relief="groove")
        self.rules.place(x=geometry.w(self)/8-50, y=geometry.h(self)        /32+80)
        self.lbl_speed = LabelFrame(self, text = "Скорость рокеток", relief=GROOVE, bg = "#DCDCDC", labelanchor = N)
        self.lbl_speed.place(x=geometry.w(self)/8-geometry.width(self)/10, y=geometry.h(self)/2+80)
        self.lbl_speed_ball = LabelFrame(self, text = "Скорость мяча", relief=GROOVE, bg = "#DCDCDC", labelanchor = N)
        self.lbl_speed_ball.place(x=geometry.w(self)/8-geometry.width(self)/10, y=geometry.h(self)/3+80)
        self.speed = Entry(self.lbl_speed, width = 20, justify = CENTER)
        self.speed.grid(row=0, column=0)
        self.speed_ball = Entry(self.lbl_speed_ball, width = 20, justify = CENTER)
        self.speed_ball.grid(row=0, column=0)        
    def get_speed(self):
        speed = self.speed.get()
        self.speed.delete(0, END)
        self.speed["state"] = DISABLED
        if speed == "":
            return "10", self.speed
        else:
            if int(speed) > 0:
                return speed, self.speed
            else:
                msb.showwarning("Ошибка", "Нет такой скорости, установленна стандартная скорость!")
                return "10", self.speed
    def get_speed_ball(self):
        speed_ball = self.speed_ball.get()
        self.speed_ball.delete(0, END)
        self.speed_ball["state"] = DISABLED
        if speed_ball == "":
            return "5", self.speed_ball
        else:
            if int(speed_ball) > 0:
                return speed_ball, self.speed_ball
            else:
                msb.showwarning("Ошибка", "Нет такой скорости, установленна стандартная скорость!")
                return "5", self.speed_ball
    def open_game(self):
        speed = self.get_speed()
        speed_ball = self.get_speed_ball()
        window = Game(self, speed, speed_ball)
        window.grab_set()
        speed[1]["state"] = NORMAL
        speed_ball[1]["state"] = NORMAL
    def open_setting(self):
        window = Setting(self)
        window.grab_set()
        
class Setting(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(
            f"{int(geometry.w(self)/2)}x{int(geometry.h(self)/2)}+{int(geometry.width(self)/2-geometry.w(self)/4)}+{int(geometry.height(self)/2-geometry.h(self)/4)}")
        self.center_x = int(geometry.width(self)/2-geometry.w(self)/2)
        self.center_y = int(geometry.height(self)/2-geometry.h(self)/2)
        self.rules = Label(self, text = "Правила", justify = CENTER, font = "Arial 13 bold")
        self.rules.place(x = self.center_x*4-15, y = self.center_y/8)
        self.rules_text = Label(self, text = "Задачей игроков является удерживать мяч в игре при помощи ракеток и вычислив траекторию мячя отправить его на половину поля соперника. Очко начисляется игроку, если мяч коснулся границы поля противника.\nСтандартная скорость мяча = 3\nСтандартная скорость рокеток = 10", justify = CENTER, font = "Arial 10", wraplength = 500)
        self.rules_text.place(x = self.center_x, y = self.center_y/4)

class Game(Toplevel):
    def __init__(self, parent, speed_0_1, speed_ball):
        super().__init__(parent)
        speed = speed_0_1[0]
        self.x_speed = r.choice([1, -1])
        self.y_speed = r.choice([1, -1])
        self.speed_ball = speed_ball[0]
        self.left_score = 0
        self.right_score = 0
        self.stop = True
        self.center_x = int(geometry.width(self)/2-geometry.w(self)/2)
        self.center_y = int(geometry.height(self)/2-geometry.h(self)/2)
        self.geometry(
            f"{geometry.w(self)}x{geometry.h(self)}+{self.center_x}+{self.center_y}")
        self.resizable(False, False)
        self.game_frame = Canvas(self, width = geometry.w(self), height = geometry.h(self), bg = "green")
        self.game_frame.place(y = 0, x = 0)
        self.score_table = self.game_frame.create_rectangle(geometry.w(self)/2-100, 0, geometry.w(self)/2+100, 50, width = 10, fill = "black")
        self.text_l = self.game_frame.create_text(geometry.w(self)/2-50, 25, text = f"{self.left_score}", fill = "white", font = "Arial, 30")
        self.text_r = self.game_frame.create_text(geometry.w(self)/2+50, 25, text = f"{self.right_score}", fill = "white", font = "Arial 30")
        self.game_frame.create_line(geometry.w(self)/2, 0, geometry.w(self)/2, geometry.h(self), fill = "white", width = 2)
        self.left_object = self.game_frame.create_rectangle(0, 0, 20, 120, fill = "white")
        self.right_object = self.game_frame.create_rectangle(geometry.w(self)-20, geometry.h(self)-120, geometry.w(self), geometry.h(self), fill = "white")
        self.ball = self.game_frame.create_oval(geometry.w(self)/2-20, geometry.h(self)/2-20, geometry.w(self)/2+20, geometry.h(self)/2+20, fill = "white")
        self.ball_line = self.game_frame.create_oval(geometry.w(self)/2-20, geometry.h(self)/2-20, geometry.w(self)/2+20, geometry.h(self)/2+20, outline= "white", fill = "green", width=2)
        self.run = True
        self.protocol("WM_DELETE_WINDOW", self.handler)  
        keyboard.add_hotkey("w", lambda: Move.move(self, speed, "w") if self.run == True else self.destroy())
        keyboard.add_hotkey("s", lambda: Move.move(self, speed, "s") if self.run == True else self.destroy())
        keyboard.add_hotkey("up", lambda: Move.move(self, speed, "up") if self.run == True else self.destroy())
        keyboard.add_hotkey("down", lambda: Move.move(self, speed, "down") if self.run == True else self.destroy())
        keyboard.add_hotkey("space", lambda: time.sleep(5))
        self.play()
        task1 = threading.Thread(target=self.key_pause, daemon=True)
        task1.start()
        self.pause()    
    def handler(self):
        self.run = False
        self.destroy()
    def play(self):
        Move.move_ball(self, self.x_speed, self.y_speed)
        self.after(self.speed_ball, self.play)
    def key_pause(self):
        keyboard.add_hotkey('space', self.stopgame)
        keyboard.wait()
    def stopgame(self):
        if self.stop == False:
            self.stop = True
        else:
            self.stop = False    
    def pause(self):
        while self.stop:
            time.sleep(0.1)      
        
          
app = App()
app.mainloop()
