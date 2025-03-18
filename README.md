# PYTHON PEAT STRATIGRAPHY PLOTTER (PPSP)

PROGRAM DESCRIPTION
This program is primarily used to plot Troels Smith (ts) type data from multiple cores for peatlands. These cores are typically shown vs altitude but can aslo be shown vs depth. Distance between cores is shown on the x axis and altitude or depth on the y. Other data can be plotted along side Troels Smith information such as von Post humification, and presence and absence of charcoal. PPSP displays TS data in an alternative way to that traditionally used employing 4 rectangles per core section to represent the 1-4 for TS categories. These rectangles are cpoloured based on user choices. Using this method of display allows substantial detail to be seen even with shallow core sections. Geology/basal sediment can aslo be displayed with 10 different types. An eps file of the resulting figure is saved upon every run of the program but png and jpg formats can also be chosen. However, on a large monitor with good resolution a simple screen shot exported to another program is often more than satisfactory. 

AUTHOR
Dr Antony Blundell, School of Geography, University of Leeds

INSTALLATION
Full installation instructions are provided in the manual provided. It is recommended that the program is used in a virtual environment (see manual)

PROGRAM USAGE
Full isntructions for program usage are contained in the manual. The program is set up to be run from the cmd line or terminal however, minimal code changes will allow it to be run from an IDE. See comments in PPSP_options.py module. The program consists of four modules PPSP_strat.py, PPSP_build.py, PPSP_colours.py and PPSP_options.py. The PPSP_strat.py module is run as the controlling module. Again see manual for full instructions. Program requires users to fill out or edit example files provided for a) a data file and b) a parameter file. The former contains the field stratigraphy data and the latter the user options to control the aesthetics of the plot. Both must be available and be csv files for the program to run successfully. Placing all module files and data and parameter csv files in the same location with the virtual environment makes for simple operation. Again see manual for full isntructions. Program can be used in windows 10-11, Linux, and MacOS. The program was written using python 3.8.1 but has been run successfully in python versions up to 3.11. Manual provides full set up instructions. 


