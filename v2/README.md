# RES-SAT Procedure

## Main Directory Structure

```
v2
 ┣ dataset
 ┃ ┣ generated
 ┃ ┃ ┣ 2sat_1000l_5000c.cnf
 ┃ ┃ ┣ 2sat_100l_500c.cnf
 ┃ ┃ ┣ 2sat_30l_100c.cnf
 ┃ ┗ ┗ 2unsat_100l_500c.cnf
 ┣ src
 ┃ ┣ dataset_sat.py
 ┃ ┣ dataset_unsat.py
 ┃ ┗ res_sat.py
 ┣ .gitignore
 ┣ README.md
 ┗ requirements.txt
```

## How to Run

**Generate Dataset**

- `dataset_sat.py`: Membuat dataset yang bersifat satisfiable dan merupakan script python yang menerima argumen sebagai berikut:
  - `nvars`: Jumlah literal yang ingin dibuat.
  - `nclauses`: Jumlah klausa yang ingin dibuat dengan jumlah literal.
  - `output`: File output yang dihasilkan dari pembuatan dataset dalam format `.cnf`.
- `dataset_sat.py`: Membuat dataset yang bersifat unsatisfiable dan merupakan script python yang menerima argumen sebagai berikut:
  - `nvars`: Jumlah literal yang ingin dibuat.
  - `nclauses`: Jumlah klausa yang ingin dibuat dengan jumlah literal.
  - `output`: File output yang dihasilkan dari pembuatan dataset dalam format `.cnf`.

**Running RES-SAT**

- `res_sat.py`: Menjalankan algoritma RES-SAT terhadap suatu dataset kumpulan klausa dalam bentuk CNF dengan argumen sebagai berikut:
  - `output`: File output yang dihasilkan dari script generate dataset sebelumnya.
