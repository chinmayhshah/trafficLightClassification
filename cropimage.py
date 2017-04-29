import numpy as np
import argparse
import cv2

def parse_args():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help = "path to the image")
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"])
    return image

def print_image(title, filename):
    cv2.imshow(title, filename)
    cv2.waitKey(0)


def mask_image(imageName):
    #image = parse_args(imageName)
    image = cv2.imread(imageName)
    #image=imageName
    r =  [([17, 15, 90], [50, 56, 200])]
    b =  [([90, 31, 4], [220, 88, 50])]
    for (lower, upper) in b:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        print lower, upper
        mask = cv2.inRange(image, lower, upper)
        masked_image = cv2.bitwise_and(image, image, mask = mask)
        # cv2.imwrite('masked.png',output )
        return masked_image


def find_contours(imageName):
    im = mask_image(imageName)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite('final.png', imgray)
    return  imgray



def crop_image(imageName):
    find_contours(imageName)
    #*****#Replace the image that you want to draw on ******
    img = cv2.imread(imageName,0)
    QR_orig = cv2.imread('final.png', 0)
    QR = cv2.imread('final.png', 0)
    mask = np.zeros(QR.shape, np.uint8)

    #blurred = cv2.GaussianBlur(QR, (5, 5), 0)
    #gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    #lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    #thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("Thresh", thresh)
    contours, hierarchy = cv2.findContours(QR, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    QR_final = 0


    #print "The contours are" , contours[1]
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            cv2.drawContours(mask, [cnt], 0, 255,-1)
            x, y, w, h = cv2.boundingRect(cnt)
            roi = mask[y:y + h, x:x + w]
            QR_crop = QR_orig[y:y + h, x:x + w]
            QR_final = QR_crop * (roi / 255)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 5)
    cv2.imwrite('final.png', QR_final)
    cv2.imshow('Demo', img)
    print_image("final", QR_final)
    cv2.waitKey

def crop_original_image():
    pass
if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to the input image")
    args = vars(ap.parse_args())
    #mask_image()
    #find_contours()
    imageName=args["image"]
    crop_image(imageName)