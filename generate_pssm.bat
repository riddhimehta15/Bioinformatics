@echo off
REM Run this FROM: ...\Project\pssm

mkdir pssm_out

for %%F in (split_seqs\*.fasta) do (
    echo Processing %%F
    psiblast -query "%%F" -db mini_db -num_iterations 3 -out_ascii_pssm "pssm_out\%%~nF.pssm"
)
