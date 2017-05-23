import vtk

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

cube = vtk.vtkCubeSource()
cube.SetXLength(200)
cube.SetYLength(200)
cube.SetZLength(200)
cube.Update()
cm = vtk.vtkPolyDataMapper()
cm.SetInputConnection(cube.GetOutputPort())
ca = vtk.vtkActor()
ca.SetMapper(cm)

# assign actor to the renderer
ren.AddActor(ca)

axesActor = vtk.vtkAnnotatedCubeActor();
axesActor.SetXPlusFaceText('+X')
axesActor.SetXMinusFaceText('-X')
axesActor.SetYMinusFaceText('-Y')
axesActor.SetYPlusFaceText('+Y')
axesActor.SetZMinusFaceText('-Z')
axesActor.SetZPlusFaceText('+Z')
axesActor.GetTextEdgesProperty().SetColor(1,1,1)
axesActor.GetTextEdgesProperty().SetLineWidth(0.1)
axesActor.GetCubeProperty().SetColor(0.5,0.5,0.5)

axesActor.GetXPlusFaceProperty().SetColor(1,0,0)
axesActor.GetXMinusFaceProperty().SetColor(1,0,0)
axesActor.GetYPlusFaceProperty().SetColor(0,1,0)
axesActor.GetYMinusFaceProperty().SetColor(0,1,0)
axesActor.GetZPlusFaceProperty().SetColor(0,0,1)
axesActor.GetZMinusFaceProperty().SetColor(0,0,1)

# Call back function to resize the cone
def boxInteractionCallback(obj, event):
    print("TEST interaction callback")
    t = vtk.vtkTransform()
    obj.GetTransform(t)
    obj.GetProp3D().SetUserTransform( t )

# Call back function to resize the cone
def boxMouseCallback(obj, event):
    print("TEST mouse callback")

# consider vtkBoxWidget2
boxWidget = vtk.vtkBoxWidget()
boxWidget.DebugOn()
boxWidget.SetInteractor(iren)
# boxWidget.HandlesOff()
boxWidget.TranslationEnabledOff()
boxWidget.ScalingEnabledOff()
boxWidget.RotationEnabledOff()
boxWidget.SetProp3D(ca)
boxWidget.SetPlaceFactor( 1.25 )
boxWidget.PlaceWidget()
boxWidget.On()

boxWidget.PickingManagedOn()

# PROTECTED, but useful: boxWidget.HighlightFace(2)
#boxWidget.GetPlanes()

# Connect the event to a function
boxWidget.AddObserver("InteractionEvent", boxInteractionCallback)
boxWidget.AddObserver("LeftButtonPressEvent", boxMouseCallback, 999999.0)

axes = vtk.vtkOrientationMarkerWidget()
axes.SetOrientationMarker(axesActor)
axes.SetInteractor(iren)
axes.EnabledOn()
ren.ResetCamera()

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
