import nmrglue as ng
import numpy as np
import matplotlib.pyplot as mp
from tkinter import filedialog


def leftpeak(data,leftbound, peakcoord):
    simmetrical_peak = np.append(data[leftbound:int(peakcoord)], np.flip(data[leftbound:int(peakcoord)]))
    for i in range(len(simmetrical_peak)):
        data[leftbound+i]=data[leftbound+i]-simmetrical_peak[i]
    return data

def rightpeak(data, rightbound, peakcoord):
    simmetrical_peak = np.append(np.flip(data[int(peakcoord):rightbound]), data[int(peakcoord):rightbound])
    left_bound = int(2*peakcoord)-rightbound
    for i in range(len(simmetrical_peak)):
        data[left_bound+i]=data[left_bound+i]-simmetrical_peak[i]
    return data


file_dir= filedialog.askdirectory()
print(file_dir)
#r"C:\Prog\NMRTQ\1H-P90.fid"
qmd_text, data = ng.fileio.varian.read(dir=file_dir, fid_file="fid", read_blockhead=True)
fourierdata = ng.process.proc_base.fft_norm(data)
#uc = ng.pipe.make_uc(qmd_text, fourierdata)
#data2 = ng.proc_autophase.autops(fourierdata, 'peak_minima')
smoothdata =ng.process.proc_base.smo(fourierdata, 10)
data_acme = ng.proc_autophase.autops(smoothdata, 'acme')
dict_base, data_base =ng.process.pipe_proc.cbf(qmd_text,data_acme)
data1 = np.real(data_base)
#p0, p1 = ng.process.proc_autophase.manual_ps(data_acme)
threshold = 2e1
peaks = ng.peakpick.pick(data1, pthres=threshold, algorithm="downward")


#data1 = leftpeak(data1, 14500, peaks[11]["X_AXIS"])
#data1=rightpeak(data1,15240, peaks[10]["X_AXIS"])
#data1 = leftpeak(data1, 15050,15085)
#data1 = ng.process.proc_base.smo(data1, 10)
mp.plot(np.linspace(0, len(data1)/1000, len(data1)), data1)


for n, peak in enumerate(peaks):
    height = data1[int(peak["X_AXIS"])]
    x = int(peak["X_AXIS"])/1000
    mp.scatter(x, height, marker="o", color="r", s=100, alpha=0.5)
    mp.text(x, height + 5, n + 1, ha="center", va="center")
mp.show()


