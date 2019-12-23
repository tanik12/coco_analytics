import json
from pycocotools.coco import COCO
import xml.etree.ElementTree as et
import xml.dom.minidom as md
import numpy as np
import os
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

def cofirm_dir():
    current_path = os.getcwd()
    dirpath_anno = '/annotation'
    dirpath_debug = '/debug'

    if not os.path.isdir(current_path + dirpath_anno):
        os.mkdir("." + dirpath_anno)
    if not os.path.isdir(current_path + dirpath_debug):
        os.mkdir("." + dirpath_debug)

def get_ob_index(datapath, categories):
    with open(datapath, "rb") as file:
            dataset = json.load(file)
    # initialize COCO api for instance annotations
    coco = COCO(datapath)

    list_idx = []
    count = 0
    for img_idx in dataset['images']:
        s_dict = {}
        anno_idxes = []
        bboxes = []
        category_idxes = []

        #画像名から番号を取得
        #coco.getAnnIds(画像番号)により、画像番号に紐づいたアノテーション番号を取得できる.
        file_number = img_idx['file_name'].replace("COCO_train2014_", "").replace(".jpg", "").lstrip("0")
        annos_num = coco.getAnnIds(int(file_number)) #指定した画像ID に対応するアノテーション ID を取得する。
        print("anno_num: ", annos_num)
        
        for anno_num in annos_num:
            anno_info = coco.loadAnns(anno_num) #loadAnns で指定したアノテーション ID の情報を取得する。
            if anno_info[0]["category_id"] in categories: #欲しいカテゴリがあるかどうか
                anno_idxes.append(anno_num) #annotationの番号を入れる。
        if len(anno_idxes) < 1: #欲しいカテゴリがないのであればスキップ
            print("non indx")
            print("===============")
            continue
        else:           #欲しいカテゴリがあれば、元imageの[高さ, 幅]とannotationからbboxとcategory_idを取得
            height = img_idx["height"]
            width = img_idx["width"]
            for k in anno_idxes:
                bbox = coco.loadAnns(k)[0]['bbox']
                bbox[2] = bbox[0] + bbox[2]
                bbox[3] = bbox[1] + bbox[3]

                #bboxes.append(coco.loadAnns(k)[0]['bbox']) #bboxの中身が[xmin, ymin, width, height]の場合(COCO形式で扱いたいとき)
                bboxes.append(bbox)                         #bboxの中身が[xmin, ymin, xmax, ymax]の場合(VOC形式で扱いたい時)
                category_idxes.append(coco.loadAnns(k)[0]['category_id'])
        count += 1
        print("ano_num2: ", anno_idxes)
        print("\n")

        #imageに紐づいた情報を取得.
        #画像名、画像に紐づいたアノテーションの番号、元画像の[高さ, 幅]、annotationに紐づくbboxes、category_idに紐づいたbboxを辞書に入れる.
        s_dict["img_number"] = img_idx['file_name']
        s_dict["anno_dix"] = anno_idxes
        s_dict["img_hw"] = [height, width]
        s_dict["bboxes"] = bboxes
        s_dict["category_id"] = category_idxes
        list_idx.append(s_dict)
        print("================")
        if count == 10:
            return list_idx
def make_xml(coco_info, label_dic):
    #coco形式のアノテーション情報からvoc形式のアノテーションを作成。
    #make_xml関数の引数は、get_ob_index関数で取得したアノテーション情報と変数label_dicの2つ。
    #アノテーションは、ファイル名 ＋ .xmlで保存される。
    for item in coco_info:
        root = et.Element('annotation')
    
        folder = et.SubElement(root, 'folder')
        folder.text = 'VOCORIGINAL'
        filename = et.SubElement(root, 'filename')
        img_name = item['img_number']
        filename.text = img_name
        filepath = et.SubElement(root, 'path')
        filepath.text = "/home/gisen/git/coco_analytics/annotation/" + img_name
        source = et.SubElement(root, 'source')
        database = et.SubElement(source, 'database')
        database.text = 'Unknown'
        img_size = et.SubElement(root, 'size')
        img_width = et.SubElement(img_size, 'width')
        img_width.text = str(item['img_hw'][1])
        img_height = et.SubElement(img_size, 'height')
        img_height.text = str(item['img_hw'][0])
        img_depth = et.SubElement(img_size, 'depth')
        img_depth.text = "3"
        img_seg = et.SubElement(root, 'segmented')
        img_seg.text = "0"
    
        #objectの数だけbboxを取得する。
        for num in range(len(item['category_id'])):
            img_obj = et.SubElement(root, 'object')
            obj_name = et.SubElement(img_obj, 'name')
            obj_name.text = str(label_dic[item['category_id'][num]])
            obj_pose = et.SubElement(img_obj, 'pose')
            obj_pose.text = "Unspecified"
            truncated = et.SubElement(img_obj, 'truncated')
            truncated.text = "0"
            difficult = et.SubElement(img_obj, 'difficult')
            difficult.text = "0"
        
            bndbox = et.SubElement(img_obj, 'bndbox')
            bndbox_xmin = et.SubElement(bndbox, 'xmin')
            bndbox_xmin.text = str(round(item['bboxes'][num][0]))
            bndbox_ymin = et.SubElement(bndbox, 'ymin')
            bndbox_ymin.text = str(round(item['bboxes'][num][1]))
            bndbox_xmax = et.SubElement(bndbox, 'xmax')
            bndbox_xmax.text = str(round(item['bboxes'][num][2]))
            bndbox_ymax = et.SubElement(bndbox, 'ymax')
            bndbox_ymax.text = str(round(item['bboxes'][num][3]))
    
        # 文字列パースを介してminidomへ移す
        document = md.parseString(et.tostring(root))
        file = open("./annotation/" + img_name.replace(".jpg", ".xml"), 'w')
        # エンコーディング、改行、全体のインデント、子要素の追加インデントを設定しつつファイルへ書き出し
        document.writexml(file, encoding='utf-8', newl='\n', indent='', addindent='  ')
        file.close()
        #xmlタグを消した
        tree = et.parse("./annotation/" + img_name.replace(".jpg", ".xml")) 
        tree.write("./annotation/" + img_name.replace(".jpg", ".xml"))

def one_detection_debug():
    img_path = "./debug/COCO_train2014_000000392136.jpg"
    img = cv2.imread(img_path)

    # 長方形（水色の長方形）
    img = cv2.rectangle(img,(19,20),(289,249),(255,255,0),3)
    img = cv2.rectangle(img,(295,110),(445,326),(255,255,0),3)
    img = cv2.rectangle(img,(278,161),(314,265),(255,255,0),3)
    img = cv2.rectangle(img,(274,176),(288,187),(255,255,0),3)
    img = cv2.rectangle(img,(411,171),(426,198),(255,255,0),3)
    img = cv2.rectangle(img,(403,167),(469,325),(255,255,0),3)
    img = cv2.rectangle(img,(390,170),(413,196),(255,255,0),3)
    img = cv2.rectangle(img,(457,163),(478,281),(255,255,0),3)
    img = cv2.rectangle(img,(314,174),(328,195),(255,255,0),3)
    cv2.imwrite("./debug/rect_text.jpg", img)

if __name__ == "__main__":
    datapath = "/home/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    #datapath = "/Users/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    categories = [1, 2, 3, 4, 6, 8, 10, 16, 17, 18]
    label_dic = {1:"person", 2:"bicycle", 3:"car", 4:"motorbike", 6:"bus", 8:"truck", 10:"traffic light", 16:"bird", 17:"cat", 18:"dog"}
    #print('get_ob_index: ', get_ob_index(datapath, categories))

    cofirm_dir()
    coco_info = get_ob_index(datapath, categories)
    print(make_xml(coco_info, label_dic))
    one_detection_debug()
