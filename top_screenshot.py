# trace generated using paraview version 5.9.1
# you can generate your own by entering [Paraview] > [Tools] > [Start Trace] and then record the steps 
#### import the simple module from the paraview
from paraview.simple import *
import os

print("\n\t  \033[92m Starting plotting process \033[0m")

if len(sys.argv) < 2:
    print("Not enough arguments. \n\t Usage: python3 screenshot.py file.vti (optional: field value in mT)")
    sys.exit(1)

pwd = os.getcwd()
nameArg =  str(sys.argv[1])
#Removing the relative path
name = nameArg.split("/")[-1]
hampl = 0 if len(sys.argv) < 3 else 1
fullname = pwd + '/' + nameArg

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
print("\n\t  \033[92m Opening file \033[0m")

# create a new 'XML Image Data Reader'
m_relaxedvti = XMLImageDataReader(registrationName=nameArg, FileName=[fullname])
m_relaxedvti.CellArrayStatus = ['f000']

# Properties modified on m_relaxedvti
m_relaxedvti.TimeArray = 'None'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
m_relaxedvtiDisplay = Show(m_relaxedvti, renderView1, 'UniformGridRepresentation')
print("\n\t  \033[92m Tracing display \033[0m")
# trace defaults for the display properties.
m_relaxedvtiDisplay.Representation = 'Outline'
m_relaxedvtiDisplay.ColorArrayName = [None, '']
m_relaxedvtiDisplay.SelectTCoordArray = 'None'
m_relaxedvtiDisplay.SelectNormalArray = 'None'
m_relaxedvtiDisplay.SelectTangentArray = 'None'
m_relaxedvtiDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
m_relaxedvtiDisplay.SelectOrientationVectors = 'None'
m_relaxedvtiDisplay.ScaleFactor = 1.0000000000000002e-06
m_relaxedvtiDisplay.SelectScaleArray = 'None'
m_relaxedvtiDisplay.GlyphType = 'Arrow'
m_relaxedvtiDisplay.GlyphTableIndexArray = 'None'
m_relaxedvtiDisplay.GaussianRadius = 5.0000000000000004e-08
m_relaxedvtiDisplay.SetScaleArray = [None, '']
m_relaxedvtiDisplay.ScaleTransferFunction = 'PiecewiseFunction'
m_relaxedvtiDisplay.OpacityArray = [None, '']
m_relaxedvtiDisplay.OpacityTransferFunction = 'PiecewiseFunction'
m_relaxedvtiDisplay.DataAxesGrid = 'GridAxesRepresentation'
m_relaxedvtiDisplay.PolarAxes = 'PolarAxesRepresentation'
m_relaxedvtiDisplay.ScalarOpacityUnitDistance = 1.4142135659086292e-07
m_relaxedvtiDisplay.OpacityArrayName = ['CELLS', 'f000']
m_relaxedvtiDisplay.SliceFunction = 'Plane'

# init the 'Plane' selected for 'SliceFunction'
m_relaxedvtiDisplay.SliceFunction.Origin = [0.0, 0.0, 5e-10]

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

print("\n\t  \033[92m Setting colors \033[0m")

# set scalar coloring
ColorBy(m_relaxedvtiDisplay, ('CELLS', 'f000', 'X'))

# rescale color and/or opacity maps used to include current data range
m_relaxedvtiDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
m_relaxedvtiDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'f000'
f000LUT = GetColorTransferFunction('f000')
f000LUT.RescaleTransferFunction(-1, 1)

# get opacity transfer function/opacity map for 'f000'
f000PWF = GetOpacityTransferFunction('f000')

# change representation type
m_relaxedvtiDisplay.SetRepresentationType('Surface')

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(1430, 762)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 2.732100745380182e-05]
renderView1.CameraFocalPoint = [0.0, 0.0, 4.999999858590343e-10]
renderView1.CameraParallelScale = 7.071067650912947e-06

print("\n\t  \033[92m Saving image \033[0m")
nameWoExtension = name.split(".")[0] 

# save screenshot
SaveScreenshot(f'./fig_{nameWoExtension}_H{int(hampl):04d}.png', renderView1, ImageResolution=[1430, 762])

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1430, 762)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 2.732100745380182e-05]
renderView1.CameraFocalPoint = [0.0, 0.0, 4.999999858590343e-10]
renderView1.CameraParallelScale = 7.071067650912947e-06

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
