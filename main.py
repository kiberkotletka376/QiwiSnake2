from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import random

TILE_SIZE = 20

class SnakeEngine(Widget):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.food = (5, 5)
        Clock.schedule_interval(self.update, 0.15)

    def update(self, dt):
        # Логика движения
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Сетка (ограничена размером виджета)
        cols = self.width // TILE_SIZE
        rows = self.height // TILE_SIZE

        if (new_head[0] < 0 or new_head[0] >= cols or 
            new_head[1] < 0 or new_head[1] >= rows or 
            new_head in self.snake):
            self.reset_game()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = (random.randint(0, int(cols) - 1), random.randint(0, int(rows) - 1))
        else:
            self.snake.pop()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.1, 0.1) # Фон игрового поля
            Rectangle(pos=self.pos, size=self.size)
            
            Color(1, 1, 1) # Еда
            Rectangle(pos=(self.x + self.food[0] * TILE_SIZE, self.y + self.food[1] * TILE_SIZE), 
                      size=(TILE_SIZE - 2, TILE_SIZE - 2))

            Color(1, 0.55, 0) # Змейка
            for part in self.snake:
                Rectangle(pos=(self.x + part[0] * TILE_SIZE, self.y + part[1] * TILE_SIZE), 
                          size=(TILE_SIZE - 2, TILE_SIZE - 2))

    def reset_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)

class KiwiSnakeApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        
        # Игровое поле
        self.game = SnakeEngine()
        root.add_widget(self.game)

        # Панель управления (Кнопки)
        controls = GridLayout(cols=3, size_hint_y=0.3)
        
        # Пустая заглушка, Вверх, Пустая заглушка
        controls.add_widget(Widget())
        btn_up = Button(text='Вверх', background_color=(1, 0.55, 0, 1))
        btn_up.bind(on_press=lambda x: self.set_dir(0, 1))
        controls.add_widget(btn_up)
        controls.add_widget(Widget())

        # Лево, Вниз, Право
        btn_left = Button(text='Влево', background_color=(1, 0.55, 0, 1))
        btn_left.bind(on_press=lambda x: self.set_dir(-1, 0))
        controls.add_widget(btn_left)

        btn_down = Button(text='Вниз', background_color=(1, 0.55, 0, 1))
        btn_down.bind(on_press=lambda x: self.set_dir(0, -1))
        controls.add_widget(btn_down)

        btn_right = Button(text='Вправо', background_color=(1, 0.55, 0, 1))
        btn_right.bind(on_press=lambda x: self.set_dir(1, 0))
        controls.add_widget(btn_right)

        root.add_widget(controls)
        return root

    def set_dir(self, x, y):
        # Защита от разворота на 180 градусов
        if (x, y) != (-self.game.direction[0], -self.game.direction[1]):
            self.game.direction = (x, y)

if _name_ == '_main_':
    KiwiSnakeApp().run()
