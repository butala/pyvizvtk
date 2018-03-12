from __future__ import absolute_import

import vtk

from .earth import WGS84, earth_actor


class Renderer(object):
    def __init__(self,
                 earth=True,
                 background_color=(0.3, 0.3, 0.3),
                 size=(800, 800)):
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
        self.reset_camera()
        self.ren.SetActiveCamera(self.camera)
        # setup render window
        self.ren.SetBackground(*background_color)
        self.ren_win.SetSize(*size)
        if earth:
            self.ren.AddActor(earth_actor())

    def reset_camera(self):
        """
        """
        self.camera.SetPosition(5 * WGS84.a / 1e3, 0, 0)
        self.camera.SetClippingRange(1, 100 * WGS84.a / 1e3)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, 1)

    def start(self):
        """
        """
        self.iren.Initialize()
        self.ren_win.Render()
        self.iren.Start()


if __name__ == '__main__':
    ren = Renderer()
    ren.start()
