import turtle
import time
import datetime
from math import cos, sin, radians


class Watch:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Годинник")
        self.screen.bgcolor("white")
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)

        self.theme = "light"  # 'light' or 'dark'
        self.alarm_time = None
        self.alarm_active = False
        self.time_format = 24  # 12 or 24

        self.create_theme_switch()
        self.create_format_switch()
        self.create_alarm_controls()

    def create_theme_switch(self):
        self.theme_btn = turtle.Turtle()
        self.theme_btn.penup()
        self.theme_btn.hideturtle()
        self.theme_btn.goto(300, 250)
        self.theme_btn.write("Змінити тему", align="center", font=("Arial", 12, "normal"))
        self.theme_btn.goto(300, 230)
        self.theme_btn.onclick(self.toggle_theme)
        self.theme_btn.showturtle()
        self.theme_btn.shape("square")
        self.theme_btn.turtlesize(1, 4)

    def create_format_switch(self):
        self.format_btn = turtle.Turtle()
        self.format_btn.penup()
        self.format_btn.hideturtle()
        self.format_btn.goto(300, 200)
        self.format_btn.write("Формат часу", align="center", font=("Arial", 12, "normal"))
        self.format_btn.goto(300, 180)
        self.format_btn.onclick(self.toggle_time_format)
        self.format_btn.showturtle()
        self.format_btn.shape("square")
        self.format_btn.turtlesize(1, 4)

    def create_alarm_controls(self):
        self.alarm_label = turtle.Turtle()
        self.alarm_label.penup()
        self.alarm_label.hideturtle()
        self.alarm_label.goto(300, 150)
        self.alarm_label.write("Будильник", align="center", font=("Arial", 12, "normal"))

        self.alarm_input = turtle.Turtle()
        self.alarm_input.penup()
        self.alarm_input.hideturtle()
        self.alarm_input.goto(300, 130)

        self.alarm_btn = turtle.Turtle()
        self.alarm_btn.penup()
        self.alarm_btn.hideturtle()
        self.alarm_btn.goto(300, 100)
        self.alarm_btn.write("Встановити будильник", align="center", font=("Arial", 12, "normal"))
        self.alarm_btn.goto(300, 80)
        self.alarm_btn.onclick(self.set_alarm)
        self.alarm_btn.showturtle()
        self.alarm_btn.shape("square")
        self.alarm_btn.turtlesize(1, 6)

    def toggle_theme(self, x, y):
        self.theme = "dark" if self.theme == "light" else "light"
        self.update_theme()

    def toggle_time_format(self, x, y):
        self.time_format = 12 if self.time_format == 24 else 24
        self.update_display()

    def set_alarm(self, x, y):
        current_time = datetime.datetime.now()
        alarm_str = self.screen.textinput("Будильник", "Введіть час будильника (HH:MM):")
        try:
            if alarm_str:
                hours, minutes = map(int, alarm_str.split(':'))
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    self.alarm_time = current_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                    self.alarm_active = True
                    self.alarm_input.clear()
                    self.alarm_input.write(f"Будильник: {alarm_str}", align="center", font=("Arial", 12, "normal"))
                else:
                    raise ValueError
        except:
            self.alarm_input.clear()
            self.alarm_input.write("Невірний формат!", align="center", font=("Arial", 12, "normal"))

    def check_alarm(self):
        if self.alarm_active and self.alarm_time:
            current_time = datetime.datetime.now()
            if (current_time.hour == self.alarm_time.hour and
                    current_time.minute == self.alarm_time.minute and
                    current_time.second == 0):
                self.trigger_alarm()

    def trigger_alarm(self):
        self.alarm_active = False
        for _ in range(5):
            self.screen.bgcolor("red")
            self.screen.update()
            time.sleep(0.5)
            self.screen.bgcolor("white" if self.theme == "light" else "black")
            self.screen.update()
            time.sleep(0.5)
        self.update_theme()

    def update_theme(self):
        if self.theme == "light":
            self.screen.bgcolor("white")
            color = "black"
        else:
            self.screen.bgcolor("black")
            color = "white"

        for element in [self.theme_btn, self.format_btn, self.alarm_btn,
                        self.alarm_label, self.alarm_input]:
            element.color(color)

        self.update_display()

    def update_display(self):
        pass

    def run(self):
        while True:
            self.update_display()
            self.check_alarm()
            self.screen.update()
            time.sleep(1)


class AnalogWatch(Watch):
    def __init__(self):
        super().__init__()
        self.face = ClockFace()
        self.hand = ClockHand()

    def update_display(self):
        now = datetime.datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second

        self.hand.clear()

        self.hand.draw_hand(hours * 30 + minutes * 0.5, 100, 8, "blue")  # Годинна
        self.hand.draw_hand(minutes * 6, 150, 4, "green")  # Хвилинна
        self.hand.draw_hand(seconds * 6, 180, 2, "red")  # Секундна

        self.update_digital_display(now)

    def update_digital_display(self, now):
        if hasattr(self, 'digital_display'):
            self.digital_display.clear()
        else:
            self.digital_display = turtle.Turtle()
            self.digital_display.penup()
            self.digital_display.hideturtle()
            self.digital_display.goto(0, -200)

        if self.time_format == 12:
            time_str = now.strftime("%I:%M:%S %p")
        else:
            time_str = now.strftime("%H:%M:%S")

        color = "black" if self.theme == "light" else "white"
        self.digital_display.color(color)
        self.digital_display.write(time_str, align="center", font=("Arial", 24, "bold"))


class DigitalWatch(Watch):
    def __init__(self):
        super().__init__()
        self.display = turtle.Turtle()
        self.display.penup()
        self.display.hideturtle()
        self.display.goto(0, 0)

    def update_display(self):
        now = datetime.datetime.now()
        self.display.clear()

        if self.time_format == 12:
            time_str = now.strftime("%I:%M:%S %p")
        else:
            time_str = now.strftime("%H:%M:%S")

        date_str = now.strftime("%d.%m.%Y")

        color = "black" if self.theme == "light" else "white"
        self.display.color(color)
        self.display.write(f"{time_str}\n{date_str}", align="center", font=("Courier", 36, "bold"))


class ClockFace:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.draw_face()

    def draw_face(self):
        self.t.penup()
        self.t.goto(0, -200)
        self.t.pendown()
        self.t.circle(200)

        for i in range(12):
            angle = radians(i * 30)
            x = 180 * sin(angle)
            y = 180 * cos(angle)

            self.t.penup()
            self.t.goto(x, y - 10)
            self.t.pendown()

            if i % 3 == 0:
                self.t.goto(x, y + 10)
            else:
                self.t.goto(x, y + 5)

            self.t.penup()
            self.t.goto(x * 1.3, y * 1.3 - 10)
            self.t.write(str(12 if i == 0 else i), align="center", font=("Arial", 14, "bold"))


class ClockHand:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)

    def draw_hand(self, angle, length, width, color):
        angle_rad = radians(angle - 90)
        x = length * cos(angle_rad)
        y = length * sin(angle_rad)

        self.t.penup()
        self.t.goto(0, 0)
        self.t.pensize(width)
        self.t.pendown()
        self.t.color(color)
        self.t.goto(x, y)

    def clear(self):
        self.t.clear()


def main():
    print("Оберіть тип годинника:")
    print("1 - Аналоговий")
    print("2 - Цифровий")
    choice = input("Ваш вибір (1/2): ")

    if choice == "1":
        watch = AnalogWatch()
    elif choice == "2":
        watch = DigitalWatch()
    else:
        print("Невірний вибір. Запускаю аналоговий годинник.")
        watch = AnalogWatch()

    watch.run()


if __name__ == "__main__":
    main()