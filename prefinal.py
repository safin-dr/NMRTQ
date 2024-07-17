import nmrglue as ng
import numpy as np
import matplotlib.pyplot as mp
from tkinter import (filedialog,Tk, simpledialog)

import pandas as pd
from matplotlib.widgets import Slider, CheckButtons, RadioButtons
from matplotlib.widgets import (RectangleSelector, TextBox)

"""
def find_integral(data, peaks):
    for i, peak in enumerate(peaks):
        height = data[int(peak["X_AXIS"])]
        x_peak = int(peak["X_AXIS"]) / 1000
"""

#Нахождение интеграла
def onselect_integral(eclick, erelease):
    # Obtain (xmin, xmax, ymin, ymax) values
    # for rectangle selector box using extent attribute.
    global slider_smooth
    global graph_axes
    global fourier_data
    global y
    global x
    global slider_number
    global impulses
    global ready_data_im
    global ready_data_real
    global phases
    global prefinal_frame_real
    global prefinal_frame_im
    global shifts_im
    global shifts_real
    global isreal
    smooth_val = slider_smooth.val

    ready_data_im=[]
    ready_data_real = []
    #Приведение массива в нормальный вид. Тут надо подумать так как после первого подсчета интеграла бетонируются массивы на которых мы считаем интегралы
    #TODO
    if((not(isreal) and (len(ready_data_im)==0)) or (isreal and(len(ready_data_real)==0))):
        for i in range(len(fourier_data)):
            smoothdata = ng.process.proc_base.smo(fourier_data[i], smooth_val)
            data_phase_corrected = ng.process.proc_base.ps(smoothdata, p0=phases[0], p1=phases[1], inv=False)
            data_acme = data_phase_corrected

            dict_base, data_base = ng.process.pipe_proc.cbf(qmd_text, data_acme)
            data1_im = -np.imag(data_base)
            data1_real = np.real(data_base)
            #TODO Проверить тут
            data1_im = data1_im + shifts_im[i]
            data1_real = data1_real + shifts_real[i]
            #TODO !!!!! check ready_data
            if (isreal):
                ready_data_real.append(data1_real)
            else:
                ready_data_im.append(data1_im)
            #TODO y = data1



    extent = rect_selector.extents
    print("Extents: ", extent)
    left = extent[0]
    right = extent[1]
    y_right = extent[3]
    # Zoom the selected part
    # Set xlim range for plot as xmin to xmax
    # of rectangle selector box.
    real_left = int(left*1000)
    real_right = int(right*1000)

    # y_integral = y[real_left:real_right]
    # x_integral = x[real_left:real_right]
    print(left, right)
    list_of_integrals = []
    for i in range(len(fourier_data)):
        if(isreal):
            y =ready_data_real[i]
        else:
            y = ready_data_im[i]
        y_integral = y[real_left:real_right]
        x_integral = x[real_left:real_right]
        integral = np.trapz(y_integral, x_integral)
        list_of_integrals.append(integral)

    if(isreal):
        prefinal_frame_real[impulses[len(impulses)-1]] = list_of_integrals
    else:
        prefinal_frame_im[impulses[len(impulses)-1]] = list_of_integrals
    print(impulses[len(impulses)-1])
    print("start")
    for k in list_of_integrals:
        print(k)
    print("end")
    print(len(list_of_integrals))
    #integral = np.trapz(y_integral, x_integral)

    graph_axes.text(right, y_right, list_of_integrals[int(slider_number.val)-1], ha="center", va="center")
    # Set ylim range for plot as ymin to ymax
    # of rectangle selector box.



def updateGraph():
    '''!!! Функция для обновления графика'''
    # Будем использовать sigma и mu, установленные с помощью слайдеров
    global slider_smooth
    global graph_axes
    global fourier_data
    global y
    global x
    global slider_number
    global impulses
    global phases
    global radiobuttons_is_real
    global isreal

    if (radiobuttons_is_real.value_selected == "Real"):
        isreal=True
    else:
        isreal = False


    # Используем атрибут val, чтобы получить значение слайдеров
    smooth_val = slider_smooth.val
    number_val = slider_number.val

    smooth_data_0 = ng.process.proc_base.smo(fourier_data[0], smooth_val) #массив данных [0] по которому будем выравниваться
    data_acme_0, phases = ng.proc_autophase.autops(smooth_data_0, 'acme', return_phases='true');


    smoothdata = ng.process.proc_base.smo(fourier_data[number_val-1], smooth_val)
    data_phase_corrected = ng.process.proc_base.ps(smoothdata, p0=phases[0], p1=phases[1], inv=False)
    data_acme = data_phase_corrected

    dict_base, data_base = ng.process.pipe_proc.cbf(qmd_text, data_acme)


    data1_im = -np.imag(data_base)
    data1_real = np.real(data_base)
    #TODO Проверить как сдвиг сработал
    data1_im = data1_im+shifts_im[number_val-1]
    data1_real = data1_real+shifts_real[number_val-1]


    x = np.linspace(0, len(data1_im)/1000, len(data1_im))
    if(isreal):
        y = data1_real
    else:
        y = data1_im
    graph_axes.clear()

    graph_axes.plot(x, y)
    graph_axes.axhline(y=0,color='red')
    for i in range(len(impulses)):
        graph_axes.text(2, 300-i*30, impulses[i])
        print(impulses[i])



    mp.draw()

def onChangeValue_smooth(value: np.float64):
    '''!!! Обработчик события изменения значений слайдеров'''
    updateGraph()

def onChangeValue_number(value: np.float64):
    updateGraph()

def clickUpdate():
    #TODO Проблема с прямоугольником, не отображается иногда
    global checkbuttons_grid
    global rect_selector
    global graph_axes
    clicked_integral = checkbuttons_grid.get_status()[0]
    if(clicked_integral):
        rect_selector=RectangleSelector(graph_axes, onselect_integral, button=[1])
    else:
        rect_selector = None

def onCheckClicked(value: str):
    """!!! Обработчик события при нажатии на флажок"""
    clickUpdate()

#Добавление импульса в массив!!!
def on_impulse_clicked(event):
    # Здесь можно добавить ваш код для обработки нажатия кнопки
    # Например, отображение окна для ввода текста
    global impulses
    root = Tk()
    root.withdraw()  # Скрыть окно tkinter
    user_input = simpledialog.askstring("Input", "Введите импульс:")
    impulses.append(user_input)
    print("Введенный текст:", user_input)
    root.destroy()  # Закрыть скрытое окно tkinter
    updateGraph()

def on_baseline(event):
    #TODO добавить глобальные переменные
    global shifts_im
    global shifts_real
    global slider_number
    global isreal
    n = slider_number.val

    root = Tk()
    root.withdraw()  # Скрыть окно tkinter
    shift = float(simpledialog.askstring("Input", "Введите сдвиг:"))
    if(isreal):
        shifts_real[n-1] = shifts_real[n-1]+shift
    else:
        shifts_im[n-1]=shifts_im[n-1]+shift

    print("Сдвиг:", shift)
    root.destroy()  # Закрыть скрытое окно tkinter
    updateGraph()


def save_data_frame(event):
    global prefinal_frame_im
    global prefinal_frame_real
    global isreal

    if(isreal):
        prefinal_frame_real.to_csv("Real_frame", index=False)
    else:
        prefinal_frame_im.to_csv("Im_frame", index=False)


def onRadioButtonsClicked(value: str):
    """!!! Обработчик события при клике по RadioButtons"""
    updateGraph()


prefinal_frame_real = pd.DataFrame()
prefinal_frame_im = pd.DataFrame()

file_dir= filedialog.askdirectory()
qmd_text, data = ng.fileio.varian.read(dir=file_dir, fid_file="fid", read_blockhead=True)
fourier_data = ng.process.proc_base.fft_norm(data)
print("Shape", np.shape(fourier_data))
number_of_gr = np.shape(fourier_data)[0]
shifts_im = np.zeros(number_of_gr)
shifts_real = np.zeros(number_of_gr)
fig, graph_axes = mp.subplots()
graph_axes.grid()

fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)



axes_slider_smooth = mp.axes([0.05, 0.25, 0.85, 0.04])
slider_smooth = Slider(axes_slider_smooth, 'Smooth',
                       valmin=10,
                       valmax=500,
                       valinit=50)

axes_slider_number = mp.axes([0.05, 0.20, 0.85, 0.04])
slider_number = Slider(axes_slider_number, 'Number',
                       valmin=1,
                       valmax=np.shape(fourier_data)[0],
                       valstep=1,
                       valinit=0)

axes_checkbuttons = mp.axes([0.05, 0.01, 0.17, 0.07])
checkbuttons_grid = CheckButtons(axes_checkbuttons, ["Integral"], [False])
#Массив введенных состояний в отсутствии импульсов, последний -тот который будем заполнять
impulses = []

radiobuttons_isreal_ax = fig.add_axes([0.6, 0.05, 0.1, 0.05])
radiobuttons_is_real = RadioButtons(radiobuttons_isreal_ax, ["Real", "Imaginary"])
radiobuttons_is_real.on_clicked(onRadioButtonsClicked)



slider_smooth.on_changed(onChangeValue_smooth)
slider_number.on_changed(onChangeValue_number)
updateGraph()
checkbuttons_grid.on_clicked(onCheckClicked)




button_impulse_ax = fig.add_axes([0.8, 0.1, 0.1, 0.05])
button_impulse = mp.Button(button_impulse_ax, 'Add Data')
button_impulse.on_clicked(on_impulse_clicked)

button_save_ax = fig.add_axes([0.8, 0.15, 0.1, 0.05])
button_save = mp.Button(button_save_ax, 'Save')
button_save.on_clicked(save_data_frame)

button_baseline_ax = fig.add_axes([0.8, 0.05, 0.1, 0.05])
button_baseline = mp.Button(button_baseline_ax, 'Correct Baseline')
button_baseline.on_clicked(on_baseline)



graph_axes.set_ylabel("Spectrum", size = 30)
graph_axes.set_xlabel(r'$\omega$, MHz', size = 30)
mp.show()



