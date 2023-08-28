#!/usr/bin/python3

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, Point
from kivy.properties import ListProperty, NumericProperty

from kivymd.app import MDApp


# from kivy.core.window import Window
SCREEN_RES = [960, 540]    # Set your desired screen size here please
Window.size = (SCREEN_RES[0],SCREEN_RES[1])

from random import randint
from math import sin, cos, radians


class CircleFreq(Widget):
    color = ListProperty([randint(0,255)/255, randint(0,255)/255, randint(0,255)/255, 0.5])
    radius = NumericProperty(100)
    angle = NumericProperty(0)
    freq = NumericProperty(1)
    dot = ListProperty([0,0])
    def __init__(self, **kwargs):
        '''
        Constructor of the widget class
        '''
        self.register_event_type('on_complete_cycle')
        super().__init__(**kwargs)
        self.color =[randint(0,255)/255, randint(0,255)/255, randint(0,255)/255, 0.5]
        # self.radius =randint(50, 200)
        self.dot[0] = 0.5*self.radius*cos(radians(self.angle))
        self.dot[1] = 0.5*self.radius*sin(radians(self.angle))
        # self.freq =randint(1, 3)
        self.bind(freq=self.update_freq)
        self.bind(freq=self.update_freq)
        if (self.freq!=0):
            anim = Animation(angle = 360, duration=2/self.freq) 
            anim += Animation(angle = 360, duration=2/self.freq)
            anim.repeat = True
            anim.start(self)
        
    
    def on_angle(self, item, angle):
        # print(self.ids.dot.pos)
        if angle >= 360:
            item.angle = 0
            self.dispatch('on_complete_cycle')
        self.dot[0] = 0.5*self.radius*cos(radians(item.angle))
        self.dot[1] = 0.5*self.radius*sin(radians(item.angle))

    def update_freq(self, *args):
        '''
        Creates an animation for the circle to rotate smoothly
        '''
        Animation.cancel_all(self)
        if (self.freq!=0):
            anim = Animation(angle = 360, duration=2/self.freq) 
            anim += Animation(angle = 360, duration=2/self.freq)
            anim.repeat = True
            anim.start(self)
    
    def on_complete_cycle(self, *args):
        return

class GUIApp(MDApp):
    '''
    Main GUI app to create the visualizer.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Fourier Visualizer"
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"  # use "Dark" for dark mode
        self.theme_cls.primary_hue = "100"  # "500"

        # Load each kv file for styles
        self.screen = Builder.load_file("stuff.kv")
        # self.screen.add_widget(CircleFreq())

        self.screen.ids.c1.bind(on_complete_cycle=self.clear_canvas_cb)
        Clock.schedule_once(self.start_trace, 0.5)
        return self.screen
    def start_trace(self, *args):
        Clock.schedule_interval(self.draw_trace, 0)
    def clear_canvas_cb(self, *args):
        self.screen.canvas.remove_group('a')
        
    def draw_trace(self, *args):
        pointsize = 1
        with self.screen.canvas:
            Color(1, 1, 1, 0.8, mode='rgba')
            Point(points=self.screen.ids.c5.ids.dot.pos, pointsize=pointsize, group='a')


if __name__ == '__main__':
    app = GUIApp()
    app.run()