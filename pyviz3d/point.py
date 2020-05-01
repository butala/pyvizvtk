from itertools import repeat
from collections import Iterable

import vtk

from .color import YELLOW


def point_actor(xyz,
                color=YELLOW,
                size=100,
                phi_resolution=10,
                theta_resolution=10,
                alpha=1):
    """
    ???
    """
    if not isinstance(xyz[0], Iterable):
        xyz = [xyz]

    N = len(xyz)

    if not isinstance(color[0], Iterable):
        color = repeat(color, N)

    if not isinstance(alpha, Iterable):
        alpha = repeat(alpha, N)

    points = vtk.vtkPoints()
    for xyz_i in xyz:
        points.InsertNextPoint(xyz_i)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(4)
    for color_i, alpha_i in zip(color, alpha):
        colors.InsertNextTuple4(color_i[0],
                                color_i[1],
                                color_i[2],
                                int(alpha_i * 255))
    polydata.GetPointData().SetScalars(colors)

    # create a sphere to use as a glyph source for vtkGlyph3D.
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(size)
    sphere.SetPhiResolution(phi_resolution)
    sphere.SetThetaResolution(theta_resolution)

    vertices = vtk.vtkGlyph3D()
    vertices.SetInputData(polydata)
    vertices.SetSourceConnection(sphere.GetOutputPort())
    vertices.SetColorModeToColorByScalar()
    vertices.ScalingOff()
    vertices.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertices.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetAmbient(1)
    actor.GetProperty().SetDiffuse(0)
    return actor


if __name__ == '__main__':
    stn_xyz_m = (-2493283.706,    -4655240.239,  3565508.382)
    sat_xyz1_m = (-20507829.111,  -9658491.074, 13900101.870)
    sat_xyz2_m = (-23554289.507, -11952136.468,  3279494.183)

    stn_xyz_km = [x/1e3 for x in stn_xyz_m]
    sat_xyz1_km = [x/1e3 for x in sat_xyz1_m]
    sat_xyz2_km = [x/1e3 for x in sat_xyz2_m]

    actor = point_actor(sat_xyz1_km)

    from .viz import Renderer
    ren = Renderer()

    ren.ren.AddActor(actor)

    ren.start()
