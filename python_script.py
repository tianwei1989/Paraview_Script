'''
--------------------------------------------------------------------------------
File Brief: the python code in this file is designed to automate the post-processing
			of FFD results based on paraview. Some typical operations include: 
			1)load data files, 
			2)render active plottings, 
			3)cut one or more surfaces, 
			4)plot contour or vectors,or streamlines,
			5)save plottings
			6)extract data from a line
			7)save extracted data
			
Reference:  https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.html
			https://www.paraview.org/Wiki/ParaView_and_Python
			https://www.paraview.org/Wiki/images/f/f7/ParaViewTutorial51.pdf
			
Notes:	1)When running this file through Paraview by Tools->Python Shell, the working path
		  is NOT going to be the folder contains this file. It is critical to set the working 
		  path correctly to avoid errors.
		2)An alternative to bypass this issue is to run the file by directly launching the
		  python shell. It is necessary to put the directory of the shell into environment
		  path
		  
Author: Wei Tian, Wei.Tian@Schneider-Electric.com
Last Update: 7/18/2017

All Rights Reserved.
--------------------------------------------------------------------------------
'''
#load server manager and simple class from paraview
from paraview import servermanager
from paraview.simple import *
#load os in case of needing directory change
import os
#import sys to terminate the program
import sys
#change path to the folder
os.chdir("C:\Users/sesa461392/Desktop/Codes/FFD-C/Case-Studies/Energy-Balance-Study-CoarseGrid/Coarse-IM-CHEN/")
#print (os.getcwd())

#load the data file, in our case, is VTK.
#for other files, find compatible readers below:
#https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.LegacyVTKReader.html
My_Data = LegacyVTKReader(FileNames=["result.vtk"])

#make it visible
Show(My_Data)

#Cut a surfaces and customize it

#2-D plottings, like contour, vector, streamlines and save it

#extract data along a line

#render the active view
Render()

#make it hide
Hide(My_Data)

# hold the vtk gui
input()

#close paraview
try:
	sys.exit()
except:
	print ("cannot terminate the program")


