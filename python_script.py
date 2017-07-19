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
os.chdir("C:/Users/sesa461392/Desktop/Codes/Paraview-Script")
print (os.getcwd())

#############################################################
# function brief: cut a surface, a set up the view direction
# Reference: http://public.kitware.com/pipermail/paraview/2014-September/032160.html
# Last Update: 7/19/2017
#############################################################
def slice(object,origin,normal):
	slice = Slice(Input = object)
	slice.SliceType = 'Plane'
	slice.SliceOffsetValues = [0.0]
	slice.SliceType.Origin = origin
	slice.SliceType.Normal = normal
	#unclick the check box
	Hide3DWidgets(proxy=slice.SliceType)

	#set view direction
	view = GetActiveView()
	if not view:
    # When using the ParaView UI, the View will be present, not otherwise.
		view = CreateRenderView()
	view.CameraViewUp = [0, 0, 1]
	view.CameraFocalPoint = [0.5, 0.5, 0.5]
	view.CameraPosition = [0.5, -3, 0.5]
	view.CameraViewAngle = 45
	Show()
	Render()
	return slice
	
def plane_plot(object):
	pass

#############################################################
# save_plot: save the screen shot
# Reference: https://www.paraview.org/Wiki/ParaView/Python/Screenshot
# Last Update: 7/19/2017
#############################################################
def save_plot(object):
	#position camera
	view = GetActiveView()

	#draw the object
	Show()
	#set the background color
	view.Background = [1,1,1]  #white
	#set image size
	view.ViewSize = [200, 300] #[width, height]
	dp = GetDisplayProperties()
	#set point color
	dp.AmbientColor = [1, 0, 0] #red
	#set surface color
	dp.DiffuseColor = [0, 1, 0] #blue
	#set point size
	dp.PointSize = 2
	#set representation
	dp.Representation = "Surface"
	Render()
	#save screenshot
	WriteImage("test.png")





#load the data file, in our case, is VTK.
#for other files, find compatible readers below:
#https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.LegacyVTKReader.html
My_Data = LegacyVTKReader(FileNames=["result.vtk"])

#make it visible
Show(My_Data)

#Cut a surfaces and customize it
origin = [0.5, 0.5, 0.5]
normal = [0.0, 1.0, 0.0]
slice (My_Data,origin, normal)
#2-D plottings, like contour, vector, streamlines and save it

#extract data along a line

#render the active view
Render()

#make it hide
Hide(My_Data)

# hold the vtk gui
#input()

