import nmrglue as ng
import numpy as np
import matplotlib.pyplot as mp
from nmrglue import proc_base as pb

qmd_text, data = ng.fileio.varian.read(dir=r"C:\Prog\NMRTQ\1H-CH2-sinc-exitation.fid", fid_file="fid", read_blockhead=True)
fourierdata = ng.process.proc_base.fft_norm(data)
#data2 = ng.proc_autophase.autops(fourierdata, 'peak_minima')
data_acme = ng.proc_autophase.autops(fourierdata, 'acme')
data1 = np.real(data_acme)
#p0, p1 = ng.process.proc_autophase.manual_ps(data_acme)
threshold = 2e2
peaks = ng.peakpick.pick(data1, pthres=threshold, algorithm="downward")
print(peaks)
mp.plot(data1)
mp.show()


