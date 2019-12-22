import json
from pycocotools.coco import COCO
import xml.etree.ElementTree as et
import xml.dom.minidom as md

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
                bboxes.append(coco.loadAnns(k)[0]['bbox'])
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
def make_xml(coco_info):
    root = et.Element('root')
    tree = et.ElementTree(element=root)

    fruits = et.SubElement(root, 'fruits')
     
    fruit = et.SubElement(fruits, 'fruit')
    fruit_id = et.SubElement(fruit, 'name')
    fruit_id.text = 'apple'
    fruit_id = et.SubElement(fruit, 'price')
    fruit_id.text = '100'
     
    fruit = et.SubElement(fruits, 'fruit')
    fruit_id = et.SubElement(fruit, 'name')
    fruit_id.text = 'orange'
    fruit_id = et.SubElement(fruit, 'price')
    fruit_id.text = '200'

    ####
    # 文字列パースを介してminidomへ移す
    document = md.parseString(et.tostring(root))
    #document = md.parseString(et.tostring(root, 'utf-8'))
    file = open('test.xml', 'w')
    # エンコーディング、改行、全体のインデント、子要素の追加インデントを設定しつつファイルへ書き出し
    document.writexml(file, newl='\n', indent='', addindent='  ')
    file.close()
    #####

if __name__ == "__main__":
    datapath = "/Users/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    categories = [1, 2, 3, 4, 6, 8, 10, 16, 17, 18]
    #print('get_ob_index: ', get_ob_index(datapath, categories))
    coco_info = get_ob_index(datapath, categories)
    print(make_xml(coco_info))
