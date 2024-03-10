import cv2

def COLOR_BGR2YCrCb(img):
    img = img.astype('float32')
    B_channel, G_channel, R_channel = cv2.split(img)
    Y_channel = 0.299 * R_channel +  0.587 * G_channel + 0.114 * B_channel
    Cb_channel = 0.5 * R_channel -  0.419 * G_channel - 0.081 * B_channel + 128
    Cr_channel = -0.1687 * R_channel - 0.3313 * G_channel +   0.5 * B_channel + 128
    return cv2.merge([Y_channel, Cr_channel, Cb_channel])

def COLOR_YCrCb2BGR(img):
    img = img.astype('float32')
    Y_channel, Cr_channel, Cb_channel = cv2.split(img)
    B_channel = Y_channel + 1.40200 * (Cr_channel - 128)
    G_channel = Y_channel - 0.34414 * (Cb_channel - 128) - 0.71414 * (Cr_channel - 128)
    R_channel = Y_channel + 1.77200 * (Cb_channel - 128)
    return cv2.merge([B_channel, G_channel, R_channel])

if __name__ == '__main__':
    pass