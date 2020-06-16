import numpy as np
import matplotlib.pyplot as plt

#各ラベル数を確認するためのもの
def confirm_category_num(coco_info):
    label_num = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    ###label_num = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for item in coco_info:
        label_flag = [False, False, False, False, False, False, False, False, False]
        ###label_flag = [False, False, False, False, False, False, False, False, False, False]
        category_nums = np.array(item['category_id'])
        print("AAAAAAAAAAAA: ", category_nums)
        for label in category_nums:
            if label == 1:
                label_flag[0] = True
            elif label == 2:
                label_flag[1] = True
            elif label == 3:
                label_flag[2] = True
            elif label == 4:
                label_flag[3] = True
            elif label == 6:
                label_flag[4] = True
            elif label == 8:
                label_flag[5] = True
            elif label == 10:
                label_flag[6] = True
            ###elif label == 16:
            ###    label_flag[7] = True
            elif label == 17:
                label_flag[7] = True
            elif label == 18:
                label_flag[8] = True
         
        ids = np.where(label_flag)
        for i in ids:
            label_num[ids] += 1
        
    print(label_num)
    #left = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    #label_name = ["person", "bicycle", "car", "motorbike", "bus", "truck", "traffic light", "bird", "cat", "dog"]
    left = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    label_name = ["person", "bicycle", "car", "motorbike", "bus", "truck", "traffic light", "cat", "dog"]
    plt.bar(left, label_num, tick_label=label_name, align="center")
    plt.show()

if __name__ == '__main__':
    pass
