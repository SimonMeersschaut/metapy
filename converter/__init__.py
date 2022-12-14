"""
AUTHOR: Simon Meersschaut
Used at Imec to read & write .meta files.
"""

from . import to_json
from . import to_meta
from . import decoder


def meta_to_json(meta:str) -> str:
  """
  Converts data with a meta-layout (stored in a string) to a JSON format (stored in a string).
  Arguments:
    meta: The meta data stored in a string.
  Returns:
    The corresponding JSON data (stored in a string).
  eg.
  INPUT:
    *
    * Spectrum_ID           := ERD22_071_01A
    * Sample_ID             := PEALD 75C D02
    * Slab_min              := 111
    * Slab_max              := 846
    * 
    * Conc-H[%]             := 8.83
    * Conc-C[%]             := 0.12
    * Conc-N[%]             := 0
    * Conc-O[%]             := 63.42
    * Conc-Si[%]            := 27.63
    *
    * DATE/Time             := 2022.07.15__09:00__20.437
  OUTPUT:
    {

    "Spectrum_ID": "ERD22_071_01A",
    "Sample_ID": "PEALD 75C D02",
    "Slab_min": "111",
    "Slab_max": "846",

    "Conc-H[%]": "8.83",
    "Conc-C[%]": "0.12",
    "Conc-N[%]": "0",
    "Conc-O[%]": "63.42",
    "Conc-Si[%]": "27.63",

    "DATE/Time": "2022.07.15__09:00__20.437"
    }
  """
  return to_json.meta_to_json(meta)

def json_to_meta(json_data:str, template:list = None) -> str:
  """
  Converts json data (stored in a string) to a meta-layout (stored in a string).
  Warning: only works for json data generated by converter, not for json data in one line.
  Arguments:
    json: The json data either a dict or a string.
    format: 
      - a list of keywords.
      - the first key will be displayed first
      - the item `decoder.EmptyLine┬┤ will add a empty line to the metadata-string
      - NOTE: if there is a template-list given, any keys that are not in the list, will NOT be added to the metadata
  Returns:
    The corresponding meta data.
  INPUT:
    {

      "Spectrum_ID": "ERD22_071_01A",
      "Sample_ID": "PEALD 75C D02",
      "Slab_min": "111",
      "Slab_max": "846",

      "Conc-H[%]": "8.83",
      "Conc-C[%]": "0.12",
      "Conc-N[%]": "0",
      "Conc-O[%]": "63.42",
      "Conc-Si[%]": "27.63",

      "DATE/Time": "2022.07.15__09:00__20.437"
    }
  OUTPUT:
    *
    * Spectrum_ID := ERD22_071_01A
    * Sample_ID   := PEALD 75C D02
    * Slab_min    := 111
    * Slab_max    := 846
    *
    * Conc-H[%]   := 8.83
    * Conc-C[%]   := 0.12
    * Conc-N[%]   := 0
    * Conc-O[%]   := 63.42
    * Conc-Si[%]  := 27.63
    *
    * DATE/Time   := 2022.07.15__09:00__20.437
  """
  return to_meta.json_to_meta(json_data, template=template)


def load_format(meta_format:str) -> list:
  '''
    - (key, value)
    - decoder.EmptyLine
  '''
  format_ = []
  for line in meta_format.split('\n'):
    decoded = to_json.meta_line_to_json(line)
    if type(decoded) == tuple:
      key, value = decoded
      format_.append((key, value))
    else:
      format_.append(decoder.EmptyLine)
      # format_.append(decoded)

  return format_