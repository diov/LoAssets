# LoAssets

A Python program that modify `UnityAsset` form the game Last origin.

## Installation

```
git clone https://github.com/diov/LoAssets.git
cd LoAssets
pip install -r requirements.txt
```

## Usage

To use the program, you need to paste files copied from `UnityCache` to the `Input` folder.  The output file will be saved in the `output` folder.

### Dump

Extract TextAsset from `UnityAsset` file.

```
python3 loassets.py dump
```

This will dump csv from `localization` and bin from `table_localization_*`.

### Serialize

Serialize the binary file extracted from `table_localization_*` to normal json file.

```
python3 loassets.py serialize --input=input/Table_Localization_ja.bin
```

This will parse a C# `BinaryFormatter` format binary file through a azure function, which depends on the `azure_function` branch.

### Deserialize

Deserialize normal json file to binary file:

```
python3 loassets.py deserialize --input=input/Table_Localization_ja.json
```

### Clone

Clone target to original language in csv extracted from `localization`.

```
python3 loassets.py clone --target=tc 
```

### Patch

Patch csv / binary / another mod `UnityAsset` under `patch` directory into original file.

```
python3 processor.py patch
```

## Acknowledgements

[UnityPy](https://github.com/K0lb3/UnityPy)
