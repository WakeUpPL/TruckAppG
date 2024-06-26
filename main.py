from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.chip import MDChip
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread
from kivy.core.audio import SoundLoader
#from android.permissions import request_permissions, Permission

#df

import time
import re
import socket
import threading

#request_permissions([
#    Permission.INTERNET,
#    Permission.CAMERA,
#    Permission.WRITE_EXTERNAL_STORAGE,
#    Permission.READ_EXTERNAL_STORAGE
#])


class CameraScreen(Screen):
    def on_enter(self):
        self.ids.camera.play = True

    def on_leave(self):
        self.ids.camera.play = False

    def capture_photo(self):
        camera = self.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png(f"photo_{timestr}.png")
        print(f"Photo saved as photo_{timestr}.png")

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 38

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 38

class MDScreen(MDLabel):

    def __init__(self):
        super(MDScreen, self).__init__()


class TruckAppG(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.dialog = None 
        self.sound = SoundLoader.load('data/sound_04683.mp3')  # Завантажуємо звуковий файл

    def on_start(self):
        host = '91.207.60.55'
        #host = 'localhost'
        port = 5555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        # Event to signal the thread to stop
        self.stop_event = threading.Event()

        # Start a separate thread for receiving messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        # Schedule interval for updating the UI
        Clock.schedule_interval(self.gat_text, 1)
        Clock.schedule_interval(self.response, 1)

    def show_dialog(self):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title = "ADMINISTARTION",
            text="Za niedułogo rozpocznieć się załadunek \ rozładunek",
            auto_dismiss=False,  # Додаємо параметр auto_dismiss=False
            buttons=[
                MDFlatButton(
                    text="Close", 
                    on_release=self.close_dialog
                )
            ],
        )
        self.dialog.open()
        if self.sound:
            self.sound.play()  # Відтворюємо звук

    def show_dialog1(self):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title = "ADMINISTARTION",
            text="Załadunek/ rozładunek w trakcie- brak możliwości zamknięcia komunikatu",
            auto_dismiss=False,  # Додаємо параметр auto_dismiss=False
        )
        self.dialog.open()
        if self.sound:
            self.sound.play()  # Відтворюємо звук

    def show_dialog2(self):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title = "ADMINISTARTION",
            text="Załadunek/ rozładunek zakończony, czekaj na dokumenty- brak możliwości zamknięcia komunikatu",
            auto_dismiss=False,  # Додаємо параметр auto_dismiss=False
        )
        self.dialog.open()
        if self.sound:
            self.sound.play()  # Відтворюємо звук

    def show_dialog3(self):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title = "ADMINISTARTION",
            text="Dokumenty gotowe do odbioru- możliwość zamknięcia",
            auto_dismiss=False,  # Додаємо параметр auto_dismiss=False
            buttons=[
                MDFlatButton(
                    text="Close", 
                    on_release=self.close_dialog
                )
            ],
        )
        self.dialog.open()
        if self.sound:
            self.sound.play()  # Відтворюємо звук



    def close_dialog(self, *args):
        self.dialog.dismiss()

    def receive_messages(self):
        while not self.stop_event.is_set():
            try:
                data = self.client.recv(1024)
                if not data:
                    # If no data received, exit the loop
                    break
                message = data.decode('utf-8')
                #self.s(message)
                #print("Received message:", message)  # Debugging statement
                self.root.new_message = message  # Set the new message in the UI
                self.autoscroll()
            except Exception as e:
                print(f"Error receiving messages: {e}")
                break
    
    @mainthread
    def process_server_message(self, message):
        #print("Received server message:", message)  # Додайте цей рядок для виводу повідомлення
        if "@admin: #LOAD" in message:
            self.show_dialog1()
        elif "@admin: #END" in message:
            self.show_dialog2()
        elif "@admin: #DOC" in message:
            self.show_dialog3()


    def autoscroll(self):
        scroll_distance = 100
        scroling = screen_manager.get_screen('chats').scroll_view
        scroling.scroll_y = max(0, scroling.scroll_y - scroll_distance)

    def build(self):
        global screen_manager
        Window.bind(on_request_close=self.on_close)
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Start.kv"))
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Check.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        screen_manager.add_widget(Builder.load_file("Camera.kv"))
        return screen_manager

    def chip_callback(self, chip_number):
        screen_check = screen_manager.get_screen('check')
        chip_attribute_name = f"chip_{chip_number}"
        
        if hasattr(screen_check, chip_attribute_name):
            chip = getattr(screen_check, chip_attribute_name)
            chip.active = not chip.active
        else:
            pass

    def submit_values(self):
        chip_values = []
        for chip_number in range(1, 6):
            chip_attribute_name = f'chip_{chip_number}'
            screen_check = screen_manager.get_screen('check')

            if hasattr(screen_check, chip_attribute_name):
                chip = getattr(screen_check, chip_attribute_name)
                chip_values.append((f'Check {chip_number}', chip.active))
            else:
                print(f"Attribute {chip_attribute_name} not found.")
        
        encoded_chip_values = str(chip_values).encode('utf-8')
        self.client.send(encoded_chip_values)

        submit_button = screen_manager.get_screen('check').submit_button
        submit_button.disabled = True
        for i in range(1, 6):
            chip = getattr(screen_manager.get_screen('check'), f'chip_{i}')
            chip.disabled = True

    def gat_text(self, *args):
        global gat_dock
                # Update the UI on the main thread
        new_message = getattr(self.root, 'new_message', None)
        if new_message:
            # Extract the content after "@admin:" using regular expression
            match = re.search(r'@admin: GAT\s*(.*)', new_message)
            if match:
                gat_dock = match.group(1).strip()
                screen_manager.get_screen('check').gat_text.text = gat_dock
    
    def bot_name(self):
        global driver
        if screen_manager.get_screen('main').bot_name.text != "":
            driver = screen_manager.get_screen('main').bot_name.text
            screen_manager.get_screen('chats').bot_name.text = driver
            screen_manager.get_screen('check').bot_name.text = driver
            screen_manager.get_screen('camera').bot_name.text = driver 
            screen_manager.current = "check"
            try:
                self.client.send(driver.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to the server: {e}")

    def response(self, *args):
        # Update the UI on the main thread
        new_message = getattr(self.root, 'new_message', None)
        if new_message:
            # Extract the content after "@admin:" using regular expression
            match = re.search(r'@admin:\s*(.*)', new_message)
            if match:
                username_content = match.group(1).strip()
                screen_manager.get_screen('chats').chat_list.add_widget(Response(text=username_content, size_hint_x=.50))    
            setattr(self.root, 'new_message', '')  # Clear the new message attribute

    def send(self):
        global size, halign, values
        if screen_manager.get_screen('chats').text_input != "":
            values = screen_manager.get_screen('chats').text_input.text
            if len(values) < 6:
                size = .22
                halign = "center"
            elif len(values) < 11:
                size = .32
                halign = "center"
            elif len(values) < 16:
                size = .45
                halign = "center"
            elif len(values) < 21:
                size = .58
                halign = "center"
            elif len(values) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
                
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=values, size_hint_x=size, halign=halign))
            screen_manager.get_screen('chats').text_input.text = ""
            self.autoscroll()
            try:
                self.client.send(values.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to the server: {e}")

    def close_app(self):
        self.stop_event.set()  # Signal the thread to stop
        self.client.close()  # Close the socket
        self.stop()

    def on_close(self, *args):
        self.close_app()
        return True  # Prevent the default behavior (app exit)   

if __name__ == '__main__':
    TruckAppG().run()
