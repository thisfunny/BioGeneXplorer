# BioGeneXplorer

**A modular Python tool for integrated gene and genome analysis**  
Uses BLAST+ and MySQL to detect gene presence, filter duplicates, and produce summary statistics — all offline.

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Directory Structure](#directory-structure)  
- [Input Data](#input-data)  
- [Running the Pipeline](#running-the-pipeline)  
- [Output Files](#output-files)  
- [Code Modules](#code-modules)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **Automated file management:** Scans your gene/genome folders and syncs to a MySQL database.  
- **Offline BLAST:** Builds a local nucleotide database and runs `blastn` on each gene.  
- **Dynamic cutoffs:** Filters hits by identity (e.g. ≥85%) and coverage (e.g. ≥90%).  
- **Duplicate detection:** Pairwise BLAST comparisons flag near-identical sequences.  
- **Statistical reporting:** Aggregates gene-presence, cutoff, duplicate, and diversity metrics.  
- **Exports:** Writes results as Excel (and CSV/JSON if desired) for downstream analysis.

---

## Requirements

- **Python 3.7+**  
- **MySQL server** (client must allow connections with your `root` or specified user)  
- **BLAST+ (NCBI)** in your `$PATH` (`makeblastdb`, `blastn`)  
- Python packages (install via `pip`):  
  ```bash
  pip install mysql-connector-python pandas
  ```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/BioGeneXplorer.git
   cd BioGeneXplorer
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure BLAST+ executables are installed and accessible:
   ```bash
   makeblastdb -version
   blastn -version
   ```

4. Create your gene and genome sample folders (see [Input Data](#input-data)).

---

## Configuration

Open `model/DB/db_model.py` and edit the `self.db_info` dictionary in the `DB` class to match your MySQL credentials:

```python
self.db_info = {
    'host':     'localhost',
    'user':     'root',
    'password': 'YOUR_DB_PASSWORD',
    'database': 'wgs2'
}
```

---

## Directory Structure

```
BioGeneXplorer/
├── model/
│   ├── BL/
│   │   ├── MainProcess.py
│   │   ├── StatisticalResultProcess.py
│   │   └── DuplicateCheck.py
│   ├── DB/
│   │   └── db_model.py
│   └── entity/
│       ├── BLAST.py
│       ├── BlastResults.py
│       ├── Combine.py
│       ├── Concatenate.py
│       ├── Gene.py
│       ├── WholeGenome.py
│       └── StatisticalReport.py
├── test.py             ← Main entry point
├── results/            ← Generated at runtime
│   ├── blast_results/  
│   └── analysis_results/
└── requirements.txt
```

---

## Input Data

- **Gene samples folder**  
  A directory containing one or more FASTA files (`.fasta` or `.fas`) of individual gene sequences.  
  Example:
  ```
  genes_sample/
  ├── geneA.fasta
  ├── geneB.fasta
  └── geneC.fasta
  ```

- **Genome samples folder**  
  A directory of whole-genome FASTA files.  
  Example:
  ```
  whole_genome/
  ├── genome1.fasta
  ├── genome2.fasta
  └── genome3.fasta
  ```

In `test.py`, set the paths:
```python
gene_sample_path   = r'path/to/genes_sample'
genome_sample_path = r'path/to/whole_genome'
```

---

## Running the Pipeline

From the repository root:

```bash
python test.py
```

By default, the script will:

1. **(Re)create** the `results/` and `wgs/` folders.
2. **Drop** the existing `wgs2` database (if `create_drop=True`), then recreate it.
3. **Scan** your gene/genome folders and register files in MySQL.
4. **Combine** genome FASTA files into `results/combined_wgs.fasta`.
5. **Build** a local BLAST database (`wgs/WGS`).
6. **Loop** through each gene:
   - Run `blastn` against the combined genome DB.
   - Create a gene-specific result table.
   - Insert BLAST hits into MySQL.
   - Update `cutoff` flags based on identity/coverage thresholds.
   - Detect and flag duplicates.
7. **Perform** statistical analysis across all genes.
8. **Export** final reports to `results/analysis_results/statistical_result.xlsx` and `genome_gene.xlsx`.

---

## Output Files

- **results/combined_wgs.fasta**  
  All genomes concatenated with modified headers (`>genomeName|originalHeader`).

- **results/blast_results/**  
  CSV files of raw BLAST hits for each gene, plus per-gene folders of query/subject FASTA dumps.

- **results/analysis_results/statistical_result.xlsx**  
  Excel report summarizing for each gene:  
  - Total hits, gene-presence count & %, cutoff count & %, duplicate & diversity metrics.

- **results/analysis_results/genome_gene.xlsx**  
  Presence/absence matrix of genomes vs. genes (1 = present & passing cutoff).

---

## Code Modules

- **`db_model.py`**  
  MySQL connection, table creation, insertion, update, custom queries, and export.

- **`Combine.py`**  
  - `create_results_folder()`  
  - `create_combined_wgs()` — embeds genome names in FASTA headers.

- **`BLAST.py`**  
  - `create_blast_database()`  
  - `blast()` — runs `blastn` and writes CSV outputs.

- **`DuplicateCheck.py`**  
  - Pairwise BLAST of sequences flagged present.  
  - Flags duplicates in the database.

- **`StatisticalResultProcess.py`**  
  - Aggregates data from gene tables.  
  - Calculates and inserts statistics.

- **`MainProcess.py`**  
  Orchestrates the full workflow in `process()`.

- **Entity classes (`Gene.py`, `WholeGenome.py`, etc.)**  
  Simple data containers and JSON serializers for MySQL rows.

---

## Contributing

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/my-feature`).  
3. Commit your changes (`git commit -m 'Add new feature'`).  
4. Push to your branch (`git push origin feature/my-feature`).  
5. Open a pull request.

Please ensure you update the README and add tests where applicable.

---

## License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.
