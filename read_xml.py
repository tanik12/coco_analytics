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

#リサンプリングをする処理
def get_df_data(df, rand_sample=720):
    #元々のデータで、それぞれの物体の出現数を表示する
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

    print("========== リサンプリング前の結果 ==========")
    print(traffic_signal_count, pedestrian_signal_count, person_count, bicycle_count,
          car_count, motorbike_count, bus_count, truck_count, dog_count, cat_count)

    print("データの総数：", len(df))

    ########
    #データを減らすようにリサンプリングする。
    #画像内に1つでも物体があったらTrueにする
    df_traffic_signal      = (df["traffic signal count"][df["traffic signal count"] > 0])
    df_pedestrian_signal   = (df["pedestrian signal count"][df["pedestrian signal count"] > 0])
    df_person              = (df["person count"][df["person count"] > 0])
    df_bicycle             = (df["bicycle count"][df["bicycle count"] > 0])
    df_car                 = (df["car count"][df["car count"] > 0])
    df_motorbike           = (df["motorbike count"][df["motorbike count"] > 0])
    df_bus                 = (df["bus count"][df["bus count"] > 0])
    df_truck               = (df["truck count"][df["truck count"] > 0])
    df_dog                 = (df["dog count"][df["dog count"] > 0])
    df_cat                 = (df["cat count"][df["cat count"] > 0])

    #ランダムに2000個抽出し、インデックスを格納したlistを取得
    df_traffic_signal_idx      = df_traffic_signal.sample(n=rand_sample).index
    df_pedestrian_signal_idx   = df_pedestrian_signal.sample(n=rand_sample).index
    df_person_idx              = df_person.sample(n=rand_sample).index
    df_bicycle_idx             = df_bicycle.sample(n=rand_sample).index
    df_car_idx                 = df_car.sample(n=rand_sample).index
    df_motorbike_idx           = df_motorbike.sample(n=rand_sample).index
    df_bus_idx                 = df_bus.sample(n=rand_sample).index
    df_truck_idx               = df_truck.sample(n=rand_sample).index
    df_dog_idx                 = df_dog.sample(n=rand_sample).index
    df_cat_idx                 = df_cat.sample(n=rand_sample).index

    print("========================")
    #data選定.
    #それぞれでランダムで取得した後、重複した画像を選択しないようにする処理。
    #and_listは、重複のないインデックス情報.
    and_list = set(list(df_traffic_signal_idx) + list(df_pedestrian_signal_idx) + list(df_person_idx) + list(df_bicycle_idx) + list(df_car_idx) + list(df_motorbike_idx) + list(df_bus_idx) + list(df_truck_idx) + list(df_dog_idx) + list(df_cat_idx))

    #インデックス情報を基に必要なデータを取得。
    df_resample = []
    for idx in list(and_list):
        #print(df[idx:idx+1].values.tolist()[0])
        df_resample.append(df[idx:idx+1].values.tolist()[0])
    colum_list2 = ["xml_path", "img_path", "traffic signal count", "pedestrian signal count", "person count", "bicycle count", "car count", "motorbike count", "bus count", "truck count", "dog count", "cat count"]
    df_2 = pd.DataFrame(df_resample, columns=colum_list2)

    re_traffic_signal_count    = (df_2["traffic signal count"] > 0).sum()
    re_pedestrian_signal_count = (df_2["pedestrian signal count"] > 0).sum()
    re_person_count            = (df_2["person count"] > 0).sum()
    re_bicycle_count           = (df_2["bicycle count"] > 0).sum()
    re_car_count               = (df_2["car count"] > 0).sum()
    re_motorbike_count         = (df_2["motorbike count"] > 0).sum()
    re_bus_count               = (df_2["bus count"] > 0).sum()
    re_truck_count             = (df_2["truck count"] > 0).sum()
    re_dog_count               = (df_2["dog count"] > 0).sum()
    re_cat_count               = (df_2["cat count"] > 0).sum()

    #リサンプリングした結果を表示
    print("========== リサンプリング後の結果 ==========")
    print(re_traffic_signal_count, re_pedestrian_signal_count, re_person_count, re_bicycle_count,
          re_car_count, re_motorbike_count, re_bus_count, re_truck_count, re_dog_count, re_cat_count)

    print("リサンプル後のデータの枚数: ", len(and_list))

    print(df_2.head())
    
    return df, df_2

def main():
    label_name = ["traffic signal", "pedestrian signal", "person", "bicycle", "car", "motorbike", "bus", "truck", "dog", "cat"]

    xml_fullpathes, xml_namees = get_xml_name()
    df = read_xml_info(xml_fullpathes, label_name)

    data_org, data_resample =  get_df_data(df)


if __name__ == "__main__":
    main()
