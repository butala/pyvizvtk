from __future__ import absolute_import

from collections import namedtuple

import vtk

from .config import CACHE_PATH
from .blue_marble import fetch


class Ellipsoid(namedtuple('Ellipsoid', 'a f_inv')):
    """
    a:     semi-major axis [m]
    f_inv: flattening factor inverse
    """
    pass


WGS84 = Ellipsoid(6378137.0,
                  298.257223563)


def earth_actor(theta_resolution=60,
                phi_resolution=60,
                cache_path=CACHE_PATH):
    """
    ???
    """
    source = vtk.vtkTexturedSphereSource()
    source.SetThetaResolution(60)
    source.SetPhiResolution(60)
    source.SetRadius(WGS84.a / 1e3)
    # read texture
    pngfile = fetch(cache_path,
                    resolution='low')
    reader = vtk.vtkPNGReader()
    reader.SetFileName(pngfile)
    # create texture object
    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    transform_texture = vtk.vtkTransformTextureCoords()
    transform_texture.SetInputConnection(source.GetOutputPort())
    transform_texture.SetPosition(0.5, 0, 0)
    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_texture.GetOutputPort())
    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
    # scale sphere
    transform = vtk.vtkTransform()
    transform.Scale(1, 1, (1 - 1/WGS84.f_inv))
    actor.SetUserTransform(transform)
    actor.GetProperty().SetAmbient(1)
    actor.GetProperty().SetDiffuse(0)
    return actor
