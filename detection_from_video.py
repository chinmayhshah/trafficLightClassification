import numpy as np
import argparse
import cv2
import time
import subprocess
import sys


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
    # cv2.imwrite('masked.png', output_img)
    cv2.imshow('masked.png', output_img)
    # cv2.waitKey(0)
    output_img_blur = cv2.medianBlur(output_img, 5)  # 5 is a fairly small kernel size
    hsv_img = cv2.cvtColor(output_img_blur, cv2.COLOR_BGR2HSV)
    return hsv_img


def mask_blue_color(plain_image):
    img_hsv = cv2.cvtColor(plain_image, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    # lower_blue = np.array([70, 45, 191])
    # upper_blue = np.array([55, 33, 216])
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 225])
    # lower_blue = np.array([90, 31, 4])
    # upper_blue = np.array([220, 88, 50])
    mask0 = cv2.inRange(img_hsv, lower_blue, upper_blue)

    # upper mask (170-180)
    # upper_blue = np.array([18, 18, 255])
    # lower_blue = np.array([43, 43, 231])
    upper_blue = np.array([170, 150, 0])
    lower_blue = np.array([200, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # join masks
    mask = mask0 + mask1
    # set my output img to zero everywhere except my mask
    output_img = plain_image.copy()
    output_img[np.where(mask == 0)] = 0
    # cv2.imwrite('masked.png', output_img)
    # cv2.imshow('masked.png', output_img)
    # cv2.waitKey(0)
    output_img_blur = cv2.medianBlur(output_img, 5)  # 5 is a fairly small kernel size
    hsv_img = cv2.cvtColor(output_img_blur, cv2.COLOR_BGR2HSV)
    return hsv_img


def find_contours(input_plain_image):
    gray_image = cv2.cvtColor(input_plain_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imwrite('final.png', gray_image)
    # cv2.imshow("gray_scale",gray_image)
    # cv2.waitKey(0)
    return contours


def mark_rectangle(original_image, contours):
    imgno = 0
    final_image = ''
    for cnt in contours:
        imgno += 1
        cX = cY = 0
        perimeter = cv2.arcLength(cnt, True)
        M = cv2.moments(cnt)
        try:
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
        except:
            pass
        # skip shape/contour if it is too small or too big
        if perimeter < 100 or perimeter > 1000 or cv2.isContourConvex(cnt):
            # if perimeter < 100 or cv2.isContourConvex(cnt):
            # print "Continue"
            continue
        if cv2.contourArea(cnt) > 100:
            approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
            x, y, w, h = cv2.boundingRect(cnt)

            # colour different shapes
            if len(approx) == 3:
                final_image = original_image[y:y + h, x:x + w]
                # cv2.rectangle(original_image, (x, y), (x + w, y + h), (255, 255, 0), 2)
                # cv2.imwrite("tri_image" +str(imgno)+".png", final_image)

            elif len(approx) == 4:
                final_image = original_image[y:y + h, x:x + w]

                # cv2.imwrite("rec_image" +str(imgno)+".png", final_image)
                # cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            elif len(approx) in range(100, 105):
                final_image = original_image[y:y + h, x:x + w]
                print len(approx)
                # cv2.imwrite("cir_image" +str(imgno)+".png", final_image)
                if cX in range(1000, 1400) and cY in range(100, 200):
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.imshow("detected_image", final_image)
                # cv2.putText(final_image, str(cX)+str(cY), (0, 0), cv2.FONT_HERSHEY_SIMPLEX,
                #             0.5, (255, 255, 255), 2)
                print cX, cY
                cv2.resizeWindow('detected_image', 500, 500)

                cv2.waitKey(5)


            else:
                # cv2.rectangle(original_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                final_image = original_image[y:y + h, x:x + w]

    cv2.imshow("Show", original_image)
    cv2.imshow("rectangles", original_image)
    cv2.imwrite("rect_image.png", original_image)
    # cv2.waitKey(0)


def play_video_file(file_name):
    cap = cv2.VideoCapture(file_name)
    while (cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # time.sleep(0.05)
        # input_image = parse_arguments()
        red_mask_image = mask_red_color(frame)
        blue_mask_image = mask_blue_color(frame)
        contours_red = find_contours(red_mask_image)
        contours_blue = find_contours(blue_mask_image)
        mark_rectangle(frame, contours_red)
        # connect_to_tx1("30-cropped.png")
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def connect_to_tx1(file_name):
    HOST = "ubuntu@10.42.0.69"
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND = "python ~/caffe/python/use_archive.py ~/ACAPROJECT/20170423-190916-a8ef_epoch_10.0.tar.gz" \
              " ~/ACAPROJECT/%s" % file_name
    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >> sys.stderr, "ERROR: %s" % error
    else:
        print [i for i in result]


if __name__ == "__main__":
    # input_image = parse_arguments()
    # red_mask_image = mask_red_color(input_image)
    # blue_mask_image = mask_blue_color(input_image)
    # contours_red = find_contours(red_mask_image)
    # contours_blue = find_contours(blue_mask_image)
    # mark_rectangle(input_image,contours_red)
    # mark_rectangle(input_image,contours_blue)
    play_video_file("cut_video.mp4")
