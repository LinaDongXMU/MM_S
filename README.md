**MM_S in AmberTools**

MM_S is an extended post-processing pipeline for MM/P(G)BSA
calculations, designed to integrate seamlessly with AMBER MMPBSA.py.

MM_S is implemented as an optional post-processing module triggered
directly from MMPBSA.py, without modifying the core MM/PBSA energy
evaluation workflow.

**1. Modifications to AMBER (MMPBSA.py)**

**1.1 Design principle**

- **No modification** to AMBER force field, MD engine, or energy
  calculation

- MM_S is executed **after** standard MMPBSA results are generated

- Controlled by a **single input flag** in mmpbsa.in

- MM_S is treated as an **external plugin**, not embedded into AMBER
  source code

------------------------------------------------------------------------

**1.2 Added files**

The following file was added to AMBER:

AmberTools/src/mmpbsa_py/MMPBSA_mods/postprocess_mms.py

This module defines:

- run_mms() -- orchestrates the MM_S post-processing pipeline

- MMSPostProcessError -- unified error handling for MM_S failures

------------------------------------------------------------------------

**1.3 Changes to main.py**

In

AmberTools/src/mmpbsa_py/MMPBSA_mods/main.py

the method write_final_outputs() was extended as follows:

\# MM_S postprocessing (optional)

if self.INPUT.get(\'run_mm_s\', False):

try:

run_mms(None, self.stdout)

except MMSPostProcessError as err:

raise InternalError(str(err))

This ensures that:

- MM_S runs **only when explicitly enabled**

- Failure of MM_S does **not affect MM/PBSA energy calculation**

- Errors are reported in a controlled and user-readable manner

------------------------------------------------------------------------

**1.4 Activating MM_S in mmpbsa.in**

To enable MM_S, add the following flag:

&general

run_mm_s = 1,

/

If this flag is absent or set to 0, AMBER behaves exactly as the
original version.

------------------------------------------------------------------------

**2. Installing and Using MM_S**

**2.1 MM_S installation**

MM_S is installed **outside AMBER**, as an independent software module.

Recommended directory structure:

\$HOME/MM_S/

├── getout_GBSAPBSA.py

├── get_SASA.py

├── get_S1.py

├── get_S2.py

├── get_all.py

└── sasa/

├── featureSASA.py

├── pharma.py

├── pdb_to_xyzr

└── atmtypenumbers

------------------------------------------------------------------------

**2.2 External dependencies**

MM_S relies on the following external tools:

**Required**

1.  **MSMS**

    - Used for solvent-accessible surface area (SASA) calculation

    - Download MSMS from <http://mgltools.scripps.edu/downloads>

```
mkdir msms
tar -xvzf msms_i86_64Linux2_2.6.1.tar.gz -C msms
cd msms
cp msms.x86_64Linux2.2.6.1 msms
```


    - Ensure msms is callable from the command line:
   
    
```
msms -h
```

2.  **OpenBabel (with PyBel interface)**

    - Required for molecular format handling and pharmacophore
      assignment

    - Recommended installation:

```
conda install -c conda-forge openbabel
```

3.  **Python ≥ 3.7**

    - With standard scientific libraries (numpy, pandas)

    - Typically already available in AMBER environments

------------------------------------------------------------------------

**2.3 Environment variable setup**

Before running MMPBSA.py with MM_S enabled, set:

```
export MM_S_HOME=/path/to/MM_S
export MMS_ATMTYPENUMBERS=\$MM_S_HOME/sasa/atmtypenumbers
export PATH=\$MM_S_HOME/sasa:\$PATH
```

These variables are required to:

- Locate MM_S scripts

- Enable pdb_to_xyzr to locate atom-type radius definitions

- Ensure compatibility with MSMS

------------------------------------------------------------------------

**2.4 Required input files**

In addition to standard MMPBSA inputs, MM_S requires the following
directory:

examples/

└── \<case_id\>/

├── \<case_id\>\_protein.pdb

├── \<case_id\>\_ligand.mol2

Notes:

- Protein and ligand structures must correspond to the same complex

- Atom naming must be compatible with OpenBabel

- Hydrogen atoms are handled internally (united-atom approach)

------------------------------------------------------------------------

**3. MM_S Execution Pipeline**

When run_mm_s = 1 is enabled, the following steps are executed
automatically:

1.  **MM/P(G)BSA calculation**

    - Standard AMBER workflow

    - Produces FINAL_RESULTS_MMPBSA.dat

2.  **Energy extraction**

3.  getout_GBSAPBSA.py

→ gpbsa.csv

4.  **MSMS-based SASA calculation**

5.  get_SASA.py

→ Test_SASA.csv

6.  **SASA post-processing (S1 terms)**

7.  get_S1.py

→ Test_SASA_all.csv

8.  **Ligand flexibility descriptors**

9.  get_S2.py

→ RB.csv

10. **Final data aggregation**

11. get_all.py

→ all.csv

The final output all.csv contains:

- Standard MM/GBSA and MM/PBSA energies

- Pharmacophore-resolved SASA corrections

- Improved scoring terms:

  - P-DP+S

  - G+S

  - P-DP+S_atoms

  - G+S_atoms

------------------------------------------------------------------------

**4. Notes and Best Practices**

- MM_S does **not modify** MM/PBSA energies; it augments them

- MM_S can be safely disabled without affecting AMBER results

- All intermediate files are retained for inspection

- Failures in MM_S are reported explicitly and do not corrupt AMBER
  outputs

------------------------------------------------------------------------

**5. Citation and Attribution**

If you use MM_S in your work, please cite:

Dong, L.; Li, P.; Wang, B., Enhancing MM/P(G)BSA Methods: Integration of
Formulaic Entropy for Improved Binding Free Energy Calculations.
*Journal of Computational Chemistry* **2025**, 46, e70093.
