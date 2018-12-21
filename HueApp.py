from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import ListProperty
from phue import Bridge
from kivy.storage.jsonstore import JsonStore
from kivy.uix.switch import Switch
import time
import threading
import colorsys
from subprocess import Popen, PIPE
import sys
import fnmatch
import re

Builder.load_string('''
#:import random random.random
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import RiseInTransition kivy.uix.screenmanager.RiseInTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition
<MainScreen>:
    hue: random()
    Image:
        source: 'huedefault.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False
        
        
    Label:
        text: 'Light App For Phillips Hue'
        font_size: '25sp'
        color: [1,0,0,1]

    Button:
        text: 'Auto Connect'
        id: AutoConBut
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .25
        on_release: root.AutoCon()    
    Button:
        text: 'Connect'         
        size_hint: None, None
        pos_hint: {'right': 1}
        size_hint: .5, .25
        
        on_release:
            root.manager.current = 'Connect'
            root.manager.transition.direction = 'left'
    Button:
        text: 'Control screen'
        size_hint: None, None
        pos_hint: {'left': 1}
        size_hint: .5, .25
        on_release:
            root.manager.current = 'Control'
            root.manager.transition.direction = 'right'
    
<ConnectScreen>:
    hue: random()
    Image:
        source: 'huedefault.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False
    GridLayout:
        id: ConScre
        cols: 1
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Main'
            root.manager.transition.direction = 'right'
   
    Button:
        text: 'Connect'
        id: ConBut
        size_hint: None, None
        pos_hint: {'Bottom': 1}
        size_hint: .5, .25
        on_press: root.Connecting()
        on_release: root.Con()
    Spinner:
        text: 'Select An IP'
	
        id: ConSpin
        values: root.SpinnerTest()
        pos_hint: {'center_x': 0.75, 'center_y': 0.125}
        size_hint: 0.5, 0.25
        
        
<ControlScreen>:
    hue: random()
    Image:
        source: 'huedefault.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False
    GridLayout:
        id: Grid
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Main'
            root.manager.transition.direction = 'left'
        

<ChoiceScreen>:
    hue: random()
    Image:
        source: 'huedefault.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False
    GridLayout:
        id: Choice
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Control'
            root.manager.transition.direction = 'up'
    

<BrightScreen>:
    hue: random()
    canvas:
        Color:
            hsv: .1, .1, .1
        Rectangle:
            size: self.size
    GridLayout:
        id: Bright
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Control'
            root.manager.transition.direction = 'up'
<ColorScreen>:
    hue: random()
    canvas:
        Color:
            hsv: .1, .1, .1
        Rectangle:
            size: self.size
    GridLayout:
        id: Colr
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Choice'
            root.manager.transition.direction = 'right'

<TempScreen>:
    hue: random()
    canvas:
        Color:
            hsv: .1, .1, .1
        Rectangle:
            size: self.size
    GridLayout:
        id: Tempr
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Control'
            root.manager.transition.direction = 'up'
<TempScreen1>:
    hue: random()
    canvas:
        Color:
            hsv: .1, .1, .1
        Rectangle:
            size: self.size
    GridLayout:
        id: Tempr
        cols: 2
        padding: [0, 60, 0, 0]
    Button:
        text: 'Back'
        size_hint: None, None
        pos_hint: {'top': 1}
        size_hint: .5, .05
        on_release:
            root.manager.current = 'Choice'
            root.manager.transition.direction = 'left'
''')



#Main App Screen
class MainScreen(Screen):
    global store
    store = JsonStore('StoredIP.json')
    pass

    def AutoCon(self):
        AllIP=[]
        for x in range (2,254):
            BeginIP=['192','.','168','.','1.']
            EndIP=str(x)
            BeginIP.append(EndIP)
            AllIP.append(''.join(BeginIP))
        for x in range (0,253):
            try:
                Popen(["ping", "-c 1", AllIP[x]], stdout = PIPE)
            except:
                pass
        pid = Popen(["cat", "/proc/net/arp"], stdout = PIPE)
        s = pid.communicate()[0]
        s=s.decode("utf-8")
        Address = s.splitlines()[1:]
        AddressIP = list(add.split(None,2)[0] for add in Address if add.strip())
        AddressMac = list(add.split(None,2)[2] for add in Address if add.strip())
        AddressMac = list(add.split(None,2)[1] for add in AddressMac if add.strip())
        for x in range(0, len(AddressMac)):
            if fnmatch.fnmatch(AddressMac[x],'00-17-88*'):
                AutoAddress=AddressIP[x]
                Bridg = Bridge(AutoAddress)
                store.put('IP', name=AutoAddress)
                break
            else:
                AllIP=[]
                for x in range (2,254):
                    BeginIP=['10','.','0','.','0.']
                    EndIP=str(x)
                    BeginIP.append(EndIP)
                    AllIP.append(''.join(BeginIP))
                for x in range (0,253):
                    try:
                        Popen(["ping", "-c 1", AllIP[x]], stdout = PIPE)
                    except:
                        pass
                pid = Popen(["cat", "/proc/net/arp"], stdout = PIPE)
                s = pid.communicate()[0]
                s=s.decode("utf-8")
                Address = s.splitlines()[1:]
                AddressIP = list(add.split(None,2)[0] for add in Address if add.strip())
                AddressMac = list(add.split(None,2)[2] for add in Address if add.strip())
                AddressMac = list(add.split(None,2)[1] for add in AddressMac if add.strip())
                for x in range(0, len(AddressMac)):
                    if fnmatch.fnmatch(AddressMac[x],'00-17-88*'):
                        AutoAddress=AddressIP[x]
                        Bridg = Bridge(AutoAddress)
                        store.put('IP', name=AutoAddress)
                        break

#Connection Screen
class ConnectScreen(Screen):

    #What happens when pressing the Connect button
    def Connecting(self):
        ConLabel = Label(text='Connecting...', pos_hint={'center_x':0.5, 'center_y':0.5})
        self.ids.ConScre.add_widget(ConLabel)

    #What happens when releasing the Connect button        
    def Con(self):
        IPAddress = self.ids.ConSpin.text
        global Bridg
        try:
            # Start a connection to the Hue bridge
            Bridg = Bridge(IPAddress)  
        except:
            #If connection fails
            self.ids.ConScre.clear_widgets()
            ConLabel = Label(text='!!Connection Failed!! Press the button on the Hue bridge', pos_hint={'center_x':0.5, 'center_y':0.5})
            self.ids.ConScre.add_widget(ConLabel)
            pass
        else:
            #If connection succeeds
            self.ids.ConScre.clear_widgets()
            ConLabel = Label(text='Connected to Hue.', pos_hint={'center_x':0.5, 'center_y':0.5})
            self.ids.ConScre.add_widget(ConLabel)
            store.put('IP', name=IPAddress)
            
    def SpinnerTest(self):
        AllIP = []
        #Range of IP addresses
        for x in range(20, 255):
            BeginIP=['10','.','0','.','0.']
            EndIP=str(x)
            BeginIP.append(EndIP)
            AllIP.append(''.join(BeginIP))
        return AllIP
    pass

    def on_leave (self):
        #Clear the screen of messeges when leaving
        self.ids.ConScre.clear_widgets()
        
#Control Screen is for the room selection
class ControlScreen(Screen):
    def on_enter (self):
        self.ids.Grid.clear_widgets()
        #Create groups-
        Bridg = Bridge(store.get('IP')['name'])            
        Brid = Bridg
        G=[]
        for x in range (1, 10):
            G.append(Brid.get_group(x, 'name'))
        for i in range(len(G)):
            if Brid.get_group(G[i], 'on')== True:
                try:
                    Brid.get_group(G[i], 'hue')
                except:
                    button= Button(text=G[i], id=G[i], background_normal='', background_color=[1, 1, 1, 1], color=(0,0,0,1))
                    self.ids.Grid.add_widget(button)
                    button.fbind('on_press', self.ButtonPrint, code=G[i])
                    pass
                else:
                    if Brid.get_group(G[i], 'colormode')=='hs':
                        c=colorsys.hsv_to_rgb(Brid.get_group(G[i], 'hue')/65000, (Brid.get_group(G[i], 'sat')-25)/225, 1)
                        button= Button(text=G[i], id=G[i], background_normal='', background_color=[c[0], c[1], c[2], 1])
                        self.ids.Grid.add_widget(button)
                        button.fbind('on_press', self.ButtonPrint, code=G[i])
                    else:
                        button= Button(text=G[i], id=G[i], background_normal='', background_color=[1, 1, 1, 1], color=(0,0,0,1))
                        self.ids.Grid.add_widget(button)
                        button.fbind('on_press', self.ButtonPrint, code=G[i])
            else:
                button= Button(text=G[i], id=G[i])
                self.ids.Grid.add_widget(button)
                button.fbind('on_press', self.ButtonPrint, code=G[i])
                            
    def on_leave(self):
        #Clear the groups when leaving
        self.ids.Grid.clear_widgets()

    def ButtonPrint(self, obj, code=None):
        #Create a global param for lights reference
        global Light
        Light = code
        screen.current = 'Choice'
        screen.transition.direction = 'down'
        
#Choice Screen goes between room choice and color/temp
class ChoiceScreen(Screen):

    def on_enter(self):
        
        Brid = Bridge(store.get('IP')['name'])
        RoomLabel = Label(text=Light)
        self.ids.Choice.add_widget(RoomLabel)
        try:
            Brid.get_group(Light, 'hue')
        except:
            try:
                Brid.get_group(Light, 'ct')
            except:
                screen.current = 'Bright'
                screen.transition.direction = 'down'
            else:
                screen.current = 'Temp'
                screen.transition.direction = 'down'
        else:
            LightType=Label(text="Hue Color Lamps")
            self.ids.Choice.add_widget(LightType)
            button1= Button(text='Color')
            button2= Button(text='Temperature')
            self.ids.Choice.add_widget(button2)
            button2.bind(on_release=self.TempButton)
            self.ids.Choice.add_widget(button1)
            button1.bind(on_release=self.ColorButton)
            

    def on_leave(self):
        self.ids.Choice.clear_widgets()

    def ColorButton(self, instance):
        screen.current = 'Color'
        screen.transition.direction = 'left'
    def TempButton(self, instance):
        screen.current = 'Temp1'
        screen.transition.direction = 'right'
    pass

#Brightness Only
class BrightScreen(Screen):

    def on_enter(self):
        Brid = Bridge(store.get('IP')['name'])
        button1= Switch(active=Brid.get_group(Light, 'on'), size_hint=(.5, .25))
        #Create Sliders
        self.Temp1 = Slider(value=round((Brid.get_group(Light, 'bri'))/2.54), min=0, max=100)
        self.Temp2 = Slider(value=0, min=0, max=100)
        

        #Create labels for sliders
        self.TempL1 = Label(text='Brightness')
        self.TempL2 = Label(text='Duration')
        

        #Add labels and widgets to the screen
        self.ids.Bright.add_widget(self.TempL1)
        self.ids.Bright.add_widget(self.Temp1)
        self.ids.Bright.add_widget(self.TempL2)
        self.ids.Bright.add_widget(self.Temp2)
        

        self.ids.Bright.add_widget(button1)
        button1.bind(active=self.TurnOn)

    def TurnOn(self, instance, value):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        if value==True:
            Brid.set_group(Light, 'on', True)
        if value==False:
            Brid.set_group(Light, 'on', False)  
            

    def on_touch_up(self, touch):
        #What happens when the screen is touched
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        GroupBr=round(self.Temp1.value*2.54)
        GroupTr=round(self.Temp2.value*3)
        
        Settings = {'bri':GroupBr}  
        Brid.set_group(Light, Settings, transitiontime=GroupTr)

    def on_leave (self):
        #Clear widgets when leaving the screen
        self.ids.Bright.clear_widgets() 


# Temperature Screen
class TempScreen(Screen):

    def on_enter(self):
        Brid = Bridge(store.get('IP')['name'])
        button1= Switch(active=Brid.get_group(Light, 'on'), size_hint=(.5, .25))
        #Create Sliders
        self.Temp1 = Slider(value=round((Brid.get_group(Light, 'bri'))/2.54), min=0, max=100)
        self.Temp2 = Slider(value=0, min=0, max=100)
        self.Temp3 = Slider(value=round(Brid.get_group(Light, 'ct')), min=155, max=500)

        #Create labels for sliders
        self.TempL1 = Label(text='Brightness')
        self.TempL2 = Label(text='Duration')
        self.TempL3 = Label(text='Temperature')

        #Add labels and widgets to the screen
        self.ids.Tempr.add_widget(self.TempL1)
        self.ids.Tempr.add_widget(self.Temp1)
        self.ids.Tempr.add_widget(self.TempL2)
        self.ids.Tempr.add_widget(self.Temp2)
        self.ids.Tempr.add_widget(self.TempL3)
        self.ids.Tempr.add_widget(self.Temp3)

        self.ids.Tempr.add_widget(button1)
        button1.bind(active=self.TurnOn)

    def TurnOn(self, instance, value):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        if value==True:
            Brid.set_group(Light, 'on', True)
        if value==False:
            Brid.set_group(Light, 'on', False)  
            
    def on_touch_up(self, touch):
        #What happens when the screen is touched
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        GroupBr=round(self.Temp1.value*2.54)
        GroupTr=round(self.Temp2.value*3)
        GroupCt=round(self.Temp3.value)
        Settings = {'bri':GroupBr, 'ct':GroupCt}  
        Brid.set_group(Light, Settings, transitiontime=GroupTr)

    def on_leave (self):
        #Clear widgets when leaving the screen
        self.ids.Tempr.clear_widgets()
        
# Temperature Screen
class TempScreen1(Screen):

    def on_enter(self):
        Brid = Bridge(store.get('IP')['name'])
        button1= Switch(active=Brid.get_group(Light, 'on'), size_hint=(.5, .25))
        #Create Sliders
        self.Temp1 = Slider(value=round((Brid.get_group(Light, 'bri'))/2.54), min=0, max=100)
        self.Temp2 = Slider(value=0, min=0, max=100)
        self.Temp3 = Slider(value=round(Brid.get_group(Light, 'ct')), min=155, max=500)

        #Create labels for sliders
        self.TempL1 = Label(text='Brightness')
        self.TempL2 = Label(text='Duration')
        self.TempL3 = Label(text='Temperature')

        #Add labels and widgets to the screen
        self.ids.Tempr.add_widget(self.TempL1)
        self.ids.Tempr.add_widget(self.Temp1)
        self.ids.Tempr.add_widget(self.TempL2)
        self.ids.Tempr.add_widget(self.Temp2)
        self.ids.Tempr.add_widget(self.TempL3)
        self.ids.Tempr.add_widget(self.Temp3)

        self.ids.Tempr.add_widget(button1)
        button1.bind(active=self.TurnOn)

    def TurnOn(self, instance, value):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        if value==True:
            Brid.set_group(Light, 'on', True)
        if value==False:
            Brid.set_group(Light, 'on', False)  
            
    def on_touch_up(self, touch):
        #What happens when the screen is touched
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        GroupBr=round(self.Temp1.value*2.54)
        GroupTr=round(self.Temp2.value*3)
        GroupCt=round(self.Temp3.value)
        Settings = {'bri':GroupBr, 'ct':GroupCt}  
        Brid.set_group(Light, Settings, transitiontime=GroupTr)

    def on_leave (self):
        #Clear widgets when leaving the screen
        self.ids.Tempr.clear_widgets() 



#Color Screen   
class ColorScreen(Screen):

    def on_enter(self):
        Brid = Bridge(store.get('IP')['name'])
        button2= Switch(active=Brid.get_group(Light, 'on'), size_hint=(.5, .25))
        button3= Button(text='Sunset')
        
        self.S1 = Slider(value=round(Brid.get_group(Light, 'bri')/2.54), min=0, max=100)
        self.S2 = Slider(value=0, min=0, max=100)
        self.S3 = Slider(value=round(Brid.get_group(Light, 'hue')), min=0, max=65000)
        self.S4 = Slider(value=round(Brid.get_group(Light, 'sat')), min=25, max=250)
        
        self.L1 = Label(text='Brightness')
        self.L2 = Label(text='Duration')
        self.L3 = Label(text='Hue')
        self.L4 = Label(text='Saturation')

        self.ids.Colr.add_widget(self.L1)
        self.ids.Colr.add_widget(self.S1)
        self.ids.Colr.add_widget(self.L2)
        self.ids.Colr.add_widget(self.S2)
        self.ids.Colr.add_widget(self.L3)
        self.ids.Colr.add_widget(self.S3)
        self.ids.Colr.add_widget(self.L4)
        self.ids.Colr.add_widget(self.S4)
        
        self.ids.Colr.add_widget(button2)
        button2.bind(active=self.TurnOn)

        self.ids.Colr.add_widget(button3)
        button3.bind(on_release=self.SunS1)

    def on_touch_up(self, touch):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        GroupBr=round(self.S1.value*2.54)
        GroupTr=round(self.S2.value*3)
        GroupHu=round(self.S3.value)
        GroupSa=round(self.S4.value)
        Settings = {'bri':GroupBr, 'hue':GroupHu, 'sat':GroupSa}  
        Brid.set_group(Light, Settings, transitiontime=GroupTr)
        
    def TurnOn(self, instance, value):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        if value==True:
            Brid.set_group(Light, 'on', True)
        if value==False:
            Brid.set_group(Light, 'on', False)

    def SunS1(self, instance):
        threading.Thread(target=self.SunS).start()
    def SunS(self):
        Bridg = Bridge(store.get('IP')['name'])
        Brid=Bridg
        Settings = {'bri':100, 'ct':200}
        Brid.set_group(Light, Settings, transitiontime=300)
        time.sleep(30)
        Settings = {'bri':80, 'ct':500}
        Brid.set_group(Light, Settings, transitiontime=300)
        time.sleep(30)
        Settings = {'bri':60, 'hue':0, 'sat':125}
        Brid.set_group(Light, Settings, transitiontime=300)
        time.sleep(30)
        Settings = {'bri':30, 'hue':0, 'sat':250}
        Brid.set_group(Light, Settings, transitiontime=300)
        time.sleep(30)
        Settings = {'bri':0, 'hue':0, 'sat':250}
        Brid.set_group(Light, Settings, transitiontime=10)
        time.sleep(1)
        Brid.set_group(Light, 'on', False)
        
    def on_leave (self):
        self.ids.Colr.clear_widgets()
    pass




screen = ScreenManager()
screen.add_widget(MainScreen(name='Main'))
screen.add_widget(ConnectScreen(name='Connect'))
screen.add_widget(ControlScreen(name='Control'))
screen.add_widget(ColorScreen(name='Color'))
screen.add_widget(TempScreen(name='Temp'))
screen.add_widget(ChoiceScreen(name='Choice'))
screen.add_widget(BrightScreen(name='Bright'))
screen.add_widget(TempScreen1(name='Temp1'))     





class HueApp(App):
        
    def build(self):
        return screen
    
if __name__ == '__main__':
    HueApp().run()
