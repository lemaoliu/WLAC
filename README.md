

# Word-level AutoCompletion (WLAC)

This is a new shared task in WMT 2022. In this year, the shared task involves in two language pairs German-to-English (De-En) and Chinese-to-English (Zh-En) with two directions. If you have any questions, please contact <a href="mailto:lemaoliu@gmail.com" target="_blank">Lemao Liu</a>.


# Key Steps

  
- Download the datasets for De-En and Zh-EN (see the details in next section). 
<font color=red><b>ATTENTION!!</font> Participants must use only the data provided here.</b>

- Download the scripts in the directory scripts/ to preprocess the data.

- Run the scripts to obtain the simulated training data for WLAC task from bilingual data.



# Data Preparation

## De-En Bilingual Data

The bilingual data is from WMT 14 preprocessed by Stanford NLP Group: [train.de](https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/train.de) and [train.en](https://nlp.stanford.edu/projects/nmt/data/wmt14.en-de/train.en).


## Zh-En Bilingual Data

The bilingual data is ``UN Parallel Corpus V1.0" from WMT 17. To obtain the data, one can follow three steps:
- Download two files [UNv1.0.en-zh.tar.gz.00](https://drive.google.com/uc?export=download&id=1rv2Yh5j-5da5RZO3DEaYvYRZKxE841hT) and
[UNv1.0.en-zh.tar.gz.01](https://drive.google.com/uc?export=download&id=1cfUezEOv5UPzF-d1uIm9-dkIUjtyZ9ys). You may also find both files yourself from [webpage](https://conferences.unite.un.org/UNCORPUS/en/DownloadOverview).

- Run the following command to combine two files and decompress them:
```
cat UNv1.0.en-zh.tar.gz.* | tar -xzf -
```
- en-zh/UNv1.0.en-zh.en and en-zh/UNv1.0.en-zh.zh are source and target files. Note that both files should be preprocessed (word segmentation for zh and tokenization for en) by scripts/tokenizer.perl and scripts/word_seg.py as follows:
```
pip3 install jieba
perl scripts/tokenizer.perl -l en < UNv1.0.en-zh.en > UNv1.0.en-zh.tok.en
python3 scripts/word_seg.py UNv1.0.en-zh.zh > UNv1.0.en-zh.tok.zh
```

 
## Preparing the Simulated Training data for WLAC


Bilingual data can not be used to train WLAC models directly. Instead, one can obtain training data (as well as development data) for WLAC from bilingual data via simulation following the reference [1] (See Section 3.2 in this paper). For example, this can be done by running the following cmd for zh->en subtask:
```
pip3 install pypinyin tqdm
python3 scripts/generate_samples.py --source-lang zh --target-lang en --file-prefix UNv1.0.en-zh.tok
```
Then UNv1.0.en-zh.tok.samples.json is the simulated training data for WLAC, whose format is as follows:
```
{"src": "The Security Council ,", "context_type": "zero_context", "left_context": "", "right_context": "", "typed_seq": "a", "target": "安全"}
{"src": "安全 理事会 ，", "context_type": "prefix", "left_context": "The Security", "right_context": "", "typed_seq": "Coun", "target": "Council"}
```
where "typed_seq" denotes the typed sequence for the target word, i.e., "a" is the prefix of the pronunciation of "anquan" for the Chinese word "安全", or "Coun" is the prefix of the target word of "Council" for English (or German); "context_type" indicates the location of the target word between left_context and right_context and it takes value from {"prefix", "zero_context", "suffix", and "bi_context"} (See reference [1] for more details). 

## Reference

- [1] Huayang Li, Lemao Liu, Guoping Huang, Shuming Shi. 2021. GWLAN: General Word-Level AutocompletioN for Computer-Aided Translation. Proceedings of ACL. 