import glob
import converter
import os
import json
import argparse
import datetime

def create_snaptshot(max_date:str = None):
    if max_date == None:
        now = datetime.datetime.now()
        max_date= now.strftime('%Y.%m.%d_%H.%M')
        max_moment = datetime.datetime.strptime(max_date, '%Y.%m.%d_%H.%M') 
        # used to make the <now> less accurate
        # -> so the files that have been written a few seconds ago also get included
    else:
        max_moment = datetime.datetime.strptime(max_date+'_23.59', '%Y.%m.%d_%H.%M')
    snapshot = '{'

    folders = glob.glob('../*')
    folders = [folder for folder in folders if not('__' in folder) and os.path.isdir(folder)]
    
    for i, folder in enumerate(folders):
        metafiles = glob.glob(folder+'\\datafiles\\*.meta')
        
        filtered = []
        for metafile in metafiles:
            try:
                if datetime.datetime.strptime(metafile.split('.meta')[0].split('datafiles\\')[-1][:-1], '%Y.%m.%d_%H.%M') <= max_moment:
                    filtered.append(metafile)
            except:
                raise Exception(f'[SNAPSHOT] "{metafile}" does not match file format (in folder "{folder}").')
        if len(filtered) == 0:
            if len(metafiles) > 0:
                raise Exception(f'[SNAPSHOT] All files were filtered out (in folder "{folder}")!')
            else:
                raise Exception(f'[SNAPSHOT] "{folder}"-folder is empty. Maybe you want to exclude this file by putting "__" in the foldername. (no snapshot has been made)')
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
    
    with open('../__snapshot__.json', 'w') as f:
        f.write(snapshot)


def main():
    parser = argparse.ArgumentParser(description='Create a snapshot of all machines (take the last log-file and combine them into a json file).')
    parser.add_argument('-d', '--date', type=str, help="the moment of the status (take the file that was last uploaded at this moment). format: 'YYYY.MM.DD'", default=None, action='store')
    args = parser.parse_args()

    if args.date: # is given
        create_snaptshot(max_date=args.date)
    else:
        create_snaptshot()
    
    print('[SUCCESS] created a snapshot')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input('[ENTER] to quit')
        exit()