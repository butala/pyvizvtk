import vtk

from .earth import WGS84, earth_actor


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

    def reset_camera(self):
        """
        """
        self.ren.ResetCamera()

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
