from utils.voc2coco import *
from utils.visualize import confirm_category_num
from utils.coco_analytics import *
from utils.file_operation import rename
from utils.data_split import read, train_val_split

#ディレクトリの存在確認をする処理。
#ないのであればディレクトリを作成。
def main():
    #Ubuntu用
    coco_json_path = "/home/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    coco_img_path = "/home/gisen/data/coco/images/train2014/"
    
    #Mac用
    #coco_json_path = "/Users/gisen/data/coco/annotations/annotations/instances_train2014.json" 
    #coco_img_path = "/Users/gisen/data/coco/images/train2014/"

    categories = [1, 2, 3, 4, 6, 8, 10, 17, 18]
    label_dic = {1:"person", 2:"bicycle", 3:"car", 4:"motorbike", 6:"bus", 8:"truck", 10:"traffic light", 17:"cat", 18:"dog"}
    #categories = [1, 2, 3, 4, 6, 8, 10, 16, 17, 18]
    #label_dic = {1:"person", 2:"bicycle", 3:"car", 4:"motorbike", 6:"bus", 8:"truck", 10:"traffic light", 16:"bird", 17:"cat", 18:"dog"}

    cofirm_dir()
    coco_info = get_ob_info(coco_json_path, categories)
    make_xml(coco_info, label_dic)
    make_img(coco_img_path, coco_info)
    #one_detection_debug()
    #specified_num_detection_debug(coco_info)
    #train_val_split(coco_info)
    confirm_category_num(coco_info)
    #extract_traffic_light_img(coco_img_path, coco_info)

    rename()
    img_name_lists = read()
    train_val_split(img_name_lists)

    ###convert("./ImageSets/Main/xmllist.txt", "./Annotations", "output.json")

if __name__ == "__main__":
    main()
