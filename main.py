import math
import random
import tkinter


def main():

    root = tkinter.Tk()
    root.title('Buffon\'s Needle Simulator')
    root.geometry('1800x1200+100+100')
    root.resizable(False, False)

    canvas = tkinter.Canvas(root, width=1000, height=1000, bg='white', bd=2)
    canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

    shape = 'line'

    def set_shape(value):
        nonlocal shape
        shape = value
        lbl_needle_shape_value.config(text=shape)

    length = 100.0

    def set_length(value):
        nonlocal length
        length = value
        lbl_needle_length_value.config(text=str(length) + '(%0.3f)' % (length / 500))
        r = length / 500

    def calculate_prop():
        r = length / 500
        p = 0
        if shape == 'line':
            if r <= 1:
                p = 2 / math.pi * r
            else:
                p = 2 / math.pi * (r * (1 - math.sqrt(1-1/(r*r))) - math.asin(1/r)) + 1

        elif shape == 'square':
            if r <= math.sqrt(0.5):
                p = 4 / math.pi * r
            elif r < 1:
                c = math.acos(math.sqrt(0.5) / r)
                p = 4 * c / math.pi + 4 * math.sqrt(2) * r / math.pi * (math.sin(math.pi / 4) - math.sin(c))
            else:
                p = 1

        elif shape == 'triangle':
            if r <= math.sqrt(1/3):
                p = 3 / math.pi * r

        elif shape == 'circle':
            p = min(2 * r, 1)

        lbl_probability_m_value.config(text='%0.3f' % p)

    attempt = 0

    def set_attempt(value):
        nonlocal attempt
        attempt = value
        lbl_attempt_value.config(text=str(attempt))

    on_line = 0

    def set_on_line(value):
        nonlocal on_line
        on_line = value
        lbl_on_line_value.config(text=str(on_line))

    def set_prob():
        if attempt == 0:
            prob = 0
        else:
            prob = on_line / attempt
        lbl_probability_value.config(text='%.3f' % prob)

    def draw_line(length, count=1):
        _on_line = 0
        set_attempt(attempt + count)

        for i in range(0, count):
            y = random.uniform(250, 750)
            x = random.uniform(250, 750)

            if shape == 'line':
                theta = random.uniform(0, math.pi)
                dy = length / 2 * math.sin(theta)
                dx = length / 2 * math.cos(theta)
                online = False
                color = 'blue'
                if dy + y > 750 or y - dy < 250:
                    online = True
                    _on_line += 1
                    color = 'red'
                canvas.create_line(x + dx, y - dy, x - dx, y + dy, fill=color, tag='needle')
            elif shape == 'square':
                theta = random.uniform(0, math.pi / 2)
                l2 = length * math.sqrt(2) / 2
                dcos = math.cos(theta) * l2
                dsin = math.sin(theta) * l2
                color = 'blue'
                if y + max(dcos, dsin) > 750 or y - max(dcos, dsin) < 250:
                    online = True
                    _on_line += 1
                    color = 'red'
                canvas.create_line(x + dcos, y + dsin, x - dsin, y + dcos, fill=color, tag='needle')
                canvas.create_line(x - dsin, y + dcos, x - dcos, y - dsin, fill=color, tag='needle')
                canvas.create_line(x - dcos, y - dsin, x + dsin, y - dcos, fill=color, tag='needle')
                canvas.create_line(x + dsin, y - dcos, x + dcos, y + dsin, fill=color, tag='needle')
            elif shape == 'circle':
                color = 'blue'
                if y + length > 750 or y - length < 250:
                    _on_line += 1
                    color = 'red'
                canvas.create_oval(x - length, y - length, x + length, y + length, outline=color, tag='needle')
            elif shape == 'triangle':
                theta = random.uniform(0, math.pi / 3 * 2)
                l3 = length * math.sqrt(3) / 3

        set_on_line(_on_line + on_line)
        set_prob()

    def clear_canvas():
        canvas.delete('needle')
        set_attempt(0)
        set_on_line(0)
        length_str = entry.get()
        set_shape(rv_1.get())
        try:
            val = float(length_str)
        except TypeError:
            print(f'{length_str} is not a number')
        else:
            set_length(val)
        calculate_prop()
        set_prob()

    line1 = canvas.create_line(0, 250, 1000, 250)
    line2 = canvas.create_line(0, 750, 1000, 750)

    lblframe_button = tkinter.LabelFrame(root, text='Buttons')
    lblframe_button.grid(row=0, column=1, padx=10)
    button = tkinter.Button(lblframe_button, text='바늘 던지기', bg='darkgray', width=15, command=lambda: draw_line(length))
    button.grid(row=0, column=0, pady=2)

    button = tkinter.Button(lblframe_button, text='바늘 던지기 100회', bg='darkgray', width=15, command=lambda: draw_line(length, 100))
    button.grid(row=1, column=0, pady=2)

    button = tkinter.Button(lblframe_button, text='바늘 던지기 1000회', bg='darkgray', width=15, command=lambda: draw_line(length, 1000))
    button.grid(row=3, column=0, pady=2)

    button = tkinter.Button(root, text='재설정', bg='darkgray', width=15, command=clear_canvas)
    button.grid(row=0, column=2, padx=10)

    lblframe_info = tkinter.LabelFrame(root, text='INFO')
    lblframe_info.grid(row=0, column=3, padx=10)

    lbl_needle_length = tkinter.Label(lblframe_info, text='바늘 길이:')
    lbl_needle_length.grid(row=0, column=0)
    lbl_needle_length_value = tkinter.Label(lblframe_info, text=str(length) + '(%0.3f)' % (length / 500))
    lbl_needle_length_value.grid(row=0, column=1)

    lbl_needle_shape = tkinter.Label(lblframe_info, text='바늘 모양:')
    lbl_needle_shape.grid(row=1, column=0)
    lbl_needle_shape_value = tkinter.Label(lblframe_info, text=shape)
    lbl_needle_shape_value.grid(row=1, column=1)

    lbl_attempt = tkinter.Label(lblframe_info, text='시행 횟수:')
    lbl_attempt.grid(row=2, column=0)
    lbl_attempt_value = tkinter.Label(lblframe_info, text='0')
    lbl_attempt_value.grid(row=2, column=1)

    lbl_on_line = tkinter.Label(lblframe_info, text='선 위의 바늘 수:')
    lbl_on_line.grid(row=3, column=0)
    lbl_on_line_value = tkinter.Label(lblframe_info, text='0')
    lbl_on_line_value.grid(row=3, column=1)

    lbl_probability = tkinter.Label(lblframe_info, text='통계적 확률')
    lbl_probability.grid(row=4, column=0)
    lbl_probability_value = tkinter.Label(lblframe_info, text='0.000')
    lbl_probability_value.grid(row=4, column=1)

    lbl_probability_m = tkinter.Label(lblframe_info, text='수학적 확률')
    lbl_probability_m.grid(row=5, column=0)
    lbl_probability_m_value = tkinter.Label(lblframe_info, text='0.127')
    lbl_probability_m_value.grid(row=5, column=1)

    lbl_length = tkinter.Label(root, text='바늘 길이', fg='black')
    lbl_length.grid(row=1, column=1, padx=10)

    entry = tkinter.Entry(root)
    entry.grid(row=1, column=2, padx=10)
    entry.insert(0, str(length))

    lblframe_radio = tkinter.LabelFrame(root, text='바늘 종류')
    lblframe_radio.grid(row=1, column=3)
    rv_1 = tkinter.StringVar()

    radio_line = tkinter.Radiobutton(lblframe_radio, text='선분', value='line', variable=rv_1)
    radio_line.select()
    radio_line.grid(row=0, column=0)

    radio_circle = tkinter.Radiobutton(lblframe_radio, text='원', value='circle', variable=rv_1)
    radio_circle.grid(row=1, column=0)

    radio_square = tkinter.Radiobutton(lblframe_radio, text='정사각형', value='square', variable=rv_1)
    radio_square.grid(row=2, column=0)

    root.mainloop()


if __name__ == '__main__':
    main()