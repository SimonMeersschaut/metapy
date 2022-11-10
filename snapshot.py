import glob
import converter
import os
import json

def create_snaptshot():
    snapshot = '{'

    folders = glob.glob('\\\\winbe.imec.be/wasp/meta/*')
    folders = [folder for folder in folders if not('__' in folder) and os.path.isdir(folder)]
    
    for i, folder in enumerate(folders):
        metafiles = glob.glob(folder+'\\datafiles\\*.meta')
        last_file = sorted(metafiles)[-1]
        with open(last_file, 'r') as f:
            content = f.read()
            json_data = converter.meta_to_json(content)
            #print(json_data)
        if i != 0:
            snapshot += ', '
        snapshot += f'"' + folder.split('meta\\')[-1] + f'": {json_data}'
        #snapshot.update({folder.split('meta\\')[-1]:json_data})
    
    snapshot += '}'
    
    with open('\\\\winbe.imec.be/wasp/meta/test.dat', 'w+') as f:
        f.write(snapshot)

if __name__ == '__main__':
    create_snaptshot()