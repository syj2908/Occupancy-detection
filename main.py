import cv2


def compare_img_hist(img1, img2):
    """
    Compare the similarity of two pictures using histogram
        Attention: this is a comparision of similarity, using histogram to calculate

        For example:
         1. img1 and img2 are both 720P .PNG file,
            and if compare with img1, img2 only add a black dot(about 9*9px),
            the result will be 0.999999999953

    :param img1: img1 in MAT format(img1 = cv2.imread(image1))
    :param img2: img2 in MAT format(img2 = cv2.imread(image2))
    :return: the similarity of two pictures
    """
    # Get the histogram data of image 1, then using normalize the picture for better compare
    degree = 0
    H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
    H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
    for i in range(len(H1)):
        if H1[i] != H2[i]:
            degree = degree + (1 - abs(H1[i] - H2[i]) / max(H1[i], H2[i]))
        else:
            degree += 1
    degree = degree / len(H1)
    return degree


def start_detect(gap, threshold):
    #Video you want to process
    path = r"./test.mp4" 
    capture = cv2.VideoCapture(path)
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #position you want to save your video
    videowriter = cv2.VideoWriter(
        r'.\out.avi', cv2.VideoWriter_fourcc(*'XVID'), capture.get(cv2.CAP_PROP_FPS), size)
    ret, background = capture.read()
    fps = capture.get(cv2.CAP_PROP_FPS)
    cv2.destroyAllWindows()
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    pos_point = [(900, 400), (1200, 400), (900, 600), (1200, 600)]
    x_min = pos_point[0][0]
    x_max = pos_point[1][0]
    y_min = pos_point[0][1]
    y_max = pos_point[2][1]
    background_cut = background[int(y_min):int(y_max), int(x_min):int(x_max)]
    flag = False
    count_frame = 0
    warning = False
    warning_count = 0
    while (True):
        for i in range(gap):
            ret, frame = capture.read()
            if (not ret):
                exit(0)
            if (warning):
                cv2.rectangle(frame, pos_point[0],
                              pos_point[3], (0, 0, 255), 6)
                frame = cv2.putText(frame, 'Do not place objects', pos_point[0],
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
                cv2.imshow("frame", frame)
            else:
                cv2.rectangle(frame, pos_point[0],
                              pos_point[3], (0, 255, 0), 6)
                cv2.imshow("frame", frame)
            videowriter.write(frame)
        frame_cut = frame[int(y_min):int(y_max), int(x_min):int(x_max)]
        sim = compare_img_hist(background_cut, frame_cut)
        print(sim)
        if (sim < 0.7):
            count_frame += 1
            if flag is False:
                flag = True
            elif flag is True and (count_frame > int(threshold*fps/gap)):
                warning = True
                warning_count += 1
                warning_name = 'warning'+str(warning_count)+".png"
                cv2.rectangle(frame, pos_point[0],
                              pos_point[3], (0, 0, 255), 6)
                frame = cv2.putText(frame, 'Do not place objects', pos_point[0],
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
                cv2.imwrite(warning_name, frame)
                count_frame = 0
        else:
            warning = False
            flag = False
            count_frame = 0
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
    videowriter.release()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_detect(5, 3)
