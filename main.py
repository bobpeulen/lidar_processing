#%%writefile main.py
import glob
import pylas 
import numpy as np
import laspy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import ocifs


#create local folder
path_input_locally = "./input_files/" 

try:       
    if not os.path.exists(path_input_locally):         
        os.makedirs(path_input_locally)    

except OSError: 
    print ('Error: Creating directory files ocally')

    
path_output_locally = "./output_files/" 

try:       
    if not os.path.exists(path_output_locally):         
        os.makedirs(path_output_locally)    

except OSError: 
    print ('Error: Creating directory files ocally')


#get files from bucket and store locally

def get_files_from_input_bucket(full_input_bucket):
        
    #get the files from the bucket and store locally
    fs = ocifs.OCIFileSystem()
    
    #invalidate cache
    fs.invalidate_cache(full_input_bucket)
    
    #copy files
    all_files_in_bucket = fs.ls(full_input_bucket) #all files, including files that are not selected to run in experiment
    print(all_files_in_bucket)
    
    #fetch files
    fs.get(full_input_bucket, path_input_locally, recursive=True, refresh=True)  #store files in the bucket in "./" in Job Block storage
    
    return all_files_in_bucket

#call function
all_files_in_bucket = get_files_from_input_bucket("oci://West_BP@frqap2zhtzbe/lidar_data/")

#get file names only
file_list = glob.glob(path_input_locally + "*.las")

loopx = 1

#### read files and convert file file
for file in file_list:
    
    file_name = file
    file_output_name = file
    
    print()
    print("----------------------")
    print("file name " + file_name)
    print("file output name, after conversion" + file_output_name)
    
    print("Convert " + file_name)
    
    #read and convert las to laz
    las = pylas.read(file_name)    
    las = pylas.convert(las)    
    las.write(file_output_name)
    
    # reading las file and copy points
    print("Read " + file_output_name)
    input_las = laspy.read(file_output_name)
    point_records = input_las.points.copy() 
    

    x_mask_g = np.array(point_records.X)
    y_mask_g = np.array(point_records.Y)
    z_mask_g = np.array(point_records.Z)

    x = x_mask_g[:90000]
    y = y_mask_g[:90000]
    z = z_mask_g[:90000]   

    fig_surf_g = plt.figure()
    ax = fig_surf_g.add_subplot(111, projection = '3d')
    ax.plot_trisurf(x, y, z)
    out_name = "./output_files/" + "file_" + str(loopx) + ".png"
    print("save image " + out_name)
    plt.savefig(out_name)
    
    loopx += 1
    print("----------------------")
