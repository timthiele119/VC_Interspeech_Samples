#!/usr/bin/env python

import os, shutil
import pandas as pd

ROOT = r"/Users/timthiele/Desktop/VC_Samples/Submission_RENEWED"

# === 1. PREPARE CSV ===
csv_filename = "StudySamples.xlsx"
csv_filename_mod = "StudySamplesMod.xlsx"
csv_filename_mod_csv = "StudySamplesMod.csv"

df = pd.read_excel(os.path.join(ROOT, csv_filename))
df["Dataset"] = df["Dataset"].apply(lambda x: x.replace(" ", "_"))


# Define a custom function to concatenate values
def concat_values_VANILLA(row):
    if row["Dataset"] == "VCTK":
        return f"VCTK_VANILLA_" + row["Baseline"] + ".wav"
    else:
        return f"LibriSpeech_VANILLA_" + row["Baseline"] + ".wav"
     
def concat_values_OURMODEL(row):
    if row["Dataset"] == "VCTK":
        return f"VCTK_OURMODEL_" + row["Improved"] + ".wav"
    else:
        return f"LibriSpeech_OURMODEL_" + row["Improved"] + ".wav"
    
def concat_values_ORIGINAL(row):
    if row["Dataset"] == "VCTK":
        return f"VCTK_" + row["Source"] + ".wav"
    else:
        return f"LibriSpeech_" + row["Source"] + ".wav"
    
def concat_values_OTHER(row):
    if row["Dataset"] == "VCTK":
        return f"VCTK_" + row["Other utterance"] + ".wav"
    else:
        return f"LibriSpeech_" + row["Other utterance"] + ".wav"


# Apply the custom function to create a new column
df["Baseline_FullFileName"] = df.apply(concat_values_VANILLA, axis=1)
df["OurModel_FullFileName"] = df.apply(concat_values_OURMODEL, axis=1)
df["Original_FullFileName"] = df.apply(concat_values_ORIGINAL, axis=1)
df["Other_FullFileName"] = df.apply(concat_values_OTHER, axis=1)

df.to_excel(os.path.join(ROOT, csv_filename_mod))

df_csv = pd.DataFrame()
df_csv["Original"] = df["Original_FullFileName"]
df_csv["Baseline"] = df["Baseline_FullFileName"]
df_csv["OurModel"] = df["OurModel_FullFileName"]
df_csv["Other"] = df["Other_FullFileName"]
df_csv.to_csv(os.path.join(ROOT, csv_filename_mod_csv))
a = 0


# === 2. PREPARE FILENAMES ===
sourcedirpath = os.path.join(ROOT, "All")
os.makedirs(sourcedirpath, exist_ok=True)

for dataset in ["VCTK", "LibriSpeech"]:
    for basedirname in ["Originals", "VANILLA", "OURMODEL"]:
        dirname = dataset + "_" + basedirname
        dirpath = os.path.join(ROOT, dirname)
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            basedirnamerep = basedirname + "_" if basedirname in ["VANILLA", "OURMODEL"] else ""
            new_filepath = os.path.join(sourcedirpath, f"{dataset}_{basedirnamerep}{filename}")
            if "DS_Store" in new_filepath:
                continue
            shutil.copy(filepath, new_filepath)