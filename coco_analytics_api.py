import json
from pycocotools.coco import COCO

def get_ob_index(datapath, categories):
    with open(datapath, "rb") as file:
            dataset = json.load(file)
    # initialize COCO api for instance annotations
    coco = COCO(datapath)

    list_idx = []
    count = 0
    for img_idx in dataset['images']:
        s_dict = {}
        li = []

        img_idx = img_idx['file_name'].replace("COCO_train2014_", "").replace(".jpg", "").lstrip("0")
        imgs = coco.getAnnIds(int(img_idx))
        print("anno_num: ", imgs)
        
        for idx, i in enumerate(imgs):
            test = coco.loadAnns(i)
            if test[0]["category_id"] in categories: #欲しいカテゴリがあるかどうか
                li.append(i)
        if len(li) < 1:
            print("non indx")
            print("===============")
            continue

        count += 1
        print("ano_num2: ", li)
        print("\n")
        s_dict["img_idx"] = int(img_idx)
        s_dict["anno_dix"] = li
        list_idx.append(s_dict)
        print("================")
        if count == 10:
            return list_idx

if __name__ == "__main__":
    datapath = "/Users/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    categories = [1, 2, 3, 4, 6, 8, 10, 16, 17, 18]
    print('get_ob_index: ', get_ob_index(datapath, categories))
