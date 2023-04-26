import pandas as pd
import jsonlines
import os
import sys

if __name__ == '__main__':
    data_directory = sys.argv[1]
    amd_cpu = pd.read_csv(os.path.join(data_directory,'amd_cpu_specs(updated_core_format).csv'))
    intel_cpu = pd.read_csv(os.path.join(data_directory, 'intel_cpu_specs.csv'))

    with jsonlines.open(os.path.join(data_directory,'cpu_specs'),'w') as writer:

        for i, row in amd_cpu.iterrows():
            obj = {'name':row['Name'],'Codename':row['Codename'],'Cores':row['Cores'],'Clock':row['Clock'],'Socket':row['Socket'],
                   'Process':row['Process'],'L3 Cache':row['L3 Cache'],'TDP':row['TDP'],'Released':row['Released'],'Company':'AMD'}
            writer.write(obj)

        for i, row in intel_cpu.iterrows():
            obj = {'name': row['Name'], 'Codename': row['Codename'], 'Cores': row['Cores'], 'Clock': row['Clock'],
                   'Socket': row['Socket'],
                   'Process': row['Process'], 'L3 Cache': row['L3 Cache'], 'TDP': row['TDP'],
                   'Released': row['Released'], 'Company': 'Intel'}
            writer.write(obj)
