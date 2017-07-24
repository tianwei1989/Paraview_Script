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
#print (os.getcwd())
class FFD_Postprocess(object):
	def __init__(self):
                #size of screenshot for saving plottings
		self.width = 936
		self.height = 813
		self.str_res = 200
		self.str_len = 2
		self.str_seed = [[0.0, 0.5, 0.0],[1.0, 0.5, 1.0]]
        #############################################################
        # function brief: set up the camera
        #############################################################
        def set_camera(self):
                view = GetActiveView()
                view.CameraViewUp = [0, 0, 1]
                view.CameraFocalPoint = [0.5, 0.5, 0.5]
                view.CameraPosition = [0.5, -2, 0.5]
                view.CameraViewAngle = 45
                
        #############################################################
        # function brief: plot contours of temperature and speed
        #############################################################
        def plot_contour(self, my_slice, VarNam):
                #get active view
                view = GetActiveViewOrCreate('RenderView')
                #select active pipeline
                SetActiveSource(my_slice)
                #show pipeline in the vew
                Show(my_slice,view)
                #get properties
                slice1Display = GetDisplayProperties(my_slice, view=view)
                #which contour: temperature or velicity
                ColorBy(slice1Display, ('POINTS', VarNam))
                #HideScalarBarIfNotNeeded(tLUT, view)
                #automatic mapping
                slice1Display.RescaleTransferFunctionToDataRange(True, False)
                #activate to show legend
                slice1Display.SetScalarBarVisibility(view, True)
                #show the legend
                vELLUT = GetColorTransferFunction(VarNam)
                #choose preset
                vELLUT.ApplyPreset('Blue to Red Rainbow', True)
                #set mounting position of the bar
                vELLUTColorBar = GetScalarBar(vELLUT, view)
                vELLUTColorBar.Position = [0.85, 0.25]
                #save plot
                self.save_plot(self.width,self.height,VarNam)
                #HideScalarBarIfNotNeeded(tLUT, view)
                #turn off the scalar bar for next plotting
                slice1Display.SetScalarBarVisibility(view, False)

        #############################################################
        # function brief: cut a surface, plot, save the plottings
        # Reference: http://public.kitware.com/pipermail/paraview/2014-September/032160.html
        #############################################################
        def cut_slice(self,threeD_object,origin,normal):
                '''
                Hide three D object
                '''
                view = GetActiveViewOrCreate('RenderView')
                threeD = GetActiveSource()
                Hide(threeD, view)
                        
                '''
                Setting camera
                '''
                
                self.set_camera()

                '''
                Slicing
                '''
                my_slice = Slice(Input = threeD_object)
                my_slice.SliceType = 'Plane'
                my_slice.SliceOffsetValues = [0.0]
                my_slice.SliceType.Origin = origin
                my_slice.SliceType.Normal = normal
                #unclick the check box
                Hide3DWidgets(proxy=my_slice.SliceType)

                '''
                Get properties of slice display
                '''
                slice1Display = GetDisplayProperties(my_slice, view=view)
                slice1Display.SetScalarBarVisibility(view, True)
                #enable axis view
                view.AxesGrid.Visibility = 1
                
                '''
                Start preparing for first plotting: T
                '''
                Plot_Variable = ["T","VEL"]
                for variable in Plot_Variable:
                        self.plot_contour(my_slice, variable)

                '''
                Hide current pipeline 
                '''
                Hide(my_slice, view)

                return my_slice

        #############################################################
        # function brief: draw velocity vector on a 2D plane
        #############################################################
        def plot_vector(object):
                pass

        #############################################################
        # function brief: draw streamline on a 2D plane
        #############################################################
        def plot_streamline(self,my_slice):
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
                streamTracer1.SeedType.Point1 = self.str_seed[0]
                streamTracer1.SeedType.Point2 = self.str_seed[1]
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
                # turn on "Surface Streamlines" check box
                streamTracer1.SurfaceStreamlines = 1
                
                #change length of the streamline
                streamTracer1.MaximumStreamlineLength = self.str_len
                
                #change the resolution
                streamTracer1.SeedType.Resolution = self.str_res
                
                '''
                Save the streamline
                '''
                self.save_plot(self.width,self.height,'Vel_Str')
                
        #############################################################
        # function brief: extract a line in a 2-D plane and save
        #                 data into a csv file
        #############################################################
        def extract_line(object):
                pass

        #############################################################
        # function brief: save the screen shot, i.e. contour, vector
        # Reference: https://www.paraview.org/Wiki/ParaView/Python/Screenshot
        #############################################################
        def save_plot(self,width, height, plot_name):
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
Note: other than a bug (interactive) mode, !=  should be replaced by ==
'''
if __name__ != "__main__":
	#############################################################
	#Main entrance of the script
	#Author: Wei Tian, Wei.Tian@Schneider-Electric.com
	#############################################################
	FFD = FFD_Postprocess()
	'''
	disable automatic camera reset on 'Show'
	'''
	paraview.simple._DisableFirstRenderCameraReset()

	'''
	load the data file, in our case, is VTK.
	for other files, find compatible readers below:
	https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.LegacyVTKReader.html
	'''
	FilNam = ["result.vtk"]
	My_Data = LegacyVTKReader(FileNames=FilNam)

	'''
	Display three D object
	'''
	Show(My_Data)

	'''
	Cut surface for contours
	'''
	origin = [0.5, 0.5, 0.5]
	normal = [0.0, 1.0, 0.0]
	slice_1 = FFD.cut_slice(My_Data,origin, normal)

	'''
	plot vectors
	'''

	'''
	plot streamlines
	'''
	FFD.plot_streamline(slice_1)

	'''
	extract data along a line
	'''


