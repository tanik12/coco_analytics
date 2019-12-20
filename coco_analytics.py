import json

with open("/home/gisen/data/coco/annotations/annotations/instances_train2014.json", "rb") as file:
    dataset = json.load(file)

print(dataset.keys())
#print(dataset["categories"])
print("=============\n")
#print(dataset['annotations'][0])

img_indexes = set([])
img_num1 = set([])
img_num2 = set([])
img_num3 = set([])
img_num4 = set([])
img_num5 = set([])
img_num6 = set([])
img_num7 = set([])
img_num8 = set([])
img_num9 = set([])
img_num10 = set([])
categories = [1, 2, 3, 4, 6, 8, 10, 16, 17, 18]

count = 0
for item in dataset['annotations']:
    count += 1
    if item["category_id"] in categories:
        img_indexes.add(item["image_id"])
        if item["category_id"] == 1:
            img_num1.add(item["image_id"])
        elif item["category_id"] == 2:
            img_num2.add(item["image_id"])
        elif item["category_id"] == 3:
            img_num3.add(item["image_id"])
        elif item["category_id"] == 4:
            img_num4.add(item["image_id"])
        elif item["category_id"] == 6:
            img_num5.add(item["image_id"])
        elif item["category_id"] == 8:
            img_num6.add(item["image_id"])
        elif item["category_id"] == 10:
            img_num7.add(item["image_id"])
        elif item["category_id"] == 16:
            img_num8.add(item["image_id"])
        elif item["category_id"] == 17:
            img_num9.add(item["image_id"])
        elif item["category_id"] == 18:
            img_num10.add(item["image_id"])

#print(img_indexes) 
print("ほしいカテゴリだけの総数: ", len(img_indexes))
print("元データの総数：", count)

print("img_num1:", len(img_num1))
print("img_num2:", len(img_num2))
print("img_num3:", len(img_num3))
print("img_num4:", len(img_num4))
print("img_num5:", len(img_num5))
print("img_num6:", len(img_num6))
print("img_num7:", len(img_num7))
print("img_num8:", len(img_num8))
print("img_num9:", len(img_num9))
print("img_num10:", len(img_num10))
