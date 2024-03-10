# DCT 编码器及解码器
## 文件夹构成
- core/ \
    包含dct等算法
- img/ \
    储存图片demo
- tools/ \
    包含工具类函数及系数相关矩阵
- configs.yaml \
    默认输入输出的相关配置
- encode.py \
    编码函数
- decode.py \
    解码函数
## 环境
> 大致需要`numpy`、`argparse`、`PIL`、`os`、`yaml`
```bash
pip install -r requirements.txt
```
## Usage
### config
为了防止生成文件杂乱，可以在 `config.yaml` 中设置默认输出文件的目标文件夹
### 编码
```bash
python encode.py '图片输入' '输出文件名字'
```
e.g.
```bash
python encode.py img/building.bmp data.txt
```
将生成 `data.txt` 于设定的输出文件夹中（如 `data_outputs\data.txt`）
### 解码
```bash
python decode.py '编码文件输入' '图像输出名'
```
e.g.
```bash
python decode.py data_outputs/data.txt img_de.bmp
```
将生成 `img_de.bmp` 于设定的输出文件夹中（如 `img_outputs\img_de.bmp`）
### demo
输入的原始图片及图片编码读取重新解码获取的图片
<p align="center">
  <img src="demo/Lenna_gray.bmp" width="200" alt="Image 1">
  <img src="demo/img_de.bmp" width="200" alt="Image 2">
</p>
