import numpy as np

# 从data.txt中读取数据，使用np.genfromtxt处理不定长数据
def txt2npz(txt, out):
    data = np.genfromtxt(txt, delimiter='\n')
    np.savez(out, data=data)
