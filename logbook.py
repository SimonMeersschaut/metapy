import converter
from fpdf import FPDF
import glob
import json
import argparse
import os
import datetime
import sys
import converter
import datetime

current_filename = ''

DEFAULT_FONTSIZE = 9
TITLE_FONTSIZE = 16

class PDF(FPDF):
    def footer(self):
      global current_filename
      # Go to 1.5 cm from bottom
      self.set_y(-15)
      # Select Arial italic 8
      self.set_font('Arial', 'I', 8)
      # Print centered page number
      # try:
      self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'L')
      # except:
      #   print('s')
      self.cell(0, 10, current_filename, 0, 0, 'R')
    
def render_metafiles(metafiles:list, outputfile:str, frontpage:bool=True, title="PDF file"):
  global current_filename
  # setup PDF
  pdf = PDF('P', 'mm', 'A4')

  if frontpage:
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font('Courier', '', 20)
    #pdf.cell(w = 210, h = 10, txt=f'Logbook for {segment}', border = 1, ln = 1, align = 'C', fill = False, link = '')
    #pdf.cell(w = 210, h = 10, txt=f"Created on", border = 1, ln = 1, align = 'C', fill = False, link = '')
    pdf.set_margins(0, 0, 0)
    pdf.cell(w = 210, h = 10, txt=f'', border = 0, ln = 1, align = 'C', fill = False, link = '')
    now = datetime.datetime.now()
    pdf.cell(w = 210, h = 10, txt=f"Segment {title}", border = 0, ln = 1, align = 'C', fill = False, link = '')
    pdf.set_font('Courier', '', 15)
    pdf.cell(w = 210, h = 10, txt=f"Created on {now.strftime('%Y.%m.%d')}", border = 0, ln = 1, align = 'C', fill = False, link = '')
  

  # render files
  pdf.set_font('Courier', '', 15)
  pdf.set_margins(10, 0, 10)
  pdf.add_page()
  for i, current_filename in enumerate(metafiles):
    print(f'reading {current_filename}')
    with open(current_filename, 'r') as f:
      render_metafile(pdf, f.read())
      if i != len(metafiles) -1:
        pdf.add_page()

  # output pdf file
  try:
    pdf.output(f'logbook_{outputfile}.pdf', 'F')
  except PermissionError:
    raise PermissionError("Permission denied. Is the logbook opened by another program?")

def render_metafile(pdf:FPDF, content:str) -> None:
  json_data = json.loads(converter.meta_to_json(content))
  try:
    activity = json_data['Activity']
  except KeyError:
    activity = '?'
  pdf.set_font('Courier', '', TITLE_FONTSIZE)
  pdf.ln(5)
  pdf.cell(w = 40, h = 10, txt=activity, border = 0, ln = 1, align = '', fill = False, link = '')
  pdf.set_font('Courier', '', DEFAULT_FONTSIZE)
  # pdf.set_y(-5)
  # pdf.cell(0, 0, txt='')
  pdf.ln(7)
  pdf.multi_cell(w=0, h=.08*len(content.split('\n')), txt=content, border=0)
  # pdf.write(5, content)


def main():
  parser = argparse.ArgumentParser(description='')
  current_path = os.getcwd()

  args = sys.argv[1:] # skip filename
  # print(args)
  if args[0] == "-i": # interval

    # parser.add_argument('startdate', type=str)
    # parser.add_argument('enddate', type=str)
    # args = parser.parse_args()
    begindate = datetime.datetime.strptime(args[1], '%Y.%m.%d_%H:%M')
    enddate = datetime.datetime.strptime(args[2], '%Y.%m.%d_%H:%M')
    # print(begindate)

    segment = current_path.split("\\analysis")[0].split('\\')[-1]
    ## check if pdf is accessible
    try:
      with open(f'logbook_{segment}.pdf', 'w') as f:
        pass
    except PermissionError:
      raise PermissionError("Permission denied. Is the logbook opened by another program?")

    metafiles = glob.glob(current_path + '/../datafiles/*.meta')
    # filter files by date
    filtered = []
    for metafile in metafiles:
      with open(metafile, 'r') as f:
        content = f.read()
      data = json.loads(converter.meta_to_json(content))
      if begindate < datetime.datetime.strptime(data["Date"]+"_"+data["Time"], '%Y.%m.%d_%H:%M') < enddate:
        filtered.append(metafile)

    # print(filtered)
    render_metafiles(filtered, segment, frontpage=True, title=segment)
  else:
    file = args[1].split("\\")[-1]
    render_metafiles([file], file, frontpage=False)
  
    


if __name__ == '__main__':
  # try:
    main()
    print('success')
  # except Exception as e:
  #   print('ERORR:')
  #   print(e)
  #   input('[enter to quit]')

    

