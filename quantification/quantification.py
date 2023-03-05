import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from crack_distance_center import positive_contours_kp,negative_contours_kp
import os
from utils import Logger


def img_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# img = cv2.imread("/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results/picture/0001.png")
# # img = cv2.resize(img,(224,224)) # 很关键，根据自己需求
# img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# img_gray = img_gray[:,:,None]
# img_show("img",img)
# img_show("img_gray",img_gray)


# 真实图片测试需调用;二值化图片无需调用
# img_blur = cv2.GaussianBlur(img_gray,(9,9),0) # 很关键,单条斜裂缝采用(9*9)
# img_canny = cv2.Canny(img_blur,threshold1=70,threshold2=220)
# print(img_canny.shape)
# res = np.hstack((img_blur,img_canny))
# img_show("GaussianBlur_and_Canny",res)
#
# kernel = np.ones((7,7),np.uint8)
# closing = cv2.morphologyEx(img_canny,cv2.MORPH_CLOSE,kernel)
# img_close = np.hstack((img_canny,closing))
# img_show("imgCanny_and_morphologyExClose",img_close)


# res,thresh = cv2.threshold(closing,127,255,cv2.THRESH_BINARY) # 真实图片调用该行
# res,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY) # 二值图片调用该行
# img_show("img_binary",thresh)

def img_contours(thresh,epoch_logger):
    contours,hierarchy = cv2.findContours(thresh,mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_NONE)
    contours = np.array(contours)

    draw_img = img.copy()
    # original_img = cv2.imread("/home/an/Desktop/lunwen/2.png")
    all_contours = cv2.drawContours(draw_img,contours,-1,(0,255,0),1)
    img_show("all_img_contours",all_contours)



    cnt_area_list = []
    for i in range(0,len(contours)):
        cnt = contours[i]
        draw_img2 = img.copy() # 若去掉，则在之前的draw_img再次绘图，会显示所有轮廓
        res_contours = cv2.drawContours(draw_img2, [cnt], -1, (0, 255, 0), 1)
        cnt_area = cv2.contourArea(cnt)
        print("第{}个轮廓面积:{}".format(i+1,cnt_area))
        cnt_length = cv2.arcLength(cnt,True)
        print("第{}个轮廓周长:{}".format(i+1,cnt_length))
        img_show("the {} contour".format(i+1), res_contours)

        x,y,w,h = cv2.boundingRect(cnt)
        img_rec = cv2.rectangle(draw_img2,(x,y),(x+w,y+h),(0,255,0),1)
        print("第{}个矩形轮廓的长为{},宽为{}".format(i+1,h,cnt_area/h))
        img_show("the {} rectangular box".format(i+1),img_rec)

        rect_area = w*h
        extent = float(cnt_area)/rect_area
        print("轮廓面积与边界矩形比:",extent)
        cnt_area_list.append(cnt_area)


    # 获取最大轮廓
    draw_img3 = img.copy()

    cnt_index = cnt_area_list.index(np.max(cnt_area_list))
    cnt = contours[cnt_index]
    # print("cnt",cnt)
    # print("cnt.shape",cnt.shape)
    main_cnt = cv2.drawContours(draw_img3,[cnt],-1,(0,255,0),1)

    cnt_area = cv2.contourArea(cnt)
    cnt_length = cv2.arcLength(cnt,True)
    print("面积|周长:",cnt_area,cnt_length)



    # 比例尺 10 mm : 32 pixel
    # real_distance = 10
    # pixel_distance = 32
    # scale = real_distance / pixel_distance

    # 最小外接矩形
    rect = cv2.minAreaRect(cnt) # 得到最小外接矩形的(中心(x,y),(宽，高),旋转角度)
    x,y = rect[0]
    h,w = rect[1]
    print("h,w",h,w)
    rotation = rect[2]
    print("最小外接矩形的中心坐标:{},宽：高:{}，旋转角度:{}".format((x, y), (w, h), rotation))
    if w < h and np.abs(rotation) < 45:
        print("-------------选用负轮廓-------------")
        w,h = rect[1]
        distance_pixel, real_distance_pixel, center_x_list = negative_contours_kp(cnt,img.shape)
    elif w > h and np.abs(rotation) > 72: # 70
        print("-------------选用负轮廓-------------")
        w, h = rect[1]
        distance_pixel, real_distance_pixel, center_x_list = negative_contours_kp(cnt, img.shape)
    else:
        print("-------------选用正轮廓-------------")
        distance_pixel, real_distance_pixel, center_x_list = positive_contours_kp(cnt, img.shape)
    box = cv2.boxPoints(rect) # 得到最小外接矩形的4个顶点坐标
    box = np.int0(box) # 在64位操作系统中，int0等价与int64

    cen_length = len(center_x_list)
    center_x_list = np.int0(center_x_list)


    print("面积法|裂缝长度为{},宽度为{}".format(h,cnt_area/h))
    print("周长法|裂缝长度为{},宽度为{}".format(h,(cnt_length/2)-h))
    print("中轴法(像素点)|裂缝长度为{},宽度为{}".format(cen_length,((cnt_area+cnt_length/2)/(cen_length))))
    print("中轴法(欧式距离)|裂缝长度为{},宽度为{}".format(real_distance_pixel,((cnt_area+cnt_length/2)/(real_distance_pixel))))
    # print("中轴法(欧式距离)|裂缝长度为{},宽度为{}".format(real_distance_pixel,((cnt_area)/(real_distance_pixel)))) # 比较真实

    # 添加比例尺，与真实环境对照
    # print("面积法|裂缝长度为{}mm,宽度为{}mm".format(h*scale,cnt_area/h*scale))
    # print("周长法|裂缝长度为{}mm,宽度为{}mm".format(h*scale,((cnt_length/2)-h)*scale))
    # print("中轴法(像素点)|裂缝长度为{}mm,宽度为{}mm".format(cen_length*scale,((cnt_area+cnt_length/2)/(cen_length))*scale))
    # print("中轴法(欧式距离)|裂缝长度为{}mm,宽度为{}mm".format(real_distance_pixel*scale,((cnt_area)/(real_distance_pixel))*scale))


    cv2.putText(draw_img3,"O: {:.2f}".format(rotation),(5,13),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.putText(draw_img3,"L: {:.2f}".format(real_distance_pixel),(5,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    # cv2.putText(draw_img3,"W: {:.2f}".format(((cnt_area)/(real_distance_pixel))),(5,48),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.putText(draw_img3,"W: {:.2f}".format(((cnt_area+cnt_length/2)/(real_distance_pixel))),(5,48),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

    main_cnt = cv2.drawContours(draw_img3,[box],-1,(0,0,255),2)


    for i in tuple(tuple(x) for x in center_x_list):
        main_cnt = cv2.circle(main_cnt,i,0,(100,246,255),0) # 黄色
    img_show("main_cnt_{}".format(i),main_cnt)

    epoch_logger.log({
        'name':file,
        'ORI': rotation,
        'Length': real_distance_pixel,
        'Width': (cnt_area)/(real_distance_pixel),
    })
    cv2.imwrite(output + file, main_cnt)


if __name__ == '__main__':

    # all_path = '/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results/picture/lab/'
    all_path = '/home/hndx/za/香博士/guocheng/seg_crack/initial/'
    # all_path = '/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results/mul_crack/'

    # output = '/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results/picture_output/'
    # output = '/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results/picture/seg_crack_output/'
    output = '/home/hndx/za/香博士/guocheng/seg_crack_output/1/'




    result_path = "/home/hndx/za/香博士/guocheng/image_and_results"
    train_logger = Logger(
        os.path.join(result_path, 'result.log'),
        ['name','ORI', 'Length', 'Width'])
    for file in os.listdir(all_path):
        # if file.endswith('pixel_9_h.png') or file.endswith("pixel_9_h.jpg"):
        if file.endswith('.png') or file.endswith(".jpg"):
            img_path = all_path + file
            print(file)
            img = cv2.imread(img_path)
            img_show("img", img)

            # resize
            # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            # print('Resized Dimensions : ', img.shape)
            # img_show("resized_img", img)

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_gray = img_gray[:, :, None]
            img_show("img_gray", img_gray)




            # 真实图片测试需调用;二值化图片无需调用
            img_blur = cv2.GaussianBlur(img_gray,(5,5),0) # 很关键,单条斜裂缝采用(9*9)
            img_canny = cv2.Canny(img_blur,threshold1=20,threshold2=50) # 70,220 也很重要 20,30
            print(img_canny.shape)
            res = np.hstack((img_blur,img_canny))
            img_show("GaussianBlur_and_Canny",res)

            kernel = np.ones((7,7),np.uint8) # 默认7*7
            closing = cv2.morphologyEx(img_canny,cv2.MORPH_CLOSE,kernel)
            img_close = np.hstack((img_canny,closing))
            img_show("imgCanny_and_morphologyExClose",img_close)

            res,thresh = cv2.threshold(closing,127,255,cv2.THRESH_BINARY) # 真实图片调用该行
            closing = cv2.morphologyEx(img_gray,cv2.MORPH_CLOSE,kernel)
            # res, thresh = cv2.threshold(closing, 50, 255, cv2.THRESH_BINARY)  # 二值图片调用该行
            img_show("img_binary", thresh)

            # result_path = "/home/an/PycharmProjects/pytorch_Concrete_Inspection-master/image_and_results"
            # train_logger = Logger(
            #     os.path.join(result_path, 'result.log'),
            #     ['ORI', 'Length', 'Width'])

            img_contours(thresh,train_logger)
            # cv2.imwrite(output + file, thresh)










