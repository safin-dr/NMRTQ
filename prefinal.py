import nmrglue as ng
import numpy as np
import matplotlib.pyplot as mp
from tkinter import filedialog
from matplotlib.widgets import Slider, CheckButtons
from matplotlib.widgets import RectangleSelector
def onselect_function(eclick, erelease):
    # Obtain (xmin, xmax, ymin, ymax) values
    # for rectangle selector box using extent attribute.
    global y
    global x
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
    y_integral = y[real_left:real_right]
    x_integral = x[real_left:real_right]
    print(left, right)
    integral = np.trapz(y_integral, x_integral)

    graph_axes.text(right, y_right, integral, ha="center", va="center")
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
    # Используем атрибут val, чтобы получить значение слайдеров
    smooth_val = slider_smooth.val
    smoothdata = ng.process.proc_base.smo(fourier_data, smooth_val)
    data_acme = ng.proc_autophase.autops(smoothdata, 'acme')
    dict_base, data_base = ng.process.pipe_proc.cbf(qmd_text, data_acme)
    data1 = np.real(data_base)
    threshold = 2e1
    #peaks = ng.peakpick.pick(data1, pthres=threshold, algorithm="downward")
    x = np.linspace(0, len(data1) / 1000, len(data1))
    y = data1
    graph_axes.clear()
    graph_axes.plot(x, y)
    threshold = 2e1
    peaks = ng.peakpick.pick(data1, pthres=threshold, algorithm="downward")
    # for n, peak in enumerate(peaks):
    #     height = data1[int(peak["X_AXIS"])]
    #     x_peak = int(peak["X_AXIS"]) / 1000
    #     graph_axes.scatter(x_peak, height, marker="o", color="r", s=100, alpha=0.5)
    #     graph_axes.text(x_peak, height + 5, n + 1, ha="center", va="center")

    mp.draw()

def onChangeValue(value: np.float64):
    '''!!! Обработчик события изменения значений слайдеров'''
    updateGraph()

def clickUpdate():
    global checkbuttons_grid
    global rect_selector
    global graph_axes
    clicked_integral = checkbuttons_grid.get_status()[0]
    if(clicked_integral):
        rect_selector=RectangleSelector(graph_axes, onselect_function, button=[1])
    else:
        rect_selector = None

def onCheckClicked(value: str):
    """!!! Обработчик события при нажатии на флажок"""
    clickUpdate()

file_dir= filedialog.askdirectory()
qmd_text, data = ng.fileio.varian.read(dir=file_dir, fid_file="fid", read_blockhead=True)
fourier_data = ng.process.proc_base.fft_norm(data)
fig, graph_axes = mp.subplots()
graph_axes.grid()

fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)



axes_slider_smooth = mp.axes([0.05, 0.25, 0.85, 0.04])
slider_smooth = Slider(axes_slider_smooth, 'Smooth',
                       valmin=10,
                       valmax=500,
                       valinit=50)
axes_checkbuttons = mp.axes([0.05, 0.01, 0.17, 0.07])
checkbuttons_grid = CheckButtons(axes_checkbuttons, ["Integral"], [False])
slider_smooth.on_changed(onChangeValue)
updateGraph()
checkbuttons_grid.on_clicked(onCheckClicked)
#rect_selector = RectangleSelector(graph_axes, onselect_function, button=[1])
mp.show()

