import converter
from fpdf import FPDF
import glob
import json
import argparse
import os

current_filename = ''

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

def render_metafile(pdf:FPDF, content:str) -> None:
  json_data = json.loads(converter.meta_to_json(content))
  print(json_data)
  try:
    activity = json_data['Activity']
  except KeyError:
    activity = '?'
  pdf.set_font('Courier', '', 16)
  pdf.ln(5)
  pdf.cell(w = 40, h = 10, txt=activity, border = 0, ln = 1, align = '', fill = False, link = '')
  pdf.set_font('Courier', '', 10)
  # pdf.set_y(-5)
  # pdf.cell(0, 0, txt='')
  pdf.ln(7)
  pdf.multi_cell(w=0, h=.11*len(content.split('\n')), txt=content, border=0)
  # pdf.write(5, content)


def main():
  parser = argparse.ArgumentParser(description='')
  current_path = os.getcwd()
  parser.add_argument('startdate', type=str)
  parser.add_argument('enddate', type=str)
  args = parser.parse_args()

  global current_filename
  # setup
  pdf = PDF('P', 'mm', 'A4')
  pdf.add_page()
  pdf.set_margins(0, 0, 0)

  # write meta files
  # for segment in [folder for folder in glob.glob('../*') if not('__' in folder) and not('.' in folder.split('..\\')[1])]:
    # print(segment)
    # print(metafiles)
  print(current_path)
  metafiles = glob.glob(current_path + '/../datafiles/*.meta')
  print(metafiles)
  for current_filename in metafiles:

    with open(current_filename, 'r') as f:
      pdf.add_page()
      render_metafile(pdf, f.read())


  # output pdf file
  segment = current_path.split("\\analyse")[0].split('\\')[-1]
  pdf.output(f'logbook_{segment}.pdf', 'F')


if __name__ == '__main__':
  main()

