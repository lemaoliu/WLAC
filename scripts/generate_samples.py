"""
This file is used to generate samples for train/dev/test set
"""
import json
import random
import argparse
from tqdm import tqdm
from pypinyin import lazy_pinyin

def get_span(start, end):
    # sample a span from [start, end]
    x = random.randint(start, end)
    y = random.randint(start, end)
    if x > y:
        return y, x
    else:
        return x, y

def generate_bi_context(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(1, length-2) # exclude the first and last word

    left_low, left_high =  get_span(0, position-1)
    right_low, right_high = get_span(position+1, length-1) 
    
    left_context = " ".join(tgt_sentence[ left_low : left_high+1 ])
    right_context = " ".join(tgt_sentence[ right_low : right_high+1 ])

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]
        target = tgt_sentence[position]
    

    return left_context, right_context, typed_seq, target

def generate_prefix(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(1, length-1) # exclude the first word

    left_low, left_high =  get_span(0, position-1)

    left_context = " ".join(tgt_sentence[ left_low : left_high+1])
    right_context = "" # no right context

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]
        target = tgt_sentence[position]

    return left_context, right_context, typed_seq, target    

def generate_suffix(lang, tgt_sentence):

    length = len(tgt_sentence)

    position = random.randint(0, length-2) # exclude the first word

    right_low, right_high = get_span(position+1, length-1)

    left_context = "" # no left context
    right_context = " ".join(tgt_sentence[ right_low : right_high+1 ])

    if lang != "zh":
        target = tgt_sentence[position]
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = tgt_sentence[position][ :typed_seq_length ]
    else:
        target = "".join(lazy_pinyin(tgt_sentence[position]))
        typed_seq_length = random.randint( 1, len(target) )
        typed_seq = target[ :typed_seq_length ]
        target = tgt_sentence[position]

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
        target = tgt_sentence[position]

    return left_context, right_context, typed_seq, target 

def generate_samples(src_sentences, tgt_sentences, dst_file, target_lang):
        
    # read sentences from source language file
    src_sentences = []
    with open(src_file, "r", encoding="utf-8") as f:
        for line in f:
            src_sentences.append( line.rstrip("\n") )
    
    # read sentences from target language file
    tgt_sentences = []
    with open(tgt_file, "r", encoding="utf-8") as f:
        for line in f:
            tgt_sentences.append( list( filter(None, line.rstrip("\n").split(" ")) ) )  # filter() is used to remove empty string
    
    # generate samples
    samples = []
    for src_sentence, tgt_sentence in tqdm(zip(src_sentences, tgt_sentences)):

        sample= dict()
        sample["src"] = src_sentence
        sample["context_type"] = "bi_context"
        if len(tgt_sentence) >= 3:
            sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_bi_context(target_lang, tgt_sentence)
            samples.append(sample)
        
        sample= dict()
        sample["src"] = src_sentence
        sample["context_type"] = "prefix"
        if len(tgt_sentence) >= 2: 
            sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_prefix(target_lang, tgt_sentence)
            samples.append(sample)                

        sample= dict()
        sample["src"] = src_sentence
        sample["context_type"] = "suffix"
        if len(tgt_sentence) >= 2:
            sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_suffix(target_lang, tgt_sentence)
            samples.append(sample)  

        sample= dict()
        sample["src"] = src_sentence
        sample["context_type"] = "zero_context"
        sample["left_context"], sample["right_context"], sample["typed_seq"], sample["target"] = generate_zero_context(target_lang, tgt_sentence)
        samples.append(sample)              
    
    # write samples to file
    with open(dst_file, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--source-lang", default="en", type=str, required=False, help="source language")
    parser.add_argument("--target-lang", default="de", type=str, required=False, help="target language")
    parser.add_argument("--file-prefix", default="data/raw/en-de/train", type=str, required=False, help="file prefix")
    # parser.add_argument("--context-type", default="zero_context", type=str, required=False, choices=["bi_context", "prefix", "suffix", "zero_context"] , help="context type for WLAC")

    args = parser.parse_args()

    src_file = args.file_prefix + "." + args.source_lang
    tgt_file = args.file_prefix + "." + args.target_lang
    dst_file = args.file_prefix + "." + "samples.json"

    print("Generating samples...")
    generate_samples(src_file, tgt_file, dst_file, args.target_lang)
    print("Generation finished")