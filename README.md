# DCT 编码器及解码器
## 环境
> 大致需要`numpy`、`argparse`、`PIL`、`os`、`yaml`、`json`、`tqdm`
```bash
pip install -r requirements.txt
```
## Usage
### config
为了防止生成文件杂乱，可以在 `config.yaml` 中设置默认输出文件的目标文件夹
> 分为两个部分 一部分只采用z字形重构，一部分使用霍夫曼编码器
### 只使用基础z字形
#### 编码
```bash
python encode.py *.bmp *.txt
```
e.g.
```bash
python encode.py img/building.bmp data.txt
```
将生成 `data.txt` 于设定的输出文件夹中（如 `data_outputs\data.txt`）
#### 解码
```bash
python decode.py *.txt*.bmp
```
e.g.
```bash
python decode.py data_outputs/data.txt img_de.bmp
```
将生成 `img_de.bmp` 于设定的输出文件夹中（如 `img_outputs\img_de.bmp`）
### 使用霍夫曼编码器
#### 编码
```bash
python encode.py *.bmp *
```
e.g.
```bash
python encode_huffman.py img/building.bmp data
```
将生成 `data.txt` 于设定的输出文件夹中（如 `data_outputs\data.txt`）
#### 解码
```bash
python decode.py * *.bmp
```
e.g.
```bash
python decode_huffman.py data_outputs/data img_de.bmp
```
将生成 `img_de.bmp` 于设定的输出文件夹中（如 `img_outputs\img_de.bmp`）
### 压缩效率
下图从左至右分别为原图、只经过z字转换、经过哈夫曼编码并以二进制储存三者的文件大小
<p align="center">
  <img src="demo\yasuo.png">
</p>

> 只经过z字转换压缩效率大约为 `1.93`\
> 最终经过哈夫曼编码压缩效率大约为 `7.98`
### demo
输入的原始图片及图片编码读取重新解码获取的图片
<p align="center">
  <img src="demo/Lenna_gray.bmp" width="200" alt="Image 1">
  <img src="demo/img_de.bmp" width="200" alt="Image 2">
</p>
