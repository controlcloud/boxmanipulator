import vtk
import numpy as np

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self,obj,event):
        clickPos = self.GetInteractor().GetEventPosition()
        ren = self.GetDefaultRenderer()
        cam = ren.GetActiveCamera()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, ren)

        # get the new
        self.NewPickedActor = picker.GetActor()
        # picker.GetPickPosition()

        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            # pos = np.array(self.NewPickedActor.GetProperty().GetPosition())
            pos = np.array(self.NewPickedActor.GetCenter())

            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            newPickColor = np.array(self.NewPickedActor.GetProperty().GetColor())
            self.NewPickedActor.GetProperty().SetColor(newPickColor * 1.25)
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)

            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor

            # this could be made smoother and could probably use the vtkRenderWindowInteractor
            cam.SetPosition(pos * 10.0)
            cam.SetFocalPoint(0.0,0.0,0.0)

            up = np.array([1.0,0.0,0.0])
            if (np.dot(pos,up) != 0.0):
                up = np.array([0.0,1.0,0.0])
            
            cam.SetViewUp(up)

        self.OnLeftButtonDown()
        return


# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

xPosPlane = vtk.vtkPlaneSource()
xNegPlane = vtk.vtkPlaneSource()
yPosPlane = vtk.vtkPlaneSource()
yNegPlane = vtk.vtkPlaneSource()
zPosPlane = vtk.vtkPlaneSource()
zNegPlane = vtk.vtkPlaneSource()

xPosPlane.SetCenter(0.5,0.0,0.0)
xNegPlane.SetCenter(-0.5,0.0,0.0)
yPosPlane.SetCenter(0.0,0.5,0.0)
yNegPlane.SetCenter(0.0,-0.5,0.0)
zPosPlane.SetCenter(0.0,0.0,0.5)
zNegPlane.SetCenter(0.0,0.0,-0.5)

xPosPlane.SetNormal(1.0,0.0,0.0)
xNegPlane.SetNormal(-1.0,0.0,0.0)
yPosPlane.SetNormal(0.0,1.0,0.0)
yNegPlane.SetNormal(0.0,-1.0,0.0)
zPosPlane.SetNormal(0.0,0.0,1.0)
zNegPlane.SetNormal(0.0,0.0,-1.0)

xPosM = vtk.vtkPolyDataMapper()
xNegM = vtk.vtkPolyDataMapper()
yPosM = vtk.vtkPolyDataMapper()
yNegM = vtk.vtkPolyDataMapper()
zPosM = vtk.vtkPolyDataMapper()
zNegM = vtk.vtkPolyDataMapper()

xPosM.SetInputConnection(xPosPlane.GetOutputPort())
xNegM.SetInputConnection(xNegPlane.GetOutputPort())
yPosM.SetInputConnection(yPosPlane.GetOutputPort())
yNegM.SetInputConnection(yNegPlane.GetOutputPort())
zPosM.SetInputConnection(zPosPlane.GetOutputPort())
zNegM.SetInputConnection(zNegPlane.GetOutputPort())

xPosA = vtk.vtkActor()
xNegA = vtk.vtkActor()
yPosA = vtk.vtkActor()
yNegA = vtk.vtkActor()
zPosA = vtk.vtkActor()
zNegA = vtk.vtkActor()

xPosA.GetProperty().SetColor(0.8,0.0,0.0)
xNegA.GetProperty().SetColor(0.8,0.0,0.0)
yPosA.GetProperty().SetColor(0.0,0.8,0.0)
yNegA.GetProperty().SetColor(0.0,0.8,0.0)
zPosA.GetProperty().SetColor(0.0,0.0,0.8)
zNegA.GetProperty().SetColor(0.0,0.0,0.8)

xPosA.SetMapper(xPosM)
xNegA.SetMapper(xNegM)
yPosA.SetMapper(yPosM)
yNegA.SetMapper(yNegM)
zPosA.SetMapper(zPosM)
zNegA.SetMapper(zNegM)

# assign actor to the renderer
ren.AddActor(xPosA)
ren.AddActor(xNegA)
ren.AddActor(yPosA)
ren.AddActor(yNegA)
ren.AddActor(zPosA)
ren.AddActor(zNegA)

axesActor = vtk.vtkAnnotatedCubeActor();
axesActor.SetXPlusFaceText('+X')
axesActor.SetXMinusFaceText('-X')
axesActor.SetYMinusFaceText('-Y')
axesActor.SetYPlusFaceText('+Y')
axesActor.SetZMinusFaceText('-Z')
axesActor.SetZPlusFaceText('+Z')
axesActor.GetTextEdgesProperty().SetColor(1,1,0)
axesActor.GetTextEdgesProperty().SetLineWidth(2)
axesActor.GetCubeProperty().SetColor(0,0,1)

axes = vtk.vtkOrientationMarkerWidget()
axes.SetOrientationMarker(axesActor)
axes.SetInteractor(iren)
axes.EnabledOn()
ren.ResetCamera()

# add the custom style
style = MouseInteractorHighLightActor()
style.SetDefaultRenderer(ren)
iren.SetInteractorStyle(style)

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
