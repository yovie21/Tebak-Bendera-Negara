from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock
import random

# Load the KV file
Builder.load_file('tebakgambar.kv')

questions = [
    {"image": "images/Indonesia.png", "answer": "Indonesia", "choices": ["Indonesia", "Malaysia", "Thailand", "Singapore"]},
    {"image": "images/Jepang.png", "answer": "Jepang", "choices": ["Vietnam", "Filiphina", "Thailand", "Jepang"]},
    {"image": "images/Australia.png", "answer": "Australia", "choices": ["Australia", "Haiti", "Afrika", "Inggris"]},
    {"image": "images/Jerman.png", "answer": "Jerman", "choices": ["Jerman", "Jamaika", "Sudan", "India"]},
    {"image": "images/Argentina.png", "answer": "Argentina", "choices": ["Spain", "Argentina", "Peru", "Kroasia"]},
    {"image": "images/Amerika.png", "answer": "Amerika", "choices": ["Brazil", "Belanda", "Amerika", "United States"]},
    {"image": "images/Korea Utara.png", "answer": "Korea Utara", "choices": ["Singapura", "Indonesia", "Korea Utara", "Malaysia"]},
    {"image": "images/Korea Selatan.png", "answer": "Korea Selatan", "choices": ["Timor Leste", "Palestina", "Malaysia", "Iran", "Korea Selatan"]},
    {"image": "images/Portugal.png", "answer": "Portugal", "choices": ["Jerman", "Spanyol", "Inggris", "Portugal"]},
    {"image": "images/Belanda.png", "answer": "Belanda", "choices": ["Qatar", "Belanda", "China", "Malaysia"]},
    {"image": "images/Saudi Arabia.png", "answer": "Saudi Arabia", "choices": ["Indonesia", "Malaysia", "Saudi Arabia", "Singapore"]},
]
class StartScreen(Screen):
    def start_game(self):
        self.manager.current = 'game'
        self.manager.get_screen('game').start_timer()

class GameWidget(Screen):
    image_source = StringProperty("")
    timer = NumericProperty(0)  # Timer in seconds

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.score = 0
        self.question_count = 0
        self.current_question = None
        self.timer_event = None  # Event for scheduling the timer
        self.load_question()

    def start_timer(self):
        # Start the timer when the game begins
        self.timer = 0
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        # Increment the timer by 1 second
        self.timer += 1
        self.ids.timer_label.text = f"Time: {self.timer}s"

    def load_question(self):
        if self.question_count >= 10:
            self.end_game()
        else:
            self.current_question = random.choice(questions)
            self.image_source = self.current_question["image"]
            self.ids.score_label.text = f"Your Score: {self.score}"
            self.ids.answer_label.text = ""
            choices = self.current_question["choices"]
            random.shuffle(choices)
            self.ids.choice1.text = choices[0]
            self.ids.choice2.text = choices[1]
            self.ids.choice3.text = choices[2]
            self.ids.choice4.text = choices[3]

    def check_answer(self, answer):
        if answer == self.current_question["answer"]:
            self.score += 1
            message = "Benar!"
        else:
            message = "Salah!"
        self.question_count += 1
        self.ids.answer_label.text = message
        self.ids.score_label.text = f"Your Score: {self.score}"
        self.load_question()

    def end_game(self):
        # Stop the timer and display results
        if self.timer_event:
            self.timer_event.cancel()  # Stop updating the timer
        self.manager.get_screen('result').ids.final_score_label.text = f"Your Final Score: {self.score}"
        self.manager.get_screen('result').ids.time_label.text = f"Time Taken: {self.timer} seconds"
        self.manager.current = 'result'

class ResultScreen(Screen):
    pass

class TebakBenderaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameWidget(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    TebakBenderaApp().run()
