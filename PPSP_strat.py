#!/usr/bin/env python3
###############################################################################
############################# PPSP_PROGRAM ####################################
###############################################################################
########################## DR ANTONY BLUNDELL #################################
################ SCHOOL OF GEOGRAPHY, UNIVERSITY OF LEEDS #####################
################################# 2024 ########################################
###############################################################################

"""The program is built upon the Turtle module and is used to plot 
   predominantly peat core stratigraphy data that employs Troels Smith 
   classifications. However, the program could be used for salt marsh or lake 
   stratigraphy data if Troels Smith has been used. The program can also 
   display von Post and charcoal data alongside the cores.
   Cores are plotted altitudinally but can also be plotted simply with depth
   and there is a wide range of aesthetic 
   parameters that can be changed to get the figure the user requires. 
   A manual is provided with the download and the user is directed there for 
   instructions in the programs usage. 
   
   The program was written by Dr Antony Blundell (School of Geography, 
   University of Leeds) in 2025. Please remember to cite the paper that goes
   with this program if you use it or the doi for the storage location in
   zenodo.
   
   This is the main module PPSP_strat.py to run the program. It brings in 
   functions from modules PPSP_options.py, PPSP_build.py and PPSP_colours.py.
   
   Required input
   ------------------
       A DATA FILE.csv file - This is the file that holds the stratigraphy 
       field data for the plot. Consult the manual and downloaded examples to 
       see how to fill this out correctly. This input is actually used in the 
       PPSP_build.py module. This can have any name the user likes but must
       be a csv file and be named in the parameter file,
       
       A PARAMETER FILE.csv file - This is the file that holds the user 
       options for the aesthetics of the stratigraphy plot. Consult the manual
       and downloaded examples to see how to fill this out correctly. This 
       input is used in then PPSP_options.py module primarily. This file can
       have any name but must be a csv file. 
                    
       Both these files are required before the program is run.
       
   Output
   ----------
       By defualt at eps file is saved of the figure and possibly a png or jpg
       deoending on user options selected in the parameter file. Outputs are
       saved to the location nominated in the parameter file.
   
   The program can be run in an IDE or from the command line. If you run it in 
   an IDE you should comment out the code for argparse in the PPSP_options.py 
   module (lines 46-53) and uncomment lines 55-56 and add in a location
   address and a filename for the parameter file with .csv extension.
   
   The program does have an associated General Public License v3.
   
   All the best to all.
   
   
   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
   """

###############################################################################
# IMPORT REQUIRED MODULES #####################################################
###############################################################################
import math as math
import numpy as np
import os as os
import pandas as pd  
from tkinter import ttk
import tkinter.font as TkFont
from tkinter import *     
import turtle

###############################################################################
from PIL import Image
from PIL import EpsImagePlugin

###############################################################################
from PPSP_options import geol_errors as ge
from PPSP_options import option_sort as oss
import PPSP_build as bb
import PPSP_colours as colours 

###############################################################################
###############################################################################
print("######################################################################")
print("######################################################################")
print("################# PYTHON PEAT STRAT PLOTTER (2025) ###################")
print("######################## Dr Antony Blundell ##########################")
print("########### School of Geography, University of Leeds, Leeds ##########")
print("######################################################################")
print("######################################################################")
print("                                                                      ")
print("          #######          |           #####                  __      ")
print("         #########     |            | #######        |       ____     ")
print("   |      #######                      ####                   __      ")
print("                                                                      ")
print("     |           |               |                                    ")
print("                                               |       |              ")
print("        |          ___                                                ")
print("                    |     |       |         |                         ")
print(" |  0             0 |                                |                ")
print("   000   |       /|/|                                        00      ")
print("  0000         __//_|____||__||__||__||__||__||__||___       00      ")
print("  0000        //______||______________________________\\     0000     ")
print("   00        //_______||_______________________________\\     00      ")
print("   ||       //        ||                                \\    ||      ")
print("----------------------------------------------------------------------")
print("----------------------------------------------------------------------")
print("----------------------------------------------------------------------")
print("----------------------------------------------------------------------")
print("")
###############################################################################
# Run options function to get dictionary of inputs from parameter file#########
###############################################################################
options = oss()

###############################################################################
###############################################################################
## SET GENERAL OVERALL NAMES AND ASSIGNMENTS MOST OF WHICH ARE TAKEN FROM ##### 
## THE PARAMETER_FILE THAT THE USER EDITS #####################################
###############################################################################
###############################################################################
# Set directory as the one where this program is saved
basedir = options["directory**"]
# Get data file name from options.csv
file_name = options["input_file_name**"]

###############################################################################
# Obtain output name  #########################################################
###############################################################################
output = str(options["output_file_name**"])

###############################################################################
# Obtain user defined parameters for width and height for canvas ##############
###############################################################################
mm_x = float(options["canvas_width_mm**"]) #width in mm on screen 600
mm_y = float(options["canvas_height_mm**"]) #height in mm on screen 350

###############################################################################
# Obtain user parameters for defined proportion of the canvas used for the ####
# figure ######################################################################
###############################################################################
fig_height_prop = float(options["figure_scale_factor**"])

#border in mm round the inside of the axes
border = float(options["figure_border**"].replace(" ",""))

###############################################################################
# Obtain main title parameters ################################################
###############################################################################
main_title_on_off = str(options["main_title_on_off**"]).lower().replace(" ","")

try:
    if main_title_on_off == "on":
        main_title = str(options["main_title"])
        main_title_col = str(options["main_title_colour"].
                             lower().replace(" ",""))
        main_title_size = int(options["main_title_size"])
        main_title_style = str(options["main_title_style"].
                               lower().replace(" ",""))
        
        main_title_v_adj = float(options["main_title_v_adjust"])
        main_title_h_adj = float(options["main_title_h_adjust"])
        if str(main_title_v_adj) == "nan":
            main_title_v_adj = 1
        if str(main_title_h_adj) == "nan":
            main_title_h_adj = 1
except:
    ge("One of the options for the main title is not complete or correct")

###############################################################################
# Obtain x axis parameters ####################################################
###############################################################################
x_axis_colour = str(options["x_axis_colour**"]).replace(" ","")
x_axis_width = int(options["x_axis_width**"].replace(" ",""))

x_axis_title_on_off = str(options["x_title_on_off**"])
x_axis_title_1 = str(options["x_title_line_1"])
x_axis_title_2 = str(options["x_title_line_2"])
x_axis_t_font_size = int(options["x_title_font_size"].replace(" ",""))

x_title_col = str(options["x_title_colour"]).replace(" ","")
x_axis_t_style = options["x_title_style"].replace(" ","")
x_title_h_adjust = float(options["x_title_h_adjust"].replace(" ",""))
x_title_v_adjust = float(options["x_title_v_adjust"].replace(" ",""))


x_maj_ticks = list(options["x_major_ticks**"].split("*")) 
x_maj_ticks = [float(x.replace(" ",""))for x in x_maj_ticks]
x_maj_ticks_check = x_maj_ticks.copy() 

#Ticks used for display
x_maj_ticks_2 = x_maj_ticks.copy()

x_dec = int(options["x_major_tick_decimal**"].replace(" ",""))
x_maj_ticks_strs = [str(x) for x in x_maj_ticks_2]
x_maj_ticks_strs = [f"{x:.{x_dec}f}" for x in x_maj_ticks_2]

#Ticks used for scaling
x_maj_ticks = [x-x_maj_ticks[0] for x in x_maj_ticks]
x_maj_shift = float(options["x_major_shift**"].replace(" ",""))

###############################################################################
if x_maj_ticks_check[0] == 0:
    x_min_ticks = np.round(np.arange(x_maj_ticks[0],
                                     float(options["x_minor_ticks_max"])+
                                     float(options["x_minor_ticks_step"]), 
                                     float(options["x_minor_ticks_step"]))
                                     ,2)
else:
    x_min_ticks = np.round(np.arange(0,
                                     
                                     
                                    (float(options["x_minor_ticks_max"]) +
                                     float(options["x_minor_ticks_step"]))
                                     - x_maj_ticks_check[0], 
                                     float(options["x_minor_ticks_step"]))
                                     ,2) 
    
###############################################################################
x_maj_tick_len = float(options["x_major_tick_length**"].replace(" ",""))
x_maj_tick_wid = float(options["x_major_tick_width**"].replace(" ",""))
x_maj_tick_col = str(options["x_major_tick_colour**"]).replace(" ","")

x_min_tick_len = float(options["x_minor_tick_length"].replace(" ",""))
x_min_tick_wid = int(options["x_minor_tick_width"].replace(" ",""))
x_min_tick_col = str(options["x_minor_tick_colour"]).replace(" ","")

x_l_font_size = int(options["x_label_font_size**"].replace(" ",""))
x_lab_col = str(options["x_label_colour**"]).replace(" ","")
x_maj_l_style = options["x_label_style**"].replace(" ","")  

x_maj_tick_l_vertical_adjust = float(options["x_tick_label_v_adjust**"]
                                     .replace(" ","")) 
x_maj_tick_l_horiz_adjust = float(options["x_tick_label_h_adjust**"]
                                  .replace(" ",""))

###############################################################################
# Obtain y axis parameters ####################################################
###############################################################################
y_axis_colour = str(options["y_axis_colour**"]).replace(" ","")
y_axis_width = int(options["y_axis_width**"].replace(" ",""))

y_axis_title_on_off = str(options["y_axis_title_on_off**"])
y_axis_title_1 = str(options["y_axis_title_line_1"])
y_axis_title_2 = str(options["y_axis_title_line_2"])
y_axis_t_font_size = int(options["y_title_font_size"].replace(" ",""))

y_title_col = str(options["y_title_colour"]).replace(" ","")
y_axis_t_style = options["y_title_style"].replace(" ","")
y_title_h_adjust = float(options["y_title_h_adjust"].replace(" ",""))
y_title_v_adjust = float(options["y_title_v_adjust"])

y_maj_ticks = list(options["y_major_ticks**"].split("*")) 
y_maj_ticks = [float(x.replace(" ","")) for x in y_maj_ticks]

y_maj_ticks_depth_mode = str(options["y_major_ticks_depth_mode**"].
                             replace(" ",""))
y_dec = int(options["y_major_tick_decimal**"].replace(" ",""))

###############################################################################
#If depth mode is on make the labels positive not negative
if y_maj_ticks_depth_mode == "on":
    y_maj_ticks_1 = [x*-1 for x in y_maj_ticks]
    y_maj_ticks_strs = [f"{x:.{y_dec}f}" for x in y_maj_ticks_1]
    y_maj_ticks_strs [0] = f"{0:.{y_dec}f}"
else:    
    y_maj_ticks_strs = [str(x) for x in y_maj_ticks]
    y_maj_ticks_strs = [f"{x:.{y_dec}f}" for x in y_maj_ticks]
    
###############################################################################
y_maj_tick_len = float(options["y_major_tick_length**"].replace(" ",""))
y_maj_tick_wid = int(options["y_major_tick_width**"].replace(" ",""))
y_maj_tick_col = str(options["y_major_tick_colour**"]).replace(" ","")

y_maj_tick_l_vertical_adjust = float(options["y_tick_label_v_adjust**"]
                                     .replace(" ","")) 
y_maj_tick_l_horiz_adjust = float(options["y_tick_label_h_adjust**"]
                                  .replace(" ","")) 

y_l_font_size = int(options["y_label_font_size**"].replace(" ",""))
y_tick_lab_col = str(options["y_label_colour**"]).replace(" ","")
y_maj_l_style = options["y_label_style**"].replace(" ","") 
    

y_min_ticks = np.flip(np.round(np.arange(y_maj_ticks[-1],
                                        float(options["y_minor_ticks_max"]), 
                                        float(options["y_minor_ticks_step"]))
                                        ,2))

y_min_ticks_strs = [str(x) for x in y_min_ticks]
   
y_min_tick_len = float(options["y_minor_tick_length"].replace(" ",""))
y_min_tick_wid = int(options["y_minor_tick_width"].replace(" ",""))
y_min_tick_col = str(options["y_minor_tick_colour"]).replace(" ","")

#Obtain grid style for Y axis from options.csv. Can be dashed or solid
grid_dash = str(options["y_grid_style"]).replace(" ","").lower()
# Obtain grid line colour and dash for Y axis from options.csv.
y_grid_col = str(options["y_grid_colour"]).replace(" ","").lower()
y_grid_width = float(options["y_grid_width"].replace(" ",""))
y_grid_len_adj = float(options["y_grid_length_adjust"].replace(" ",""))
y_grid_dash_length = float(options["y_grid_dash_length"].replace(" ",""))

###############################################################################
# Obtain join line colour and dash length parameters ##########################
###############################################################################
join_col_sur = str(options["surface_join_line_colour"]).replace(" ","").lower()
join_line_width_sur = int(options["surface_join_line_width"].replace(" ",""))
join_line_style_sur = str(options["surface_join_line_style"]).\
                          replace(" ","").lower()
join_dash_length_sur = float(options["surface_join_line_dash_length"].\
                             replace(" ",""))

join_col_base = str(options["base_join_line_colour"]).replace(" ","").lower()
join_line_width_base = int(options["base_join_line_width"].replace(" ",""))
join_line_style_base = str(options["base_join_line_style"]).\
                           replace(" ","").lower()
join_dash_length_base = float(options["base_join_line_dash_length"].\
                              replace(" ",""))
    
###############################################################################
# Obtain width of Troels Smith rectangles and seperating line colour ##########
###############################################################################    
wid_x = float(options["ts_width_section**"].replace(" ",""))    
pen_colour_rect = str(options["line_colour**"]).lower().replace(" ","")   
remove_seg = str(options["Remove segments**"]).lower().replace(" ","") 
    
###############################################################################
# Obtain Troels Smith legend parameters #######################################
###############################################################################
legend_title_on_off = str(options["legend_title_on_off"]).\
                          replace(" ","").lower()
legend_title = str(options["legend_title"])
legend_title_size = int(options["legend_title_size"].replace(" ",""))
legend_title_style = str(options["legend_title_style"]).replace(" ","").lower()
legend_title_col = str(options["legend_title_colour"]).replace(" ","").lower()
legend_title_v_adjust = float(options["legend_title_v_adjust"].replace(" ",""))
legend_title_h_adjust = float(options["legend_title_h_adjust"].replace(" ",""))

legend_x = float(options["legend_x_position"].replace(" ",""))
legend_y = float(options["legend_y_position"].replace(" ",""))

legend_font_size = str(options["legend_font_size"]).replace(" ","")
legend_font_style = str(options["legend_font_style"].replace(" ","").lower())
legend_txt_col = str(options["legend_text_colour"].
                          replace(" ","").lower())   

leg_section_height = float(options["legend_section_height"].replace(" ",""))
leg_section_width = float(options["legend_section_width"].replace(" ","")) 

leg_label_v_adjust = float(options["legend_label_v_adjust"].replace(" ",""))
leg_label_h_adjust = float(options["legend_label_h_adjust"].replace(" ",""))
                        
###############################################################################
# As above but for von Post ###################################################
###############################################################################
border_colour = str(options["vp_border_colour"]).replace(" ","").lower()
vp_wid = float(options["vp_width_section"].replace(" ",""))
vp_gap = float(options["gap_between_TS_and_vp"].replace(" ",""))

legend_title_on_off_vp = str(options["legend_title_on_off_vp"]
                             .replace(" ","").lower())
legend_title_vp = str(options["legend_title_vp"])
legend_title_size_vp = int(options["legend_title_size_vp"].replace(" ",""))
legend_title_style_vp = str(options["legend_title_style_vp"])\
                            .replace(" ","").lower()
legend_title_col_vp = str(options["legend_title_colour_vp"]).\
                          replace(" ","").lower()

legend_title_v_adjust_vp = float(options["legend_title_v_adjust_vp"]
                                 .replace(" ",""))
legend_title_h_adjust_vp = float(options["legend_title_h_adjust_vp"]
                                 .replace(" ",""))

legend_x_vp = float(options["legend_x_position_vp"].replace(" ",""))
legend_y_vp = float(options["legend_y_position_vp"].replace(" ",""))

legend_font_size_vp = int(options["legend_font_size_vp"].replace(" ",""))
legend_font_style_vp = str(options["legend_font_style_vp"])\
                           .replace(" ","").lower()
legend_txt_col_vp = str(options["legend_text_colour_vp"]).\
                          replace(" ","").lower()

leg_section_height_vp = float(options["legend_section_height_vp"]
                              .replace(" ","")) 
leg_section_width_vp = float(options["legend_section_width_vp"]
                             .replace(" ","")) 

leg_label_v_adjust_vp = float(options["legend_label_v_adjust_vp"].\
                              replace(" ",""))
leg_label_h_adjust_vp = float(options["legend_label_h_adjust_vp"].\
                              replace(" ",""))

###############################################################################
# As above but for geology ####################################################
############################################################################### 
geo_border_col = str(options["border_colour_geo**"]).replace(" ","").lower()
   
legend_title_on_off_geo = str(options["legend_title_on_off_geo"])\
                             .replace(" ","").lower()  
legend_title_geo = str(options["legend_title_geo"])
legend_title_size_geo = int(options["legend_title_size_geo"].replace(" ",""))
legend_title_style_geo = str(options["legend_title_style_geo"])\
                            .replace(" ","").lower()
legend_title_col_geo = str(options["legend_title_colour_geo"])\
                            .replace(" ","").lower()  
legend_title_v_adjust_geo = float(options["legend_title_v_adjust_geo"]
                                 .replace(" ",""))
legend_title_h_adjust_geo = float(options["legend_title_h_adjust_geo"]
                                 .replace(" ",""))

legend_x_geo = float(options["legend_x_position_geo"].replace(" ",""))
legend_y_geo = float(options["legend_y_position_geo"].replace(" ",""))
 
legend_font_size_geo = int(options["legend_font_size_geo"].replace(" ",""))
legend_font_style_geo = str(options["legend_font_style_geo"])\
                           .replace(" ","").lower()                         
legend_text_col_geo = str(options["legend_text_colour_geo"])\
                           .replace(" ","").lower()    

leg_section_height_geo = float(options["legend_section_height_geo"]
                              .replace(" ","")) 
leg_section_width_geo = float(options["legend_section_width_geo"]
                             .replace(" ","")) 

leg_label_v_adjust_geo = float(options["legend_label_v_adjust_geo"].
                               replace(" ",""))
leg_label_h_adjust_geo = float(options["legend_label_h_adjust_geo"].\
                               replace(" ",""))

###############################################################################                               
#Obtain charcoal width and gap and colour parameters###########################
###############################################################################
char_wid = float(options["charcoal_width"].replace(" ",""))    
char_line_colour =   str(options["charcoal_line_colour"]).lower().\
                                                          replace(" ","")    
char_gap = float(options["gap_between_TS_and_charcoal"].replace(" ",""))    

###############################################################################                               
#Obtain other width and gap and colour parameters #############################
############################################################################### 
other_wid = float(options["other_width"].replace(" ",""))       
line_colour_other = str(options["other_line_colour"]).lower().replace(" ","")
other_gap = float(options["gap_between_TS_and_other"].replace(" ","")) 

###############################################################################
#Obtain core labels parameters ################################################
###############################################################################
core_label_on_off = str(options["core_label_on_off**"]).replace(" ","").lower()
core_label_size = int(options["core_label_size"].replace(" ",""))
core_label_style = str(options["core_label_style"]).replace(" ","").lower() 
core_label_colour = str(options["core_label_colour"]).replace(" ","").lower() 

core_label_v_adjust = float(options["core_label_v_adjust"].replace(" ",""))
core_label_h_adjust = float(options["core_label_h_adjust"].replace(" ",""))
                      
###############################################################################
# Obtain colours to use to change incoming numeric information from ########### 
# parameter file ##############################################################
###############################################################################
colour_dict = colours.col_dict()
alt_name_dict = colours.alt_ts_name_dict()
tex_dict = colours.tex_dict()

tex_dict_status = tex_dict[0]
tex_dict_colour = tex_dict[1]

use_alt_name = options["Use alternative TS name**"].lower().replace(" ","")

colour_rock_list = colours.col_rock_list()

colour_rock_dict_f = colour_rock_list[0]
colour_rock_dict_b = colour_rock_list[1]
colour_rock_dict_n = colour_rock_list[2]

col_rock_dict = colours.col_rock_dict()

colour_vp_dict = colours.vp_col_dict()
colour_vp_dict_leg = colour_vp_dict.copy() 
colour_vp_dict_leg.pop("N_A")
colour_other_dict = colours.other_col_dict()

###############################################################################
# Turtle draw speed ###########################################################
###############################################################################
speed = "fastest"

###############################################################################
###############################################################################
############################## WINDOW 1 #######################################
###############################################################################
###############################################################################
class window_1():
    def __init__(self, master):
        self.master = master        
        screen_width = (master.winfo_screenwidth())
        screen_width_mm = (master.winfo_screenmmwidth())
        pixels_mm = screen_width / screen_width_mm
        
        #######################################################################
        # Obtain size in pixels of canvas area from size in mm nominated in ###
        # options.csv #########################################################
        #######################################################################
        canvas_x = mm_x*pixels_mm
        canvas_y = mm_y*pixels_mm
        
        #Obtain the figures actual width by using propotion value from
        #options.csv in pixels and mm
        figure_width_pix = canvas_x * fig_height_prop
        figure_height_pix = canvas_y * fig_height_prop
        
        figure_width_mm = figure_width_pix / pixels_mm
        figure_height_mm = figure_height_pix / pixels_mm
        
        #Place the figure centrally in the canvas with these coordinates
        y_co = (canvas_y/2) - (canvas_y - figure_height_pix)/2  
 
        #Wid is value in pixels for width of each of the four rectangles in 
        #Troels Smith assessment
        wid = wid_x*pixels_mm
        
        #######################################################################
        # Create window size to work in and give it a title ###################
        #######################################################################
        self.master.minsize(int(canvas_x), int(canvas_y))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.title("Peat core plotter - Welcome")
        self.frame_1 = ttk.Frame(self.master)

        #######################################################################
        self.frame_1.grid(row=0,
                          column=0,
                          sticky=(N, W, E, S))
        
        #create a canvas to do turtle drawing of same size as frame and window
        self.canvas = Canvas(self.frame_1,
                             width = int(canvas_x),
                             height = int(canvas_y),
                             bg="lightcyan")  

        self.canvas.grid(column=0,
                         row=0,
                         sticky=(N,S,E,W))
        
        #Add turtle on to the canvas
        screen = turtle.TurtleScreen(self.canvas)
        dave = turtle.RawTurtle(screen, shape="turtle")
        screen.tracer(0)
        
        #######################################################################
        def silt_shapes (hi,wid,sym_col):
            dave.pencolor("black")

            hi_inc = wid*0.1
            wid_inc = wid*0.4
            shape_wid = wid*0.3
            shape_hi = wid*0.2
            
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            
            dave.setheading(0)
            dave.forward(wid_inc)
           
            for x in range(0,100):
                dave.penup()
                dave.pensize(1)
                
                dave.setheading(270)
                if x > 0:
                    dave.forward(hi_inc*4)
                else:
                    dave.forward(hi_inc)
                
                pos_inc_start = dave.pos()
                
                dave.penup()
                dave.forward(shape_hi)
                end_point = dave.pos()
                dave.setheading(90)
                dave.forward(shape_hi)
                dave.setheading(270)
                
                if end_point[1]  > pos_lowest_y[1]:
                    dave.pendown()
                    dave.pencolor(sym_col)
                    dave.forward(shape_hi)
                    
                    dave.setheading(0)
                    
                    dave.forward(shape_wid)
                    dave.pensize(1)
                    dave.penup()
                    
                    dave.setheading(180)
                    dave.forward(shape_wid)
                else:
                    break
                
            dave.pensize(1)
        
        #######################################################################    
        def sand_shapes (hi,wid,sym_col):
            dave.pencolor("black")
        
            hi_inc = wid*0.1
            wid_inc = wid*0.4
            shape_hi = wid*0.15
            
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)

            dave.setheading(0)
            dave.forward(wid_inc*1.25)
                      
            for x in range(0,100):
                dave.penup()
                dave.pensize(1)
                
                dave.setheading(270)
                
                if x > 0:
                    dave.forward(hi_inc*4)
                else:
                    dave.forward(hi_inc)
                    
                pos_inc_start = dave.pos()
                
                dave.penup()
                dave.forward(shape_hi)
                end_point = dave.pos()
                dave.setheading(90)
                dave.forward(shape_hi)
                dave.setheading(270)
                
                if end_point[1]  > pos_lowest_y[1]:
                    dave.pendown()
                    dave.pencolor(sym_col)
                    dave.fillcolor(sym_col)
                    dave.begin_fill()
                    dave.circle(1)
                    dave.end_fill()
                    dave.penup()
                    dave.forward(shape_hi)
                else:
                    break
                
            dave.pensize(1)

        #######################################################################    
        def gravel_shapes (hi,wid,sym_col):
            dave.pencolor("black")
        
            hi_inc = wid*0.15
            wid_inc = wid*0.4
            shape_hi = wid*0.15
            
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)

            dave.setheading(0)
            dave.forward(wid_inc)
                      
            for x in range(0,100):
                dave.penup()
                dave.pensize(1)
                
                dave.setheading(270)
                
                if x > 0:
                    dave.forward(hi_inc*4)
                else:
                    dave.forward(hi_inc*1.5)
                
                dave.penup()
                dave.forward(shape_hi)
                end_point = dave.pos()
                dave.setheading(90)
                dave.forward(shape_hi)
                dave.setheading(270)
                
                if end_point[1]  > pos_lowest_y[1]:
                    dave.pendown()
                    dave.pencolor(sym_col)

                    dave.circle((wid/6))
                    dave.penup()
                    dave.forward(shape_hi)               
                else:
                    break
                
            dave.pensize(1)

        #######################################################################
        # Function used to draw out each section of core with four rectangular#
        # troels smith units inside. ##########################################
        #######################################################################
        def rectangle(name,
                      col,
                      wid,
                      hi,
                      x,
                      y,
                      unrec,
                      section_num,
                      core_num,
                      core_labels):
            
            same_col = "False"
            
            if remove_seg == "on":
                unique_names = set(name)
                if  len(unique_names) == 1 and unique_names !="Ur":
                    same_col = "True"
                else:
                    same_col = "False"
                    
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x+shift,y)
            dave.setheading(90)

            dave.forward(core_label_v_adjust*pixels_mm)
            dave.setheading(0)
            dave.forward(core_label_h_adjust*pixels_mm)
                
            dave.pendown()
            
            ###################################################################
            
            if core_label_on_off == "on":
                if section_num == 0:
                    dave.pencolor(core_label_colour)
                    dave.write(core_labels[str(float(core_num+1))],
                               move=False,
                               align="left",
                               font=("Arial",
                                     core_label_size,
                                     core_label_style))
                
            dave.penup() 
            dave.setpos(x+shift,y)
            dave.pendown()
            
            ###################################################################
            #Error check entries
            try:
                dave.pencolor(pen_colour_rect)
            except:
                ge("Line colour")
                
            try:
                dave.fillcolor(col[0])
            except:
                 ge("TS colour entry")
                 
            ###################################################################
            dave.begin_fill()
            dave.pencolor(pen_colour_rect)

            dave.setheading(0)
            dave.forward(wid)
            
            if unrec == "yes":
                dave.pencolor("white")
                                
            dave.setheading(270)
            dave.forward(hi)
            dave.pencolor(pen_colour_rect)
            dave.setheading(180)
            dave.forward(wid)  
            
            if unrec == "yes":
                dave.pencolor("white")
                
            if same_col == "True":
                dave.pencolor(col[0])
                
            dave.setheading(90)            
            dave.forward(hi) 
            dave.end_fill()
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x+shift,y)
            
            if name[0] == "Ag" or name[0] == "As":
                if name[0] == "Ag":
                    if tex_dict_status["Argilla granosa tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla granosa tex**"]
                        silt_shapes(hi,wid,sym_col)
                               
                if name[0] == "As":
                    if tex_dict_status["Argilla steatodes tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla steatodes tex**"]
                        silt_shapes(hi,wid,sym_col)
            
            if name[0] == "Gg(min)" or name[0] == "Gg(maj)":
                
                if name[0] == "Gg(min)":
                    if tex_dict_status["Grana glareosa minora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa minora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                               
                if name[0] == "Gg(maj)":
                    if tex_dict_status["Grana glareosa majora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa majora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                
            if name[0] == "Ga" or name[0] == "Gs":
                if name[0] == "Ga":
                    if tex_dict_status["Grana arenosa tex**"] == "on":
                        sym_col = tex_dict_colour["Grana arenosa tex**"]
                        sand_shapes(hi,wid,sym_col)
                               
                if name[0] == "Gs":
                    if tex_dict_status["Grana saburralia tex**"] == "on":
                        sym_col = tex_dict_colour["Grana saburralia tex**"]
                        sand_shapes(hi,wid,sym_col)
                
            dave.pencolor(pen_colour_rect)
            dave.penup() 
            dave.setpos((x-wid)+shift,y)
            dave.pendown()
            

            dave.pencolor(pen_colour_rect)
            ###################################################################
            #Error check entries
            try:
                dave.fillcolor(col[1])
            except:
                ge("TS colour entry")
            
            ###################################################################
            dave.begin_fill()
            dave.setheading(0)
            dave.pencolor(pen_colour_rect)
            dave.forward(wid) 
            dave.setheading(270)
            
            if unrec == "yes":
                dave.pencolor("white")
            
            if same_col == "True":
                dave.pencolor(col[0])
        
            dave.forward(hi)
            
            dave.setheading(180)
            dave.pencolor(pen_colour_rect)
            dave.forward(wid) 
            
            if unrec == "yes":
                dave.pencolor("white")
                
            if same_col == "True":
                dave.pencolor(col[0])
                
            dave.setheading(90)
            
            dave.forward(hi) 
            dave.end_fill()
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos((x-wid)+shift,y)
            
            if name[1] == "Ag" or name[1] == "As":
                if name[1] == "Ag":
                    if tex_dict_status["Argilla granosa tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla granosa tex**"]
                        silt_shapes(hi,wid,sym_col)
                               
                if name[1] == "As":
                    if tex_dict_status["Argilla steatodes tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla steatodes tex**"]
                        silt_shapes(hi,wid,sym_col)

            if name[1] == "Gg(min)" or name[1] == "Gg(maj)":
                if name[1] == "Gg(min)":
                    if tex_dict_status["Grana glareosa minora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa minora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                               
                if name[1] == "Gg(maj)":
                    if tex_dict_status["Grana glareosa majora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa majora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                
            if name[1] == "Ga" or name[1] == "Gs":
                if name[1] == "Ga":
                    if tex_dict_status["Grana arenosa tex**"] == "on":
                        sym_col = tex_dict_colour["Grana arenosa tex**"]
                        sand_shapes(hi,wid,sym_col)
                               
                if name[1] == "Gs":
                    if tex_dict_status["Grana saburralia tex**"] == "on":
                        sym_col = tex_dict_colour["Grana saburralia tex**"]
                        sand_shapes(hi,wid,sym_col)

             
            dave.pencolor(pen_colour_rect)
            dave.penup() 
            dave.setpos((x-wid*2)+shift,y)
            dave.pendown()
            
            if unrec == "yes":
                dave.pencolor("white")
            elif same_col == "True":
                dave.pencolor(col[0])
            else:
                dave.pencolor(pen_colour_rect)
            
            ###################################################################
            #Error check entries
            try:
                dave.fillcolor(col[2])
            except:
                ge("TS colour entry")
            
            ###################################################################
            dave.begin_fill()
            dave.pencolor(pen_colour_rect)
            dave.setheading(0)
            dave.forward(wid) 
            
            if unrec == "yes":
                dave.pencolor("white")
            elif same_col == "True":
                dave.pencolor(col[0])
            else:
                dave.pencolor(pen_colour_rect)
            
            dave.setheading(270)
            dave.forward(hi)
            
            dave.pencolor(pen_colour_rect)
            dave.setheading(180)
            
            dave.forward(wid)
            
            if unrec == "yes":
                dave.pencolor("white")
            elif same_col == "True":
                dave.pencolor(col[0])
            else:
                dave.pencolor(pen_colour_rect)
                
            dave.setheading(90)
            dave.forward(hi) 
            dave.end_fill()
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos((x-wid*2)+shift,y)
            
            if name[2] == "Ag" or name[2] == "As":
                if name[2] == "Ag":
                    if tex_dict_status["Argilla granosa tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla granosa tex**"]
                        silt_shapes(hi,wid,sym_col)
                              
                if name[2] == "As":
                    if tex_dict_status["Argilla steatodes tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla steatodes tex**"]
                        silt_shapes(hi,wid,sym_col)
                        
            if name[2] == "Gg(min)" or name[2] == "Gg(maj)":
                if name[2] == "Gg(min)":
                    if tex_dict_status["Grana glareosa minora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa minora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                               
                if name[2] == "Gg(maj)":
                    if tex_dict_status["Grana glareosa majora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa majora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                        
            if name[2] == "Ga" or name[2] == "Gs":
                if name[2] == "Ga":
                    if tex_dict_status["Grana arenosa tex**"] == "on":
                        sym_col = tex_dict_colour["Grana arenosa tex**"]
                        sand_shapes(hi,wid,sym_col)
                               
                if name[2] == "Gs":
                    if tex_dict_status["Grana saburralia tex**"] == "on":
                        sym_col = tex_dict_colour["Grana saburralia tex**"]
                        sand_shapes(hi,wid,sym_col)

            
            dave.pencolor(pen_colour_rect)
            dave.penup() 
            dave.setpos((x-wid*3)+shift,y)
            dave.pendown()
            
            if unrec == "yes":
                dave.pencolor("white")
            elif same_col == "True":
                dave.pencolor(col[0])
            else:
                dave.pencolor(pen_colour_rect)
            
            ###################################################################
            #Error check entries
            try:
                dave.fillcolor(col[3])
            except:
                ge("TS colour entry")
            
            ###################################################################
            dave.begin_fill()
            dave.setheading(0)
            dave.forward(wid) 
            
            dave.setheading(270)
            
            if unrec == "yes":
                dave.pencolor("white")
            elif same_col == "True":
                dave.pencolor(col[0])
            else:
                dave.pencolor(pen_colour_rect)
            
            dave.forward(hi)
            
            dave.setheading(180)
            dave.pencolor(pen_colour_rect)
            dave.forward(wid) 
            
            if unrec == "yes":
                dave.pencolor("white")
                dave.setheading(0)
                dave.forward(wid*4)
                dave.penup()
                dave.setheading(180)
                dave.forward(wid*4)

            dave.pendown()
  
            dave.setheading(90)
            
            if unrec == "yes":
                dave.pencolor("white")
            else:
                dave.pencolor(pen_colour_rect)
                

            dave.forward(hi) 
            dave.end_fill()
            
            if unrec == "yes" or same_col == "True" :
                dave.pendown()
                dave.pencolor(pen_colour_rect)
                dave.setheading(0)
                dave.forward(wid*4)
                dave.penup()
                dave.setheading(180)
                dave.forward(wid*4)
                
            
                
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos((x-wid*3)+shift,y)
            
            if name[3] == "Ag" or name[3] == "As":
                if name[3] == "Ag":
                    if tex_dict_status["Argilla granosa tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla granosa tex**"]
                        silt_shapes(hi,wid,sym_col)
                               
                if name[3] == "As":
                    if tex_dict_status["Argilla steatodes tex**"] == "on":
                        sym_col = tex_dict_colour["Argilla steatodes tex**"]
                        silt_shapes(hi,wid,sym_col)
                        
            if name[3] == "Gg(min)" or name[3] == "Gg(maj)":
                if name[3] == "Gg(min)":
                    if tex_dict_status["Grana glareosa minora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa minora tex**"]
                        gravel_shapes(hi,wid,sym_col)
                               
                if name[3] == "Gg(maj)":
                    if tex_dict_status["Grana glareosa majora tex**"] == "on":
                        sym_col = tex_dict_colour["Grana glareosa majora tex**"]
                        gravel_shapes(hi,wid,sym_col)

            if name[3] == "Ga" or name[3] == "Gs":
                if name[3] == "Ga":
                    if tex_dict_status["Grana arenosa tex**"] == "on":
                        sym_col = tex_dict_colour["Grana arenosa tex**"]
                        sand_shapes(hi,wid,sym_col)
                               
                if name[3] == "Gs":
                    if tex_dict_status["Grana saburralia tex**"] == "on":
                        sym_col = tex_dict_colour["Grana saburralia tex**"]
                        sand_shapes(hi,wid,sym_col)
            
            dave.pencolor(pen_colour_rect)
            dave.penup() 
            dave.hideturtle()
            dave.setpos(x,y-hi)

        #######################################################################
        # Function draws a large simple rectangle of entire width of core and #
        # to the depth defined by the hi variable for geology##################
        #######################################################################
        def big_rect(hi,
                     back_col="white",
                     geo_border_col="black"):
            
            dave.setheading(0)
            dave.forward(shift)
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.pendown()
            
            ###################################################################
            #Error check entries
            try:
                dave.pencolor(geo_border_col)
            except:
                ge("Geology border colour")
            
            ###################################################################
            dave.pencolor(geo_border_col)
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup()
            
            ###################################################################
            #Error check entries
            try:
                dave.fillcolor(back_col)
            except:
                ge("Geology background colour")
            
            ###################################################################
            dave.begin_fill()
            dave.pendown()
            dave.pencolor(geo_border_col)
            dave.setheading(0)
            dave.forward(wid) 
            dave.setheading(270)
            dave.forward(hi)
            dave.setheading(180)
            dave.forward(wid*4)  
            dave.setheading(90)
            dave.forward(hi)
            dave.end_fill()
            dave.pendown()
            dave.setheading(0)
            dave.forward(wid*4) 
            dave.setheading(270)
            dave.forward(hi)
            dave.setheading(180)
            dave.forward(wid*4)  
            dave.setheading(90)
            dave.forward(hi)
    
        #######################################################################
        # Function draws a large simple rectangle of entire width of core and #
        # to the depth defined by the hi variable for geology legend ##########
        #######################################################################
        def big_rect_leg(x,
                         y,
                         width,
                         height,
                         legend_x_geo,
                         legend_y_geo,
                         back_col="white",
                         geo_border_col="black",
                         label = "geology"):
            
            dave.penup() 
            dave.setpos(x,y)
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            
            ###################################################################
            #Error check entries
            try:
                dave.pencolor(geo_border_col)
            except:
                ge("Geology border colour")
            
            ###################################################################
            dave.pencolor(geo_border_col)
            dave.pensize(1)
            dave.setheading(270)
            dave.pendown()
            dave.forward(height)
            dave.penup()
 
            ###################################################################
            #Error check entries
            try:
                dave.fillcolor(back_col)
            except:
                ge("Geology background colour")
                
            ###################################################################
            dave.begin_fill()
            dave.pencolor(geo_border_col)
            dave.setheading(0)
            dave.pendown()
            dave.forward(width) 
            dave.setheading(90)
            dave.forward(height)
            dave.setheading(180)
            dave.forward(width) 
            dave.setheading(270)
            dave.forward(height)
            dave.setheading(90)
            dave.forward(height)
            dave.end_fill()
            dave.penup()
            dave.setheading(0)
            dave.forward(width+5*pixels_mm+(leg_label_h_adjust_geo*pixels_mm))
            dave.setheading(270)
            dave.forward(height/2)
            dave.setheading(90)
            dave.forward(leg_label_v_adjust_geo*pixels_mm)
            dave.pendown()
            dave.pencolor(legend_text_col_geo)
            
            ###################################################################
            dave.write(label,
                       move=False,
                       align="left",
                       font=("Arial",
                             legend_font_size_geo,
                             legend_font_style_geo))
            
            ###################################################################
            dave.penup()
            dave.setheading(180)
            dave.forward(width+5*pixels_mm +(leg_label_h_adjust_geo*pixels_mm))
            dave.setheading(90)
            dave.forward(height/2)
            dave.setheading(270)
            dave.forward(leg_label_v_adjust_geo*pixels_mm)
        
        #######################################################################
        # Function to provide a title for the geology legend ##################
        #######################################################################
        def big_rect_leg_title(x,
                               y,
                               height,
                               col,
                               style,
                               size,
                               title_adj_v,
                               title_adj_h,
                               title = "Geology"):
            
            dave.penup() 
            dave.setpos(x,y)
            dave.setheading(90)
            
            dave.forward(title_adj_v*pixels_mm)
            dave.setheading(0)
            dave.forward(title_adj_h*pixels_mm)
            dave.pencolor(col)
            dave.write(title,
                       move=False,
                       align="left",
                       font=("Arial",
                             size,
                             style))
            
        #######################################################################
        # Function draws symbols for sandstone in the relavent rectangle ######
        #######################################################################
        def sand_stone(col,
                       width,
                       hi,
                       x,
                       y,
                       geo_border_col = "black",
                       back_col = "white",
                       fore_col = "black",
                       legend = "off"):
            
            ###################################################################
            inc = 1
            gap = 1#1
            stagger_space = 1
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Sandstone**"],
                             colour_rock_dict_f["Sandstone**"],
                             colour_rock_dict_n["Sandstone**"])   
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
                    
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            pos_start = dave.pos()
            
            if legend == "on":
                pos_2_x_max = x + width
            else:  
                #furthest x position for any symbols
                pos_2_x_max = x + width+shift 

            ###################################################################
            for f in range(100):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    break
                
                if f %2 == 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward(pixels_mm*stagger_space)
                
                ###############################################################
                for dash in range(100):
                    dave.pensize(1)
                    dave.setheading(0)
                    
                    ###########################################################
                    try:
                        dave.pencolor(fore_col)
                    except:
                        ge("Geology colour entry")
                    
                    ###########################################################
                    dave.pendown()
                    dave.forward(pixels_mm*0.5)
                    dave.penup()
                    dave.forward(pixels_mm*gap)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0] + pixels_mm*gap >= pos_2_x_max:
                        if pos_2_x_max - pos_post_dash[0] > 0:
                            extra = pos_2_x_max - pos_post_dash[0]
                            if extra >= gap*pixels_mm:
                                dave.pendown()
                                dave.forward(pixels_mm*gap)
                                dave.penup()
                            if extra < gap*pixels_mm: 
                                dave.pendown()
                                dave.forward(pixels_mm*0.5)
                                dave.penup()
                        break
                inc+=1  
                
        #######################################################################
        # Function draws symbols for siltstone in the relavent rectangle ######
        #######################################################################
        def silt_stone(col,
                       width,
                       hi,
                       x,
                       y,
                       geo_border_col = "black",
                       back_col = "white",
                       fore_col = "black",
                       legend = "off"):
            
            ###################################################################
            inc = wid_x/2 
            big_dash_len = wid_x/1.5
            small_dash_len = wid_x/3
            gap = wid_x/4
            stagger_space = wid_x/1.5
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Siltstone**"],
                             colour_rock_dict_f["Siltstone**"],
                             colour_rock_dict_n["Siltstone**"])   
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
                    
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            pos_start = dave.pos()
            
            if legend == "on":
                pos_2_x_max = x + width
            else:
                #furthest x position for any symbols
                pos_2_x_max = x + width+shift 

            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] <= pos_lowest_y[1]:
                    break

                if f %2 != 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward(pixels_mm*stagger_space)
                
                ###############################################################
                for dash in range(100):
                    dave.pensize(1)
                    dave.setheading(0)
                    dave.pendown()
                    
                    ###########################################################
                    #Error check entries
                    try:
                        dave.pencolor(fore_col)
                    except:
                        ge("Geology colour entry")
                        sys.exit()
                        
                    ###########################################################    
                    dave.forward(pixels_mm*big_dash_len)
                    pos_post_dash = dave.pos()

                    if pos_post_dash[0]+(pixels_mm*big_dash_len) \
                        >= pos_2_x_max :
                        dave.penup()
                        break
                    
                    dave.penup()
                    dave.forward(pixels_mm*gap)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]+(pixels_mm*gap) >= pos_2_x_max :
                        dave.penup()
                        break
                    
                    dave.pensize(1)
                    dave.setheading(0)
                    dave.pendown()
                    dave.forward(pixels_mm *small_dash_len)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]+(pixels_mm*small_dash_len)\
                        >= pos_2_x_max :
                        dave.penup()
                        break
                    
                    dave.penup()
                    dave.forward(pixels_mm*gap)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]+(pixels_mm*big_dash_len)\
                        >= pos_2_x_max :
                        dave.penup()
                        break

                inc+= wid_x/2
                
        #######################################################################
        # Function draws symbols for shale in the relavent rectangle ##########
        #######################################################################        
        def shale(col,
                  width,
                  hi,
                  x,
                  y,
                  geo_border_col = "black",
                  back_col = "white",
                  fore_col = "black",
                  legend = "off"):
            
            ###################################################################
            inc = wid_x/2
            big_dash_len = wid_x/1.2
            gap = wid_x/2
            stagger_space = wid_x/1.2
         
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Shale**"],
                             colour_rock_dict_f["Shale**"],
                             colour_rock_dict_n["Shale**"])
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
        
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            pos_start = dave.pos() 
            
            if legend == "on":
                pos_2_x_max = x + width
            else:
                #furthest x position for any symbols
                pos_2_x_max = x + width+shift 

            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    break

                if f %2 == 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward(pixels_mm*stagger_space)
                
                ###############################################################
                for dash in range(100):
                    dave.pensize(1)
                    dave.setheading(0)
                    dave.pendown()
                    
                    ###########################################################
                    #Error check entries
                    try:
                        dave.pencolor(fore_col)
                    except:
                        ge("Geology colour entry")
                    
                    ###########################################################
                    dave.forward(pixels_mm*big_dash_len)
                    dave.penup()
                    dave.forward(pixels_mm*gap)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]+(pixels_mm*big_dash_len)\
                        >= pos_2_x_max :
                        dave.penup()
                        break
    
                inc+=wid_x/2
                
        #######################################################################
        # Function draws symbols for marl in the relavent rectangle ###########
        #######################################################################             
        def marl(col,
                 width,
                 hi,
                 x,
                 y,
                 geo_border_col = "black",
                 back_col = "white",
                 fore_col = "black",
                 legend = "off"):
            
            ###################################################################
            inc = 2
            half_dash = 1
            vert_dash = 1
            gap = 1
            stagger_space = 2
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Marl**"],
                             colour_rock_dict_f["Marl**"],
                             colour_rock_dict_n["Marl**"])    
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
        
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            pos_start = dave.pos()
            
            if legend == "on":
                pos_2_x_max = x + width
            else:    
                pos_2_x_max = x + width+shift

            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc*  pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    break
                
                if pos_inc_start[1]-(pixels_mm*vert_dash) < pos_lowest_y[1]\
                    and legend =="on":
                    break

                if f %2 == 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward(pixels_mm*stagger_space)
                
                ###############################################################
                for dash in range(100):
                    dave.pensize(1)
                    dave.setheading(0)
                    pos = dave.pos()
                    
                    if pos[0]+(half_dash*2) >= pos_2_x_max:
                        break
                    dave.pendown()
                    
                    ###########################################################
                    #Error check entires
                    try:
                        dave.pencolor(fore_col)
                    except:
                        ge("Geology colour entry")
                        sys.exit()
                        
                    ###########################################################    
                    dave.forward(pixels_mm*half_dash)
                    dave.setheading(270)
                    
                    if pos_inc_start[1]-(pixels_mm*vert_dash)\
                        < pos_lowest_y[1]:
                        dave.forward(pos_inc_start[1] - pos_lowest_y[1])
                    else:
                        dave.forward(pixels_mm*vert_dash)
                        
                    dave.setheading(90)
                    dave.penup()
                    
                    if pos_inc_start[1]-(pixels_mm*vert_dash)\
                        < pos_lowest_y[1]:
                        dave.forward(pos_inc_start[1] - pos_lowest_y[1])
                    else:
                        dave.forward(pixels_mm*vert_dash)
                        
                    dave.setheading(0)
                    dave.pendown()
                    dave.forward(pixels_mm*half_dash)
                    dave.penup()
                    dave.forward(pixels_mm*gap)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]-(pixels_mm*1) \
                       < pos_2_x_max < pos_post_dash[0] \
                       + (pixels_mm*1):
                        break
    
                inc+=2 
                
            ###################################################################   
            if legend == "off":
                dave.penup() 
                dave.setpos(x+shift,y)
                dave.pendown()
                dave.pensize(1)
                dave.pencolor(col)
                dave.setheading(0)
                dave.forward(wid) 
                dave.setheading(270)
                dave.forward(hi)
                pos_lowest_y = dave.pos()
                dave.setheading(180)
                dave.forward(wid*4)  
                dave.setheading(90)
                dave.forward(hi)
                dave.setheading(0)
                dave.forward(wid*3) 
        
        #######################################################################
        # Function draws symbols for limestone in the relavent rectangle ######
        #######################################################################             
        def lime_stone(col,
                       width,
                       hi,
                       x,
                       y,
                       geo_border_col = "black",
                       back_col = "white",
                       fore_col = "black",
                       legend = "off"):
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Limestone**"],
                             colour_rock_dict_f["Limestone**"],
                             colour_rock_dict_n["Limestone**"])   
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
        
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            
            pos_start = dave.pos()
            if legend == "on":
                pos_2_x_max = x + width
            else:   
                pos_2_x_max = x + width+shift #furthest x position
            
            stagger_space = wid_x/4
            space = wid_x/2
            
            inc_3 = wid_x/2
            inc = wid_x/2 
            
            ###################################################################
            for f in range(1000):
                dave.setpos(pos_start)
                dave.penup()
                dave.setheading(270)
                dave.forward(inc*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] <= pos_lowest_y[1]:
                    adjust_vert = inc_3*pixels_mm + (pos_inc_start[1] -
                                                      pos_lowest_y[1])
                    break

                dave.pensize(1)
                dave.setheading(0)
                dave.pendown()
                
                ###############################################################
                #Error check entries
                try:
                    dave.pencolor(fore_col)
                except:
                    ge("Geology colour entry")
                
                ###############################################################
                if legend=="on":
                    dave.forward(width)
                else:
                    dave.forward(wid*4)
                dave.penup()
                pos_post_dash = dave.pos()
    
                inc+=wid_x/2
                
            inc_1 = wid_x/2
            inc = wid_x/2
            
            ###################################################################
            for f in range(1000):
                dave.setpos(pos_start)
                dave.penup()
                dave.setheading(270)
                dave.forward(inc_1*pixels_mm)
                pos_inc_start = dave.pos()
                
                if f %2 == 0:
                    dave.setheading(0)
                    dave.penup()
                    dave.forward(pixels_mm*stagger_space)
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    diff = pos_lowest_y[1] - pos_inc_start[1]
                    dave.setpos(pos_inc_start[0],pos_inc_start[1]+diff)
                    
                    if f %2 == 0:
                        dave.setheading(0)
                        dave.penup()
                        dave.forward(pixels_mm*stagger_space)
                        
                    ########################################################### 
                    if legend == "off":
                        for dash in range(100):
                            dave.penup()
                            dave.pensize(1)
                            dave.setheading(0)
                            dave.forward(space*pixels_mm)
                            dave.pendown()
                            dave.setheading(90)
                            dave.forward(adjust_vert)
                            dave.penup()
                            dave.setheading(270)
                            dave.forward(adjust_vert)
                            pos_post_dash = dave.pos()
                            
                            if pos_post_dash[0]+(pixels_mm*space)\
                                >= pos_2_x_max :
                                break
                    break
                
                ###############################################################
                for dash in range(100):
                    dave.pensize(1)
                    dave.setheading(0)
                    dave.forward(pixels_mm*space)
                    dave.pendown()
                    dave.setheading(90)
                    dave.forward(pixels_mm*inc)
                    dave.penup()
                    dave.setheading(270)
                    dave.forward(pixels_mm*inc)
                    pos_post_dash = dave.pos()
                    
                    if pos_post_dash[0]+(pixels_mm*space) >= pos_2_x_max :
                        break
                    
                inc_1+=wid_x/2 
                      
        #######################################################################
        # Function draws symbols for till in the relavent rectangle ###########
        ####################################################################### 
        def till(col,
                 width,
                 hi,
                 x,
                 y,
                 geo_border_col = "black",
                 back_col = "white",
                 fore_col = "black",
                 legend = "off"):
            
            ###################################################################
            if wid_x <=3:
                inc = wid_x/8 
                inc_1 = wid_x/8 
                tri_side = wid_x/1.5
                stagger_space = wid_x/1.5
                gap = wid_x/1.5 #gap between triangles
            else: 
                inc = wid_x/10 
                inc_1 = wid_x/10 
                tri_side = wid_x/3
                stagger_space = wid_x/3
                gap = wid_x/1.5 #gap between triangles
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Till**"],
                             colour_rock_dict_f["Till**"],
                             colour_rock_dict_n["Till**"])
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)

            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            
            if legend == "on":
                pos_start = dave.pos()
                pos_2_x_max = x + width
            else:
                pos_start = dave.pos()
                pos_2_x_max = x + width + shift

            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1]- ((inc_1*pixels_mm) + 
                                      ((wid_x/3)*pixels_mm)) < pos_lowest_y[1]:
                    break
    
                if f %2 == 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward((pixels_mm*stagger_space)+((gap*pixels_mm/2)))
                
                ###############################################################
                for dash in range(100):
                    pos = dave.pos()
                    if pos[0] + ((tri_side*2)*pixels_mm) >= pos_2_x_max:
                        break
                    dave.pensize(1)
                    dave.setheading(0)
                    dave.penup()
                    dave.forward((pixels_mm*1)+(gap*pixels_mm/2))

                    ###########################################################
                    #Error check entries
                    try:
                        dave.pencolor(fore_col)
                    except:
                        ge("Geology colour entry")
                        
                    ###########################################################   
                    dave.pendown()
                    dave.setheading(240)
                    dave.forward(pixels_mm*tri_side)
                    dave.setheading(0)
                    dave.forward(pixels_mm*tri_side)
                    pos_post_dash = dave.pos()
                    dave.setheading(120)
                    dave.forward(pixels_mm*tri_side)
                    dave.penup()
                    dave.setheading(0)
                    dave.forward(pixels_mm*gap)
                
                if wid_x<=3:
                    inc+=wid_x
                else:    
                    inc+=wid_x/3 

        #######################################################################
        # Function draws symbols for mudstone in the relavent rectangle #######
        ####################################################################### 
        def mud_stone (width,
                       hi,
                       x,
                       y,
                       geo_border_col = "black",
                       back_col = "white",
                       fore_col = "black",
                       legend = "off"):
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Mudstone**"],
                             colour_rock_dict_f["Mudstone**"],
                             colour_rock_dict_n["Mudstone**"])    
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
            
            ###################################################################
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x+shift,y)
            dave.pendown()
            dave.pencolor(fore_col)
            dave.setheading(0)
            
            if legend =="off":
                dave.forward(wid) 
                dave.setheading(270)
                dave.forward(hi)
                pos_lowest_y = dave.pos()#lowest y position
                dave.setheading(180)
                dave.forward(wid*4)  
                dave.setheading(90)
                dave.forward(hi)
                pos_start = dave.pos()
                pos_2_x_max = x + wid  #furthest x position
            
            if legend =="on":
                dave.setheading(180)
                dave.forward(shift)
                dave.setheading(270)
                dave.forward(hi)
                pos_lowest_y = dave.pos()#lowest y position 
                dave.setheading(90)
                dave.forward(hi)
                pos_start = dave.pos()
                pos_2_x_max = x + width  #furthest x position
        
            ###################################################################
            if wid_x <=7:
                inc = wid_x/4
            else:
                inc = wid_x/6
            
            inc_1 = inc
            
            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.penup()
                dave.setheading(270)
                dave.forward(inc_1*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    break
                
                dave.pensize(1)
                dave.setheading(0)
                dave.pendown()
                dave.pencolor(fore_col)
                
                if legend =="off":
                    dave.forward(wid*4)
                if legend =="on":
                    dave.forward(width)    
                    
                dave.penup()
            
                inc_1+=inc
                
            ###################################################################
            for f in range(50):
                dave.setpos(pos_start)
                dave.penup()
                dave.setheading(270)
                dave.forward(inc_1*pixels_mm)
                pos_inc_start = dave.pos()
                
                if pos_inc_start[1] < pos_lowest_y[1]:
                    break
                
                dave.pensize(1)
                dave.setheading(0)
                dave.pendown()
                dave.pencolor(fore_col)
                dave.forward(wid*4)
                dave.penup()
            
                inc_1+=inc
        
        #######################################################################
        # Function draws v shape symbols for volcanic #########################
        #######################################################################
        def vs(pos_low,
               fore_col = "black"):
            
            factor = 0.6
            factor_3 = 0.2
            if wid_x <=2:
                factor = 0.8
                factor_3 = 0.2  
                
            dave.pensize(1)
            dave.pendown()
            
            ###################################################################
            #Error check entries
            try:
                dave.pencolor(fore_col)
            except:
                ge("Geology colour entry")
            
            ###################################################################
            dave.setheading(300)
            dave.pendown()
            new_pos = dave.pos()
            
            if new_pos[1]-((wid*factor_3)*4) < pos_low:
                dave.penup()
 
            dave.forward(wid*factor)
            dave.setheading(60)
            dave.forward(wid*factor)
            dave.penup()
            
        #######################################################################
        # Function draws symbols for volcanic rocks in the relavent rectangle #
        # Could be used for igneous and employs vs function to draw v shapes ##
        #######################################################################
        def volcanic (width,
                      hi,
                      x,
                      y,
                      geo_border_col = "black",
                      back_col = "white",
                      fore_col = "black",
                      legend = "off"):
            
            ###################################################################
            factor = 0.8#0.4
            factor_3 = 0.1 #0.1
            
            if wid_x <=2:
               factor = 0.8
               factor_3 = 0.2 
               
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Volcanic**"],
                             colour_rock_dict_f["Volcanic**"],
                             colour_rock_dict_n["Volcanic**"])
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
            
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            
            pos_start = dave.pos()
            if legend == "on":
                pos_2_x_max = x + width
            else:    
                pos_2_x_max = x + width +shift #furthest x position
            
            stagger_space = wid*factor
            inc = wid*factor_3
            gap = wid*factor_3
            
            ###################################################################
            inc_1 = inc
            
            for f in range(200):
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.forward(inc_1)
                pos_inc_start = dave.pos()
                 
                if pos_inc_start[1]-(gap*8) < pos_lowest_y[1]:
                    break
    
                if f %2 == 0:
                   dave.setheading(0)
                   dave.penup()
                   dave.forward(stagger_space) 
                
                ###############################################################
                for dash in range(100):
                    pos = dave.pos()
                    if pos[0] + (wid*factor) >= pos_2_x_max:
                        break
                    
                    vs(pos_lowest_y[1],
                       fore_col)
                    
                    dave.setheading(0)
                    dave.forward(pixels_mm*gap)

                inc_1 += gap*8
        
        #######################################################################
        # Function draws symbols for metamorphic in the relavent rectangle ####
        #######################################################################
        def metamorphic(col,
                        width,
                        hi,
                        x,
                        y,
                        geo_border_col = "black",
                        back_col = "white",
                        fore_col = "black",
                        legend = "off"):
            
            factor = 0.5
            factor_2 = 0.8
            factor_3 = 0.1
            stagger_space = wid*factor
            inc = wid*factor_3
            gap = wid*factor_3
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Metamorphic**"],
                             colour_rock_dict_f["Metamorphic**"],
                             colour_rock_dict_n["Metamorphic**"])
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)
            
            ###################################################################
            dave.penup()
            dave.setheading(270)
            dave.forward(hi)
            pos_lowest_y = dave.pos()
            dave.setheading(90)
            dave.forward(hi)
            pos_start = dave.pos()
            
            if legend == "off":
                pos_2_x_max = x + wid
                
            if legend == "on":
                pos_2_x_max = x + width 
                pos_2_x_max_2 = x + wid+shift
                
            ###################################################################
            #Error check entries
            try:
                dave.pencolor(fore_col)
            except:
                ge("Geology colour")
                
            ###################################################################
            for f in range(100):
                dave.setheading(0)
                dave.forward(shift)
                dave.setpos(pos_start)
                dave.setheading(270)
                dave.penup()
                dave.forward(inc)
                pos_inc_start = dave.pos()
                
                ###############################################################
                if legend == "off":
                    for w in range((int(x-(wid*3)+shift)),
                                   int(pos_2_x_max+shift)):

                        dave.pendown()
    
                        r = (pos_inc_start[1]-(1.7 * math.sin(((math.pi*2)/0.2)
                                                        * math.radians(w))))
                        if r < pos_lowest_y[1]:
                            dave.penup()
                        else:
                            dave.pendown()
                            dave.goto(w,r)
                            dave.penup()
                    
                    if wid_x <=5:
                        inc+=wid/2
                    else:
                        inc+=wid/5
                        
                ###############################################################
                if legend == "on":
                    for w in range(int(x), int(pos_2_x_max)):

                        dave.pendown()
    
                        r = (pos_inc_start[1]-(1.7 * math.sin(((math.pi*2)/0.2)
                                                        * math.radians(w))))
                        if r <= pos_lowest_y[1]:
                            dave.penup()
                            break
                        else:
                            dave.pendown()
                            dave.goto(w,r)
                            dave.penup()
                    
                    if wid_x <=5:
                        inc+=wid/2
                    else:
                        inc+=wid/5
                               
        #######################################################################
        # Function draws symbols for coal in the relavent rectangle ###########
        #######################################################################
        def coal(col,
                 width,
                 hi,
                 x,
                 y,
                 geo_border_col = "black",
                 back_col = "black",
                 fore_col = "black",
                 legend = "off"):
            
            ###################################################################
            if legend == "on":
                big_rect_leg(x,
                             y,
                             leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             legend_x_geo,
                             legend_y_geo,
                             colour_rock_dict_b["Coal**"],
                             colour_rock_dict_f["Coal**"],
                             colour_rock_dict_n["Coal**"])    
            else:    
                big_rect(hi,
                         back_col,
                         geo_border_col)

        #######################################################################
        # Function to draw 'other' presence/absence data ######################
        #######################################################################
        def other(other_cols,
                  wid,
                  hi,
                  x,
                  y,
                  border_col = "white"):
            
            if other_cols !="white":
                dave.speed(f"{speed}")
                dave.hideturtle()
                dave.pensize(1)
                dave.penup() 
                dave.setpos(x+shift,y)
                dave.pendown()
                
                ###############################################################
                #Error check entries
                try:
                    dave.pencolor(border_col)
                except:
                    ge("Border line colour for von Post or Troels smith")
                    
                ###############################################################
                try:
                    dave.fillcolor(other_cols)
                except:
                    ge("Colour for von post or none troels smith")
                    
                ###############################################################    
                dave.begin_fill()
                dave.setheading(0)
                dave.forward(wid) 
                dave.setheading(270)
                dave.forward(hi)
                dave.setheading(180)
                dave.forward(wid)  
                dave.setheading(90)
                dave.forward(hi) 
                dave.end_fill()
        
        #######################################################################
        # Function to draw axes for plot and axis titles ######################
        #######################################################################
        def draw_axis(all_range_span_m,
                      x,
                      y,
                      figure_width_pix,
                      x_axis_width,
                      y_axis_width,
                      x_axis_title_1,
                      x_axis_title_2,
                      y_axis_title_1,
                      y_axis_title_2,
                      y_axis_col = "black",
                      x_axis_col= "black",
                      x_title_col = "black",
                      y_title_col = "black"):
            
            ###################################################################
            global x_y_cross

            ###################################################################
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(y_axis_width)
            dave.penup() 
            dave.setpos(x,y)
            dave.pencolor(y_axis_col)
            dave.pendown() 
            dave.setheading(270)
            dave.forward(all_range_span_m + (pixels_mm* border))
            
            x_y_cross = dave.pos()
            
            dave.setheading(360)
            dave.pencolor(x_axis_col)
            dave.pensize(x_axis_width)
            dave.forward(figure_width_pix + (pixels_mm* border))
            dave.penup() 
            dave.setheading(180)
            dave.forward((figure_width_pix + (pixels_mm* border))/2)
            dave.setheading(0)
            dave.forward(x_title_h_adjust*pixels_mm)
            dave.setheading(90)
            dave.forward(x_title_v_adjust*pixels_mm)
            dave.pendown()
            dave.pencolor(x_title_col)
            
            ###################################################################
            if x_axis_title_on_off == "on":
                if x_axis_title_1 != "nan" and \
                   x_axis_title_1.replace(" ,","") != "":
                       
                    if x_axis_title_2 != "nan" and \
                       x_axis_title_2.replace(" ,","") != "":
                           
                        dave.write(f"{x_axis_title_1}\n{x_axis_title_2}",
                                    move=False,
                                    align="center",
                                    font=("Arial",
                                          x_axis_t_font_size,
                                          x_axis_t_style)) 
                    else:
                        dave.write(f"{x_axis_title_1}",
                                    move=False,
                                    align="center",
                                    font=("Arial",
                                          x_axis_t_font_size,
                                          x_axis_t_style)) 
            
            ###################################################################
            dave.penup() 
            dave.setpos(x,y)
            dave.setheading(270)
            dave.forward((all_range_span_m + (pixels_mm* border))/2)
            dave.setheading(90)
            dave.forward(y_title_v_adjust*pixels_mm)
            dave.setheading(0)
            dave.forward(y_title_h_adjust*pixels_mm)
            dave.pendown()
            dave.pencolor(y_title_col)
            
            ###################################################################
            if y_axis_title_on_off == "on":
                if y_axis_title_1 != "nan" and \
                   y_axis_title_1.replace(" ,","") != "":
                    if y_axis_title_2 != "nan" and \
                       y_axis_title_2.replace(" ,","") != "":
                           
                        dave.write(f"{y_axis_title_1}\n{y_axis_title_2}",
                                    move=False,
                                    align="center",
                                    font=("Arial",
                                          y_axis_t_font_size,
                                          y_axis_t_style)) 
                    else:
                        dave.write(f"{y_axis_title_1}",
                                    move=False,
                                    align="center",
                                    font=("Arial",
                                          y_axis_t_font_size,
                                          y_axis_t_style)) 
            dave.pencolor(x_title_col)
            dave.penup() 
            
            return x_y_cross
        
        #######################################################################
        # Function to add main title if required ##############################
        #######################################################################
        def add_title(x,
                      y,
                      main_title,
                      main_title_size,
                      main_title_style,
                       main_title_v_adj,
                      main_title_h_adj):
            
            dave.setpos(x,y)
            dave.penup()
            dave.setheading(0)
            dave.forward(main_title_h_adj*pixels_mm)
            dave.setheading(90)
            dave.forward(main_title_v_adj*pixels_mm)
            dave.pencolor(main_title_col)
            
            ###################################################################
            dave.write(main_title,
                        move=False,
                        align="left",
                        font=("Arial",
                              main_title_size,
                              main_title_style))

        #######################################################################
        #Function to draw Y major ticks and tick labels #######################
        #######################################################################
        def draw_y_maj (x,
                        y,
                        y_maj_ticks_str,
                        y_maj_tick_wid,
                        y_tick_lab_col = "black",
                        y_maj_tick_col = "black"):

            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.setpos(x,y)
            dave.penup()
            dave.pensize(y_maj_tick_wid)
            dave.setheading(180)
            dave.pendown()
            dave.pencolor(y_maj_tick_col)
            dave.forward(y_maj_tick_len*pixels_mm)
            dave.penup()
            dave.setheading(90)
            dave.forward(y_maj_tick_l_vertical_adjust*pixels_mm)
            dave.setheading(0)
            dave.forward(y_maj_tick_l_horiz_adjust*pixels_mm)
            dave.pendown()
            dave.pencolor(y_tick_lab_col)

            ###################################################################
            dave.write(y_maj_ticks_str,
                       move=False,
                       align="right",
                       font=("Arial", 
                              y_l_font_size, 
                              y_maj_l_style))
            
            ###################################################################
            dave.pencolor(y_tick_lab_col)
            dave.penup()
        
        #######################################################################
        # Function to draw Y minor ticks ######################################
        #######################################################################
        def draw_y_min (x,
                        y,
                        y_min_ticks_str,
                        y_min_tick_wid,
                        y_min_tick_col = "black"):
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.setpos(x,y)
            dave.penup()
            dave.pensize(y_min_tick_wid)
            dave.setheading(180)
            dave.pendown()
            dave.pencolor(y_min_tick_col)
            dave.forward(y_min_tick_len*pixels_mm)
            dave.penup()
            dave.setheading(270)
            dave.setheading(0)
            dave.penup()
        
        #######################################################################
        #Function to draw X major ticks and tick labels #######################
        #######################################################################
        def draw_x_maj (x,
                        y,
                        x_maj_ticks_str,
                        x_maj_tick_wid,
                        x_tick_lab_col = "black",
                        x_maj_tick_col = "black"):
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(x_maj_tick_wid)
            dave.penup() 
            dave.setpos(x,y)
            dave.pencolor("black")
            dave.setheading(0)
            dave.forward(pixels_mm*border)
            dave.pendown()
            dave.setheading(270)
            dave.pencolor(x_maj_tick_col)
            dave.forward(x_maj_tick_len*pixels_mm)
            dave.penup()
            dave.setheading(90)
            dave.forward(x_maj_tick_l_vertical_adjust*pixels_mm)
            dave.setheading(0)
            dave.forward(x_maj_tick_l_horiz_adjust*pixels_mm)
            dave.pendown()
            dave.pencolor(x_lab_col)
            
            ###################################################################
            dave.write(x_maj_ticks_str,
                       move=False,
                       align="right",
                       font=("Arial", 
                             x_l_font_size,
                             x_maj_l_style))
            
            ###################################################################
            dave.pencolor("black")
            dave.penup()
        
        #######################################################################
        # Function to draw X minor ticks ######################################
        #######################################################################
        def draw_x_min (x,
                        y,
                        x_min_tick_col = "black",
                        x_min_tick_wid = 1):
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x,y)
            dave.pencolor(x_min_tick_col)
            dave.setheading(0)
            dave.forward(pixels_mm*border)
            dave.pendown()
            dave.pensize(x_min_tick_wid)
            dave.setheading(270)
            dave.forward(x_min_tick_len*pixels_mm)
            dave.penup()
        
        #######################################################################
        # Function to draw legend key on figure with labels ###################
        #######################################################################
        def legend(x,
                   y,
                   leg_wid,
                   leg_height,
                   col,
                   label,
                   label_2,
                   legend_x,
                   legend_y,
                   tex_status,
                   tex_colour,
                   leg_sty,
                   leg_label_v_adj = 0,
                   leg_label_h_adj = 0,
                   legend_txt_col = "black"):
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x,y)
            dave.setheading(0)
            dave.forward(legend_x*pixels_mm)
            dave.setheading(90)
            dave.forward(legend_y*pixels_mm)
            dave.setheading(270)
            dave.pendown()
            dave.pencolor("black")
            
            ###################################################################
            #Error check colour entry
            try:
                dave.fillcolor(col)
            except:
                ge("Colour for troels smith")
                sys.exit()
            
            ###################################################################
            dave.begin_fill()
            dave.forward(leg_height) 
            dave.setheading(0)
            dave.forward(leg_wid)
            dave.setheading(90)
            dave.forward(leg_height)
            dave.setheading(180)
            dave.forward(leg_wid)
            dave.end_fill()
            dave.penup()
            
            temp_pos = dave.pos()
            
            ###################################################################        
            if label == "Argilla granosa**" or \
                label == "Argilla steatodes**":
                        
                if tex_status["Argilla steatodes tex**"] == "on":
                    dave.pencolor(tex_colour["Argilla steatodes tex**"])
                    

                if tex_status["Argilla granosa tex**"] == "on":
                    dave.pencolor(tex_colour["Argilla granosa tex**"])   

                if tex_status["Argilla steatodes tex**"] == "on" or \
                    tex_status["Argilla granosa tex**"] == "on":  
                        
                    dave.pensize(2)
                    dave.setheading(270)
                    dave.forward(leg_height*0.4)
                    dave.setheading(0)
                    dave.forward(leg_wid*0.5)
                    dave.pendown()
                    dave.setheading(270)
                    
                    dave.forward(leg_height*0.2)
                    dave.setheading(0)
                    dave.forward(leg_height*0.2)
                    dave.penup()
                
            ###############################################################
            if label == "Grana glareosa minora**" or \
                label == "Grana glareosa majora**":

                if tex_status["Grana glareosa minora tex**"] == "on":   
                    dave.pencolor(tex_colour["Grana glareosa minora tex**"])
                        
                if tex_status["Grana glareosa majora tex**"] == "on":  
                    dave.pencolor(tex_colour["Grana glareosa majora tex**"])
                    
                if tex_status["Grana glareosa minora tex**"] == "on" or \
                    tex_status["Grana glareosa majora tex**"] == "on":
                        
                    dave.pensize(1)
                    dave.setheading(270)
                    dave.forward(leg_height*0.6)
                    dave.setheading(0)
                    dave.forward(leg_wid*0.5)
                    dave.pendown()
                    
                    dave.circle((leg_wid/10))
                    dave.penup()
                
            ###############################################################    
            if label == "Grana arenosa**" or label == "Grana saburralia**":
                
                if tex_status["Grana arenosa tex**"] == "on":
                    dave.pencolor(tex_colour["Grana arenosa tex**"])
                    fill_col = tex_colour["Grana arenosa tex**"]
                    
                if tex_status["Grana saburralia tex**"] == "on":  
                    dave.pencolor(tex_colour["Grana saburralia tex**"])
                    fill_col = tex_colour["Grana saburralia tex**"]
                     
                if tex_status["Grana arenosa tex**"] == "on" or \
                    tex_status["Grana saburralia tex**"] == "on":

                    dave.pensize(1)
                    dave.setheading(270)
                    dave.forward(leg_height*0.6)
                    dave.setheading(0)
                    dave.forward(leg_wid*0.5)
                    dave.pendown()
                    
                    dave.begin_fill()
                    dave.fillcolor(fill_col)
                    
                    dave.circle(leg_wid/20)
                    dave.end_fill()
                    dave.penup()
        
            ###################################################################
            dave.setposition(temp_pos)   
            dave.pensize(1)    
            
            dave.setheading(0)
            dave.forward(leg_wid+5*pixels_mm)
            dave.setheading(270)
            dave.forward(leg_height/2)
            dave.setheading(90)
            dave.forward(leg_label_v_adj*pixels_mm)
            dave.setheading(0)
            dave.forward(leg_label_h_adj*pixels_mm)
            dave.pendown()
            dave.pencolor(legend_txt_col)
            
            ###################################################################
            if leg_sty == "italic":
                if label == "Unrecovered**":
                    style = ('Arial',legend_font_size,'normal')
                else:
                    style = ('Arial',legend_font_size,'italic')
            if leg_sty == "normal":
                style = ('Arial',legend_font_size)
            if leg_sty == "bold":
                style = ('Arial',legend_font_size,"bold")
                
            dave.write(label.replace("**",""),
                       move=False,
                       align="left",
                       font=(style))
            
            dave.penup()
            
        ####################################################################### 
        # Function to add legend title if required ############################
        #######################################################################
        def legend_titles(x,
                          y,
                          leg_title_on_off,
                          leg_title,
                          leg_title_size,
                          leg_title_sty,
                          leg_title_v_adj,
                          leg_title_h_adj,
                          legend_x,
                          legend_y,
                          legend_title_col = "black"):
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.pensize(1)
            dave.penup() 
            dave.setpos(x,y)
            dave.setheading(0)
            dave.forward(legend_x*pixels_mm)
            dave.setheading(90)
            dave.forward(legend_y*pixels_mm)

            ###################################################################
            if leg_title_on_off == "on":
                # dave.goto(title_initial)
                dave.setheading(0)
                dave.forward(leg_title_h_adj*pixels_mm)
                dave.setheading(90)
                dave.forward(leg_title_v_adj*pixels_mm)
                dave.pencolor(legend_title_col)
                dave.write(leg_title,
                           move=False,
                           align="left",
                           font=('Arial',
                                 leg_title_size,
                                 leg_title_sty))
            
        #######################################################################
        # Function to draw Y major tick grid lines if required ################
        #######################################################################
        def draw_y_maj_grid (x,y):
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.setpos(x,y)
            dave.penup()
            dave.pensize(y_grid_width)
            dave.pencolor(y_grid_col)
            dave.setheading(0)
            dave.pendown()
            figure_width_adjust = figure_width_mm + border+(wid_x*5)
            
            ###################################################################
            if grid_dash == "dashed":
                for dash in range(int((figure_width_adjust+y_grid_len_adj)/
                                       (y_grid_dash_length*2))):
                    dave.pendown()
                    dave.forward(pixels_mm*y_grid_dash_length)
                    dave.penup()
                    dave.forward(pixels_mm*y_grid_dash_length)        
            else:
                dave.forward(figure_width_adjust*pixels_mm)
                
            dave.penup()
        
        ####################################################################### 
        # Function for drawing lines joining top and/or base of each core if ## 
        # required ############################################################
        #######################################################################
        def join_line(x1,
                      y1,
                      x2,
                      y2,
                      join_col,
                      join_line_style,
                      join_line_width,
                      join_dash_length):
            
            x1= x1+shift
            x2= x2+shift
            
            dave.speed(f"{speed}")
            dave.hideturtle()
            dave.penup()
            dave.setpos(x1, y1)
            dave.pendown()
            dave.pencolor(join_col)
            dave.pensize(join_line_width)
            dave.setheading(dave.towards(x2, y2))
            dave.pensize(join_line_width)

            ###################################################################
            #if want dashed line
            if join_line_style == "dashed":
                for dash in range(1000):
                    dave.pendown()
                    dave.forward(pixels_mm*join_dash_length)
                    dave.penup()
                    dave.forward(pixels_mm*join_dash_length)
                    r = dave.pos() 
    
                    if r[0]-(pixels_mm*join_dash_length)\
                        < x2 < r[0]+(pixels_mm*join_dash_length)\
                        and r[1]-(pixels_mm*join_dash_length)\
                        < y2 < r[1]+(pixels_mm*join_dash_length):
                        break
                    
            ###################################################################        
            #if want solid line
            if join_line_style == "solid":
                dave.pendown()

            dave.setpos(x2, y2)
            
        #######################################################################
        # Run all required pre drawing functions for main parts of cores ######
        #######################################################################
        core_labels = colours.core_label("Core_number_label",
                                         "Core_label")
        
        data_colour = colours.data_colour("Core_number",
                                          "TS_description",
                                          colour_dict)
        
        data_name = colours.data_name("Core_number",
                                      "TS_description")
        
        data_vp_colour = colours.vp_colours("Core_number",
                                            "von_Post",
                                            colour_vp_dict)
        
        all_range_span_m = bb.all_range_span_m()
        each_core_range = bb.each_core_range()
        
        diff_from_max = bb.diff_from_max(all_range_span_m,
                                         figure_height_mm)
        geo = bb.geo_yn()
        
        #######################################################################
        other_all_diffs_cores = bb.data_diffs("Altitude_m_other",
                                              "Core_number_other",
                                              each_core_range,
                                              all_range_span_m,
                                              figure_height_mm)
        
        section_number_core_other = bb.section_number_core(other_all_diffs_cores)
        
        #######################################################################
        char_all_diffs_cores = bb.data_diffs("Altitude_m_charcoal",
                                             "Core_number_charcoal",
                                              each_core_range,
                                              all_range_span_m,
                                              figure_height_mm)
        
        section_number_core_char = bb.section_number_core(char_all_diffs_cores)
        
        #######################################################################
        all_diffs_cores = bb.data_diffs("Altitude_m",
                                        "Core_number",
                                         each_core_range,
                                         all_range_span_m,
                                         figure_height_mm)
        
        section_number_core = bb.section_number_core(all_diffs_cores)
        #######################################################################
        x_distance_m = bb.x_distance_m()
        
        #######################################################################
        #######################################################################
        # Draw out diagram ####################################################
        #######################################################################
        #######################################################################
        #work out pixels per m for entire distance
        x_ratio = figure_width_pix/max(x_distance_m)
        
        #######################################################################
        #determine the pixel distance on x for each core
        x_lens_adjust = [x*x_ratio for x in x_distance_m]
        
        shift = x_maj_shift*x_ratio
        
        #######################################################################
        #adjust this so 0 is the centre of the pixel range
        x_lens_adjust = [x-(figure_width_pix/2) for x in x_lens_adjust]
        
        x2_co = x_lens_adjust[0]
        y2_co = y_co
        
        #######################################################################
        #Determine x and y tick locations
        y_maj_axis_ticks = bb.y_maj_axis_ticks(figure_height_pix,
                                               y_maj_ticks)
        
        y_min_axis_ticks = bb.y_min_axis_ticks(figure_height_pix,
                                               y_min_ticks)

        x_maj_axis_ticks = bb.x_maj_axis_ticks(figure_width_pix,
                                               x_maj_ticks) 
        
        x_min_axis_ticks = bb.x_min_axis_ticks(figure_width_pix,
                                               x_min_ticks)
        
        if len(x_min_ticks) > len(x_min_axis_ticks):
            diff = len(x_min_ticks) - len(x_min_axis_ticks) 
            step = x_min_axis_ticks[1] - x_min_axis_ticks[0]
            
            for x in range(diff):
                x_min_axis_ticks.append(x_min_axis_ticks[-1]+step)

        #######################################################################
        # Draw X and Y axes without ticks #####################################
        #######################################################################
        draw_axis(figure_height_pix,
                  x_lens_adjust[0]-(pixels_mm* (border+(wid_x*3))),
                  y_co,
                  figure_width_pix+(pixels_mm* (border+(wid_x*3))),
                  y_axis_width,
                  x_axis_width,
                  x_axis_title_1,
                  x_axis_title_2,
                  y_axis_title_1,
                  y_axis_title_2,
                  y_axis_colour,
                  x_axis_colour,
                  x_title_col,
                  y_title_col)
        
        #######################################################################
        # Include main title if required ######################################
        #######################################################################
        if main_title_on_off ==  "on":
            add_title(x_lens_adjust[0]-(pixels_mm* (wid_x*3)),
                      y_co+wid,
                      main_title,
                      main_title_size,
                      main_title_style,
                      main_title_v_adj,
                      main_title_h_adj)
          
        #######################################################################
        # Draw Y minor ticks if required ######################################
        #######################################################################
        if options["y_minor_ticks_on_off**"] == "on":
            for i, (y_min_tick,y_min_ticks_str) \
                    in enumerate(zip(y_min_axis_ticks, y_min_ticks_strs)):
                
                draw_y_min(x_lens_adjust[0] - (pixels_mm*(border+(wid_x*3))),
                           y_co-y_min_tick,
                           y_min_ticks_str,
                           y_min_tick_wid,
                           y_min_tick_col)
                
        #######################################################################
        # Draw Y major ticks ##################################################
        #######################################################################
        for i, (y_maj_tick,y_maj_ticks_str) \
                in enumerate(zip(y_maj_axis_ticks,
                                 y_maj_ticks_strs)):
            
            draw_y_maj(x_lens_adjust[0] - (pixels_mm*(border+(wid_x*3))),
                       y_co-y_maj_tick,
                       y_maj_ticks_str,
                       y_maj_tick_wid,
                       y_tick_lab_col,
                       y_maj_tick_col)
                
        #######################################################################
        # Draw X minor ticks if required ######################################
        #######################################################################
        if options["x_minor_ticks_on_off**"] == "on":
            for i,x_minor_tick in enumerate(x_min_axis_ticks):
                draw_x_min(x_y_cross[0] + x_minor_tick+(wid*2),
                           x_y_cross[1],
                           x_min_tick_col,
                           x_min_tick_wid)
        
        #######################################################################
        # Draw X major ticks ##################################################
        #######################################################################
        for i,(x_major_tick,x_maj_ticks_str) in \
                                             enumerate(zip(x_maj_axis_ticks,
                                                           x_maj_ticks_strs)):
            
            draw_x_maj(x_y_cross[0] + x_major_tick+(wid*2),
                       x_y_cross[1],
                       x_maj_ticks_str,
                       x_maj_tick_wid,
                       x_lab_col,
                       x_maj_tick_col)
            
        #######################################################################
        # Create legend if required ###########################################
        #######################################################################
        if options["legend_on_off**"]  == "on":
            
            if use_alt_name == "on": 
            
                for i, ((key_1,col), (key_2,name)) in \
                        enumerate(zip(reversed(colour_dict.items()),
                        reversed(alt_name_dict.items()))):
                    legend(x_y_cross[0],
                           x_y_cross[1] + ((leg_section_height*pixels_mm)*i+1),
                           leg_section_width*pixels_mm,
                           leg_section_height*pixels_mm,  
                           col,
                           name,
                           key_2,
                           legend_x,
                           legend_y,
                           tex_dict_status,
                           tex_dict_colour,
                           legend_font_style,
                           leg_label_v_adjust,
                           leg_label_h_adjust,
                           legend_txt_col)
            else:
                for i, (key,col) in enumerate(reversed(colour_dict.items())):
                    legend(x_y_cross[0],
                           x_y_cross[1] + ((leg_section_height*pixels_mm)*i+1),
                           leg_section_width*pixels_mm,
                           leg_section_height*pixels_mm,  
                           col,
                           key,
                           key,
                           legend_x,
                           legend_y,
                           tex_dict_status,
                           tex_dict_colour,
                           legend_font_style,
                           leg_label_v_adjust,
                           leg_label_h_adjust,
                           legend_txt_col)
            
            ###################################################################
            #Add legend title if required #####################################
            ###################################################################
            if options["legend_on_off**"] == "on" and \
                options["legend_title_on_off"]  == "on":
                legend_titles(x_y_cross[0],
                              x_y_cross[1] + ((leg_section_height*pixels_mm)*
                                            (len(colour_dict)-1)),
                              legend_title_on_off,
                              legend_title,
                              legend_title_size,
                              legend_title_style,
                              legend_title_v_adjust,
                              legend_title_h_adjust,
                              legend_x,
                              legend_y,
                              legend_title_col)    
        
        #######################################################################
        #Draw von post legend if required #####################################
        #######################################################################
        if options["legend_on_off_vp**"]  == "on":
            for i, (key,col) in enumerate(colour_vp_dict_leg.items()):
                legend(x_y_cross[0],
                       x_y_cross[1] + ((leg_section_height_vp*pixels_mm)*i+1),
                       leg_section_width_vp*pixels_mm,
                       leg_section_height_vp*pixels_mm,  
                       col,
                       key,
                       key,
                       legend_x_vp,
                       legend_y_vp,
                       tex_dict_status,
                       tex_dict_colour,
                       legend_font_style_vp,
                       leg_label_v_adjust_vp,
                       leg_label_h_adjust_vp,
                       legend_txt_col_vp)
        
        #######################################################################
        # Add von post legend title if required ###############################
        #######################################################################
        if options["legend_on_off_vp**"]  == "on" and \
            options["legend_title_on_off_vp"]  == "on"  :
            legend_titles(x_y_cross[0],
                          x_y_cross[1] + ((leg_section_height_vp*pixels_mm)*9),
                          legend_title_on_off_vp,
                          legend_title_vp,
                          legend_title_size_vp,
                          legend_title_style_vp,
                          legend_title_v_adjust_vp,
                          legend_title_h_adjust_vp,
                          legend_x_vp,
                          legend_y_vp,
                          legend_title_col_vp)
        
        #######################################################################
        # Draw geology legend if required #####################################
        #######################################################################
        if options["legend_on_off_geo**"]  == "on":
            i = 0
            for k,v in col_rock_dict.items():
                
                ###############################################################    
                if k == "Coal**":
                    coal("black",
                         leg_section_width_geo*pixels_mm,
                         leg_section_height_geo*pixels_mm,
                         x_y_cross[0] + (legend_x_geo*pixels_mm),
                         x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                         geo_border_col,
                         colour_rock_dict_b["Coal**"],
                         colour_rock_dict_f["Coal**"],
                         "on") 
                    i+=1
                    
                ###############################################################    
                if k == "Limestone**":
                    lime_stone("black",
                               leg_section_width_geo*pixels_mm,
                               leg_section_height_geo*pixels_mm,
                               x_y_cross[0] + (legend_x_geo*pixels_mm),
                               x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                               geo_border_col,
                               colour_rock_dict_b["Limestone**"],
                               colour_rock_dict_f["Limestone**"],
                               "on")
                    i+=1
                
                ###############################################################
                if k == "Marl**":
                    marl("black",
                         leg_section_width_geo*pixels_mm,
                         leg_section_height_geo*pixels_mm,
                         x_y_cross[0] + (legend_x_geo*pixels_mm),
                         x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                         geo_border_col,
                         colour_rock_dict_b["Marl**"],
                         colour_rock_dict_f["Marl**"],
                         "on")
                    i+=1
                
                ###############################################################    
                if k == "Metamorphic**":
                    metamorphic("black",
                                leg_section_width_geo*pixels_mm,
                                leg_section_height_geo*pixels_mm,
                                x_y_cross[0] + (legend_x_geo*pixels_mm),
                                x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                     ((leg_section_height_geo*pixels_mm)*i)),
                                geo_border_col,
                                colour_rock_dict_b["Metamorphic**"],
                                colour_rock_dict_f["Metamorphic**"],
                                "on") 
                    i+=1

                ###############################################################
                if k == "Mudstone**":
                    mud_stone(leg_section_width_geo*pixels_mm,
                              leg_section_height_geo*pixels_mm,
                              x_y_cross[0] + (legend_x_geo*pixels_mm),
                              x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                              geo_border_col,
                              colour_rock_dict_b["Mudstone**"],
                              colour_rock_dict_f["Mudstone**"],
                              "on")
                    i+=1
                    
                ###############################################################
                if k == "Sandstone**":
                    sand_stone("black",
                               leg_section_width_geo*pixels_mm,
                               leg_section_height_geo*pixels_mm,
                               x_y_cross[0] + (legend_x_geo*pixels_mm),
                               x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                               geo_border_col,
                               colour_rock_dict_b["Sandstone**"],
                               colour_rock_dict_f["Sandstone**"],
                               "on")
                    i+=1
                    
                ###############################################################
                if k == "Shale**":
                    shale("black",
                          leg_section_width_geo*pixels_mm,
                          leg_section_height_geo*pixels_mm,
                          x_y_cross[0] + (legend_x_geo*pixels_mm),
                          x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                          geo_border_col,
                          colour_rock_dict_b["Shale**"],
                          colour_rock_dict_f["Shale**"],
                          "on")
                    i+=1
                    
                ###############################################################    
                if k == "Siltstone**":
                    silt_stone("black",
                               leg_section_width_geo*pixels_mm,
                               leg_section_height_geo*pixels_mm,
                               x_y_cross[0] + (legend_x_geo*pixels_mm),
                               x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                     ((leg_section_height_geo*pixels_mm)*i)),
                               geo_border_col,
                               colour_rock_dict_b["Siltstone**"],
                               colour_rock_dict_f["Siltstone**"],
                               "on")
                    i+=1

                ###############################################################
                if k == "Till**":
                    till("black",
                         leg_section_width_geo*pixels_mm,
                         leg_section_height_geo*pixels_mm,
                         x_y_cross[0] + (legend_x_geo*pixels_mm),
                         x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                         geo_border_col,
                         colour_rock_dict_b["Till**"],
                         colour_rock_dict_f["Till**"],
                         "on")
                    i+=1
                    
                ###############################################################
                if k == "Volcanic**":
                    volcanic(leg_section_width_geo*pixels_mm,
                             leg_section_height_geo*pixels_mm,
                             x_y_cross[0] + (legend_x_geo*pixels_mm),
                             x_y_cross[1] + ((legend_y_geo*pixels_mm) - 
                                    ((leg_section_height_geo*pixels_mm)*i)),
                             geo_border_col,
                             colour_rock_dict_b["Volcanic**"],
                             colour_rock_dict_f["Volcanic**"],
                             "on")
                    i+=1
                    
            ###################################################################
            # Add geology legend title if required ############################
            ###################################################################
            if legend_title_on_off_geo == "on":
                big_rect_leg_title(x_y_cross[0] + (legend_x_geo*pixels_mm),
                                   x_y_cross[1] + (legend_y_geo*pixels_mm),
                                   leg_section_height_geo*pixels_mm,
                                   legend_title_col_geo,
                                   legend_title_style_geo,
                                   legend_title_size_geo,
                                   legend_title_v_adjust_geo,
                                   legend_title_h_adjust_geo,
                                   legend_title_geo)
            
        #######################################################################
        # Create Y grid lines on major ticks if required ######################
        #######################################################################
        if options["y_grid_on_off**"] == "on":
            for i, y_maj_tick in enumerate(y_maj_axis_ticks):
                
                draw_y_maj_grid(x_lens_adjust[0] - \
                                (pixels_mm*(border+(wid_x*3))),
                                 y_co-y_maj_tick)
            
        #######################################################################
        # Draw out geology and TS sections on the main figure #################
        #######################################################################
        #Draw all the core rectangles for TS and Geo options
        for x in range(len(all_diffs_cores)):
            y2_co = y_co - (diff_from_max[x] * pixels_mm)
            for t in range(section_number_core[x]-1):
                
                ###############################################################
                # Draw out Troels Smith rectangles ############################
                ###############################################################
                if geo[x] [t] == "TS" or geo[x] [t] == "UR" or \
                    geo[x] [t] == "TS_all" :
                    if geo[x] [t] == "UR" or geo[x] [t] == "TS_all":
                        unrec = "yes"
                    else:
                        unrec = "no" 
                        
                    core_num = x   
                    
                    rectangle(data_name[x][t],
                              data_colour[x][t],
                              wid,
                              all_diffs_cores[x][t]*pixels_mm,
                              x_lens_adjust[x],
                              y2_co,
                              unrec,
                              t,
                              core_num,
                              core_labels)
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                # Draw geology sections if required ###########################
                ###############################################################
                if geo[x] [t] == "GEO_sandstone":
                    sand_stone("black",
                               wid,
                               all_diffs_cores[x][t]*pixels_mm,
                               x_lens_adjust[x],
                               y2_co,
                               geo_border_col,
                               colour_rock_dict_b["Sandstone**"],
                               colour_rock_dict_f["Sandstone**"],
                               "off")
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                    
                ###############################################################
                if geo[x] [t] == "GEO_siltstone":
                    silt_stone("black",
                               wid,
                               all_diffs_cores[x][t]*pixels_mm,
                               x_lens_adjust[x],
                               y2_co,
                               geo_border_col,
                               colour_rock_dict_b["Siltstone**"],
                               colour_rock_dict_f["Siltstone**"],
                               "off")
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_shale":
                    shale("black",
                          wid,
                          all_diffs_cores[x][t]*pixels_mm,
                          x_lens_adjust[x],
                          y2_co,
                          geo_border_col,
                          colour_rock_dict_b["Shale**"],
                          colour_rock_dict_f["Shale**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_mudstone":
                    mud_stone(wid,
                              all_diffs_cores[x][t]*pixels_mm,
                              x_lens_adjust[x],
                              y2_co,
                              geo_border_col,
                              colour_rock_dict_b["Mudstone**"],
                              colour_rock_dict_f["Mudstone**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_limestone":
                    lime_stone("black",
                               wid,
                               all_diffs_cores[x][t]*pixels_mm,
                               x_lens_adjust[x],
                               y2_co,
                               geo_border_col,
                               colour_rock_dict_b["Limestone**"],
                               colour_rock_dict_f["Limestone**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_marl":
                    marl("black",
                         wid,
                         all_diffs_cores[x][t]*pixels_mm,
                         x_lens_adjust[x],
                         y2_co,
                         geo_border_col,
                         colour_rock_dict_b["Marl**"],
                         colour_rock_dict_f["Marl**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_till":
                    till("black",
                         wid,
                         all_diffs_cores[x][t]*pixels_mm,
                         x_lens_adjust[x],
                         y2_co,
                         geo_border_col,
                         colour_rock_dict_b["Till**"],
                         colour_rock_dict_f["Till**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                    
                ###############################################################
                if geo[x] [t] == "GEO_volcanic":
                    volcanic(wid,
                             all_diffs_cores[x][t]*pixels_mm,
                             x_lens_adjust[x],
                             y2_co,
                             geo_border_col,
                             colour_rock_dict_b["Volcanic**"],
                             colour_rock_dict_f["Volcanic**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                
                ###############################################################
                if geo[x] [t] == "GEO_coal":
                    coal("black",
                          wid,
                          all_diffs_cores[x][t]*pixels_mm,
                          x_lens_adjust[x],
                          y2_co,
                          geo_border_col,
                          colour_rock_dict_b["Coal**"],
                          colour_rock_dict_f["Coal**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm 
                    
                ###############################################################
                if geo[x] [t] == "GEO_metamorphic":
                    metamorphic("black",
                                 wid,
                                 all_diffs_cores[x][t]*pixels_mm,
                                 x_lens_adjust[x],
                                 y2_co,
                                 geo_border_col,
                                 colour_rock_dict_b["Metamorphic**"],
                                 colour_rock_dict_f["Metamorphic**"])
                    
                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
                               
        #######################################################################
        # Draw upper join lines if required ###################################
        #######################################################################
        if options["surface_join_line_on_off**"] == "on":
            for x in range(len(all_diffs_cores)-1):
                y1 = y_co - (diff_from_max[x] * pixels_mm)
                y2 = y_co - (diff_from_max[x+1] * pixels_mm)
                
                join_line(x_lens_adjust[x] + wid,
                          y1,
                          x_lens_adjust[x+1] - (wid*3),
                          y2,
                          join_col_sur,
                          join_line_style_sur,
                          join_line_width_sur,
                          join_dash_length_sur)
            
        #######################################################################   
        # Draw lower join lines if required ###################################
        #######################################################################
        if options["base_join_line_on_off**"] == "on":
            for x in range(len(all_diffs_cores)-1):
                y1 = y_co - (diff_from_max[x] * pixels_mm)
                y2_prep = y_co - (diff_from_max[x+1] * pixels_mm)
                y1_prep_1 = sum(all_diffs_cores [x]) * pixels_mm
                
                try:
                    y2_prep_1 = sum(all_diffs_cores [x+1]) * pixels_mm
                    
                    join_line(int(x_lens_adjust[x] + wid),
                              int(y1 - y1_prep_1),
                              int(x_lens_adjust[x+1] - (wid*3)),
                              int(y2_prep - y2_prep_1))
                except:
                    all_diffs_cores [x+1] [-1] = 0
                    y2_prep_1 = sum(all_diffs_cores [x+1]) * pixels_mm
                    
                    join_line(int(x_lens_adjust[x] + wid),
                              int(y1 - y1_prep_1),
                              int(x_lens_adjust[x+1] - (wid*3)),
                              int(y2_prep - y2_prep_1),
                              join_col_base,
                              join_line_style_base,
                              join_line_width_base,
                              join_dash_length_base)

        #######################################################################
        # Create charcoal display if required #################################
        #######################################################################
        char_colour = colours.other_colour("Core_number_charcoal",
                                           "Charcoal",
                                           colour_other_dict)

        if options["charcoal_on_off**"] == "on":
            for x in range(len(char_all_diffs_cores)):
                y2_co = y_co - (diff_from_max[x]*pixels_mm)
                
                for t in range(section_number_core_char [x]-1): 
                    other(char_colour[x][t],
                          char_wid*pixels_mm,
                          char_all_diffs_cores[x][t]*pixels_mm,
                          x_lens_adjust[x]+((char_gap*pixels_mm)+wid),
                          y2_co,
                          char_line_colour)
                    
                    y2_co = y2_co - char_all_diffs_cores[x][t]*pixels_mm

        #######################################################################
        # Create 'other' display if required (phragmites or maybe wood) #######
        #######################################################################
        if options["other_on_off**"] == "on":
            other_colour = colours.other_colour("Core_number_other",
                                                "other",
                                                colour_other_dict)

            ###################################################################
            for x in range(len(other_all_diffs_cores)):
                y2_co = y_co - (diff_from_max[x]*pixels_mm)
               
                try:            
                    for t in range(section_number_core_char[x]-1): 
                        other(other_colour[x][t],
                              other_wid*pixels_mm,
                              other_all_diffs_cores[x][t]*pixels_mm,
                              x_lens_adjust[x]+((other_gap*pixels_mm)+wid),
                              y2_co,
                              line_colour_other)
                        y2_co = y2_co - other_all_diffs_cores[x][t]*pixels_mm
                except:
                    continue
                
        #######################################################################
        # Create von post column if required ##################################
        #######################################################################
        if options["vp_on_off**"] == "on":
            for x in range(len(all_diffs_cores)):
                y2_co = y_co - (diff_from_max[x]*pixels_mm)
                
                for t in range(section_number_core [x]-1): 
                    if data_vp_colour[x][t] == "none":
                        break
                    
                    other(data_vp_colour[x][t],
                          vp_wid*pixels_mm,
                          all_diffs_cores[x][t]*pixels_mm,
                          x_lens_adjust[x]+((vp_gap*pixels_mm)+wid),
                          y2_co,
                          border_colour)

                    y2_co = y2_co - all_diffs_cores[x][t]*pixels_mm
        
        #######################################################################
        # Update screen. Means not have to see the turtle draw out all the ####
        # figure and speeds up production #####################################   
        #######################################################################
        screen.update()

        #######################################################################
        # Save the output to an eps file that can then open in inkscape or ####
        # similar. Great results can be had if used on a big screen and take ##
        # a screen shot or with windows snip tool and then paste in to inkscape
        # can then save that as pdf or whatever. png and jpg options offered ##
        # here though #########################################################
        #######################################################################
        EpsImagePlugin.gs_windows_binary =  r"C:\Program Files\gs\gs10.05.0\bin\gswin64c"
        ts = dave.getscreen().getcanvas()
        ts = dave.getscreen().getcanvas()
        ts.postscript(file= f"{output}.eps")
        
        eps_image = Image.open(f"{output}.eps")
        eps_image.load(scale=4)
        try:
            if str(options["image_format**"]).lower().replace(" ","") == "png":
                eps_image.save(f"{output}.png")
            if str(options["image_format**"]).lower().replace(" ","") == "jpg":
                eps_image.save(f"{output}.jpg")
        except:
            pass

        #######################################################################
        #######################################################################
        print("     #############################################################")
        print("     #############################################################")
        print("     ############# Figure completed and exported. ################")
        print("     ###### Check, and if required and edit parameters in ########")
        print("     ############ parameter or data file and re run ##############")
        print("     #############################################################")
        print("     #############################################################")

###############################################################################
###############################################################################
def main():
    root = Tk()
    root.option_add('*Font', '12')
    bigfont = TkFont.Font(family="Arial",
                          size=8)
    root.option_add("*TCombobox*Listbox*Font",
                    bigfont)
    app = window_1(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################