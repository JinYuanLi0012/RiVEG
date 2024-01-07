#用来统计最终的结果，需要GMNER_finall_label.txt/OFAVE_to_OFAREC.txt/OFA_REC_pred.json
#OFAVE_to_OFAREC.txt是一个字典，里面是包含了所有的测试样本
#OFA_REC_pred.json是OFA根据ALBEF_to_SeqTR.txt的预测结果，要将上述两者整合，再和GMNER_finall_label做统计

import json

sample_dict = {}
sample_dict_path = r"OFAVE_to_OFAREC_augment.txt"

with open(sample_dict_path,'r',encoding='utf-8') as A:
    L = A.readlines()

for line in L:
    sample_dict[line.split('###')[0].split('Imageid:')[1]] = line.split('###')[2]

with open(r"refcoco_val_predict.json", 'r') as file:
    data = json.load(file)


img = []
box = []
sent = []
for _ in data:
    img.append(_['uniq_id'])
    box.append(_['box'])
    sent.append(sample_dict[_['uniq_id']])

assert len(img)==len(box)
assert len(box)==len(sent)
print(len(img))

with open(r'OFA_pred_test(OFAve)_final.txt', 'w', encoding='utf-8') as F:
    for image,des,bbox in zip(img,sent,box):
        line = str(image) +'###'+des+'###'+str(bbox)
        F.write(line)
        F.write('\n')
        F.flush()
    F.close()


seq_pred_path = r'OFA_pred_test(OFAve)_final.txt'

finall_label_path = r"GMNER_finall_label.txt"

def iou(box1, box2):

    x1, y1, x2, y2 = box1
    x1_, y1_, x2_, y2_ = box2

    x_left = max(x1, x1_)
    y_top = max(y1, y1_)
    x_right = min(x2, x2_)
    y_bottom = min(y2, y2_)

    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_ - x1_) * (y2_ - y1_)
    union_area = box1_area + box2_area - intersection_area

    if union_area == 0:
        iou = 0
    else:
        iou = intersection_area / union_area

    return iou

with open(sample_dict_path,'r',encoding='utf-8') as A:
    L = A.readlines()

for id,line in enumerate(L):
    L[id] = line.split('Imageid:')[1]

with open(seq_pred_path,'r',encoding='utf-8') as B:
    seq_pred = B.readlines()

with open(finall_label_path,'r') as C:
    label = C.readlines()

for id,_ in enumerate(label):
    label[id] = _.split('\n')[0]

count = 0
for id,line in enumerate(L):

    if line.split('\n')[0][-1]=='0':
        L[id] = line.split('\n')[0] + '###&[0, 0, 0, 0]'

    else:
        box = seq_pred[count].split('\n')[0].split('###')[-1]
        L[id] = line.split('\n')[0] + '###&' + str(box)
        count += 1

pred = L

all_number_label = len(label)
print("all_number_label: "+ str(all_number_label))
all_number_pred = len(pred)
print("all_number_pred: "+ str(all_number_pred))
right = 0


for pre in pred:
    rightflag = 0
    for gl in label:
        #this line is the result of GMNER
        if pre.split('###')[0].split('.jpg#')[0]+'.jpg'+pre.split('###')[1]==gl.split('###')[0]+gl.split('###')[1]:

        #this line is the result of EEG
        #if pre.split('###')[0].split('.jpg#')[0]+'.jpg'+pre.split('###')[1].split('(')[0]==gl.split('###')[0]+gl.split('###')[1].split('(')[0]:

            if int(pre.split('###')[-2]) == 0 and int(gl.split('###')[-2])==0:
                rightflag += 1

            elif int(pre.split('###')[-2]) != 0:
                gl_allbox_str = gl.split('###')[-1].split('&')[1:]
                gl_allbox = []
                for _ in gl_allbox_str:
                    xmin = float(_.split(',')[0].split('[')[1])
                    ymin = float(_.split(',')[1])
                    xmax = float(_.split(',')[2])
                    ymax = float(_.split(',')[3].split(']')[0])
                    gl_allbox.append([xmin,ymin,xmax,ymax])

                pred_box = pre.split('&')[-1]
                pred_xmin = float(pred_box.split(',')[0].split('[')[1])
                pred_ymin = float(pred_box.split(',')[1])
                pred_xmax = float(pred_box.split(',')[2])
                pred_ymax = float(pred_box.split(',')[3].split(']')[0])
                pred_box = [pred_xmin, pred_ymin, pred_xmax, pred_ymax]

                flag = 0
                for each_glbox in gl_allbox:
                    Iouresult = iou(each_glbox,pred_box)
                    if Iouresult >= 0.5:
                        flag = 1

                if flag == 1:
                    rightflag += 1
    if rightflag != 0:
        right+=1


print("right: "+ str(right))
pre = right/all_number_pred
rec = right/all_number_label
print('pre: ' + str(pre))
print('rec: ' + str(rec))
F1 = (2*pre*rec)/(pre+rec)
print('Recall: ' + str(F1))