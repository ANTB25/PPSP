# -*- coding: utf-8 -*-

"""Module to obtain the colours required for the Troels Smith, von Post, geology
and 'other' parts of the cores in the main figure"""

###############################################################################
# Import required modules #####################################################
###############################################################################
import os as os
import pandas as pd
import sys as sys

from PPSP_options import option_sort as oss

###############################################################################
# Run options sort function from PPSP_options.py module #######################
###############################################################################
options = oss()

###############################################################################
# Obtain directory where files are and the data file name #####################
###############################################################################
location = os.path.dirname(__file__)
file_name = options["input_file_name**"]

os.chdir(location)

###############################################################################
# Function to obtain the colours used for the Troels Smith elements of the ####
# figure. If colour entry is followed by '*n'is not included ##################
###############################################################################
def col_dict():
    ts_list = ["Argilla granosa**",
               "Argilla steatodes**",
               "Detritus granosus**",
               "Detritus herbosus**",
               "Detritus lignosus**",
               "Grana arenosa**",
               "Grana glareosa majora**",
               "Grana glareosa minora**",
               "Grana saburralia**",
               "Limus calcareus**",
               "Limus detrituosus**",
               "Limus ferrugineus**",
               "Particulae testae molloscorum**",
               "Substantia humosa**",
               "Turfa bryophitica**",
               "Turfa herbosa**",
               "Turfa lignosa**"]
    
    rem = "-n"
    
    colour_dict = {k:v.replace(" ","") for k,v in options.items()
                   if k in ts_list}
    colour_dict = {k:v for k,v in colour_dict.items()
                   if rem not in v.strip()}

    return colour_dict

###############################################################################
# Function to obtain the colours used for the geology elements of the #########
# figure. If colour entry is followed by '*n'is not included. The colour is ###
# in two parts seperated by a hyphen, The first colour is for the foreground ##
# the second for the background. A list of dictionaries is produced. One ######
# for the foreground and background colour and one for the name ###############
###############################################################################
def col_rock_list():
    colour_rock_list = [] 
    
    geo_list = ["Coal**",
                "Limestone**",
                "Marl**",
                "Mudstone**",
                "Sandstone**",
                "Shale**",
                "Siltstone**",
                "Till**",
                "Volcanic**",
                "Metamorphic**"]
    
    rem = "*n"
    
    colour_rock_f_dict = {k:v.replace(" ","").split("*")[0]
                          for k,v in options.items() if k in geo_list}
    colour_rock_b_dict = {k:v.replace(" ","").split("*")[1]
                          for k,v in options.items() if k in geo_list}
    
    colour_rock_n_dict = {k:v.replace(" ","").split("*")[2]
                          for k,v in options.items() 
                          if k in geo_list and rem not in v.strip()}
    
    colour_rock_list.append(colour_rock_f_dict)
    colour_rock_list.append(colour_rock_b_dict)
    colour_rock_list.append(colour_rock_n_dict)

    return colour_rock_list

###############################################################################
# As above but does not split the entries of foreground and background colour #
# and the name. All together in a single dictionary ###########################
###############################################################################
def col_rock_dict(): 
    
    geo_list = ["Coal**",
                "Limestone**",
                "Marl**",
                "Mudstone**",
                "Sandstone**",
                "Shale**",
                "Siltstone**",
                "Till**",
                "Volcanic**",
                "Metamorphic**"]

    rem = "-n"
    colour_rock_dict = {k:v.replace(" ","")
                          for k,v in options.items() if k in geo_list}
    colour_rock_dict  = {k:v.replace(" ","")
                          for k,v in colour_rock_dict.items()
                          if rem not in v.strip()}
    
    return colour_rock_dict

###############################################################################
# Look at supplied data input csv file and load in and convert colours from ###
# numbers to text for each part of the Troels Smith sections for each core. ###
# Create a nested list ########################################################
###############################################################################
def data_colour(core_column,
                col_column,
                colour_dict):
   
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        data_core_cols = []
        section = data.groupby(f"{core_column}")
        try:
            for name, group in section:                    
                section_colours = [x for x in group[f"{col_column}"]]
                section_colours = [x.split("-") for x in section_colours]
                section_colours = [list(reversed(x))for x in section_colours]
                
                section_colours = [[colour_dict["Argilla granosa**"]
                                  if y.lower() == "ag" else y for y in x]
                                   for x in section_colours]
                                  
                section_colours = [[colour_dict["Argilla steatodes**"]
                                  if y.lower() == "as" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Detritus granosus**"]
                                  if y.lower == "dg" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Detritus herbosus**"]
                                  if y.lower() == "dh" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Detritus lignosus**"]
                                  if y.lower() == "dl" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Grana arenosa**"]
                                  if y.lower() == "ga" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Grana glareosa majora**"]
                                  if y.lower() == "gg(maj)" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Grana glareosa minora**"]
                                  if y.lower() == "gg(min)" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Grana saburralia**"]
                                  if y.lower() == "gs" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Limus calcareus**"]
                                  if y.lower() == "lc" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Limus detrituosus**"]
                                  if y.lower() == "ld" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Limus ferrugineus**"]
                                  if y.lower() == "lf" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Particulae testae "
                                                "molloscorum**"]
                                  if y.lower() == "ptm" else y for y in x] 
                                  for x in section_colours]
                section_colours= [[colour_dict["Substantia humosa**"]
                                  if y.lower() == "sh" else y for y in x] 
                                  for x in section_colours] 
                section_colours = [[colour_dict["Turfa bryophitica**"] 
                                  if y.lower() == "tb" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Turfa herbosa**"] 
                                  if y.lower() == "th" else y for y in x] 
                                  for x in section_colours]
                section_colours = [[colour_dict["Turfa lignosa**"]
                                  if y.lower() == "tl" else y for y in x] 
                                  for x in section_colours]
                
                data_core_cols.append(section_colours)  

        except:
            print("Problem encoutered in data file. Make sure there are"
                  " no empty\nentries in the TS_description column."
                  " If there are at the base\nof the cores fill them in "
                  "with 0-0-0-0")
            sys.exit()

    return data_core_cols
    
###############################################################################
# Create a dictionary for the colours provided for each von Post value ########
###############################################################################
def vp_col_dict():
    
    vp_list = ["H01",
               "H02",
               "H03",
               "H04",
               "H05",
               "H06",
               "H07",
               "H08",
               "H09",
               "H10",
               "N_A"]
    
    colour_vp_dict = {k:v.replace(" ","").lower()
                          for k,v in options.items() if k in vp_list}

    return colour_vp_dict
    
###############################################################################
# Look at the data file and convert the von post values to colours specified ##
# in the parameters file using the vp col dict function above #################
###############################################################################
def vp_colours(core_column,
               col_column,
               colour_vp_dict):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        
        vp_col_list = []
        
        section = data.groupby(f"{core_column}")

        for name, group in section:
            vp_colours = [x for x in group[f"{col_column}"]]
            vp_colours = [colour_vp_dict["H01"] if x == 1 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H02"] if x == 2 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H03"] if x == 3 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H04"] if x == 4 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H05"] if x == 5 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H06"] if x == 6 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H07"] if x == 7 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H08"] if x == 8 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H09"] if x == 9 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["H10"] if x == 10 
                          else x for x in vp_colours]
            vp_colours = [colour_vp_dict["N_A"] if x == 0 
                          else x for x in vp_colours]
        
            vp_col_list.append(vp_colours)
                  
        return vp_col_list

###############################################################################
# Create a dictionary for the other colours provided for by other and charcoal#
# colours in the parameters.csv file ##########################################
###############################################################################
def other_col_dict():
    other_list = ["charcoal_colour",
                  "other_colour"]
    
    other_col_dict = {k:v.replace(" ","").lower() for 
                  k,v in options.items() if k in other_list}

    return other_col_dict

###############################################################################
# Look at the data file and convert the charcoal and other values to colours ##
# specified in the parameters.csv file using the other_col_dict function above#
###############################################################################
def other_colour(core_num,
                 col_num,
                 other_cols):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        other_core_cols = []            
        e = data.groupby(f"{core_num}")
        
        for name, group in e: 
            other_colours = [int(x) for x in group[f"{col_num}"]]

            other_colours = [other_cols["charcoal_colour"] if x == 1 
                             else x for x in other_colours]                    
            other_colours = [other_cols["other_colour"] if x == 2
                             else x for x in other_colours]
            other_colours = ["white" if x == 0 else x for x in 
                             other_colours]
            
            other_core_cols.append(other_colours)
            
    return other_core_cols 

###############################################################################
###############################################################################
###############################################################################
###############################################################################
