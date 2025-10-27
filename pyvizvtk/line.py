import logging
from itertools import repeat
from collections.abc import Iterable

import vtk

from .color import get_color


def line_actor(xyz1,
               xyz2,
               color=get_color('cyan'),
               alpha=1):
    """
    ???
    """
    if isinstance(xyz1[0], Iterable):
        xyz1_id = list(range(len(xyz1)))
    else:
        xyz1 = [xyz1]
        xyz1_id = repeat(0)

    if isinstance(xyz2[0], Iterable):
        xyz2_id = list(range(len(xyz2)))
    else:
        xyz2 = [xyz2]
        xyz2_id = repeat(0)

    N = max(len(xyz1), len(xyz2))

    if not isinstance(color[0], Iterable):
        color = repeat(color, N)

    if not isinstance(alpha, Iterable):
        alpha = repeat(alpha, N)

    points = vtk.vtkPoints()
    for xyz1_i in xyz1:
        points.InsertNextPoint(xyz1_i)
    for xyz2_i in xyz2:
        points.InsertNextPoint(xyz2_i)

    lines = vtk.vtkCellArray()
    for i, j, _ in zip(xyz1_id, xyz2_id, range(N)):
        lines.InsertNextCell(2)
        lines.InsertCellPoint(i)
        lines.InsertCellPoint(len(xyz1) + j)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(4)
    for color_i, alpha_i in zip(color, alpha):
        colors.InsertNextTuple4(color_i[0],
                                color_i[1],
                                color_i[2],
                                int(alpha_i * 255))
        polydata.GetCellData().SetScalars(colors)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    stn_xyz_m = (-2493283.706,    -4655240.239,  3565508.382)
    sat_xyz1_m = (-20507829.111,  -9658491.074, 13900101.870)
    sat_xyz2_m = (-23554289.507, -11952136.468,  3279494.183)

    stn_xyz_km = [x/1e3 for x in stn_xyz_m]
    sat_xyz1_km = [x/1e3 for x in sat_xyz1_m]
    sat_xyz2_km = [x/1e3 for x in sat_xyz2_m]

    #actor = line_actor(stn_xyz_km, [sat_xyz1_km, sat_xyz2_km])
    actor = line_actor([sat_xyz1_km, sat_xyz2_km], stn_xyz_km)

    from .viz import EarthRenderer
    ren = EarthRenderer()

    ren.ren.AddActor(actor)

    ren.start()
