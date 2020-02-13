import defusedxml.ElementTree as ET

import glob
import os
import sys
import re

import pandas as pd

def get_xml_name():
    xml_names = []

    # 拡張子.xmlのファイルを取得する
    xml_fullpath = '/home/gisen/data_own_nobird/VOCdevkit/VOC_own/Annotations/*.xml'
    # xmlを取得する
    xml_fullpath_lists = glob.glob(xml_fullpath)
    for path in xml_fullpath_lists:
        xml_name = os.path.basename(path)
        xml_names.append(xml_name)

    return xml_fullpath_lists, xml_names

def read_xml_info(xml_fullpath_list, label_name_list):
    xml_info_mass = []

    #xmlの読み込み
    for xml_fullpath in xml_fullpath_list:
        label_count_dict = {"traffic signal" : 0, "pedestrian signal": 0, "person" : 0, "bicycle": 0, "car" : 0, "motorbike" : 0, "bus" : 0, "truck" : 0, "dog" : 0, "cat" : 0}
        xml_info_chunk = []

        tree = ET.parse(xml_fullpath)
        tree_child = tree.getroot()

        #徐々に子ツリーを見ていく
        for item in tree_child: 
            if item.tag == "path":
                xml_info_chunk.append(xml_fullpath)
                xml_info_chunk.append(item.text)
            if item.tag == "object":
                for name in item.findall('name'):
                    label_count_dict[name.text] += 1

        for label_name in label_name_list:
            xml_info_chunk.append(label_count_dict[label_name])
        
            
        xml_info_mass.append(xml_info_chunk)
    
    colum_list = ["xml_path", "img_path", "traffic signal count", "pedestrian signal count", "person count", "bicycle count", "car count", "motorbike count", "bus count", "truck count", "dog count", "cat count"]
    df = pd.DataFrame(xml_info_mass, columns=colum_list)
        
    return df

def main():
    pass

if __name__ == "__main__":
    label_name = ["traffic signal", "pedestrian signal", "person", "bicycle", "car", "motorbike", "bus", "truck", "dog", "cat"]

    xml_fullpathes, xml_namees = get_xml_name()
    df = read_xml_info(xml_fullpathes, label_name)
    
    print(df.head())

    print("データの総数：", len(df))

    traffic_signal_count    = (df["traffic signal count"] > 0).sum()
    pedestrian_signal_count = (df["pedestrian signal count"] > 0).sum()
    person_count            = (df["person count"] > 0).sum()
    bicycle_count           = (df["bicycle count"] > 0).sum()
    car_count               = (df["car count"] > 0).sum()
    motorbike_count         = (df["motorbike count"] > 0).sum()
    bus_count               = (df["bus count"] > 0).sum()
    truck_count             = (df["truck count"] > 0).sum()
    dog_count               = (df["dog count"] > 0).sum()
    cat_count               = (df["cat count"] > 0).sum()

    print(traffic_signal_count, pedestrian_signal_count, person_count, bicycle_count,
          car_count, motorbike_count, bus_count, truck_count, dog_count, cat_count)

