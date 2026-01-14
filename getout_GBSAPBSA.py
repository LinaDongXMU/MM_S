import os
import re
import csv


def main():
    path = './gpbsa'

    add = open('./gpbsa.csv', 'w')
    addWriter = csv.writer(add)

    d = [
        'id',
        'GC-vdw','GC-ele','GC-gb','GC-sa',
        'GL-vdw','GL-ele','GL-gb','GL-sa',
        'GP-vdw','GP-ele','GP-gb','GP-sa',
        'GA-vdw','GA-ele','GA-gb','GA-sa',
        'GTotal',
        'PC-vdw','PC-ele','PC-Pb','PC-sa','PC-di',
        'PL-vdw','PL-ele','PL-pb','PL-sa','PL-di',
        'PP-vdw','PP-ele','PP-pb','PP-sa','PP-di',
        'PA-vdw','PA-ele','PA-pb','PA-sa','PA-di',
        'PTotal'
    ]
    addWriter.writerow(d)

    for filename in os.listdir(path):
        final = re.compile(r'_FINAL_RESULTS_MMPBSA.dat')
        mo = final.search(filename)
        if mo is None:
            continue

        line = []
        id = filename[:-25]

        file1 = open(os.path.join(path, filename))
        content = file1.read()
        file1.close()

        # =========================
        # GB section
        # =========================
        GB = re.compile(r'GENERALIZED BORN:.*?POISSON BOLTZMANN:', re.DOTALL)
        GB1 = GB.search(content).group()

        complex = re.compile(r'Complex:.*?TOTAL', re.DOTALL)
        complex1 = complex.search(GB1).group()

        v = re.compile(r'VDWAALS\s+\S+')
        v3 = re.search(r'\s\S+', v.search(complex1).group()).group()[1:]

        e = re.compile(r'EEL\s+\S+')
        e3 = re.search(r'\s\S+', e.search(complex1).group()).group()[1:]

        g = re.compile(r'EGB\s+\S+')
        g3 = re.search(r'\s\S+', g.search(complex1).group()).group()[1:]

        s = re.compile(r'ESURF\s+\S+')
        s3 = re.search(r'\s\S+', s.search(complex1).group()).group()[1:]

        ligand = re.compile(r'Ligand:.*?TOTAL', re.DOTALL)
        ligand1 = ligand.search(GB1).group()

        vv3 = re.search(r'\s\S+', re.search(r'VDWAALS\s+\S+', ligand1).group()).group()[1:]
        ee3 = re.search(r'\s\S+', re.search(r'EEL\s+\S+', ligand1).group()).group()[1:]
        gg3 = re.search(r'\s\S+', re.search(r'EGB\s+\S+', ligand1).group()).group()[1:]
        ss3 = re.search(r'\s\S+', re.search(r'ESURF\s+\S+', ligand1).group()).group()[1:]

        protein = re.compile(r'Receptor:.*?TOTAL', re.DOTALL)
        protein1 = protein.search(GB1).group()

        vvv3 = re.search(r'\s\S+', re.search(r'VDWAALS\s+\S+', protein1).group()).group()[1:]
        eee3 = re.search(r'\s\S+', re.search(r'EEL\s+\S+', protein1).group()).group()[1:]
        ggg3 = re.search(r'\s\S+', re.search(r'EGB\s+\S+', protein1).group()).group()[1:]
        sss3 = re.search(r'\s\S+', re.search(r'ESURF\s+\S+', protein1).group()).group()[1:]

        all = re.compile(r'Differences.*?TOTAL', re.DOTALL)
        all1 = all.search(GB1).group()

        vvvv3 = re.search(r'\s\S+', re.search(r'VDWAALS\s+\S+', all1).group()).group()[1:]
        eeee3 = re.search(r'\s\S+', re.search(r'EEL\s+\S+', all1).group()).group()[1:]
        gggg3 = re.search(r'\s\S+', re.search(r'EGB\s+\S+', all1).group()).group()[1:]
        ssss3 = re.search(r'\s\S+', re.search(r'ESURF\s+\S+', all1).group()).group()[1:]

        line.extend([
            id,
            v3, e3, g3, s3,
            vv3, ee3, gg3, ss3,
            vvv3, eee3, ggg3, sss3,
            vvvv3, eeee3, gggg3, ssss3,
            round(float(vvvv3) + float(eeee3) + float(gggg3) + float(ssss3), 4)
        ])

        # =========================
        # PB section
        # =========================
        PB = re.compile(
            r'POISSON BOLTZMANN:.*?-------------------------------------------------------------------------------\n-------------------------------------------------------------------------------',
            re.DOTALL
        )
        PB1 = PB.search(content).group()

        complex1 = re.search(r'Complex:.*?TOTAL', PB1, re.DOTALL).group()

        def get_val(block, key):
            return re.search(r'\s\S+', re.search(key + r'\s+\S+', block).group()).group()[1:]

        line.extend([
            get_val(complex1, 'VDWAALS'),
            get_val(complex1, 'EEL'),
            get_val(complex1, 'EPB'),
            get_val(complex1, 'ENPOLAR'),
            get_val(complex1, 'EDISPER')
        ])

        ligand1 = re.search(r'Ligand:.*?TOTAL', PB1, re.DOTALL).group()
        protein1 = re.search(r'Receptor:.*?TOTAL', PB1, re.DOTALL).group()
        all1 = re.search(r'Differences.*?TOTAL', PB1, re.DOTALL).group()

        for block in (ligand1, protein1):
            line.extend([
                get_val(block, 'VDWAALS'),
                get_val(block, 'EEL'),
                get_val(block, 'EPB'),
                get_val(block, 'ENPOLAR'),
                get_val(block, 'EDISPER')
            ])

        vals = [
            get_val(all1, 'VDWAALS'),
            get_val(all1, 'EEL'),
            get_val(all1, 'EPB'),
            get_val(all1, 'ENPOLAR'),
            get_val(all1, 'EDISPER')
        ]
        line.extend(vals)
        line.append(round(sum(map(float, vals)), 4))

        addWriter.writerow(line)

    add.close()


if __name__ == '__main__':
    main()
