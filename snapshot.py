import glob
import converter
import os
import json
import argparse
import datetime

def create_snaptshot(max_date:str):
    max_moment = datetime.datetime.strptime(max_date, '%Y.%m.%d')
    snapshot = '{'

    folders = glob.glob('../*')
    folders = [folder for folder in folders if not('__' in folder) and os.path.isdir(folder)]
    
    for i, folder in enumerate(folders):
        metafiles = glob.glob(folder+'\\datafiles\\*.meta')
        
        filtered = []
        for metafile in metafiles:
            try:
                if datetime.datetime.strptime(metafile.split('.meta')[0].split('datafiles\\')[-1][:-1], '%Y.%m.%d') < max_moment:
                    filtered.append(metafile)
            except:
                print(f'[ALERT] "{metafile}" does not match file format. This file will be skipped.')
        if len(filtered) == 0:
            if len(metafiles) > 0:
                raise Exception('[ERROR] All files were filtered out!')
            else:
                raise Exception(f'[ERROR] "{folder}"-folder is empty. Maybe you want to exclude this file by putting "__" in the foldername.')
        last_file = sorted(filtered)[-1]
        with open(last_file, 'r') as f:
            content = f.read()
            json_data = converter.meta_to_json(content)
            #print(json_data)
        if i != 0:
            snapshot += ', '
        snapshot += f'"' + folder.split('meta\\')[-1] + f'": {json_data}'
        #snapshot.update({folder.split('meta\\')[-1]:json_data})
    
    snapshot += '}'
    
    with open('../snapshot.json', 'w') as f:
        f.write(snapshot)


def main():
    parser = argparse.ArgumentParser(description='Create a snapshot of all machines (take the last log-file and combine them into a json file).')
    parser.add_argument('-d', '--date', type=str, help="the moment of the status (take the file that was last uploaded at this moment). format: 'YYYY.MM.DD'", default=None, action='store')
    args = parser.parse_args()

    if args.date: # is given
        create_snaptshot(max_date=args.date)
    else:
        now = datetime.datetime.now()
        print(now.strftime('%Y.%M.%D'))
        create_snaptshot(max_date= now.strftime('%Y.%m.%d'))
    
    print('[SUCCESS] created a snapshot')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input('[ENTER] to quit')
        exit()