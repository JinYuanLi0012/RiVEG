import csv
import uuid
import xml.etree.ElementTree as ET
import os
from PIL import Image
from io import BytesIO
import base64

def getbase64(image_path):
    img = Image.open(image_path) # path to file
    img_buffer = BytesIO()
    img.save(img_buffer, format=img.format)
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data) # bytes
    base64_str = base64_str.decode("utf-8") # str
    return base64_str


pathtest  = r"testAnswer.txt"
tsvdata = []


def totsv(pathgpt):

    #先读取图像描述
    image_caption = {}
    with open(r"Image caption\BLIP2_15.txt", 'r', encoding='utf-8') as f:
        L = f.readlines()

    for _ in L:
        image_caption[_.split('.jpg')[0]] = _.split(':')[1]

    with open(r"Image caption\BLIP2_17.txt", 'r', encoding='utf-8') as f:
        L = f.readlines()

    for _ in L:
        image_caption[_.split('.jpg')[0]] = _.split(':')[1]

    #Here are all the xml file paths of the Twitter-GMNER dataset
    xml_path = r"xml"

    Imageid = []
    entity = []
    entity_desc = []
    Imageid_filter = []
    entity_filter = []
    entity_desc_filter = []
    label = []
    e_count = 0
    c_count = 0


    with open(pathgpt, 'r', encoding='utf-8') as f:
        L = f.readlines()

    for line in L:

        Imageid.append(line.split('.jpg###')[0].split('Imageid:')[1])
        entity.append(line.split('###')[1])
        entity_desc.append(line.split('###')[2])


    assert len(Imageid) == len(entity)
    assert len(entity) == len(entity_desc)

    for id, ent, desc in zip(Imageid, entity, entity_desc):

        boxlabel = []
        try:
            tree = ET.parse(xml_path + '\\' + id + '.xml')
            xmlentity = tree.findall('object')
            for j in xmlentity:

                if j.find('name').text == ent.split('(')[0]:

                    ##get truebox list
                    box = []
                    box.append(float(j.find('bndbox').find('xmin').text))
                    box.append(float(j.find('bndbox').find('ymin').text))
                    box.append(float(j.find('bndbox').find('xmax').text))
                    box.append(float(j.find('bndbox').find('ymax').text))
                    boxlabel.append(box)


        except FileNotFoundError:
            pass

        if len(boxlabel) != 0:
            Imageid_filter.append(id)
            entity_filter.append(ent)
            entity_desc_filter.append(desc)
            label.append("entailment")
            e_count += 1

        else:
            Imageid_filter.append(id)
            entity_filter.append(ent)
            entity_desc_filter.append(desc)
            label.append("contradiction")
            c_count += 1

    print(len(Imageid_filter))
    print("entailment:" + str(e_count))
    print("contradiction:" + str(c_count))

    assert len(label) == len(entity_desc_filter)
    assert len(label) == len(entity_filter)
    assert len(label) == len(Imageid_filter)


    for id, ent, desc, lab in zip(Imageid_filter, entity_filter, entity_desc_filter, label):

        data = []

        unique_id = str(uuid.uuid4()).replace('-', '')[:4]
        new_filename = f"{id}.jpg#{unique_id}"
        data.append(new_filename)
        data.append(id)

        #image to base64
        #Here are all the img file paths of the Twitter-GMNER dataset
        image_path = os.path.join("img",id+'.jpg')
        data.append(getbase64(image_path))

        #get image caption
        image_cap= image_caption[id].split('\n')[0]
        data.append(image_cap)

        data.append(ent+'-'+desc.split('\n')[0])
        #data.append(ent)
        #data.append(desc.split('\n')[0])

        data.append(lab)
        tsvdata.append(data)


    # write to TSV
    with open('twitter10000_addent_test_pred.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        tsvwriter = csv.writer(tsvfile, delimiter='\t')
        for row in tsvdata:
            tsvwriter.writerow(row)

if __name__ == '__main__':
    totsv(pathtest)