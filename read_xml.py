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
                xml_info_chunk.append(item.text)
            if item.tag == "object":
                for name in item.findall('name'):
                    label_count_dict[name.text] += 1

        for label_name in label_name_list:
            xml_info_chunk.append(label_count_dict[label_name])
        
            
        xml_info_mass.append(xml_info_chunk)
    
    colum_list = ["xml_path", "traffic signal count", "pedestrian signal count", "person count", "bicycle count", "car count", "motorbike count", "bus count", "truck count", "dog count", "cat count"]
    df = pd.DataFrame(xml_info_mass, columns=colum_list)
    #df = pd.DataFrame(xml_info_mass, columns=list("xml_path", "traffic signal count", "pedestrian signal count", "person count", "bicycle count", "car count", "motorbike count", "bus count", "truck count", "dog count", "cat count"))
        
    return df

def main():
    pass

if __name__ == "__main__":
    label_name = ["traffic signal", "pedestrian signal", "person", "bicycle", "car", "motorbike", "bus", "truck", "dog", "cat"]

    xml_fullpathes, xml_namees = get_xml_name()
    df = read_xml_info(xml_fullpathes, label_name)
    
    print(df.head())
