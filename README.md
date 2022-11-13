# Metapy
Metapy is an application that helps the user to manage user-initated data-logging. 
## Converter
metapy contains a library called 'converter' which is used to convert .meta file to JSON and vice versa.
The functions of converter are:
 * meta_to_json: input meta (a string [the content of a meta file]), returs: a json_string (a string that looks like a dictionary, but is kept as a string to keep the format of the original meta file
 PLEASE NOTE that if you want to convert metadata to a python-dict, you will also need something to interprate the json-dict (like the python json-module). 
  * json_to_meta: input string (a string that contains a dictionary [like the output of meta_to_json]), returns: a string (the corresponding meta-data)
  * load_format: used to extract the format of a meta file. Returns a list of:
      - (key, value)
      - decoder.EmptyLine


## Form
The form is a GUI to enter logging data. Can be runned using:

      python form.py <allowed_keywords> <template_file>

When clicking Save, the script will run upload.py to upload all the data in the form.

Arguments:
 * allowed keywords: a path to a .meta file. The script will check if every key in the template file is also in the allowed_keywords-file. If not, an error will be raised.
 * template file: The layout of the form will be based on this file: the same keys will be used, the default values of the form will be those in the template file. And, when clicking save, the program will check if a value corresponds with the value on the template file (if the value on the template file is an integer, the value in the form should be too). If these values do not correspond (most probably because of a typo), an error will be raise.
## Buttons.py
 The <buttons.py> script is a part of the Form, and is used to program update-buttons in the GUI. To add a new button, use the following format:

      {
            the key in the template file (where in the form to place the button): {
                  "text": the text to display on the button (fetch/now...),
                  "on_click": the function to run when the button is click. The value that the function returns, will be used as the value of the entry. (Tip: use lambda to define your functions)
            }
      }
      

## Snapshot
This script will go in each directory (excluding those with '__' in their name) and take the last datafile (.meta). It will combine those files in a .dat file. This can be used to send the current status to another program.

## File To JSON
Run this script with a meta file as an argument, and it will convert it into a JSON file (using the Converter library).

## Upload.py
A script that will first check a few requirements, and then upload the data to a datafiles-directory. ( see logical flow char below )

## Uploading a file
Logical Flow:
![image](https://user-images.githubusercontent.com/88823772/201519598-739b8875-7ac1-4b06-85c0-bd24c531c75b.png)


## The meta format

The meta-format is a key-value based format, designed to be easily readable by humans as well as computers. For users, you can just open the file in Notepad for example and the data whill be easy to read. For computers, however, we created the Converter library to convert meta-file to json

An example of this format:

      *
      * Date                    := 2022.08.08
      * Time                    := 11:11
      * Activity                := One-line description of what needs to be logged
      * Spectrum_ID             := ERDcc22_023 or other
      *
      * Primary-beam            := 35Cl4+, 63Cu4+, ...
      * Energy[MeV]             := 8.0
      * T1_MCP[V]               := +2754
      * T2_MCP[V]               := -2100
      * Energ-det               := GIC or PIPS
      * Energ-det-ser-nr        := in case of pips serial number, otherwise n.a.
      * Energ-det-current[nA]   := in case of pips - leakage current in nA, otherwise n.a.
      * 
      * Sample_ID               := PEALD 75C D02
      * Sample_piece            := #1, use ? if not known
      * Spec_H_min[%]           := 8.5
      * Spec_H_max[%]           := 11.6
      * Spec_O_min[%]           := 60.0
      * Spec_O_max[%]           := 69.0
      * Hide-in-plot            := False
      * 
      * Sample Tilt[Degr]       := 15.0
      * Slab_min                := 111
      * Slab_max                := 846
      * 
      * Measd-Conc_H[%]         := 8.83
      * Measd-Conc_C[%]         := 0.12
      * Measd-Conc_N[%]         := 0
      * Measd-Conc_O[%]         := 63.42
      * Measd-Conc_Si[%]        := 27.63
      *
      * Note001                 := 16O + 18O considered as total O. Z steps =8.  Measured with GIC.  
      * Note002                 := Measuremnt time is 3600 seconds. After this measurment, PHA LLD    optimized to 209 mV.
      * Note003                 := count rate from T2 MCP was 1000 counts/s even without a beam
      *
