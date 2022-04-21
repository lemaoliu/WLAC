#!/bin/bash

FILE=${1}
LANG=${2}
SCRIPTS=mosesdecoder/scripts
NORM_PUNC=$SCRIPTS/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$SCRIPTS/tokenizer/remove-non-printing-char.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl

# normalize punctuation
echo "Normalizing punctuation ..."
perl $NORM_PUNC -l $LANG < $FILE > $FILE.norm

# remove non-printing characters
echo "Removing non-printing characters ..."
perl $REM_NON_PRINT_CHAR < $FILE.norm > $FILE.np

# lowercase
echo "Lowercasing ..."
perl $LC < $FILE.np > $FILE.lc

# tokenize
echo "Tokenizing ..."
perl $TOKENIZER -threads 8 -a -l $LANG < $FILE.lc > $FILE.tok

# perl $TOKENIZER -threads 8 -a -l en < "/home/yc21/project/WLAC/data/train-sample/zh-en/train-sample.zh-en.en" > "/home/yc21/project/WLAC/processed/train-sample/zh-en/train-sample.zh-en.en"