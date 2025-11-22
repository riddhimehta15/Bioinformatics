import os
import re

# If all_sequences.fasta is in the parent folder ("Project"), use this path:
input_fasta = "../all_sequences.fasta"  # adjust if needed
output_dir = "split_seqs"

os.makedirs(output_dir, exist_ok=True)

def sanitize_id(raw_id: str) -> str:
    """
    Make a safe filename from a FASTA header ID.
    - Keep letters, numbers, underscore, dash, dot
    - Replace everything else with '_'
    - Limit length to 80 chars to avoid crazy-long filenames
    """
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", raw_id)
    return safe[:80]  # in case IDs are huge

current_id = None
current_lines = []

with open(input_fasta, "r") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue

        if line.startswith(">"):
            # save previous sequence
            if current_id is not None:
                safe_id = sanitize_id(current_id)
                out_path = os.path.join(output_dir, f"{safe_id}.fasta")
                with open(out_path, "w") as out_f:
                    out_f.write(">" + current_id + "\n")
                    out_f.write("\n".join(current_lines) + "\n")

            # start new
            current_id = line[1:].split()[0]  # ID is first token after '>'
            current_lines = []
        else:
            current_lines.append(line)

# save last sequence
if current_id is not None:
    safe_id = sanitize_id(current_id)
    out_path = os.path.join(output_dir, f"{safe_id}.fasta")
    with open(out_path, "w") as out_f:
        out_f.write(">" + current_id + "\n")
        out_f.write("\n".join(current_lines) + "\n")

print("Done splitting FASTA into split_seqs/")
