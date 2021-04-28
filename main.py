from kivy.core.audio import SoundLoader,Sound
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from random import randint
from kivy.app import App

lev=10
class diffLevel(Screen,Widget):
    def playSound(self):
        sound = SoundLoader.load('Assets\\ButtClick.wav')
        sound.loop = False
        sound.play()
    def press_read(self,l):
        global lev
        lev=l

class aboutUs(Screen):
    def playSound(self):
        sound = SoundLoader.load('Assets\\ButtClick.wav')
        sound.loop = False
        sound.play()

class pongPaddle(Widget):
    pass

class secondScreen(Screen):
     winner_name = ObjectProperty("")
     mi=0
     winner_score = 2
     ready=0
     i=0
     firstPlayer=NumericProperty(0)
     secondPlayer = NumericProperty(0)
     ball=ObjectProperty(None)
     player1 = ObjectProperty(None)
     player2 = ObjectProperty(None)

     def playSound(self):
         sound = SoundLoader.load('Assets\\ButtClick.wav')
         sound.loop = False
         sound.play()
     def serve_ball(self):
         self.ball.center = self.center

     def stop_serve(self):
         self.ball.center = self.center
         self.ball.velocity = Vector(0,0)

     def update(self,dt):
        self.i+=1
        self.ball.move()

        if (self.ball.y<0) or (self.ball.y>self.height-50):
            self.ball.velocity_y *= -1

        if (self.ball.x<0) or (self.ball.x>self.width-50):
            self.ball.velocity_x *= -1

        if(self.secondPlayer==self.winner_score):
            self.stop_serve()
            self.winner_name="SECOND PLAYER WON"
            if(self.mi == 1):
                self.sound = SoundLoader.load('Assets\\WinSound.wav')
                self.sound.loop = True
                self.sound.play()
                self.mi = 2

        elif(self.firstPlayer==self.winner_score):
            self.stop_serve()
            self.winner_name = "FIRST PLAYER WON"
            if (self.mi == 1):
                self.sound = SoundLoader.load('Assets\\WinSound.wav')
                self.sound.loop = True
                self.sound.play()
                self.mi = 2

        if (self.ready==1):
            if(self.mi==0):
                self.mi+=1
                print(lev)
                self.ball.velocity = Vector(lev, -2).rotate(randint(30, 45))

            if int(self.ball.x)>0 and int(self.ball.x)<19 and\
                int(self.ball.y)>int(self.player1.y) and\
                    int(self.ball.y)<int(self.player1.y)+120:
                self.ball.velocity_x *= -1
            elif int(self.ball.x)>0 and int(self.ball.x)<6:
                self.secondPlayer=self.secondPlayer+1
                self.ball.velocity_x *= -1

            if int(self.ball.x) > 200 and int(self.ball.x) < 745 and \
                    int(self.ball.y) > int(self.player2.y) and \
                    int(self.ball.y) < int(self.player2.y) + 120:
                self.ball.velocity_y *= 1
            elif int(self.ball.x) > 740 and int(self.ball.x) < 745:
                self.firstPlayer=self.firstPlayer+1
                self.ball.velocity_x *= -1

     def on_touch_move(self, touch):
         if touch.x < self.width/2:
             self.player1.y = touch.y
         if touch.x > self.width/2:
             self.player2.y = touch.y

class GameScreen(Screen,Widget):
     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound=SoundLoader.load('Assets\\song.wav')
        self.sound.loop=False
        self.sound.play()

     def playSound(self):
         sound = SoundLoader.load('Assets\\ButtClick.wav')
         sound.loop = False
         sound.play()

class myMainClass(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='Game'))
        dl = diffLevel(name='diff')
        sm.add_widget(dl)
        ss = secondScreen(name='second')
        sm.add_widget(ss)
        au = aboutUs(name='About')
        sm.add_widget(au)
        ss.serve_ball()
        Clock.schedule_interval(ss.update, 1.0 / 60.0)
        return sm

class pongBall(Widget):
    velocity_x=NumericProperty(0)
    velocity_y=NumericProperty(0)
    velocity=ReferenceListProperty(velocity_x,velocity_y)
    color = ListProperty((1,0,1,0))

    def move(self):
        self.pos=Vector(*self.velocity)+self.pos

if __name__ == '__main__':
    myMainClass().run()