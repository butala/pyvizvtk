from itertools import repeat
from collections.abc import Iterable

import vtk

from .color import RED


def linear_path(xyz_list,
                color=RED,
                alpha=1):
    """
    """
    N = len(xyz_list)

    if not isinstance(color[0], Iterable):
        color = repeat(color, N)

    if not isinstance(alpha, Iterable):
        alpha = repeat(alpha, N)

    points = vtk.vtkPoints()
    for xyz in xyz_list:
        points.InsertNextPoint(xyz)

    lines = vtk.vtkCellArray()
    ids = list(range(N))
    for i, j in zip(ids[:-1], ids[1:]):
        lines.InsertNextCell(2)
        lines.InsertCellPoint(i)
        lines.InsertCellPoint(j)

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
    stn_xyz_m = (-2493283.706,    -4655240.239,  3565508.382)
    sat_xyz1_m = (-20507829.111,  -9658491.074, 13900101.870)
    sat_xyz2_m = (-23554289.507, -11952136.468,  3279494.183)

    stn_xyz_km = [x/1e3 for x in stn_xyz_m]
    sat_xyz1_km = [x/1e3 for x in sat_xyz1_m]
    sat_xyz2_km = [x/1e3 for x in sat_xyz2_m]

    xyz_km = [stn_xyz_km,
              sat_xyz1_km,
              sat_xyz2_km]

    actor = linear_path(xyz_km)

    from .viz import Renderer
    ren = Renderer()

    ren.ren.AddActor(actor)

    ren.start()
