# BioGeneXplorer

Welcome to **BioGeneXplorer**, a user-friendly tool for analyzing gene sequences and preparing submissions to NCBI (National Center for Biotechnology Information).

This guide assumes no prior experience with Python, MySQL, or command-line tools. We’ll walk you through every step so you can get started quickly.

---

## Table of Contents

- [Features](#features)
- [What You’ll Need](#what-youll-need)
- [Dependencies](#dependencies)
- [Download & Setup](#download--setup)
- [Configure Your Project](#configure-your-project)
- [Project Structure](#project-structure)
- [Code Modules](#code-modules)
- [How to Organize Your Files](#how-to-organize-your-files)
- [Running BioGeneXplorer](#running-biogenexplorer)
  - [Using Command Line](#using-command-line)
  - [Using PyCharm (Graphical Interface)](#using-pycharm-graphical-interface)
- [Understanding Inputs & Outputs](#understanding-inputs--outputs)
- [Troubleshooting Tips](#troubleshooting-tips)
- [Advanced Configuration](#advanced-configuration)
- [Performance Note](#performance-note)
- [License](#license)

---

## Features

- **Duplicate Detection** — Identify and filter duplicate gene entries.
- **Statistical Analysis** — Generate statistical summaries of sequence data.
- **Sequence Alignment** — Compare gene sequences using built-in alignment scripts.
- **Automated Submission** — Prepare and submit sequence data to NCBI seamlessly.
- **Extensible Modules** — Support for future charting and phylogenetic tree generation.

## What You’ll Need

1. **A computer running Windows, macOS, or Linux**
2. **Python 3.7 or higher**
3. **MySQL Server**
4. **BioGeneXplorer code** — Downloadable from GitHub.

> If any of these terms are unfamiliar, don’t worry — we provide detailed steps below.

## Dependencies

BioGeneXplorer relies on several Python libraries:

- **Biopython** — For reading and handling sequence files
- **pandas** — For data tables and CSV/JSON output
- **matplotlib** — For generating charts (in future modules)

Install them all via:

```bash
pip install -r requirements.txt
```

---

## Download & Setup

### 1. Install Python

- Visit [python.org](https://www.python.org/downloads/) and download the latest Python 3 installer.
- On Windows, ensure you check **Add Python to PATH**.
- Follow on-screen instructions.

### 2. Install MySQL Server

- **Windows**: Download MySQL Installer from [dev.mysql.com](https://dev.mysql.com/downloads/installer/) and choose “Developer Default.”
- **macOS**: `brew install mysql`
- **Linux (Ubuntu)**: `sudo apt-get install mysql-server`
- Start MySQL:
  - Windows: Start “MySQL80” service.
  - macOS/Linux: `mysql.server start`

### 3. Clone the Repository

```bash
git clone https://github.com/yourusername/BioGeneXplorer.git
cd BioGeneXplorer
```

*(Or download ZIP and extract.)*

### 4. Install Python Libraries

```bash
pip install -r requirements.txt
```

---

## Configure Your Project

### MySQL Database Settings

1. Open a MySQL client:
   - Windows: MySQL Workbench
   - macOS/Linux: `mysql -u root -p`
2. Create database and user:
   ```sql
   CREATE DATABASE biogenexplorer;
   CREATE USER 'bio_user'@'localhost' IDENTIFIED BY 'YourPassword';
   GRANT ALL PRIVILEGES ON biogenexplorer.* TO 'bio_user'@'localhost';
   ```
3. Edit `model/DB/__init__.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',      # or your DB host
       'port': 3306,             # or your DB port
       'user': 'bio_user',       # your DB username
       'password': 'YourPassword',
       'database': 'biogenexplorer'
   }
   ```

### NCBI Submission Settings

Open `Submission/NCBI_submission.py` or `cfg.ini` and update:

```ini
[NCBI]
api_url = https://api.ncbi.nlm.nih.gov/submit
email   = your.email@example.com
```

Add more endpoints or emails as needed.

---

## Project Structure

```
BioGeneXplorer/
├── main.py                   # Entry point for analysis
├── submission_test.py        # Tests for NCBI submission workflows
├── model/                    # Core processing
│   ├── BL/                   # DuplicateCheck, MainProcess, StatisticalResultProcess
│   ├── DB/                   # MySQL connection (DB_CONFIG)
│   ├── align/                # Alignment utilities
│   └── future/               # GeneDiversityChart, phylogenetic tree
├── Submission/               # NCBI submission scripts
│   ├── NCBI_submission.py
│   └── File_process/         # NCBI_file_process.py
└── requirements.txt          # Python dependencies
```

---

## Code Modules

- **model/BL/DuplicateCheck.py** — Filters duplicate gene sequences.
- **model/BL/MainProcess.py** — Orchestrates the analysis pipeline.
- **model/BL/StatisticalResultProcess.py** — Calculates counts, GC content, and other metrics.
- **model/DB/****init****.py** — Defines `DB_CONFIG` and establishes MySQL connections.
- **model/align/** — Scripts and wrappers for sequence alignment.
- **model/future/**
  - `GeneDiversityChart.py` — Generates diversity charts.
  - `tree.py` — Builds phylogenetic trees.
- **Submission/NCBI\_submission.py** — Sends prepared data to NCBI.
- **Submission/File\_process/NCBI\_file\_process.py** — Formats files for submission.

---

## How to Organize Your Files

Create two folders anywhere on your computer:

```
YourProjectFolder/
├── Input_Genes/        # .txt and .fas files go here
└── Output_Results/     # Generated statistics, submissions, and logs
```

---

## Running BioGeneXplorer

### Using Command Line

```bash
python main.py --input /full/path/to/Input_Genes \
               --output /full/path/to/Output_Results
```

### Using PyCharm (GUI)

1. Open the **BioGeneXplorer** folder.
2. Set Python interpreter in **File > Settings > Project > Python Interpreter**.
3. Add run configuration:
   - Script: `main.py`
   - Parameters: `--input /path/to/Input_Genes --output /path/to/Output_Results`
   - Working dir: project root
4. Click **Run**.

---

## Understanding Inputs & Outputs

- **Inputs**:
  - `.txt` files: Plain gene sequences.
  - `.fas` files: FASTA-formatted whole-genome sequences.
- **Outputs** (in `Output_Results/`):
  - **statistics/** — CSV and JSON reports.
  - **submissions/** — `.sqn` or XML files for NCBI.
  - **logs/** — Detailed logs for each run.

---

## Troubleshooting Tips

- **MySQL connection refused**: Verify service running and `DB_CONFIG` settings.
- **Module not found**: Re-run `pip install -r requirements.txt`.
- **Permission errors**: Run terminal/PyCharm as **Administrator** or **sudo**.
- Check `Output_Results/logs/` for error details.

---

## Advanced Configuration

You can extend or customize:

- **Statistical processing**: `model/BL/StatisticalResultProcess.py`
- **Alignment settings**: files under `model/align/`
- **Charting & trees**: `model/future/`

All scripts include comments for guidance.

---

## Performance Note

BioGeneXplorer caches data locally. It runs significantly faster when **offline**, avoiding external network calls.

---

## License

This project is released under the [MIT License](LICENSE).

