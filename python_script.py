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
Last Update: 7/24/2017

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
# function brief: cut a surface, plot, save
# Reference: http://public.kitware.com/pipermail/paraview/2014-September/032160.html
#############################################################
def cut_slice(object,origin,normal):
        '''
        Hide three D object
        '''
        view = GetActiveViewOrCreate('RenderView')
	threeD = GetActiveSource()
	Hide(threeD, view)
	
        '''
        Setting slicing
        '''
	my_slice = Slice(Input = object)
	my_slice.SliceType = 'Plane'
	my_slice.SliceOffsetValues = [0.0]
	my_slice.SliceType.Origin = origin
	my_slice.SliceType.Normal = normal
	#unclick the check box
	Hide3DWidgets(proxy=my_slice.SliceType)

        '''
        Get current view
        '''

        slice1Display = GetDisplayProperties(my_slice, view=view)
	slice1Display.SetScalarBarVisibility(view, True)
	#enable axis view
	view.AxesGrid.Visibility = 1

        '''
        Setting camera
        '''
	view.CameraViewUp = [0, 0, 1]
	view.CameraFocalPoint = [0.5, 0.5, 0.5]
	view.CameraPosition = [0.5, -2, 0.5]
	view.CameraViewAngle = 45

        '''
        Start preparing for first plotting: T
        '''
        # get color transfer function/color map for 'T'
        tLUT = GetColorTransferFunction('T')
        tLUT.ApplyPreset('Blue to Red Rainbow', True)
        tLUTColorBar = GetScalarBar(tLUT, view)
        tLUTColorBar.Position = [0.85, 0.25]
        save_plot(936,813,'T')
        
        '''
        Start preparing for second plotting: Vel
        '''
        ColorBy(slice1Display, ('POINTS', 'VEL'))
        HideScalarBarIfNotNeeded(tLUT, view)
        slice1Display.RescaleTransferFunctionToDataRange(True, False)
        slice1Display.SetScalarBarVisibility(view, True)
        vELLUT = GetColorTransferFunction('VEL')
        vELLUT.ApplyPreset('Blue to Red Rainbow', True)
        vELLUTColorBar = GetScalarBar(vELLUT, view)
        vELLUTColorBar.Position = [0.85, 0.25]
        save_plot(936,813,'Vel')

        '''
        Hide current pipeline 
        '''
        Hide(my_slice, view)

	return my_slice

def plot_contour(object):
	pass

def plot_vector(object):
	pass

def plot_streamline(my_slice):
        '''
        Get active view
        '''
        view = GetActiveViewOrCreate('RenderView')

        '''
        Generate the streamline
        '''   
	streamTracer1 = StreamTracer(Input=my_slice,SeedType='High Resolution Line Source')
	SetActiveSource(streamTracer1)
        streamTracer1.Vectors = ['POINTS', 'velocity']
        # init the 'High Resolution Line Source' selected for 'SeedType'
        streamTracer1.SeedType.Point1 = [0.0, 0.5, 0.0]
        streamTracer1.SeedType.Point2 = [1.0, 0.5, 1.0]
        # hie the line
        Hide3DWidgets(proxy=streamTracer1.SeedType)

        '''
        Show the streamline
        '''   
        streamTracer1Display = Show(streamTracer1, view)
        ColorBy(streamTracer1Display, ('POINTS', 'VEL'))
        vELLUT = GetColorTransferFunction('VEL')
        HideScalarBarIfNotNeeded(vELLUT, view)
        streamTracer1Display.SetScalarBarVisibility(view, True)

        '''
        trace defaults for the display properties.
        '''
        streamTracer1Display.Representation = 'Surface'
        streamTracer1Display.ColorArrayName = ['POINTS', 'VEL']
        streamTracer1Display.LookupTable = vELLUT
        streamTracer1Display.OSPRayScaleArray = 'VEL'
        streamTracer1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        streamTracer1Display.SelectOrientationVectors = 'Normals'
        streamTracer1Display.ScaleFactor = 0.09995596805238166
        streamTracer1Display.SelectScaleArray = 'VEL'
        streamTracer1Display.GlyphType = 'Arrow'
        streamTracer1Display.PolarAxes = 'PolarAxesRepresentation'
        streamTracer1Display.GaussianRadius = 0.04997798402619083
        streamTracer1Display.SetScaleArray = ['POINTS', 'VEL']
        streamTracer1Display.ScaleTransferFunction = 'PiecewiseFunction'
        streamTracer1Display.OpacityArray = ['POINTS', 'VEL']
        streamTracer1Display.OpacityTransferFunction = 'PiecewiseFunction'
        '''
        Customize the streamline
        '''

        '''
        Save the streamline
        '''
        save_plot(936,813,'Vel_Str')
        
        

#############################################################
# function brief: extract a line in a two-D plane and save
#                 data into a csv file
#############################################################
def extract_line(object):
	pass

#############################################################
# save_plot: save the screen shot
# Reference: https://www.paraview.org/Wiki/ParaView/Python/Screenshot
# Last Update: 7/19/2017
#############################################################
def save_plot(width, height, plot_name):
	#position camera
	view = GetActiveView()
	#show the object
	Show()
	#set the background color
	#view.Background = [1,1,1]  #white
	#set image size
	view.ViewSize = [width, height] #[width, height]
	dp = GetDisplayProperties()
	#set representation
	dp.Representation = "Surface"
	Render()
	#save screenshot
	WriteImage(plot_name+".png")

'''
Main entrance of the script
Author: Wei Tian, Wei.Tian@Schneider-Electric.com
'''

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

#load the data file, in our case, is VTK.
#for other files, find compatible readers below:
#https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.LegacyVTKReader.html
FilNam = ["result.vtk"]
My_Data = LegacyVTKReader(FileNames=FilNam)

#make it visible
Show(My_Data)

#Cut a surfaces and draw contours
origin = [0.5, 0.5, 0.5]
normal = [0.0, 1.0, 0.0]
slice_1 = cut_slice(My_Data,origin, normal)

# plot vectors

# plot streamlines
plot_streamline(slice_1)
# extract data along a line

