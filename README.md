# metapy
## Introduction
"metapy" is an application that helps the user to manage user-initated data-logging. The GUI is a tkinter input based on the template meta-file. The main  functionality of the application is to store a collection of key-value pairs. The result is uploaded to a child folder. 

The used format is the so-called meta-format.  It is designed to be easily readable by humans as well as computers. For humans, you can just open the file in Notepad for example and the data whill be very easy to read. For computers, however, we created the Metapy software: a way to convert meta-data into dictionaries.

You can store multiple template files in the parent directory, to cover a variety of data-sets that you want to store. Creating these template files, could be done with a ASCII text editor, such as Notepad. An example meta-file is added below.

The application is designed to be used to record parameters of a set-up that varies over time, and for which the logging is initiated by the user (for example in the GUI). 

## Use cases
One of the use-cases is to analyze the trend of a specific value over time. For this, it is advised to always have date/time values inside the meta-file. But, the use is not limited to the analysis of data as a function of time. One can analyze the correlation between any two parameters in the file, or select files with a specific key-value pair etc., just as you would do with a collection of json files.

Another use-case is to consult the settings as a whole on a specific moment in the past. For this, it is a good practice to also include a short note which describes the context of the logging: for example "Good functional set-up after maintenance", or "Performance of the set-up after installation of new detector" etc. This will help you later to give meaning to the values and trends.

## Example of a Meta-file

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
      * Note002                 := Measuremnt time is 3600 seconds. After this measurment, PHA LLD optimized to 209 mV.
      * Note003                 := count rate from T2 MCP was 1000 counts/s even without a beam
      *
