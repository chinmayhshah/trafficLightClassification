import Tkinter
import argparse, cv2, numpy as np, os, sys, subprocess, thread, time
import threading
import tkMessageBox


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    file_name = args.filename
    img = cv2.imread(file_name)
    return img


def mask_red_color(plain_image):
    img_hsv = cv2.cvtColor(plain_image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    lower_red = np.array([170, 70, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    mask = mask0 + mask1
    output_img = plain_image.copy()
    output_img[np.where(mask == 0)] = 0
    # cv2.imwrite('masked.png', output_img)
    # cv2.imshow('masked.png', output_img)
    # cv2.waitKey(0)
    output_img_blur = cv2.medianBlur(output_img, 5)  # 5 is a fairly small kernel size
    hsv_img = cv2.cvtColor(output_img_blur, cv2.COLOR_BGR2HSV)
    return hsv_img


def mask_blue_color(plain_image):
    img_hsv = cv2.cvtColor(plain_image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 225])
    mask0 = cv2.inRange(img_hsv, lower_blue, upper_blue)
    upper_blue = np.array([170, 150, 0])
    lower_blue = np.array([200, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_blue, upper_blue)
    mask = mask0 + mask1
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
        if perimeter < 100 or perimeter > 1000 or cv2.isContourConvex(cnt):
            continue
        if cv2.contourArea(cnt) > 100:
            approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)
            x, y, w, h = cv2.boundingRect(cnt)

            # colour different shapes
            if len(approx) == 3:
                final_image = original_image[y:y + h, x:x + w]
            elif len(approx) == 4:
                final_image = original_image[y:y + h, x:x + w]
                print cX, cY
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            elif len(approx) in range(100, 105):
                final_image = original_image[y:y + h, x:x + w]
                print len(approx)
                if cX-cY in range(1000, 1400) and cY in range(100, 200):
                    final_image = original_image[y:y + h, x:x + w]
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.imshow("detected_image", final_image)
                    cv2.imwrite("to_classify.png", final_image )
                    # thread.start_new_thread(connect_to_tx1,("to_classify.png",1))
                    t = threading.Thread(target=connect_to_tx1, args=("to_classify.png",1))
                    t.start()

                print cX, cY
                cv2.resizeWindow('detected_image', 500, 500)
                cv2.waitKey(5)
            else:
                final_image = original_image[y:y + h, x:x + w]
    cv2.imwrite("rect_image.png", original_image)



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


def connect_to_tx1(file_name,delay):
    HOST = "ubuntu@10.42.0.69"
    os.system("scp "+str(file_name)+" ubuntu@10.42.0.69:~/ACAPROJECT ")
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
       print result[2:10]

       root = Tkinter.Tk()
       root.withdraw()
       message_display = result[2] + result[3] + result[4] + result[5]
       tkMessageBox.showinfo(title="Prediction", message= message_display)
       root.destroy()


if __name__ == "__main__":
    input_image = parse_arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    file_name = args.filename
    play_video_file(file_name)
