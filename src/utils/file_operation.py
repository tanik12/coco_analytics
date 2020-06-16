import glob
import os
import sys
import re
import xml.etree.ElementTree as et

def rename():
    # 拡張子.jpgのファイルを取得する
    xml_path = './Annotations/*.xml'
    img_path = './JPEGImages/*.jpg'
    i = 1
    # image pathを取得する
    file_lists = glob.glob(xml_path)
    img_lists = glob.glob(img_path)
    print('変更前')
    #print(img_lists)
    tmp = set() 
    for img_path in img_lists:
        img_name = os.path.basename(img_path)
        #print(img_name)
        sp_str = img_name.split("_")
        tri_name = img_name.replace(sp_str[-1], "")
        #print(sp_str)
        tmp.add(tri_name)
    print(tmp)
    for file_name in file_lists:
        tree = et.ElementTree(file=file_name)
        root = tree.getroot()
        #print(root)
        img_name = ""
        for fruits in root:
            #print(fruits.tag, ':', fruits.text)
            if fruits.tag == "filename":
                fruits.text = 'COCO_train9999_' + "%09.f.jpg" % i
            elif fruits.tag == "path":
                basename = os.path.basename(fruits.text) #get file name
                #print("GGGG: ", basename)
                for test in tmp:
                     if test in basename: 
                         number = re.sub(r'\D', '', basename.replace(test, ""))
                #print("HHHH: ", number)
                for item in tmp:
                    #print('./images/train9999/' + item + number + ".jpg")
                    #print(os.path.isfile('./images/train9999/' + item + number + ".jpg"))
                    if os.path.isfile('./JPEGImages/' + item + number + ".jpg"):
                        print("Yes!!!")
                        os.rename('./JPEGImages/' + item + number + ".jpg", './JPEGImages/COCO_train9999_' + "%09.f.jpg" % i)
                        #os.rename('./images/train9999/COCO_train9999_' + basename + ".jpg", './images/train9999/COCO_train9999_' + "%06.f.jpg" % i)
                        fruits.text = "./JPEGImages/" + 'COCO_train9999_' + "%09.f.jpg" % i
                        tree.write('./Annotations/' + "%09.f.xml" % i)
                        os.remove(file_name)
                        print("=========================")
                        break
                    else:
                        print("No. file name")
                        continue
        i += 1

if __name__ == "__main__":
    rename()