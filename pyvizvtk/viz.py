import vtk

from .earth import WGS84, earth_actor
from .util import cube_axes_actor


class Renderer:
    def __init__(self,
                 position_camera=True,
                 background_color=(0.3, 0.3, 0.3),
                 size=(1600, 1600)):
        """
        """
        # create a rendering window and renderer
        self.ren_win = vtk.vtkRenderWindow()
        self.ren = vtk.vtkRenderer()
        self.ren_win.AddRenderer(self.ren)
        # create a renderwindowinteractor and customize
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.ren_win)
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)
        # setup camera
        self.camera = vtk.vtkCamera()
        if position_camera:
            self.reset_camera()
        self.ren.SetActiveCamera(self.camera)
        # setup render window
        self.ren.SetBackground(*background_color)
        self.ren_win.SetSize(*size)

    def add_actor(self, actor):
        """
        """
        return self.ren.AddActor(actor)

    def remove_actor(self, actor):
        """
        """
        return self.ren.RemoveActor(actor)

    def add_volume(self, volume):
        """
        """
        return self.ren.AddVolume(volume)

    def remove_volume(self, volume):
        """
        """
        return self.ren.RemoveVolume(volume)

    def reset_camera(self):
        """
        """
        self.ren.ResetCamera()

    def axes_on(self, bounds):
        """
        """
        self._cube_axes_actor = cube_axes_actor(bounds, self.ren.GetActiveCamera())
        self.add_actor(self._cube_axes_actor)
        return self._cube_axes_actor

    def axes_off(self):
        """
        """
        try:
            self.ren.RemoveActor(self._cube_axes_actor)
        except NameError:
            pass

    def orientation_on(self, viewport=(0.8, 0, 1.0, 0.2)):
        """
        """
        self._om_axes = vtk.vtkAxesActor()
        self._om = vtk.vtkOrientationMarkerWidget()
        self._om.SetOrientationMarker(self._om_axes)
        # Position lower right in the viewport.
        self._om.SetViewport(*viewport)
        self._om.SetInteractor(self.iren)
        self._om.EnabledOn()
        self._om.InteractiveOn()

    def orientation_off(self):
        """
        """
        try:
            self._om.EnabledOff()
        except NameError:
            pass

    def colorbar(self, lut):
        """
        """
        self._scalar_bar = vtk.vtkScalarBarActor()
        self._scalar_bar.SetOrientationToHorizontal()
        self._scalar_bar.SetLookupTable(lut)

        self._scalar_bar_widget = vtk.vtkScalarBarWidget()
        self._scalar_bar_widget.SetInteractor(self.iren)
        self._scalar_bar_widget.SetScalarBarActor(self._scalar_bar)
        self._scalar_bar_widget.On()
        return self._scalar_bar_widget

    def png(self, png_fname, scale=1):
        """
        """
        self.ren_win.Render()
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.ren_win)
        w2if.SetScale(scale)
        # w2if.SetInputBufferTypeToRGBA()
        w2if.SetInputBufferTypeToRGB()
        w2if.ReadFrontBufferOff()
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(png_fname)
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()
        return png_fname

    def depth_peeling_setup(self):
        """
        https://gitlab.kitware.com/vtk/vtk/-/issues/18135
        """
        self.ren.UseDepthPeelingOn()
        self.ren.UseDepthPeelingForVolumesOn()

    def start(self):
        """
        """
        self.iren.Initialize()
        self.ren_win.Render()
        self.iren.Start()


class EarthRenderer(Renderer):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.add_actor(earth_actor())

    def reset_camera(self):
        """
        """
        self.camera.SetPosition(5 * WGS84.a / 1e3, 0, 0)
        self.camera.SetClippingRange(1, 100 * WGS84.a / 1e3)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)


if __name__ == '__main__':
    ren = EarthRenderer()
    ren.start()
