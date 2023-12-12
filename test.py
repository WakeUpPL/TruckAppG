from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.chip import MDChip
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)  # Відстань між MDChip
        size_hint: None, None
        size: dp(500), dp(500)  # Змініть розмір MDBoxLayout за потребою
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру

        canvas:
            Color:
                rgba: 0.2, 0.2, 0.8, 1  # Змініть значення RGBA на ваш вибір
            Rectangle:
                pos: self.pos
                size: self.size

        MDChip:
            id: chip_1
            text: 'Chip 1'
            on_release: app.chip_callback(1)
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Чорний колір тексту
            size_hint_x: None
            width: dp(120)  # Змініть ширину MDChip за потребою
            size_hint_y: None
            height: dp(48)  # Змініть висоту MDChip за потребою
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру
        MDChip:
            id: chip_2
            text: 'Chip 2'
            on_release: app.chip_callback(2)
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Чорний колір тексту
            size_hint_x: None
            width: dp(120)  # Змініть ширину MDChip за потребою
            size_hint_y: None
            height: dp(48)  # Змініть висоту MDChip за потребою
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру
        MDChip:
            id: chip_3
            text: 'Chip 3'
            on_release: app.chip_callback(3)
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Чорний колір тексту
            size_hint_x: None
            width: dp(120)  # Змініть ширину MDChip за потребою
            size_hint_y: None
            height: dp(48)  # Змініть висоту MDChip за потребою
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру
        MDChip:
            id: chip_4
            text: 'Chip 4'
            on_release: app.chip_callback(4)
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Чорний колір тексту
            size_hint_x: None
            width: dp(120)  # Змініть ширину MDChip за потребою
            size_hint_y: None
            height: dp(48)  # Змініть висоту MDChip за потребою
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру
        MDChip:
            id: chip_5
            text: 'Chip 5'
            on_release: app.chip_callback(5)
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]  # Чорний колір тексту
            size_hint_x: None
            width: dp(120)  # Змініть ширину MDChip за потребою
            size_hint_y: None
            height: dp(48)  # Змініть висоту MDChip за потребою
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # Вирівнювання по центру

    MDRaisedButton:
        text: 'Submit'
        on_release: app.submit_values()
'''

class ChipMDApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def chip_callback(self, chip_number):
        chip = self.root.ids[f'chip_{chip_number}']
        chip.active = not chip.active

    def submit_values(self):
        chip_values = []
        for chip_number in range(1, 6):
            chip = self.root.ids[f'chip_{chip_number}']
            chip_values.append((f'MDChip {chip_number}', chip.active))

        print("Значення чіпів:", chip_values)

if __name__ == '__main__':
    ChipMDApp().run()
