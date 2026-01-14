# Instructions

1. **Place MM/P(G)BSA results from AMBER into the `gpbsa` folder.**
   - The input file for calculations (`mmpbsa.in`) is provided in the current directory as an example.

2. **Run the Python script for processing MM/P(G)BSA data.**
   - Execute `python getout_GBSAPBSA.py` in the current directory to generate `gpbsa.csv`.

3. **Prepare data for ΔvinaXGB calculations.**
   - Create a folder (e.g., `examples`) to store the structural data you wish to analyze.

4. **Setup deltavinaXGB.**
   - Install deltavinaXGB and place `get_SASA.py` in the `deltaVinaXGB-Light/DXGB` directory.

5. **Adjust paths in `get_SASA.py` script.**
   - Modify the path in `get_SASA.py` to point to the `examples` folder created in step 3.

6. **Run `get_SASA.py`.**
   - Execute `python get_SASA.py` to obtain `Test_SASA.csv` in the `examples` folder.

7. **Process SASA data further.**
   - Place `get_S1.py` in the `examples` folder.
   - Run `python get_S1.py` to create `Test_SASA_all.csv`.
   - Copy `Test_SASA_all.csv` to the current directory.

8. **Generate `RB.csv`.**
   - From the current directory, execute `python get_S2.py` to produce `RB.csv`.

9. **Combine all data.**
   - Run `python get_all.py` in the current directory to generate `all.csv`.

10. **Review final results.**

    - In `all.csv`, 'P-DP+S' and 'G+S_atoms' represent the recommended improved MM/GBSA and MM/PBSA methods' results discussed in the article.

