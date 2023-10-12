import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.clock import Clock


class AudioPlayerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.time_label = Label(text='', font_size=90)
        self.layout.add_widget(self.time_label)

        self.timer_label = Label(text='10:00', font_size=100)
        self.layout.add_widget(self.timer_label)
        
        self.burn = Label(text='Please,\nBurn Yourself!', font_size=100, underline= True)
        self.layout.add_widget(self.burn)
        
        self.audio = SoundLoader.load('ya.wav')
        self.remaining_time = 6  # 10 minutes in seconds
        self.cycle_phase = 1  # 1 for 10-minute countdown, 2 for 2-minute countdown
        self.play_audio = False

        self.update_time()
        Clock.schedule_interval(self.update_time, 1)

        self.light_button = Button(text="Light\nMode")
        self.light_button.bind(on_press=self.Light)
        self.home_button = Button(text="Home")
        self.home_button.bind(on_press=self.home)
        self.reset_button = Button(text="Reset")
        self.reset_button.bind(on_press=self.reset)

        button_layout = BoxLayout()
        button_layout.add_widget(self.light_button)
        button_layout.add_widget(self.home_button)
        button_layout.add_widget(self.reset_button)
        self.layout.add_widget(button_layout)

        return self.layout

    def update_time(self, *args):
        current_time = time.strftime('%I:%M:%S %p')  # Get time in AM/PM format
        self.time_label.text = current_time

        if self.remaining_time >= 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.text = f'{minutes:02d}:{seconds:02d}'

            if self.remaining_time == 0 and not self.play_audio:
                self.audio.play()
                self.play_audio = True
            else:
                self.play_audio = False

            self.remaining_time -= 1
        else:
            self.play_audio = False

            if self.cycle_phase == 1:
                self.remaining_time = 12  # 2 minutes in seconds
                self.cycle_phase = 2
            else:
                self.remaining_time = 6  # 10 minutes in seconds
                self.cycle_phase = 1

    def Light(self, instance):
        self.remaining_time = 600
        self.cycle_phase = 1
        self.timer_label.text = 'Light Mode\nComing Soon'

    def home(self, instance):
        self.stop()
        self.root_window.close()

    def reset(self, instance):
        self.remaining_time = 600
        self.cycle_phase = 1
        self.timer_label.text = '10:00'


if __name__ == '__main__':
    AudioPlayerApp().run()