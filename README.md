# RiVEG

Here are code and dataset for our paper: **Improving Grounded Multimodal Named Entity Recognition via Visual Entailment and Grounding**

# Usage

The implementation of RiVEG mainly includes the following three parts:

## MNER Module

The MNER stage of RiVEG is mainly based on AdaSeq, AdaSeq project is based on Python version >= 3.7 and PyTorch version >= 1.8. For details on the configuration of the environment, see [PGIM](https://github.com/JinYuanLi0012/PGIM) and [AdaSeq](https://github.com/modelscope/AdaSeq).

After following the instructions of PGIM to complete the configuration, use the following commands to complete the training and prediction of the MNER stage.
Note that we have provided RiVEG's yaml configuration file, please replace the original configuration of PGIM with the configuration file [here](MNER/twitter-10000.yaml).
```
python -m scripts.train -c examples/PGIM/twitter-10000.yaml
```

After completing training, the inference results will be saved in **experiments/RiVEG-twitter-10000/.../pred.txt**.

## Visual Entailment Module

The VE stage of RiVEG is mainly based on [OFA](https://github.com/OFA-Sys/OFA), please configure the corresponding environment according to its instructions.

RiVEG's VE data are available [here](https://drive.google.com/drive/folders/153WtZiHHZBzxSG8Sk76byPRynlt-nUl3?usp=sharing). Download these data and place them in the **OFA/dataset/snli_ve_data/** folder. 

We have provided the **twitter10000_addent_test_pred.tsv** file which contains the ChatGPT answers. If you want to obtain the corresponding VE test set based on your own MNER inference results, you can run the corresponding code we provide [here](data_processing/MNER_processing). First put the MNER prediction results **experiments/RiVEG-twitter-10000/.../pred.txt** into the **data_processing/MNER_processing** folder, and then run the **extract entities.py** and **GPT request.py** files in sequence. The GPT answer will be written into **data_processing/MNER_processing/testAnswer.txt**. Note that line 9 of the **GPT request.py** file needs to be replaced with your own key. And there will be a small amount of expenses. 

After this, use [Twitter10000_to_OFA_VE.py](data_processing/VE_processing
) file to get the final tsv dataset, don't forget to replace lines 40 and 122 with the xml and img data paths of the original [GMNER dataset](https://github.com/NUSTM/GMNER).

Same usage as [OFA_Visual Entailment](https://github.com/OFA-Sys/OFA#visual-entailment), then use the [script](VE) we provide to perform training and inference. Please pay attention to the modification of various file paths.
```
cd run_scripts/snli_ve
nohup sh train_twitter10000.sh > train_twitter10000.out &  # finetune for twitter10000_VE
sh evaluate_twitter10000.sh test  # inference and specify 'dev' or 'test'
```

## Visual Grounding Module

Same as VE Module, the VG stage of RiVEG is also based on [OFA](https://github.com/OFA-Sys/OFA).

RiVEG's VG data are available [here](https://drive.google.com/drive/folders/1Tc_oNEixbcRcxuVVXgdp4gAmEfB2ZAcv?usp=sharing). Download these data and place them in the **OFA/dataset/refcoco_data/** folder.

Same usage as [OFA_Visual Grounding](https://github.com/OFA-Sys/OFA#visual-grounding-referring-expression-comprehension), then use the [script](VG) we provide to perform training and inference. Please pay attention to the modification of various file paths.
```
cd run_scripts/refcoco
nohup sh train_twitter10000REC.sh > train_twitter10000REC.out &  # finetune for twitter10000_VG
sh evaluate_twitter10000REC.sh test  # inference and specify 'dev' or 'test'
```

# Result statistics

The inference results of Visual Grounding are located at **../results/twitter10000REC/OFAlargeVE_OFAlargeREC_pred/**
