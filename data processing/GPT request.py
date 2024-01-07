import re
import openai
import os
import time

# os.environ["http_proxy"] = "http://127.0.0.1:49714"
# os.environ["https_proxy"] = "http://127.0.0.1:49714"

openai.api_key = "your key"

def rawContent_(path):
    with open(path,'r',encoding='utf-8') as f:
        L = f.readlines()
        new_L = L
        
    if L[-1] == ' ':
        new_L = L[:-1]
        
    rawContentDict = {}

    for i in range(0, len(new_L), 2):
        key = re.findall(r'IMGID:(.*?)\n', new_L[i])[0]
        value = new_L[i+1]
        rawContentDict[key] = value

    return rawContentDict

def entity_(path):
    with open(path,'r',encoding='utf-8') as f:
        L = f.readlines()

    entityDict = {}

    for i in L:
        key = re.findall(r'^(.*?)###', i)[0]
        value = re.findall(r'###(.*?)\)', i)
        entityDict[key] = value

    for key in entityDict:
        for i,enti in enumerate(entityDict[key]):
            entityDict[key][i] = enti + ')'

    return entityDict

def caption_(path):

    with open(path,'r',encoding='utf-8') as f:
        L = f.readlines()

    id_list = []
    for i, cont in enumerate(L):
        if 'imgid:' in cont:
            id_list.append(i)
            
    adjust_list = id_list[1:]
    adjust_list.append(len(L))

    captionDict = {}

    for i in range(len(id_list)):
        head = id_list[i]
        tail = adjust_list[i]
        temp = ''.join(L[head:tail])
        key = re.findall(r'imgid:(.*?)###', temp.replace('\n', ' '))[0]
        value = re.findall(r'###(.*?)$', temp.replace('\n', ' '))[0]
        captionDict[key] = value

    return captionDict

if __name__ == "__main__":

    path1 = r"twitter-GMNER\newtest.txt"
    path2 = r"test_entity_pred.txt"
    path3 = r"owl_image_caption\owltestcaption_1.txt"

    rawContentDict = rawContent_(path1)
    entityDict = entity_(path2)
    captionDict = caption_(path3)

    print('reading done!\n')

    Str = "SYSTEM：You are a concise language assistant, please imitate my example and answer\n \
           Background: 'The image features a large stadium with a crowd of people gathered inside the arena. The stadium is filled with people of different ages who are all engaged in watching a soccer (or football) match. \
           The atmosphere of the event is lively and exciting, capturing the spirit of a live sporting event.'\n \
           Text: 'Premier League stadiums : Every top flight ground ranked by age '\n \
           Q: In the context of the provided information, Please tell me simply, without any modification, what is the 'Premier League' in the Text?\n \
           A: A football (soccer) league in England.\n \
           Background:'This picture features the same woman wearing a blue sweater, with the difference being that in the first picture, she has a blond hairstyle, whereas in the second picture, her hair is red. The image showcases a comparison of her appearance over time, emphasizing the changing nature of physical features, hairstyle, and fashion trends. The message is a reminder that people are constantly evolving and changing, and it is important to embrace these changes and adapt as they come.'\n \
           Text: '19 things Taylor Swift does that no one else could ever get away with' \n \
           Q: In the context of the provided information, Please tell me simply, without any modification, what is the 'Taylor Swift' in the Text? \n \
           A: A women singer-songwriter.\n \
           Background: 'The image features a majestic view of the Golden Gate Bridge in San Francisco, California at sunset. The iconic red structure is prominently featured in the scene, stretching out across the water and reaching towards the sky. The bridge is surrounded by the city's beautiful skyline, adding to the breathtaking scenery. The sunset casts a warm glow across the landscape, enhancing the overall beauty of the scene. This image captures a moment when the bridge and the city come alive at dusk, creating a captivating and awe-inspiring sight.' \n \
           Text: 'RT @ henryklee : Golden Gate Bridge back open as of 930p , 8 . 5 hrs early , after median installation' \n \
           Q: In the context of the provided information, Please tell me simply, without any modification, what is the 'Golden Gate Bridge' in the text? \n \
           A: A iconic red suspension bridge in San Francisco, California. \n "

    with open(r"testAnswer.txt",'a+',encoding='utf-8') as f:
        flag = 0
        for key in rawContentDict:

            flag = flag + 1
            print(str(flag))
            # if flag < 1337:
            #     continue

            rawContent = rawContentDict[key]
            caption = captionDict[key]
            entity = entityDict[key]
            
            if len(entity) == 0:
                continue

            for index, i in enumerate(entity):
                pattern = f"{Str} \
                            Background: '{caption}'\n \
                            Text: '{rawContent}'\n \
                            Q:In the context of the provided information, Tell me briefly what is the  '{i}' in the text？\n \
                            A:"

                # if index < 5:
                #     print(pattern)

                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content": pattern},])
                except:
                    time.sleep(2)
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content": pattern},])

                response = response["choices"][0]["message"]["content"]
                write_cont = f'Imageid:{key}.jpg###{i}###{response}'
                f.write(write_cont)
                f.write('\n')
                f.flush()