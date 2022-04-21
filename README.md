# Word-level AutoCompletion (WLAC)
This is a Shared task in WMT 2022. 


# Data
This year the training/dev datasets are provided in the data directory. 

# Data Preprocessing
1. `cd WLAC` 
2. Download mosesdecoder to preprocess data.
    ```
    git clone https://github.com/moses-smt/mosesdecoder.git
    ```
3. `bash data/prepare_data.sh`

for more details, you can check the `data/prepare_data.sh` and `data/generate_samples.py`