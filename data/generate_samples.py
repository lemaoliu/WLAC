"""
This file is used to generate samples for train/dev/test set
"""
import jieba
import json
import random
import argparse
from tqdm import tqdm
import os
from pypinyin import lazy_pinyin

def generate_bi_context(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(1, length-2) # exclude the first and last word
    
    left_bound = random.randint(0, position-1)
    right_bound = random.randint(position+1, length-1)
    
    left_context = " ".join(tgt_sentence[0 : left_bound+1])
    right_context = " ".join(tgt_sentence[right_bound : length])

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]
    

    return left_context, right_context, typed_seq, target

def generate_prefix(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(1, length-1) # exclude the first word

    left_bound = random.randint(0, position-1)

    left_context = " ".join(tgt_sentence[0 : left_bound+1])
    right_context = "" # no right context

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]

    return left_context, right_context, typed_seq, target    

def generate_suffix(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(0, length-2) # exclude the first word

    right_bound = random.randint(position+1, length-1)

    left_context = "" # no left context
    right_context = " ".join(tgt_sentence[right_bound : length])

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]

    return left_context, right_context, typed_seq, target

def generate_zero_context(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(0, length-1)

    left_context = "" # no left context
    right_context = "" # no right context

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]

    return left_context, right_context, typed_seq, target 

def generate_samples(src_sentences, tgt_sentences, dst_file, context_type, target_lang):

    tgt_sentences = [ list(filter(None,tgt_sentence.split(" "))) for tgt_sentence in tgt_sentences ]
        
    # # read sentences from source language file
    # src_sentences = []
    # with open(src_file, "r", encoding="utf-8") as f:
    #     for line in f:
    #         src_sentences.append( line.rstrip("\n") )
    
    # # read sentences from target language file
    # tgt_sentences = []
    # with open(tgt_file, "r", encoding="utf-8") as f:
    #     for line in f:
    #         tgt_sentences.append( line.rstrip("\n").split(" ") )
    
    # generate samples
    samples = []
    for i,(src_sentence, tgt_sentence) in tqdm(enumerate(zip(src_sentences, tgt_sentences))):
        sample= dict()
        sample["src"] = src_sentence
        sample["context_type"] = context_type
        
        if context_type == "bi_context":
            if len(tgt_sentence) >= 3:
                sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_bi_context(target_lang, tgt_sentence)
                samples.append(sample)
            else:
                continue
        elif context_type == "prefix":
            if len(tgt_sentence) >= 2: 
                sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_prefix(target_lang, tgt_sentence)
                samples.append(sample)                
            else:
                continue
        elif context_type == "suffix":
            if len(tgt_sentence) >= 2:
                sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_suffix(target_lang, tgt_sentence)
                samples.append(sample)  
            else:
                continue
        elif context_type == "zero_context":
                sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_zero_context(target_lang, tgt_sentence)
                samples.append(sample)              
        else:
            raise ValueError("Unknown context type: {}".format(context_type))
    
    # write samples to file
    with open(dst_file, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

def zh_tokenization(src_file):
    sentences = []

    # read sentences from file
    with open(src_file, "r", encoding="utf-8") as f:
        for line in f:
            sentences.append(line.rstrip("\n"))
    
    # tokenize sentences
    tokenized_sentences = []
    for sentence in sentences:
        words = jieba.cut(sentence)  
        tokenized_sentences.append(" ".join(words))

    return tokenized_sentences

def en_de_word_tokenization(filename, lang):
    # in this function, we will invoke scripts to tokenize sentences.
    os.system(f"bash data/run_mosesdecoder.sh {filename} {lang}")

    # read from file
    tokenized_sentences = []
    with open(filename+".tok", "r", encoding="utf-8") as f:
        for line in f:
            tokenized_sentences.append( line.rstrip("\n"))
    
    # remove file
    os.system(f"rm {filename}.tok")
    os.system(f"rm {filename}.norm")
    os.system(f"rm {filename}.np")
    os.system(f"rm {filename}.lc")

    return tokenized_sentences

def tokenize(lang, filename):

    tokenized_sentences = []
    if lang == "zh":
        tokenized_sentences = zh_tokenization(filename)
    elif lang in ["de", "en"]:
        tokenized_sentences = en_de_word_tokenization(filename, lang)
    else:
        raise ValueError("Unknown language: {}".format(lang))
    
    return tokenized_sentences

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--source-lang", default="en", type=str, required=False, help="source language")
    parser.add_argument("--target-lang", default="de", type=str, required=False, help="target language")
    parser.add_argument("--file-prefix", default="data/raw/en-de/train", type=str, required=False, help="file prefix")
    parser.add_argument("--context-type", default="zero_context", type=str, required=False, choices=["bi_context", "prefix", "suffix", "zero_context"] , help="context type for WLAC")

    args = parser.parse_args()

    src_file = args.file_prefix + "." + args.source_lang
    tgt_file = args.file_prefix + "." + args.target_lang
    dst_file = args.file_prefix + "." + args.context_type

    # do tokenization for src_file and tgt_file
    print("Tokenizing {} and {}".format(src_file, tgt_file))
    src_sentences = tokenize(args.source_lang, src_file)
    tgt_sentences = tokenize(args.target_lang, tgt_file)
    print("Tokenization finished")

    print("Generating samples...")
    generate_samples(src_sentences, tgt_sentences, dst_file, args.context_type, args.target_lang)
    print("Generation finished")