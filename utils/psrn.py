import cv2
import numpy as np

def calculate_psnr(original_image, compressed_image):
    original = cv2.imread(original_image)
    compressed = cv2.imread(compressed_image)

    if original.shape != compressed.shape:
        raise ValueError("两张图片需要相同的尺寸")

    # MSE
    mse = np.mean((original - compressed)**2)

    # Calculate PSNR using the formula: PSNR = 10 * log10(MAX^2 / MSE)
    max_pixel_value = 255  # Assuming 8-bit images
    psnr = 10 * np.log10((max_pixel_value**2) / mse)

    return psnr

if __name__ == "__main__":
    original_image_path = "demo/Lenna_gray.bmp"
    compressed_image_path = "demo/img_de.bmp"

    psnr_value = calculate_psnr(original_image_path, compressed_image_path)
    print(f"PSNR: {psnr_value} dB")
