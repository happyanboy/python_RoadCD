import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator,FormatStrFormatter
# plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False

def positive_contours_kp(contours,img_shape):
    # 正轮廓
    contours2 = np.array(contours)
    print("contours:",contours2)
    print("contours_shape:",contours2.shape)
    x = contours2[ :, :, 0]
    y = contours2[ :, :, 1]

    # plt.plot(x, y) # color="#00FF00" 纯绿
    # # plt.xlim(0,224)
    # # plt.ylim(0,224)
    # plt.xlim(0, img_shape[1])
    # plt.ylim(img_shape[0], 0)
    #
    # x_major = MultipleLocator(13)
    # # x_formatter = FormatStrFormatter("%5.1f")
    # x_min = MultipleLocator(1)
    # y_major = MultipleLocator(13)
    # y_min = MultipleLocator(1)
    #
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(x_major)
    # # ax.xaxis.set_major_formatter(x_formatter)
    # ax.xaxis.set_minor_locator(x_min)
    # ax.yaxis.set_major_locator(y_major)
    # ax.yaxis.set_minor_locator(y_min)
    #
    # ax.xaxis.grid(True,which="major",color="#E4E4E4")
    # ax.xaxis.grid(True,which="minor",color="#E4E4E4")
    # ax.yaxis.grid(True, which="major",color="#E4E4E4")
    # ax.yaxis.grid(True, which="minor",color="#E4E4E4")
    #
    #
    # plt.title("正轮廓")
    #
    # plt.show()

    # 反轮廓
    x = contours2[ ::-1, :, 0]
    y = contours2[ ::-1, :, 1]
    # plt.plot(x, y, color="orange")
    # # plt.xlim(0, 224)
    # # plt.ylim(0, 224)
    # plt.xlim(0, img_shape[1])
    # plt.ylim(img_shape[0], 0)
    # plt.title("负轮廓")
    # plt.grid()
    # plt.show()

    k_list = []
    center_x_list = []
    width_list = []

    # for i in range(contours2.shape[0]):
    contours2_ud = contours2[::-1] # 上下反转
    # print("contours2_ud",contours2_ud)
    # print("66",contours2[i].shape[0])
    # quit()
    for j,k in enumerate(range(contours2.shape[0])):
        # print("key point:",j,k)
        # print(contours2[i, j, 0, 1])
        # print(contours2_ud[j, 0, 1])
        # print(j[0,1])
        # print(contours2_ud[j])
        # quit()

        if j == 0:
            # print("正轮廓索引/关键点--> {}/{}".format( j + 1, contours2[ j]))
            while contours2[j,0,1] == contours2_ud[k,0,1]:
                k = k+1
                # print("k:",k)
                k_list.append(k)
            # print("k_list",k_list)
            # quit()

            # print("反轮廓索引/关键点--> {}/{}".format( k-1, contours2_ud[k-1]))
            width_ = contours2_ud[k-1,0,0] - contours2[j,0,0]
            center_x = contours2[j,0,0] + (contours2_ud[k-1,0,0] - contours2[j,0,0])/2
            # print("center_x",center_x)
            center_x_list.append([center_x,contours2[ j, 0, 1]])
            width_list.append([j,width_])
            # print("宽度值:",width_)
            # print("*"*25)

        elif j<((contours2.shape[0])/2 - len(k_list)+1): # 这个1可以去掉
            # print("正轮廓索引/关键点--> {}/{}".format( j + 1, contours2[ j]))
            while contours2[j, 0, 1] != contours2_ud[k , 0, 1]:
                k = k + 1
                # print("k:", k)


            # print("反轮廓索引/关键点--> {}/{}".format( k, contours2_ud[k]))
            # width_ = contours2_ud[k, 0, 0] - contours2[j, 0, 0]
            # center_x = contours2[ j, 0, 0] + (contours2_ud[k, 0, 0] - contours2[ j, 0, 0]) / 2
            # print("center_x", center_x)
            # center_x_list.append([center_x,contours2[j, 0, 1]])
            # width_list.append([j, width_])
            # print("宽度值:", width_)
            # print("*" * 25)

            # print("反轮廓索引/关键点--> {}/{}".format(k, contours2_ud[k]))
            if contours2[j,0,1] == contours2[j-1,0,1] :
                # print("第{}存在重复点".format(j))
                a = 1
                continue

            width_ = contours2_ud[k, 0, 0] - contours2[j, 0, 0]
            center_x = contours2[j, 0, 0] + (contours2_ud[k, 0, 0] - contours2[j, 0, 0]) / 2
            # print("center_x", center_x)
            center_x_list.append([center_x, contours2[j, 0, 1]])
            width_list.append([j, width_])
            # print("宽度值:", width_)
            # print("*" * 25)

    # print(center_x_list)
    # print("关键信息:",len(center_x_list))
    # print("水平宽度:",width_list)
    # print("宽度个数:",len(width_list))


    # 中轴线
    center_x_list = np.array(center_x_list)
    print("center_x_list:",center_x_list)
    print("center_x_list_shape:",center_x_list.shape)
    # print("99",type(center_x_list))

    # x = center_x_list[:,0]
    # y = center_x_list[:,1]
    # plt.plot(x,y)
    # plt.xlim(0, img_shape[1])
    # plt.ylim(img_shape[0], 0)
    # plt.title("中轴线")
    #
    # x_major = MultipleLocator(13)
    # # x_formatter = FormatStrFormatter("%5.1f")
    # x_min = MultipleLocator(1)
    # y_major = MultipleLocator(13)
    # y_min = MultipleLocator(1)
    #
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(x_major)
    # # ax.xaxis.set_major_formatter(x_formatter)
    # ax.xaxis.set_minor_locator(x_min)
    # ax.yaxis.set_major_locator(y_major)
    # ax.yaxis.set_minor_locator(y_min)
    #
    # ax.xaxis.grid(True, which="major", color="#E4E4E4")
    # ax.xaxis.grid(True, which="minor", color="#E4E4E4")
    # ax.yaxis.grid(True, which="major", color="#E4E4E4")
    # ax.yaxis.grid(True, which="minor", color="#E4E4E4")
    #
    # plt.show()


    # 水平宽度
    width_list = np.array(width_list)
    width_list[:,0] = np.arange(len(width_list)) # 很重要
    # print("99",type(center_x_list))

    # x = width_list[:, 0]
    # # print("width_list_x",x)
    # y1 = width_list[:, 1] # 注意，很重要
    # print("y1",y1)
    # y2 =  sum(width_list[:, 1]) / len(width_list)
    # # y3 = real_distance()
    #
    # plt.scatter(x, y1,color="white",marker ="o",edgecolors="#1F77B4",s=15) # 绘制空心圆
    # # plt.scatter(x, y3,color="white",marker ="s",edgecolors="#FF7F0E",s=15,alpha=0.6) # 绘制空心矩形
    # plt.plot(x, y1)
    # # plt.plot(x,y3,alpha=0.6)
    # plt.hlines(y2,x[0],x[-1],colors="red")
    # plt.xlim(0, img_shape[1])
    # plt.ylim(min(y1)-2, max(y1)+2)
    # plt.title("水平宽度")
    # print("宽度总面积:",sum(width_list[:,1]))
    # print("平均水平宽度:", sum(width_list[:, 1]) / len(width_list))
    # print("平均水平宽度(不包括边缘):", (sum((width_list[:, 1])) / len(width_list))*np.sin(47.4263305*np.pi/180)) # 要注意角度的变化
    #
    # x_major = MultipleLocator(13)
    # # x_formatter = FormatStrFormatter("%5.1f")
    # x_min = MultipleLocator(1)
    # y_major = MultipleLocator(1)
    # # y_min = MultipleLocator(1)
    #
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(x_major)
    # # ax.xaxis.set_major_formatter(x_formatter)
    # ax.xaxis.set_minor_locator(x_min)
    # ax.yaxis.set_major_locator(y_major)
    # # ax.yaxis.set_minor_locator(y_min)
    # #
    # # ax.xaxis.grid(True, which="major", color="#E4E4E4")
    # # ax.xaxis.grid(True, which="minor", color="#E4E4E4")
    # ax.yaxis.grid(True, which="major", color="#E4E4E4")
    # # ax.yaxis.grid(True, which="minor", color="#E4E4E4")
    #
    # plt.show()

    # 像素宽度差值
    # width_list = np.array(width_list)
    # width_list[:, 0] = np.arange(len(width_list))  # 很重要
    # x = width_list[:, 0]
    # y1 = width_list[:, 1]  # 注意，很重要
    # print("y1", y1)
    # y2 = real_distance()
    # y = y1 -y2
    # plt.plot(x,y,color="#1F77B4")
    #
    # plt.scatter(x, y, marker="x", edgecolors="#1F77B4", s=15)  # 绘制空心圆
    #
    # plt.plot(x, y)
    # plt.xlim(0, img_shape[1])
    # plt.ylim(min(y) - 2, max(y) + 2)
    # plt.title("像素宽度差值")
    #
    # x_major = MultipleLocator(13)
    # x_min = MultipleLocator(1)
    # y_major = MultipleLocator(1)
    #
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(x_major)
    # ax.xaxis.set_minor_locator(x_min)
    # ax.yaxis.set_major_locator(y_major)
    #
    # # ax.xaxis.grid(True, which="major", color="#E4E4E4")
    # # ax.xaxis.grid(True, which="minor", color="#E4E4E4")
    # ax.yaxis.grid(True, which="major", color="#E4E4E4")
    # # ax.yaxis.grid(True, which="minor", color="#E4E4E4")
    #
    # plt.show()

    #
    # # print("center_x_list",center_x_list)
    # print("x",center_x_list[:,0])
    # print("y",center_x_list[:,1])
    x= center_x_list[:,0]
    y = center_x_list[:,1]
    # 计算像素点欧式距离
    x_dis_square = []
    for i,_ in enumerate(x):

        if i <= len(x)-2:
            c = (np.square(x[i+1] - x[i]))
            # print(c)
            x_dis_square.append(c)
        else:
            pass
    # print("x_dis_square:",x_dis_square)


    y_dis_square = []
    for j,_ in enumerate(y):

        if j <= len(y)-2:
            d = (np.square(y[j+1] - y[j]))
            # print(d)
            y_dis_square.append(d)
        else:
            pass
    # print("y_dis_square:",y_dis_square)

    sum_pixel = np.array(x_dis_square)+np.array(y_dis_square)
    # print("sum_pixel",sum_pixel)
    # print("len:",len(sum_pixel))
    # print("cv",cv)
    distance_pixel = np.sum(np.sqrt(sum_pixel))
    real_distance_pixel = distance_pixel + 1
    # print("像素点欧式距离:",distance_pixel)
    # print("真实欧式距离:",real_distance_pixel)

    return distance_pixel,real_distance_pixel,center_x_list


"""还未修改"""
def negative_contours_kp(contours,img_shape):
    contours2 = np.array(contours)
    print("contours",contours2)
    print("contours_shape",contours2.shape)
    a = np.min(contours2[:,:,0])
    print("min_x:",a)

    end_list = []
    for i in range(contours2.shape[0]-1):

        if contours2[i,0,0] - contours2[i+1,0,0] >=0:
            # print(i)
            end_list.append(contours2[i])
        elif contours2[i,0,0] == np.min(contours2[:,:,0]):
            # print("最小序列值:",i)
            # print("坐标值:",contours2[i])
            end_list.append(contours2[i])
            break

    del end_list[-1]
    end_list = np.array(end_list)
    print("ad",end_list.shape) # (84,1,2)

    index_left = end_list.shape[0]
    contours2_start = contours2[index_left:,:,:]
    print("contours2_start.shape",contours2_start.shape)

    contours2 = np.concatenate((contours2_start,end_list))
    print("contour2",contours2)
    print("contours2.shape:",contours2.shape)
    # quit()






    x = contours2[ :, :, 0]
    y = contours2[ :, :, 1]
    plt.plot(x, y)
    # plt.xlim(0,224)
    # plt.ylim(0,224)
    plt.xlim(0, img_shape[1])
    plt.ylim(img_shape[0], 0)

    x_major = MultipleLocator(13)
    # x_formatter = FormatStrFormatter("%5.1f")
    x_min = MultipleLocator(1)
    y_major = MultipleLocator(13)
    y_min = MultipleLocator(1)

    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major)
    # ax.xaxis.set_major_formatter(x_formatter)
    ax.xaxis.set_minor_locator(x_min)
    ax.yaxis.set_major_locator(y_major)
    ax.yaxis.set_minor_locator(y_min)

    ax.xaxis.grid(True, which="major", color="#E4E4E4")
    ax.xaxis.grid(True, which="minor", color="#E4E4E4")
    ax.yaxis.grid(True, which="major", color="#E4E4E4")
    ax.yaxis.grid(True, which="minor", color="#E4E4E4")

    plt.title("negative counter")
    # plt.grid()
    plt.show()


    # 反轮廓
    x = contours2[ ::-1, :, 0]
    y = contours2[ ::-1, :, 1]
    # plt.plot(x, y, color="orange")
    # plt.xlim(0, img_shape[1])
    # plt.ylim(img_shape[0], 0)
    # plt.title("负轮廓")
    # plt.grid()
    # plt.show()

    k_list = []
    center_x_list = []
    width_list = []

    # for i in range(contours2.shape[0]):  # 轮廓数
    contours2_ud = contours2[ ::-1]
    print("contours2_ud",contours2_ud)
    # print("66",contours2[i].shape[0])
    # quit()
    for j, k in enumerate(range(contours2.shape[0])):  # 关键点数
        # print("key point:",j,k)
        # print("k_contours2",contours2[j])
        # print("k_contours2_ud",contours2_ud[j])
        # print(j[0,1])
        # print(contours2_ud[j])
        # quit()

        if j == 0:
            # print("正轮廓/索引/关键点--> {}/{}/{}".format(i + 1, j + 1, contours2[i, j]))
            print("正轮廓索引/关键点--> {}/{}".format( k, contours2[j]))
            # while contours2[i,j,0,1] == contours2_ud[k,0,1]:
            #     k = k+1
            #     # print("k:",k)
            #     k_list.append(k)
            # print("k_list",k_list)
            # # quit()
            while contours2[j, 0, 0] == contours2_ud[ k, 0, 0]:
                k = k + 1
                # print("k:",k)
                k_list.append(k)
            print("k_list", k_list)
            # quit()

            # print("反轮廓/索引/关键点--> {}/{}/{}".format(i + 1, k, contours2_ud[k]))
            # center_x = contours2[i,j,0,0] + (contours2_ud[k,0,0] - contours2[i,j,0,0])/2
            # print("center_x",center_x)
            # center_x_list.append([center_x,contours2[i, j, 0, 1]])

            # print("反轮廓/索引/关键点--> {}/{}/{}".format(i + 1, k, contours2_ud[k]))
            print("负轮廓索引/关键点--> {}/{}".format( k + 1, contours2_ud[k]))
            center_y = (contours2_ud[k, 0, 1] + contours2[ j, 0, 1]) / 2 #66
            print("center_y", center_y)
            center_x_list.append([contours2[j, 0, 0], center_y])
            # quit()

        # elif j<((contours2[i].shape[0])/2 - len(j_list)+1):
        elif j < ((contours2.shape[0]) / 2 - len(k_list)+1):

            # print("正轮廓/索引/关键点--> {}/{}/{}".format(i + 1, j + 1, contours2[i, j]))
            # while contours2[i, j, 0, 1] != contours2_ud[k, 0, 1]:
            #     k = k + 1
            #     # print("k:", k)
            #
            # print("反轮廓/索引/关键点--> {}/{}/{}".format(i + 1, k, contours2_ud[k]))
            # center_x = contours2[i, j, 0, 0] + (contours2_ud[k, 0, 0] - contours2[i, j, 0, 0]) / 2
            # print("center_x", center_x)
            # center_x_list.append([center_x,contours2[i, j, 0, 1]])

            print("正轮廓索引/关键点--> {}/{}".format( j, contours2[j]))
            while contours2_ud[k, 0, 0] != contours2[ j, 0, 0]:
                k = k + 1
                # print("k:", k)

            if contours2_ud[k,0,0] == contours2_ud[k-1,0,1]:
                a =1
                continue

            print("负轮廓索引/关键点--> {}/{}".format( k + 1, contours2_ud[ k]))
            # center_y = contours2_ud[k, 0, 1] + (-contours2_ud[k, 0, 1] + contours2[ j, 0, 1]) / 2
            center_y = (contours2_ud[k, 0, 1] + contours2[ j, 0, 1])/2
            print("center_y", center_y)
            center_x_list.append([contours2_ud[k, 0, 0], center_y])
    print(center_x_list)
    print("关键信息:", len(center_x_list))
    # quit()

    center_x_list = np.array(center_x_list)
    # print("99",type(center_x_list))
    x = center_x_list[:, 0]
    y = center_x_list[:, 1]
    plt.plot(x, y)
    plt.xlim(0, img_shape[1])
    plt.ylim(img_shape[0], 0)
    plt.show()

    # print("x:",x)
    # print("y",y)

    # 计算像素点欧式距离
    x_dis_square = []
    for i, _ in enumerate(x):

        if i <= len(x) - 2:
            c = (np.square(x[i + 1] - x[i]))
            # print(c)
            x_dis_square.append(c)
        else:
            pass
    print("x_dis_square", x_dis_square)

    y_dis_square = []
    for j, _ in enumerate(y):

        if j <= len(y) - 2:
            d = (np.square(y[j + 1] - y[j]))
            # print(d)
            y_dis_square.append(d)
        else:
            pass
    # print("y_dis_square:",y_dis_square)

    sum_pixel = np.array(x_dis_square) + np.array(y_dis_square)
    # print("len:",len(sum_pixel))
    # print("cv",cv)
    distance_pixel = np.sum(np.sqrt(sum_pixel))
    real_distance_pixel = distance_pixel + 1
    print("像素点欧式距离:", distance_pixel)
    print("真实欧式距离:", real_distance_pixel)

    return distance_pixel,real_distance_pixel,center_x_list

def mul_crack(contours,img_shape,corner_kp):

    # 正轮廓
    contours2 = np.array(contours)
    x = contours2[:, :, 0]
    y = contours2[:, :, 1]
    plt.plot(x, y)
    # plt.xlim(0,224)
    # plt.ylim(0,224)
    plt.xlim(0, img_shape[1])
    plt.ylim(img_shape[0], 0)
    plt.xticks()
    plt.grid()
    plt.show()

    # 反轮廓
    x = contours2[::-1, :, 0]
    y = contours2[::-1, :, 1]
    plt.plot(x, y, color="orange")
    # plt.xlim(0, 224)
    # plt.ylim(0, 224)
    plt.xlim(0, img_shape[1])
    plt.ylim(img_shape[0], 0)
    plt.grid()
    plt.show()

    contours2_ud = contours2[::-1]  # 上下反转
    #
    # for i in range(contours2.shape[0]):
    #     for j in range(corner_kp.shape)
    #     contours2[i]


def real_distance():
    """裂缝真实测量水平宽度"""
    x = np.arange(130)
    # y_test = [ 5 , 5 , 5 , 4 , 4 , 5 , 4 , 5 , 5 , 5 , # 10
    #            5 , 6 , 7 , 7 , 7 , 7 , 7 , 7 , 7 , 7 , # 20
    #            6 , 6 , 5 , 5 , 5 , 4 , 5 , 5 , 6 , 8 , # 30
    #            7 , 7 , 5 , 4 , 4 , 4 , 4 , 4 , 5 , 5 , # 40
    #            6 , 6 , 7 , 8 , 8 , 8 , 9 , 9 , 9 , 8 , # 50
    #            8 , 7 , 6 , 6 , 6 , 6 , 5 , 6 , 6 , 5 , # 60
    #            4 , 5 , 5 , 5 , 6 , 7 , 8 , 9 , 9 , 9 , # 70
    #            9 , 9 , 9 , 8 , 7 , 7 , 7 , 8 , 7 , 7 , # 80
    #            6 , 5 , 5 , 6 , 5 , 6 , 6 , 5 , 6 , 6 , # 90
    #            6 , 7 , 8 , 9 , 8 , 6 , 6 , 6 , 5 , 6 , # 100
    #            6 , 7 , 7 , 9 , 8 , 8 , 9 , 10, 10, 10, # 110
    #            8 , 9 , 9 , 10, 10, 10, 12, 13, 13, 12, # 120
    #            8 , 8 , 7 , 7 , 10,  8,  6,  6,  6,  6] # 130

    # y_test = [5, 5, 5, 4, 4, 5, 5, 6, 6, 6,  # 10
    #           5, 6, 6, 7, 5, 5, 6, 7, 7, 7,  # 20
    #           5, 6, 5, 5, 5, 4, 5, 5, 6, 7,  # 30
    #           7, 5, 5, 4, 4, 4, 4, 4, 5, 5,  # 40
    #           6, 6, 7, 7, 8, 7, 9, 9, 7, 8,  # 50
    #           7, 7, 6, 5, 6, 5, 5, 6, 6, 5,  # 60
    #           4, 5, 5, 5, 6, 7, 8, 9, 10,10,  # 70
    #           10,9, 10,8, 7, 7, 7, 8, 7, 6,  # 80
    #           5, 5, 5, 5, 5, 6, 6, 5, 5, 5,  # 90
    #           6, 6, 8, 9, 8, 6, 6, 5, 4, 5,  # 100
    #           5, 7, 7, 9, 8, 8, 9, 9, 9, 10,  # 110
    #           7, 9, 9, 8, 8, 9, 11, 12, 13, 12,  # 120
    #           7, 8, 7, 7, 10, 8, 5, 5, 5, 5]  # 130

    y_test = [5, 5, 5, 4, 4, 4, 4, 5, 5, 5,  # 10
              5, 7, 7, 7, 7, 7, 7, 7, 7, 6,  # 20
              6, 6, 5, 5, 4, 4, 5, 5, 8, 9,  # 30
              7, 7, 6, 5, 4, 4, 4, 5, 5, 5,  # 40
              6, 7, 7, 8, 8, 9, 9, 9, 8, 8,  # 50
              8, 6, 6, 6, 6, 6, 7, 6, 6, 4,  # 60
              4, 5, 5, 6, 6, 7, 9, 9, 9, 9,  # 70
              9, 8, 8, 7, 7, 7, 8, 9, 7, 6,  # 80
              6, 5, 6, 6, 5, 6, 5, 5, 6, 6,  # 90
              7, 7, 9, 10, 8, 6, 6, 5, 5, 6,  # 100
              6, 7, 9, 9, 8, 8, 10, 11, 10, 10,  # 110
              8, 9, 9, 10, 10, 11, 12, 12, 13, 10,  # 120
              8, 7, 7, 9, 10, 8, 7, 6, 6, 6]  # 130

    # plt.plot(x,y_test)
    # plt.show()
    return y_test


if __name__ == '__main__':
    # real_distance()
    pass