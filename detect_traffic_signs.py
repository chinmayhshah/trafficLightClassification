import numpy as np
import argparse
import cv2


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    file_name = args.filename
    img = cv2.imread(file_name)
    return img

def mask_red_color(plain_image):
    img_hsv = cv2.cvtColor(plain_image, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    # lower_red = np.array([0, 50, 50])
    # upper_red = np.array([10, 255, 255])
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    # lower_red = np.array([170, 50, 50])
    # upper_red = np.array([180, 255, 255])
    lower_red = np.array([170, 70, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    # join masks
    mask = mask0 + mask1
    # set my output img to zero everywhere except my mask
    output_img = plain_image.copy()
    output_img[np.where(mask == 0)] = 0
    #cv2.imwrite('masked.png', output_img)
    cv2.imshow('masked.png', output_img)
    cv2.waitKey(0)
    output_img_blur = cv2.medianBlur(output_img, 5)  # 5 is a fairly small kernel size
    hsv_img = cv2.cvtColor(output_img_blur, cv2.COLOR_BGR2HSV)
    return hsv_img



def mask_blue_color(plain_image):
    img_hsv = cv2.cvtColor(plain_image, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    # lower_blue = np.array([70, 45, 191])
    # upper_blue = np.array([55, 33, 216])
    lower_blue = np.array([80, 150, 150])
    upper_blue = np.array([170, 255, 225])
    mask0 = cv2.inRange(img_hsv, lower_blue, upper_blue)

    # upper mask (170-180)
    # upper_blue = np.array([18, 18, 255])
    # lower_blue = np.array([43, 43, 231])
    upper_blue = np.array([170, 255, 225])
    lower_blue = np.array([80, 150, 150])
    mask1 = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # join masks
    mask = mask0 + mask1
    # set my output img to zero everywhere except my mask
    output_img = plain_image.copy()
    output_img[np.where(mask == 0)] = 0
    #cv2.imwrite('masked.png', output_img)
    cv2.imshow('masked.png', output_img)
    cv2.waitKey(0)
    output_img_blur = cv2.medianBlur(output_img, 5)  # 5 is a fairly small kernel size
    hsv_img = cv2.cvtColor(output_img_blur, cv2.COLOR_BGR2HSV)
    return hsv_img



def find_contours(input_plain_image):
    gray_image = cv2.cvtColor(input_plain_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imwrite('final.png', gray_image)
    cv2.imshow("gray_scale",gray_image)
    cv2.waitKey(0)
    return contours


def mark_rectangle(original_image, contours):
    # areas = [cv2.contourArea(c) for c in contours]
    #
    # max_index = np.argmax(areas)
    #
    # cnt = contours[max_index]
    for cnt in contours:

        perimeter = cv2.arcLength(cnt, True)
        # skip shape/contour if it is too small or too big
        #if perimeter < 100 or perimeter > 1000 or cv2.isContourConvex(cnt):
        if perimeter < 100 or cv2.isContourConvex(cnt):
            #print "Continue"
            continue


        if cv2.contourArea(cnt) > 100:
            approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
            x, y, w, h = cv2.boundingRect(cnt)

            # colour different shapes
            if len(approx) == 3:
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # elif len(approx) == 4:
            #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            elif len(approx) >= 100:
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 255), 2)
            else:
                # not an interesting shape for us
                pass
            #x, y, w, h = cv2.boundingRect(cnt)
            #cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Show", original_image)
    cv2.imshow("rectangles",original_image)
    cv2.waitKey(0)






if __name__ == "__main__":
    input_image = parse_arguments()
    red_mask_image = mask_red_color(input_image)
    blue_mask_image = mask_blue_color(input_image)
    contours_red = find_contours(red_mask_image)
    contours_blue = find_contours(blue_mask_image)
    mark_rectangle(input_image,contours_red)
    mark_rectangle(input_image,contours_blue)

