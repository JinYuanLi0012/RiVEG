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

The MNER stage of RiVEG is mainly based on [OFA](https://github.com/OFA-Sys/OFA), please configure the corresponding environment according to its instructions.

RiVEG's VE data are available [here](https://drive.google.com/drive/folders/153WtZiHHZBzxSG8Sk76byPRynlt-nUl3?usp=sharing). Download these data and place them in the **OFA/dataset/snli_ve_data/** folder.

Same usage as [OFA_Visual Entailment](https://github.com/OFA-Sys/OFA#visual-entailment).
