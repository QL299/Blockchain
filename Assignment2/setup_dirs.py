import os
import sys
import shutil

top_dir = "./database"

## Try to remove tree; if failed show an error using try...except on screen
if os.path.isdir(top_dir):
	try:
    		shutil.rmtree(top_dir)
	except OSError as e:
    		print ("Error deleting directory: %s - %s." % (e.filename, e.strerror))



## Create the top directory
try:  
    os.mkdir(top_dir)
except OSError:  
    print ("Failed to create the directory %s" % top_dir)
else:  
    print ("Successfully created the directory %s " % top_dir)


## Create directories for each of 6 nodes
for i in range(1, 7):
	path = top_dir + "/" + str(i)
	try:  
    		os.mkdir(path)
	except OSError:  
    		print ("Failed to create the directory %s" % path)
	else:  
   		 print ("Successfully created the directory %s " % path)
