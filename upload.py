import converter
import glob
import json
from datetime import datetime
import string
import os
import sys
import snapshot

def upload_meta(metadata:str, allowed_keywords_filename:str):
  success, keyword = check_keywords(metadata, allowed_keywords_filename)
  if not success:
    return (False, f'The following keywods in the metadata did not match those of the allowedkeywords file: {keyword}.')
  # First convert it to a dictionary to perform a check
  json_data = json.loads(converter.meta_to_json(metadata))
  if file_already_uploaded(json_data)[0]:
    # file already uploaded
    return (False, 'This file is already used in: '+file_already_uploaded(json_data)[1])
    # input('Press [enter] to exit')
    # exit()
  else:
    # file not yet uploaded
    # => UPLOAD
    with open(f"datafiles/{generate_filename(json_data['Date'], json_data['Time'])}", 'w+') as f:
      f.write(metadata)
    snapshot.create_snaptshot()
    return (True, 'successfully uploaded the file')

def check_keywords(metadata:str, allowed_keywords_filename:str) -> bool:
  '''Check if all keys in the metadata are also in the allowed keywords file.'''
  keys = list(json.loads(converter.meta_to_json(metadata)).keys())
  with open(allowed_keywords_filename, 'r') as f:
    allowed_keys = list(json.loads(converter.meta_to_json(f.read())).keys())
  for key in keys:
    if key not in allowed_keys:
      return (False, key)
  return (True, '/')


def file_already_uploaded(json_data:dict) -> (bool, str):
  '''
  Check in all uploaded files if the same date is entered (date & time).
  '''
  # Check for meta files
  for filename in glob.glob('datafiles/*.meta'):
    checking_file_date = filename.split('.meta')[0].split('datafiles\\')[-1]
    # now, we don't need to check the content of the files, as the time is also written in the filename
    try:
      print(checking_file_date, json_data['Date']+'_'+json_data['Time'].replace(':', '.'))
      if checking_file_date == json_data['Date']+'_'+json_data['Time'].replace(':', '.'):
        return (True, filename) # file already uploaded
    except KeyError:
      print('No date in previously uploaded meta file')
  
  return (False, None)

def generate_filename(date:str, time:str) -> str:
  '''
  Generates a filename for a new meta file.
  -> format: the date (Year.Month.day) + a letter (to avoid duplicate filenames)
  '''
  return f'{date}_{time.replace(":", ".")}.meta'

if __name__ == '__main__':
  # Upload file
  # TODO allowedkeywords
  try:
    allowed_keywords_filename = sys.argv[1]
    filename = sys.argv[2]
  except:
    input('Please give the right arguments: allowed_keywords, filename_to_upload')
    exit()
  print('Uploading: '+filename)
  with open(filename, 'r') as f:
    content = f.read()
  success, msg = upload_meta(content, allowed_keywords_filename)
  if success:
    print('[SUCCESS] uploaded the file')
  else:
    print('[ERROR] '+msg)