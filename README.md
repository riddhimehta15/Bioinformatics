# 🧬 RNA-Binding Protein Prediction Using Sequence-Derived Features  
**Contributors: _Nirvisha Soni_ & _Riddhi Mehta_**

## 📘 Overview  
This repository implements a full end-to-end pipeline for reconstructing the dataset and reproducing the machine learning framework from the PRBP study:

**"Prediction of RNA-Binding Proteins Using a Random Forest Algorithm Combined with an RNA-Binding Residue Predictor."**

The project includes dataset reconstruction from UniProt, redundancy reduction using CD-HIT, evolutionary feature extraction (PSSM), physicochemical profile generation (EIPP), and final Random Forest model training.

## 🚀 Features

### 1. Dataset Reconstruction
- Retrieved Swiss-Prot sequences.
- Removed fragments, non-standard amino acids.
- Positive: RNA-binding annotated.
- Negative: no nucleic acid-binding evidence.

### 2. FASTA/Excel/TSV Processing
- Header parsing.
- Cleanup and validation.
- Excel → FASTA converters.

### 3. CD-HIT Redundancy Reduction
- 40% identity clustering.
- Representative sequence extraction.

### 4. PSI-BLAST & PSSM Generation
- Local BLAST+ automation.
- Multi-iteration alignment.
- Generated PSSM matrices.

### 5. EIPP Feature Extraction
- Hydrophobicity, polarity, steric features.
- Sliding window aggregation.

### 6. Machine Learning Pipeline
- Random Forest + baselines.
- MCC, F1, ROC-AUC evaluation.

## 📂 Repository Structure

```
project/
├── data_raw/
├── data_processed/
├── cdhit_output/
├── pssm_profiles/
├── features/
├── notebooks/
├── src/
└── README.md
```

## ⚙️ Installation
```
pip install -r requirements.txt
```

## 🛠️ How to Run

### CD-HIT
```
cd-hit -i input.fasta -o clustered.fasta -c 0.4 -n 2
```

### PSI-BLAST
```
psiblast -query seq.fasta -db uniref90 -num_iterations 3 -out_ascii_pssm seq.pssm
```

### Feature Extraction
```
python src/feature_engineering.py
```

### Model Training
```
python src/model.py
```

## 👥 Contributors
- **[Riddhi Mehta](https://github.com/riddhimehta15)**
- **[Nirvisha Soni](https://github.com/Nirvisha82)**

