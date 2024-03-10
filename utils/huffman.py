import heapq
from collections import defaultdict
import bitarray
from tqdm import tqdm

def build_huffman_tree(symbol_freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in symbol_freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return heap[0][1:]

def huffman_encode(data):
    symbol_freq = defaultdict(int)
    for row in data:
        for element in row:
            symbol_freq[element] += 1
    
    huffman_tree = build_huffman_tree(symbol_freq)
    
    encoding_dict = {symbol: code for symbol, code in huffman_tree}
    
    encoded_data = []
    for row in data:
        encoded_row = [encoding_dict[element] for element in row]
        encoded_data.append(encoded_row)
    
    return encoded_data, encoding_dict

def huffman_decode(encoded_data, huffman_dict):
    decoded_data = [[0 for _ in range(64)] for _ in range(4096)]
    reverse_huffman_dict = {v: k for k, v in huffman_dict.items()}  # 反转字典，使值变为键
    i = 0
    for row in tqdm(encoded_data):
        col = 0
        # decoded_row = [reverse_huffman_dict[str(code)] for code in row]
        row_split = row[0].split()
        for data in row_split:
            decoded_row = reverse_huffman_dict.get(data)
        # decoded_row = huffman_dict[row]
            decoded_data[i][col] = int(decoded_row)
            col += 1
        i += 1

    return decoded_data
