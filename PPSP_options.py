# -*- coding: utf-8 -*-

""" Module is used via a series of functions to error check and obtain the 
    options the user has decided on from the parameter file."""
       
###############################################################################
###############################################################################
import os as os
import numpy as np
import pandas as pd
import sys
import argparse

###############################################################################
# Code to take file name, location and program name from the cmd line #########
# If using this code in an IDE comment out the code between lines 20 - 27 and #
# un comment lines 29-30 and edit parameter location (location_1) and #########
# provide a file name with .csv extention for parameter file in line 30 #######
###############################################################################
parser = argparse.ArgumentParser(description = \
                            "Options file name and location" )
parser.add_argument('--input', action ='store', type = str, nargs = 2)

args = parser.parse_args()

location_1 = args.input[0]
file_name_option = args.input[1]

# location_1  = "G:\\PPSP"
# file_name_option = "    "

###############################################################################
# Error statement used for many errors in PPSP_strat.py module ################
###############################################################################
def geol_errors (error):
    print(f"{error} entry is incorrect. Please check entry.")
    sys.exit()

###############################################################################
# Options sort function error check entries from parameter file and provide ###   
# various dictionaries used in the PPSP_strat.py module #######################
###############################################################################
def option_sort():   
    text_list = ["directory**",
                 "input_file_name**",
                 "output_file_name**",
                 "image_format**",
    
                 ##############################################################
                 "main_title_on_off**",
                 "main_title",
                 "main_title_colour",
                 "main_title_style",
    
                 ##############################################################
                 "x_axis_colour**",

                 "x_title_on_off**",
                 "x_axis_title_line_1",
                 "x_axis_title_line_2",
            
                 "x_title_colour",
                 "x_title_style",
                
                 "x_major_ticks**",
                 "x_major_tick_colour**",
                 
                 "x_minor_ticks_on_off**",
                 "x_minor_tick_colour",
                
                 "x_label_colour**",
                 "x_label_style**",
                 
                 ##############################################################
                 "y_axis_colour**",
                 
                 "y_title_on_off**",
                 "y_axis_title_line_1",
                 "y_axis_title_line_2",
                
                 "y_title_style",
                 "y_title_colour",
                
                 "y_major_ticks**",
                 "y_major_ticks_depth_mode**",
                 "y_major_tick_colour**",
                 
                 "y_label_colour**",
                 "y_label_style**"
                
                 "y_minor_ticks_on_off**",
                 "y_minor_tick_colour",
            
                 "y_grid_on_off**",
                 "y_grid_style",
                 "y_grid_colour",
                
                 ##############################################################
                 "surface_join_line_on_off**",
                 "surface_join_line_colour",
                 "surface_join_line_style",
                 
                 "base_join_line_on_off**",
                 "base_join_line_colour",
                 "base_join_line_style",
                 
                 ##############################################################
                 "line_colour**",
                
                 ##############################################################
                 "Argilla steatodes**",
                 "Argilla granosa**",
                 "Grana arenosa**",
                 "Grana saburralia**",
                 "Grana glareosa minora**",
                 "Grana glareosa majora**",
                
                 "Detritus granosus**",
                 "Detritus herbosus**",
                 "Detritus lignosus**",
                
                 "Limus calcareus**",
                 "Limus detrituosus**",
                 "Limus ferrugineus**",
                
                 "Particulae testae molloscorum**",
                
                 "Substantia humosa**",
                 "Turfa bryophitica**",
                 "Turfa herbosa**",
                 "Turfa lignosa**",
                
                 ##############################################################
                 "legend_on_off**",
                 
                 "legend_title_on_off",
                 "legend_title",
                 "legend_title_style",
                 "legend_title_colour",
                 
                 "legend_font_style",
                 "legend_text_colour",
                
                 ##############################################################
                 "vp_on_off**",
                 "vp_border_colour",
                 
                 "H01",
                 "H02",
                 "H03",
                 "H04",
                 "H05",
                 "H06",
                 "H07",
                 "H08",
                 "H09",
                 "H10",
                 "None",
                
                 "legend_on_off_vp**",
                 "legend_title_on_off_vp",
                 "legend_title_vp",
                 "legend_title_style_vp",
                 "legend_title_colour_vp",
                 
                 "legend_font_style_vp",
                 "legend_text_colour_vp",
               
                 ##############################################################
                 "border_colour_geo**",
                 
                 "Coal**",
                 "Limestone**",
                 "Marl**",
                 "Metamorphic**",
                 "Mudstone**",
                 "Sandstone**",
                 "Siltstone**",
                 "Shale**",
                 "Till**",
                 "Volcanic**",
            
                 "legend_on_off_geo**",
                 
                 "legend_title_on_off_geo",
                 "legend_title_geo",
                 "legend_title_style_geo",
                 "legend_title_colour_geo",
                 
                 "legend_font_style_geo",
                 "legend_text_colour_geo",
                
                 ##############################################################
                 "charcoal_on_off**",
                 
                 "charcoal_colour",
                 "charcoal_line_colour",
                 
                 "other_on_off**",

                 "other_colour",
                 "other_line_colour"]
                 
    ###########################################################################
    num_list = ["canvas_width_mm**",
                "canvas_height_mm**",
                "figure_scale_factor**",
                "figure_border**",
                
                ###############################################################
                "main_title_size",
                "main_title_v_adjust",
                "main_title_h_adjust",
                
                ###############################################################
                "x_axis_width**",
                
                "x_title_font_size",
                "x_title_v_adjust",
                "x_title_h_adjust",
                
                "x_major_shift**",
                "x_major_tick_decimal**",
                "x_major_tick_length**",
                "x_major_tick_width",
                
                "x_minor_tick_length",
                "x_minor_tick_width",
                "x_minor_ticks_max",
                "x_minor_ticks_step",
                
                "x_label_font_size**",
                "x_tick_label_v_adjust**",
                "x_tick_label_h_adjust**",
                
                ###############################################################
                "y_axis_width**",
                
                "y_title_font_size",
                "y_title_v_adjust",
                "y_title_h_adjust",
                
                "y_major_tick_decimal**",
                "y_major_tick_length**",
                "y_major_tick_width**",
                
                "y_label_font_size**",
                "y_tick_label_v_adjust**",
                "y_tick_label_h_adjust**",
                
                "y_minor_tick_length",
                "y_minor_tick_width",
                "y_minor_ticks_max",
                "y_minor_ticks_step",
                
                "y_grid_width",
                "y_grid_length_adj",
                "y_grid_dash_length",
                
                ###############################################################
                "surface_join_line_width",
                "surface_join_line_dash_length",
                
                "base_join_line_width",
                "base_join_line_dash_length",
                
                ###############################################################
                "ts_width_section**",
                
                "legend_title_size",
                "legend_title_v_adjust",
                "legend_title_h_adjust",

                "legend_x_position",
                "legend_y_position",
                
                "legend_font_size",
                
                "legend_section_height",
                "legend_section_width",
                
                "legend_label_v_adjust",
                "legend_label_h_adjust",
                
                ###############################################################
                "vp_width_section",
                "gap_between_TS_and_vp",
                
                "legend_title_size_vp",
                "legend_title_v_adjust_vp",
                "legend_title_h_adjust_vp",
                
                "legend_x_position_vp",
                "legend_y_position_vp",
                
                "legend_font_size_vp",
                
                "legend_section_height_vp",
                "legend_section_width_vp",
                
                "legend_label_v_adjust_vp",
                "legend_label_h_adjust_vp",
                
                ###############################################################
                "legend_title_size_geo",
                "legend_title_v_adjust_geo",
                "legend_title_h_adjust_geo",
                
                "legend_x_position_geo",
                "legend_y_position_geo",
                
                "legend_font_size_geo",
                
                "legend_section_height_geo",
                "legend_section_width_geo",
                
                "legend_label_v_adjust_geo",
                "legend_label_h_adjust_geo",
                
                "charcoal_width",
                "gap_between_TS_and_charcoal",
                
                "other_width",
                "gap_between_TS_and_other"]

    ###########################################################################
    # Try to open TS_options.csv ##############################################
    ###########################################################################
    os.chdir(location_1)

    try:
        with open (file_name_option) as file:
            data = pd.read_csv(file)
    except:
        print(f"Problem loading {file_name_option.csv} file."
              "Check name and location")
        sys.exit()
    
    ###########################################################################
    # Drop blank rows and drop main heading rows ##############################
    ###########################################################################
    data = data.dropna(subset = ["OPTIONS"]).reset_index(drop = True)
    data = data.set_index("OPTIONS")
    
    data = data.drop(["FILES AND DIRECTORY",
                      "CANVAS",
                      "MAIN TITLE",
                      "X AXIS",
                      "Y AXIS",
                      "CORE JOINING LINE",
                      "TROELS SMITH",
                      "Nomenclature",
                      "TROELS SMITH LEGEND",
                      "VON POST",
                      "Humification levels",
                      "VON POST LEGEND",
                      "GEOLOGY/BASAL SEDIMENT",
                      "Geology or basal sediment",
                      "GEOLOGY/BASAL SEDIMENT LEGEND",
                      "CHARCOAL",
                      "OTHER"])
    
    data = data.reset_index()
    
    ###########################################################################
    # Create dictionaries of essential and non esstential parameters ##########
    ###########################################################################
    options_dict  = {k:v for k,v in zip(data["OPTIONS"],
                                            data["USER INPUTS"])}
    
    ess_options_dict = {k:v for k,v in options_dict.items() if "**" in k}
    non_ess_options_dict = {k:v for k,v in options_dict.items()
                            if "**" not in k}
    ess_options_dict_num = {k:v for k,v in ess_options_dict.items()
                            if k in num_list}
    ess_options_dict_txt = {k:v for k,v in ess_options_dict.items() 
                            if k in text_list}
    
    ###########################################################################
    # Check there are entries for essential parameters and that the text and ##
    # and numeric entries are in correct format ###############################
    ###########################################################################
    for k,v in ess_options_dict.items():
        if str(v).strip() == "" or str(v) == "nan":

            print(f"******The {k} option has no entry. "
                  "Please provide an entry.******")
            sys.exit() 

    for k,v in ess_options_dict_num.items():
        if str(v).replace(" ","").replace("-","").replace(".","").\
           isnumeric() == False:
            print(f"******The {k} option has a non numeric entry. "
                  "Please provide a numeric entry.******")
            sys.exit() 
            
    for k,v in ess_options_dict_txt.items():
        if str(v).strip().isdigit() == True:
            print(f"******The {k} option does not have a text entry. "
                  "Please provide a text entry.******")
            sys.exit() 
    
    ###########################################################################
    # If a main title is required check that parameters have been provided ####
    ###########################################################################
    main_title_list = ["main_title",
                       "main_title_colour",
                       "main_title_size",
                       "main_title_style",
                       "main_title_v_adj",
                       "main_title_h_adj"]

    if options_dict["main_title_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in main_title_list:
                if v =="" or v =="nan":
                    print(f"******The {k} option does not have an entry. "
                          "Please provide an entry.******")
                    sys.exit() 
    
    ###########################################################################
    # Check y_axis_title parameter entries ####################################
    ###########################################################################     
    y_axis_title_list = ["y_title_font_size",
                         "y_title_style",
                         "y_title_colour",
                         "y_title_v_adj",
                         "y_title_h_adj"]
    
    if options_dict["y_axis_title_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in y_axis_title_list:
                if v =="" or str(v) =="nan":
                    print(f"******The {k} option does not have an entry. "
                          "Please provide an entry.******")
                    sys.exit() 
    
    ###########################################################################
    # Check x_axis_title parameter entries ####################################
    ###########################################################################
    x_axis_title_list = ["x_title_font_size",
                         "x_title_style",
                         "x_title_colour",
                         "x_title_v_adj",
                         "x_title_h_adj"]
          
    if options_dict["x_title_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in x_axis_title_list:
                if v =="" or str(v) =="nan":
                    print(f"******The {k} option does not have an entry. "
                          "Please provide an entry.******")
                    sys.exit() 

    ###########################################################################
    # if y min ticks have been requested check parameters are provided ########
    ###########################################################################
    y_min_list = ["y_minor_tick_len",
                  "y_minor_tick_width",
                  "y_minor_ticks_max",
                  "y_minor_ticks_step"
                  "y_minor_tick_colour"]

    if options_dict["y_minor_ticks_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in y_min_list:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
    
    ###########################################################################
    # If Y grid lines are required check parameters are supplied ##############
    ###########################################################################
    y_grid_list = ["y_grid_style",
                   "y_grid_colour",
                   "y_grid_width",
                   "y_grid_length_adj",
                   "y_grid_dash_length"]

    if options_dict["y_grid_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in y_grid_list:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
    
    ###########################################################################
    # if x min ticks have been requested check parameters are provided ########
    ########################################################################### 
    x_min_list = ["x_minor_tick_len",
                  "x_minor_tick_wid",
                  "x_minor_ticks_max",
                  "x_minor_ticks_step",
                  "x_minor_tick_colour"]

    if options_dict["x_minor_ticks_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in x_min_list:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
                    
    ###########################################################################
    # if join line has been requested check parameters are provided ###########
    ########################################################################### 
    sur_join_list = ["surface_join_line_colour",
                     "surface_join_line_colour"
                     "surface_join_line_style",
                     "surface_join_line_width",
                     "surface_join_line_dash_length"]
    
    base_join_list = ["base_join_line_colour",
                      "base_join_line_colour"
                      "base_join_line_style",
                      "base_join_line_width",
                      "base_join_line_dash_length"]
    
    if options_dict["surface_join_line_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in sur_join_list:
                if v =="" or pd.isnull(v):
                    print(f"****** The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
    
    if options_dict["base_join_line_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in base_join_list:
                if v =="" or pd.isnull(v):
                    print(f"****** The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
    
    ###########################################################################
    # If legend has been requested check parameters have been provided ########
    ###########################################################################
    leg_ess_list = ["legend_x_position",
                    "legend_y_position",
                    "legend_font_size",
                    "legend_font_style",
                    "legend_text_colour",
                    "legend_section_height",
                    "legend_section_width",
                    "legend_label_v_adj"]
    
    leg_title_list = ["legend_title",
                      "legend_title_size",
                      "legend_title_style",
                      "legend_title_colour",
                      "legend_title_v_adjust"]
    
    if options_dict["legend_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in leg_ess_list:
                if v =="" or pd.isnull(v):
                    print(f"****** The {k} option does not have an entry."
                          "Please provide an entry. ******")
                    sys.exit() 
                    
        if options_dict["legend_title_on_off"] == "on":
            for k,v in options_dict.items():
                if k in leg_title_list:
                    if v =="" or pd.isnull(v):
                        print(f"******The {k} option does not have an entry."
                              "Please provide an entry.******")
                        sys.exit() 

    ###########################################################################
    # If von post legend has been requested check parameters have been provided
    ###########################################################################
    leg_ess_list_vp = ["legend_x_position_vp",
                       "legend_y_position_vp",
                       "legend_font_size_vp",
                       "legend_font_style_vp",
                       "legend_text_colour_vp",
                       "legend_section_height_vp",
                       "legend_section_width_vp",
                       "legend_label_v_adj_vp"]
    
    leg_title_list_vp = ["legend_title_vp",
                         "legend_title_size_vp",
                         "legend_title_style_vp",
                         "legend_title_colour_vp",
                         "legend_title_v_adjust_vp"]
    
    if options_dict["legend_on_off_vp**"] == "on":
        for k,v in options_dict.items():
            if k in leg_ess_list_vp:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
                    
        if options_dict["legend_title_on_off_vp"] == "on":
            for k,v in options_dict.items():
                if k in leg_title_list_vp:
                    if v =="" or pd.isnull(v):
                        print(f"****** The {k} option does not have an entry."
                              "Please provide an entry. ******")
                        sys.exit() 
    
    ###########################################################################
    # If geology legend has been requested check parameters have been provided#
    ###########################################################################                    
    leg_ess_list_geo = ["legend_x_position_geo",
                        "legend_y_position_geo",
                        "legend_font_size_geo",
                        "legend_font_style_geo",
                        "legend_text_colour_geo",
                        "legend_section_height_geo",
                        "legend_section_width_geo",
                        "legend_label_v_adj_geo"]
    
    leg_title_list_geo = ["legend_title_geo",
                          "legend_title_size_geo",
                          "legend_title_style_geo",
                          "legend_title_colour_geo",
                          "legend_title_v_adjust_geo"]
    
    if options_dict["legend_on_off_geo**"] == "on":
        for k,v in options_dict.items():
            if k in leg_ess_list_geo:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
                    
        if options_dict["legend_title_on_off_geo"] == "on":
            for k,v in options_dict.items():
                if k in leg_title_list_geo:
                    if v =="" or pd.isnull(v):
                        print(f"******The {k} option does not have an entry."
                              "Please provide an entry.******")
                        sys.exit() 
    
    ###########################################################################
    # Check charcoal and other parameters #####################################
    ###########################################################################
    char_list = ["charcoal_width",
                 "charcoal_colour",
                 "charcoal_line_colour",
                 "gap_between_TS_and_charcoal"]
    
    other_list = ["other_width",
                  "other_colour",
                  "other_line_colour",
                  "gap_between_TS_and_other"]
                  
    
    if options_dict["charcoal_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in char_list:
                if v =="" or pd.isnull(v):
                    print(f"******The {k} option does not have an entry."
                          "Please provide an entry.******")
                    sys.exit() 
                    
    if options_dict["other_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in other_list:
                if v =="" or pd.isnull(v):
                    print(f"****** The {k} option does not have an entry."
                          "Please provide an entry. ******")
                    sys.exit() 

    ###########################################################################
    # If von post has been requested check parameters have been provided ######
    ###########################################################################
    vp_list = ["vp_border_colour",
               "H01",
               "H02",
               "H03",
               "H04",
               "H05",
               "H06",
               "H07",
               "H08",
               "H09",
               "H10",
               "None"]
    
    if options_dict["vp_on_off**"] == "on":
        for k,v in options_dict.items():
            if k in vp_list:
                if v =="" or pd.isnull(v):
                    print(f"****** The {k} option does not have an entry."
                          "Please provide an entry. ******")
                    sys.exit() 

    ###########################################################################
    #Check line and text styles ###############################################
    ###########################################################################
    error_st_1 = "does not have a valid entry. Please check."
    
    ###########################################################################
    #Line style error detection ###############################################
    ###########################################################################
    line_style_list = ["dashed", "solid"]
    
    if str(options_dict["y_grid_on_off**"].replace(" ","")) == "on":
        if str(options_dict["y_grid_style"]) not in line_style_list:
            print("****** Y grid style " + error_st_1)
            sys.exit()
            
    if str(options_dict["surface_join_line_on_off**"]).replace(" ","") == "on":
        if str(options_dict["surface_join_line_style"]).replace(" ","")\
            not in line_style_list:
            print("****** surface join_line_style " + error_st_1)
            sys.exit()
            
    if str(options_dict["base_join_line_on_off**"]).replace(" ","") == "on":
        if str(options_dict["base_join_line_style"]).replace(" ","")\
            not in line_style_list:
            print("****** base join_line_style " + error_st_1)
            sys.exit()
         
    ###########################################################################
    #Text style error detection ###############################################
    ###########################################################################
    text_style_list = ["bold", "italic","normal"]
    
    if str(options_dict["main_title_on_off**"]).replace(" ","") == "on":
        if str(options_dict["main_title_style"]).replace(" ","") \
            not in text_style_list:
            print("****** Main_title_style " + error_st_1)
            sys.exit()
            print("****** Main_title_style " + error_st_1)
            sys.exit()     
            
    if str(options_dict["x_title_on_off**"]).replace(" ","") == "on" or \
        str(options_dict["y_title_on_off**"]).replace(" ","") == "on":
        if str(options_dict["x_title_style"]).replace(" ","") \
            not in text_style_list or str(options_dict["y_title_style"])\
                .replace(" ","") not in text_style_list:
            print("****** X or Y Axis_title_style " + error_st_1)
            sys.exit()            
            
    ###########################################################################
    if str(options_dict["legend_on_off**"]).replace(" ","") == "on" and \
        str(options_dict["legend_title_on_off"]).replace(" ","") == "on":
        if options_dict["legend_title_style"].replace(" ","") \
            not in text_style_list:
            print("****** Legend_title_style " + error_st_1)
            sys.exit()        
                        
    if str(options_dict["legend_on_off**"]).replace(" ","") == "on":
        if str(options_dict["legend_font_style"]).replace(" ","") \
            not in text_style_list:
            print("****** Legend_font_style" + error_st_1)
            sys.exit()              
    
    ###########################################################################
    if str(options_dict["legend_on_off_vp**"]).replace(" ","") == "on" and \
        str(options_dict["legend_title_on_off_vp"]).replace(" ","") == "on":
        if str(options_dict["legend_title_style_vp"]).replace(" ","") \
            not in text_style_list:
            print("****** Legend_title_style_vp " + error_st_1)
            sys.exit()        
                        
    if str(options_dict["legend_on_off_vp**"]).replace(" ","") == "on":
        if str(options_dict["legend_font_style_vp"]).replace(" ","") \
            not in text_style_list:
            print("****** Legend_font_style " + error_st_1)
            sys.exit() 
    
    ###########################################################################
    if str(options_dict["legend_on_off_vp**"]).replace(" ","") == "on" and \
        str(options_dict["legend_title_on_off_vp"]).replace(" ","") == "on":
        if str(options_dict["legend_title_style_vp"]).replace(" ","") \
            not in text_style_list:
            print("****** Legend_title_style_vp " + error_st_1)
            sys.exit()        
                        
    if str(options_dict["legend_on_off_vp**"]).replace(" ","") == "on":
        if str(options_dict["legend_font_style_vp"]).replace(" ","") \
            not in text_style_list:
            print("****** Legend_font_style " + error_st_1)
            sys.exit() 
    
    ###########################################################################         
    for k,v in options_dict.items():
        if "on_off**" in k:
            if str(v).replace(" ","") not in ["on","off"]:
                print(f"****** The {k} option must be either on or off.******")  
                sys.exit()            
    
    x_list = ["","_geo", "_vp"]
    for x in x_list:
        if str(options_dict[f"legend_on_off{x}**"]).replace(" ","") == "on":
            if str(options_dict[f"legend_title_on_off{x}"]).replace(" ","")\
                not in ["on", "off"]:
                print(f"****** The {k} option must be either on or off.******")  
                sys.exit()    
                 
    return options_dict

###############################################################################
###############################################################################
###############################################################################
###############################################################################
