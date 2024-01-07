#From OFA_VE _predict.json to OFA_REC input
import base64
from PIL import Image
from io import BytesIO
import os

def getbase64(image_path):
    img = Image.open(image_path) # path to file
    img_buffer = BytesIO()
    img.save(img_buffer, format=img.format)
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data) # bytes
    base64_str = base64_str.decode("utf-8") # str
    return base64_str

path_OFA_VEpred = r"_predict.json" #your OFA/results/snli_ve_twitter10000pred/_predict.json file
path_basetxt = r"twitter10000_addent_test_pred.tsv"   #your twitter10000_addent_test_pred.tsv file

imgid = []
ent = []
sent = []
groundtype = []

import json
import csv
# read JSON file
with open(path_OFA_VEpred, 'r') as file:
    data = json.load(file)


for _ in data:
    imgid.append(_['uniq_id'])
    if _['answer'] == 'no':
        groundtype.append(int(0))
    else:
        groundtype.append(int(2))

assert len(imgid) == len(groundtype)
print('idall:'+ str(len(imgid)))


csv.field_size_limit(500 * 1024 * 1024)


with open(path_basetxt, newline='',encoding='utf-8') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    for row in tsvreader:
        sent.append(row[-2])
        ent.append(str(row[-2].split(')-')[0]) + ')')

assert len(imgid) == len(sent)
assert len(imgid) == len(ent)


with open(r'OFAVE_to_OFAREC.txt', 'w', encoding='utf-8') as F:
    for id,entity,sentence,groundt in zip(imgid,ent,sent,groundtype):
        line = 'Imageid:' + str(id) +'###'+entity+'###'+sentence+'###'+str(groundt)
        F.write(line)
        F.write('\n')
        F.flush()
    F.close()

tsvdata = []


#writing Done, Convert to OFA_REC input format
def totsv():

    with open(r'OFAVE_to_OFAREC.txt', 'r', encoding='utf-8') as f:
        L = f.readlines()


    imageid_filter = []
    entity_desc_filter = []
    box = []


    for line in L:

        if int(line.split('###')[-1].split('\n')[0])!=int(0):
            imageid_filter.append(line.split('###')[0].split('Imageid:')[1])
            entity_desc_filter.append(line.split('###')[2])
            box.append('0.0,0.0,0.0,0.0')

    assert len(imageid_filter) == len(entity_desc_filter)
    assert len(imageid_filter) == len(box)
    print('filterall:'+str(len(imageid_filter)))


    for id, desc, labal in zip(imageid_filter, entity_desc_filter, box):

        data = []
        data.append(id)
        data.append(id.split('.jpg#')[0])
        data.append(desc)
        data.append(str(labal))

        image_path = os.path.join(".../img",id.split('.jpg')[0]+'.jpg')
        data.append(getbase64(image_path))
        tsvdata.append(data)


    with open('twitter10000REC_addent_test_pred.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        tsvwriter = csv.writer(tsvfile, delimiter='\t')
        for row in tsvdata:
            tsvwriter.writerow(row)

totsv()