# -*- coding: utf-8 -*-

"""Functions here allow the building of the figure and its scaling as a whole
   and between cores vertically and laterally"""

###############################################################################
# Import required modules #####################################################
###############################################################################
import os as os
import numpy as np
import pandas as pd

###############################################################################
from PPSP_options import option_sort as oss

###############################################################################
# GET FILE NAME FROM OPTIONS FILE from options.csv ############################
###############################################################################
options = oss()
location = str(options["directory**"])

file_name = options["input_file_name**"]
os.chdir(location)

###############################################################################
# Function to get the highest altitudes from each core ie the upper most ###### 
# heights #####################################################################
###############################################################################
def geo_yn():
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        data_group = data.groupby("Core_number")
        
        geo_list = []
        
        #get maximum (top most height from each core and add to list)
        for name, group in data_group:
            ts_geo = [x for x in group["TS_geology_basal"]]
            geo_list.append(ts_geo)
        
    return geo_list

###############################################################################
# Function to get the range from the lowest to highest altitude from all the ##
# cores #######################################################################
###############################################################################
def all_range_span_m():
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        depth_list_min = data["Altitude_m"].min()
        depth_list_max = data["Altitude_m"].max()
        depth_list_range = depth_list_max - depth_list_min
    
    # return range in altitude
    return depth_list_range 

###############################################################################
# Function to obtain the range of altitude for each core location in metres ###
###############################################################################
def each_core_range():
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        column_number = data["Core_number"].max()
        
        #find range of depth for each core in metres
        data["RANGE"] = data.groupby("Core_number") ["Altitude_m"].\
                        transform(lambda x: x.max()-x.min())
        
        #create list of range of depth for each core
        core_ranges = []
        for x in range(int(column_number)):
            for c,d in zip(data["Core_number"],data["RANGE"]):
                if c == x+1:
                    core_ranges.append(d) 
                    break
    
    #return a list of range of altitude for each core
    return core_ranges

###############################################################################
# Function to determine the height in mm on screen from the highest point to ##
# the lowest point collectively for all cores provided ########################
###############################################################################
def diff_from_max(all_range_span_m,figure_height_mm):
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        data_group = data.groupby("Core_number")
        
        max_list = []
        
        #get maximum (top most height from each core and add to list)
        for name, group in data_group:
            max_group = group["Altitude_m"].max()
            max_list.append(max_group)
        
        #minus the highest altititude from all others so get difference
        #from all of the cores maximums
        max_diff = [((x-max(max_list))*-1) if x !=0 else 0
                    for x in max_list]

        #percentage of the difference to the entire range of altitudes*
        #by the figure height in mm. Gives the mm diference on screen 
        #from the top most core altitude
        max_diff = [(x/all_range_span_m)*figure_height_mm
                    for x in max_diff] 
       
    return max_diff

###############################################################################
# Fuction to get the distances between each core provided #####################
###############################################################################
def x_distance_m ():
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        x_distance = []
        e = data.groupby("Core_number")

        for name, group in e:
            x_distance.append(float(group["Location_m"].unique()))
        
        x_distance = [x - x_distance[0] for x in x_distance]

    return x_distance

###############################################################################
# Function to determine number of sections in each core #######################
###############################################################################
def section_number_core (cores):
    number_of_sections = []
    for element in cores:
        section = len(element)
        number_of_sections.append(section)
       
    return number_of_sections

###############################################################################
# Function to obtain the correct distance in pixels for each section of the ###
# cores #######################################################################
###############################################################################   
def data_diffs(column_name,
               core_column, 
               each_core_range, 
               all_range_span_m,
               figure_height_mm):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        column_number = data[f"{core_column}"].max()
        
        #determin differences in altitude between each section in all 
        #cores
        data["DIFF"] = data.groupby(f"{core_column}") \
                       [f"{column_name}"].diff().fillna(0)

        data["DIFF"] = data["DIFF"].shift(-1).fillna(np.nan)
        
        all_diffs = []
        
        #######################################################################
        # For each core convert the section differences in altitude into ######
        # distance in pixels for the screen ###################################
        #######################################################################
        for x in range(int(column_number)):
            core_diffs = []
            
            for core, section_diff in zip(data[f"{core_column}"],
                                          data["DIFF"]):
                if core == x+1:
                    core_fig_height_mm = figure_height_mm * \
                                         (each_core_range[x] /
                                          all_range_span_m)
                    
                    section_core_ratio = section_diff/each_core_range[x]                            
                                                
                    core_diffs.append((core_fig_height_mm * 
                                       section_core_ratio)*-1)
            all_diffs.append(core_diffs)   

    return all_diffs  

###############################################################################
# Function to establish pixel distances for Y major ticks #####################
###############################################################################
def y_maj_axis_ticks(figure_height_pix,
                     y_maj_ticks):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        depth_list_min = data["Altitude_m"].min()
        depth_list_max = data["Altitude_m"].max() 

    alts = np.arange(depth_list_min,depth_list_max,0.001)

    pixels_per_cm_alt =  figure_height_pix/(len(alts)-1)
    
    pixels = list(np.flip(np.round(np.arange(0,
                                             figure_height_pix,
                                             pixels_per_cm_alt),0)))

    if len(alts) > len(pixels):    
        pixels.insert(0, figure_height_pix)
    
    y_axis_pix_data = pd.DataFrame({"ALTS":alts,
                                    "Pixels":pixels})
    
    pixels_for_y_maj = []
    
    for y_tick in y_maj_ticks:
        
        for alts, pix in zip(y_axis_pix_data["ALTS"],
                              y_axis_pix_data["Pixels"]):
            
            if alts-0.01 < y_tick < alts+0.01:
                pixels_for_y_maj.append(pix)
                break   

    return pixels_for_y_maj

###############################################################################
# Function to establish pixel distances for Y minor ticks #####################
###############################################################################
def y_min_axis_ticks(figure_height_pix,
                     y_min_ticks):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        depth_list_min = data["Altitude_m"].min()
        depth_list_max = data["Altitude_m"].max() 
        
    alts = np.arange(depth_list_min,
                     depth_list_max,
                     0.001)

    pixels_per_cm_alt =  figure_height_pix/(len(alts)-1)
    
    pixels = list(np.flip(np.round(np.arange(0,
                                             figure_height_pix,
                                             pixels_per_cm_alt),0)))
    
    if len(alts) > len(pixels):    
        pixels.insert(0, figure_height_pix)
    
    y_axis_pix_data = pd.DataFrame({"ALTS":alts,
                                    "Pixels":pixels})
    
    pixels_for_y_min = []
    
    for y_tick in y_min_ticks:
        for alts, pix in zip(y_axis_pix_data["ALTS"],
                              y_axis_pix_data["Pixels"]):
            if alts-0.01 < y_tick < alts+0.01:
                pixels_for_y_min.append(pix)
                break  
            
    return pixels_for_y_min

###############################################################################
# Function to establish pixel distances for x major ticks #####################
###############################################################################
def x_maj_axis_ticks(figure_width_pix, x_maj_ticks):
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        dis_list = data["Location_m"]
        dis_list = [x - dis_list[0] for x in dis_list]

        
        dis_list_min = min(dis_list)
        dis_list_max = max(dis_list) 
        
    distances = np.arange(dis_list_min,  
                          dis_list_max,
                          0.001)

    pixels_per_cm_dis = figure_width_pix/(len(distances)-1)
    
    pixels = list(np.round(np.arange(0,figure_width_pix,
                                     pixels_per_cm_dis),0))
    
    if len(distances) > len(pixels):    
        pixels.append(figure_width_pix)
    
    x_axis_pix_data = pd.DataFrame({"Distances":distances,
                                    "Pixels":pixels})

    pixels_for_x_maj = []
    
    for x_tick in x_maj_ticks:
        for distance, pix in zip(x_axis_pix_data["Distances"],
                              x_axis_pix_data["Pixels"]):
            if distance-0.01 < x_tick < distance+0.01:
                pixels_for_x_maj.append(pix)
                break

    return pixels_for_x_maj

###############################################################################
# Function to establish pixel distances for Y major ticks #####################
###############################################################################
def x_min_axis_ticks(figure_width_pix,
                     x_min_ticks):
    
    with open (f"{file_name}.csv") as file:
        data = pd.read_csv(file)
        dis_list = data["Location_m"]
        dis_list = [x - dis_list[0] for x in dis_list]

        
        dis_list_min = min(dis_list)
        dis_list_max = max(dis_list) 

        
        
    distances = np.arange(dis_list_min,  
                          dis_list_max,
                          0.001)

    pixels_per_cm_dis = figure_width_pix/(len(distances)-1)
    
    pixels = list(np.round(np.arange(0,figure_width_pix,
                                     pixels_per_cm_dis),0))
    
    if len(distances) > len(pixels):    
        pixels.append(figure_width_pix)
    
    x_axis_pix_data = pd.DataFrame({"Distances":distances,
                                    "Pixels":pixels})
    
    pixels_for_x_min = []
    x_min_ticks
    x_axis_pix_data_dis_arr = np.array(x_axis_pix_data["Distances"])
    x_axis_pix_data_pix_arr = np.array(x_axis_pix_data["Pixels"])
    for x_tick in x_min_ticks:
        for distance, pix in zip(x_axis_pix_data_dis_arr,
                                 x_axis_pix_data_pix_arr):
            if distance-0.01 < x_tick < distance+0.01:
                pixels_for_x_min.append(pix)
                break

    return pixels_for_x_min

###############################################################################
###############################################################################
###############################################################################
###############################################################################
