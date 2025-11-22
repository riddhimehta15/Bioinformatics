# RNA-Binding Protein Prediction (PRBP-Style Random Forest)

This repository contains a small end-to-end pipeline to reproduce, at the **molecular (protein) level**, the RNA-binding protein (RBP) prediction setup described in:

> *Prediction of RNA-Binding Proteins Using a Random Forest Algorithm Combined with an RNA-Binding Residue Predictor* (PRBP)

The implementation uses:
- **EIPP**: Evolution-Inspired Physicochemical Profiles derived from PSI-BLAST PSSMs  
- **AAC**: Global amino-acid composition features  
- **Random Forests** for binary protein-level RBP vs non-RBP classification  

Contributors: **Nirvisha Soni** and **Riddhi Mehta**

---

## Repository Structure

All files live under the `Bioinformatics/` folder (GitHub will show this as the root of the repo):

```text
Bioinformatics/
├── Positive_Final.fasta           # Final positive-class proteins (experimentally validated RBPs)
├── Negative_Final.fasta           # Final negative-class proteins (no known nucleic-acid binding)
├── all_sequences.fasta            # Combined positive + negative FASTA
│
├── split.py                       # Script: split all_sequences.fasta into one-FASTA-per-protein
├── generate_pssm.bat              # Windows batch script to run PSI-BLAST and generate PSSMs
│
├── mini_db.p*                     # Local PSI-BLAST (BLAST+) protein database files (mini_db)
│
├── split_seqs/                    # Folder of per-sequence FASTA files (created by split.py)
└── pssm_out/                      # Folder of per-sequence PSSMs (.pssm) from PSI-BLAST
```

The main modelling code is in:

```text
Bioinformatics/PRBP_Prediction_EIPP_AAC_RF.ipynb
```

This Jupyter notebook:
1. Loads sequences and (optionally) PSSMs
2. Builds **EIPP** + **AAC** + length features
3. Trains a **RandomForestClassifier**
4. Evaluates with train/test split and 5-fold cross-validation
5. Prints metrics and example predictions for a few random proteins

---

## Requirements

### Python environment

- Python **3.8+**
- Recommended: create a conda/venv environment

Python packages used in the notebook:

```bash
pip install numpy pandas scikit-learn matplotlib
```

### BLAST+ / PSI-BLAST (for EIPP/PSSM features)

To recompute EIPP features from scratch you need:
- **NCBI BLAST+** installed (so the `psiblast` command is available on your PATH)
- The provided `mini_db.*` BLAST database files in the same folder as the scripts

On Windows, you can install BLAST+ from the NCBI site and then add the `bin` folder to your PATH.

If you prefer not to re-run PSI-BLAST, you can:
- Use any pre-computed PSSMs already shipped in `pssm_out/` (if present), or  
- Skip the EIPP step and adapt the notebook to use only AAC features (for quick testing).

---

## Getting Started

1. **Clone or download the repository**

   ```bash
   git clone https://github.com/riddhimehta15/Bioinformatics.git
   cd Bioinformatics/Bioinformatics
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   Using `conda`:

   ```bash
   conda create -n rbp-prbp python=3.10
   conda activate rbp-prbp
   pip install numpy pandas scikit-learn matplotlib
   ```

   Or using `venv`:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   pip install numpy pandas scikit-learn matplotlib
   ```

3. **Prepare per-sequence FASTA files**

   The script `split.py` takes `all_sequences.fasta` and splits it into one FASTA file per protein in the `split_seqs/` folder.

   From the `Bioinformatics/` directory:

   ```bash
   python split.py
   ```

   After this step you should have many `*.fasta` files created under:

   ```text
   Bioinformatics/split_seqs/
   ```

4. **Generate PSSMs with PSI-BLAST**

   This step computes a PSSM for each protein using the local `mini_db` BLAST database.

   From the `Bioinformatics/` directory (or wherever `generate_pssm.bat` expects to be run; typically a `pssm/` subfolder):

   ```bash
   generate_pssm.bat
   ```

   The script will:
   - Loop over `split_seqs/*.fasta`
   - Run `psiblast` for each sequence
   - Save an ASCII PSSM to `pssm_out/<sequence_id>.pssm`

   You can adjust parameters (e.g., number of iterations) inside `generate_pssm.bat` if needed.

5. **Run the Random Forest notebook**

   Start Jupyter:

   ```bash
   jupyter notebook
   ```

   Then open:

   ```text
   Bioinformatics/PRBP_Prediction_EIPP_AAC_RF.ipynb
   ```

   and run all cells in order. The notebook will:

   - Parse the FASTA sequences (positive + negative)
   - Match them with available PSSMs in `pssm_out/`
   - Compute:
     - **EIPP** features from PSSMs (6 physicochemical groups × 20 amino acids = 120 dims)
     - **AAC** features (20-dimensional amino-acid composition)
     - Optional length feature
   - Train a Random Forest classifier with stratified train/test split
   - Report:
     - Accuracy, precision, recall, F1, ROC-AUC on the test set
     - 5-fold cross-validation scores
     - Top 20 most important features
     - Example predictions for 5 random proteins

---

## Customization

- **Changing train/test split**  
  Inside the notebook, adjust the `test_size` and `RANDOM_STATE` arguments in the `train_test_split` call.

- **Changing Random Forest hyperparameters**  
  Modify the `RandomForestClassifier` parameters (e.g., `n_estimators`, `max_depth`, `class_weight`) to explore different models.

- **Using only AAC features**  
  If computing PSSMs is too expensive, you can comment out the EIPP feature extraction and use only AAC + length features. This is useful for quick experimentation or for machines without BLAST+.

- **Different datasets**  
  You can swap out `Positive_Final.fasta` and `Negative_Final.fasta` with your own datasets:
  - Make sure FASTA headers have unique IDs.
  - Rebuild `all_sequences.fasta` and re-run `split.py` + `generate_pssm.bat`.

---

## Results

The notebook prints:
- **Test set metrics** (accuracy, precision, recall, F1, ROC-AUC)  
- **5-fold cross-validation performance**  
- **Feature importance plot** for EIPP + AAC features  
- Example predictions (predicted label and probability) for a few randomly chosen proteins.

Exact numbers will depend on:
- The dataset version
- PSSM generation parameters
- Random seed and train/test split

---

## Acknowledgements

This project is inspired by:

> Wang, L., Huang, C., Yang, M.-Q., & Yang, J. Y. (2013). Prediction of RNA-binding proteins using a random forest algorithm combined with a novel RNA-binding residue predictor. *Journal of Theoretical Biology*, 1–9.

We also acknowledge the authors and maintainers of:
- **UniProtKB/Swiss-Prot**, for curated protein sequence data  
- **NCBI BLAST+**, for PSI-BLAST and PSSM generation  
- **scikit-learn**, **NumPy**, **pandas**, and **matplotlib** for model implementation and analysis  

---

## Contributors
- **[Riddhi Mehta](https://github.com/riddhimehta15)**
- **[Nirvisha Soni](https://github.com/Nirvisha82)**

