CONTEXT_TYPES="bi_context prefix suffix zero_context"

for CONTEXT_TYPE in ${CONTEXT_TYPES[@]}; do
    echo "Preparing data for ${CONTEXT_TYPE}..."
    python preprocess/generate_samples.py --source-lang de --target-lang en --file-prefix data/de-en/train --context-type ${CONTEXT_TYPE}
    python preprocess/generate_samples.py --source-lang en --target-lang de --file-prefix data/en-de/train --context-type ${CONTEXT_TYPE}
    python preprocess/generate_samples.py --source-lang zh --target-lang en --file-prefix data/zh-en/train --context-type ${CONTEXT_TYPE}
    python preprocess/generate_samples.py --source-lang en --target-lang zh --file-prefix data/en-zh/train --context-type ${CONTEXT_TYPE}
done