import sys
import jieba

### word segmentation for Chinese
file_zh = sys.argv[1]
for line in open(file_zh):
	line = line.strip()
	words = jieba.cut(line)  
	line = " ".join(words)
	print(line)

