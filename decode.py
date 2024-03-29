import numpy as np
import argparse
from PIL import Image
import os

from core.dct import dct2, idct2
from utils.config_reader import read_config
from utils.matrix import Qy, Qc, Zc

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', default='outputs/img.npz', help='data input')
    parser.add_argument('output', default='img_decode.bmp', help='image output')
    parser.add_argument('--config_file', default='./config.yaml', help='train config file path')
    
    args = parser.parse_args()
    return args

def main(args, cfgs):
    dctcoef_q = []
    with open(args.input, 'r') as file:
        for line in file:
            # 将每一行的字符串按空格分割，并将元素转换为浮点数
            row_list = list(map(float, line.strip().split()))
            # 将这一行的列表添加到还原后的二维列表中
            dctcoef_q.append(row_list)
    # loaded_data = np.load(args.input, allow_pickle=True)
    # dctcoef_q = loaded_data['data']
    decoded_blocks = []
    imsize = (512, 512)
    rows = 4096
    dctcoef_input = dctcoef_q
    for row in range(rows):
        dctcoef_input[row] = dctcoef_input[row][:-1] + [0] * (64 - len(dctcoef_input[row]) + 1)

    for i in range(0, rows):
        decoded_block = np.zeros((8, 8))

        # 逆 z字变换
        for a in range(0, 8):
            for b in range(0, 8):
                decoded_block[a][b] = dctcoef_input[i][Zc[a][b]]

        # Dequantization
        decoded_block = decoded_block * Qy
        # IDCT
        decoded_block = idct2(decoded_block)
        decoded_blocks.append(decoded_block + 128)

    decoded_image = np.zeros((imsize[0], imsize[1]))

    for i, block_num in enumerate(range(0, rows)):
        row_start = (block_num * 8) // imsize[1] * 8
        col_start = (block_num * 8) % imsize[1]
        decoded_image[row_start:row_start + 8, col_start:col_start + 8] = decoded_blocks[i]

    image_pil = Image.fromarray((decoded_image).astype(np.uint8))
    if not os.path.exists(cfgs['img_output_path']):
        os.makedirs(cfgs['img_output_path'])
    image_pil.save(cfgs['img_output_path']+args.output)

if __name__ == '__main__':
    args = parse_args()
    cfgs = read_config(args.config_file)
    # warnings.filterwarnings("ignore")

    main(args, cfgs)