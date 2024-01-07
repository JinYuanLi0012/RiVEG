import re

path_1 = r"pred.txt"
path_2 = r"test_template.txt"

with open(path_1, 'r', encoding='utf-8') as f:
    pred = f.readlines()
    pred.insert(0,'\n')
    pred.pop()
with open(path_2, 'r', encoding='utf-8') as F:
    label = F.readlines()

for i,_ in enumerate(pred):
    if _!= '\n':
        pred[i] = _.split('\t')[0] + '\t' + _.split('\t')[-1]

for i,_ in enumerate(pred):
    if 'S-PER' in _:
        pred[i] = _.replace('S-PER','B-PER')
    elif 'S-ORG' in _:
        pred[i] = _.replace('S-ORG','B-ORG')
    elif 'S-LOC' in _:
        pred[i] = _.replace('S-LOC','B-LOC')
    elif 'S-OTHER' in _:
        pred[i] = _.replace('S-OTHER','B-OTHER')
    elif 'E-PER' in _:
        pred[i] = _.replace('E-PER','I-PER')
    elif 'E-ORG' in _:
        pred[i] = _.replace('E-ORG','I-ORG')
    elif 'E-LOC' in _:
        pred[i] = _.replace('E-LOC','I-LOC')
    elif 'E-OTHER' in _:
        pred[i] = _.replace('E-OTHER','I-OTHER')

pred_base = pred.copy()
Idlist = []

for _ in label:
    if _.startswith('IMGID:'):
        Idlist.append(_)


flag = 0
for i,_ in enumerate(pred_base):
    if _.startswith('\n'):
        pred.insert(i+flag+1, Idlist[flag])
        flag +=1

pred_result = pred[1:]
pred_result.append('\n')

with open(r"twitter10000_pred_rewrite.txt", 'w',encoding='utf-8') as f:
    for _ in pred_result:
        f.write(_)
        f.flush()


def constructDict(file_path):
    with  open(file_path, encoding='utf-8') as f:
        l = f.readlines()

    L = []
    L_ = []

    for j, i in enumerate(l):
        L_.append(i)
        if i == '\n':
            L.append(L_)
            L_ = []

    Dict = {}
    for i in L:
        key = re.findall(r"IMGID:(.*?)\n", i[0])[0]
        Dict[key] = i

    return Dict


def rewrite(filename, Raw):
    with open(filename, 'w', encoding='utf-8') as f:
        for key in Raw:
            tem = Raw[key]
            neww = []
            for i in tem:
                if '\tO\n' not in i and i != '\n':
                    neww.append(i)

            neww_index = []
            for i, cont in enumerate(neww):
                if '\tB-' in cont:
                    neww_index.append(i)

            res_list = []
            id = re.findall(r'IMGID:(.*?)\n', tem[0])[0]
            res_list.append(id)

            if len(neww_index) == 0:
                res_list.append('None')

            elif len(neww_index) == 1:
                label_ = re.findall(r'\tB-(.*?)\n', neww[neww_index[0]])[0]
                tempL = neww[neww_index[0]:]
                tempL_ = []
                for i in tempL:
                    tempL_.append(re.findall(r'(.*?)\t', i)[0])
                res = ' '.join(tempL_)
                res = res + f'({label_})'
                res_list.append(res)

            else:
                for i in range(len(neww_index[1:])):
                    head = neww_index[i]
                    tail = neww_index[1:][i]
                    label = re.findall(r'\tB-(.*?)\n', neww[head])[0]
                    tempL = neww[head:tail]
                    tempL_ = []
                    for i in tempL:
                        tempL_.append(re.findall(r'(.*?)\t', i)[0])
                    res = ' '.join(tempL_)
                    res = res + f'({label})'
                    res_list.append(res)

                label_ = re.findall(r'\tB-(.*?)\n', neww[neww_index[-1]])[0]
                tempL = neww[neww_index[-1]:]
                tempL_ = []
                for i in tempL:
                    tempL_.append(re.findall(r'(.*?)\t', i)[0])
                res = ' '.join(tempL_)
                res = res + f'({label_})'

                res_list.append(res)

            final = '###'.join(res_list)
            f.write(final)
            f.write('\n')


Raw = constructDict(r"twitter10000_pred_rewrite.txt")
filename = r"test_entity_pred.txt"
rewrite(filename, Raw)