import glob
import os
import sys
import re

def read():
    img_names = []

    # 拡張子.jpgのファイルを取得する
    img_path = './JPEGImages/*.jpg'
    # imageとpathを取得する
    img_lists = glob.glob(img_path)
    for path in img_lists:
        img_name = os.path.basename(path)
        img_names.append(img_name)
    return img_names

#train data と val data に分ける
def train_val_split(img_name_lists):
    num = len(img_name_lists)
    f_train_val = open("./ImageSets/Main/xmllist.txt", "w")
    f_train = open("./ImageSets/Main/train.txt", "w")
    f_val = open("./ImageSets/Main/val.txt", "w")
    count = 0
    for item in img_name_lists:
        if int(num * 0.8) > count:
            f_train.write(item.replace(".jpg", "") + "\n")
        else:
            f_val.write(item.replace(".jpg", "") + "\n")

        f_train_val.write(item.replace("jpg", "xml") + "\n")
        count += 1
    
    f_train_val.close()
    f_train.close()
    f_val.close()

if __name__ == "__main__":
    img_name_lists = read()
    train_val_split(img_name_lists)
