import warnings
import imageio as iio
import argparse
import numpy as np
from numpy import r_
import os

from utils.config_reader import read_config
from utils.matrix import Qy, Qc, Zc
from core.dct import dct2
from utils.cvt_color import COLOR_BGR2YCrCb, COLOR_YCrCb2BGR

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='image input')
    parser.add_argument('data', help='data input')
    parser.add_argument('--config_file', default='./config.yaml', help='train config file path')
    
    args = parser.parse_args()
    return args


def main(args, cfgs):
    im = iio.imread(args.image)
    im = im.astype(float)
    imsize = im.shape # 512 512
    dctcoef = np.zeros(imsize)
    # 构建 8*8 子图 ＆ 处理
    for i in r_[0:imsize[0]:8]:
        for j in r_[:imsize[1]:8]:
            subgraph = im[i:(i+8),j:(j+8)] # 当前子图
            # 零偏置转换 
            subgraph = subgraph - 128
            # dct
            dctcoef[i:(i+8),j:(j+8)] = dct2(subgraph)
    dctcoef_q = np.zeros((4096, 64)) # 每个子图展开后储存在一行中
    rows = 4096
    cols = 64
    rol = 0
    dctcoef_q = [[0 for _ in range(cols)] for _ in range(rows)]
    dctcoef_dc = [[0 for _ in range(cols)] for _ in range(rows)]
    block_num = 0

    # Threshold
    thresh = 0.012
    dct_thresh = dctcoef * (abs(dctcoef) > (thresh*np.max(dctcoef)))
    percent_nonzeros = np.sum(dct_thresh != 0.0 ) / (imsize[0]*imsize[1]*1.0)

    for i in r_[0:imsize[0]:8]:
        for j in r_[:imsize[1]:8]:
            # 子图
            subgraph = dct_thresh[i:(i+8),j:(j+8)]
            # 量化
            dctcoef_quantized = np.round(subgraph / Qy) # 8 * 8

            # 对每一个子图 z 字重排
            # print(rol)
            for a in range(0, 8):
                for b in range(0, 8):
                    dctcoef_q[rol][Zc[a][b]] = dctcoef_quantized[a][b]

            # 符号编码
            # 全零结尾用 a 截断
            for c in range(64-1, -1, -1):
                if dctcoef_q[rol][c] != 0:
                    # dctcoef_q[rol][c + 1] = 'a'
                    # dctcoef_q[rol] = dctcoef_q[rol][: c + 2]
                    dctcoef_q[rol] = dctcoef_q[rol][: c + 1]
                    break
        
        # dc 编码
        # if block_num == 0:
        #     dctcoef_dc[rol][block_num] = dctcoef_q[rol][0]
        # else:
        #     dctcoef_dc[rol][block_num] = dctcoef_dc[rol][block_num] - dctcoef_dc[rol][block_num-1]
        
            rol += 1 # 下一行
    if not os.path.exists(cfgs['data_output_path']):
        os.makedirs(cfgs['data_output_path'])
    # np.savez(cfgs['data_output_path'] + args.data, data=dctcoef_q, dtype=np.float32)

    with open(cfgs['data_output_path'] + args.data, 'w') as file:
        for i in range(4096):
            dctcoef_q[i] = [int(element) for element in dctcoef_q[i]]
            row_str = ' '.join(map(str, dctcoef_q[i]))
            # 将每一行写入文件
            file.write(row_str + '\n')
        
if __name__ == '__main__':
    args = parse_args()
    cfgs = read_config(args.config_file)
    warnings.filterwarnings("ignore")

    main(args, cfgs)