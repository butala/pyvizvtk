import vtk
from vtk.util.numpy_support import numpy_to_vtk
import numpy as np
import matplotlib.pylab as plt


def cube_axes_actor(bounds,
                    camera,
                    axis1_color='Salmon',
                    axis2_color='PaleGreen',
                    axis3_color='LightSkyBlue',
                    fontsize=48):
    """
    """
    colors = vtk.vtkNamedColors()

    color1 = colors.GetColor3d(axis1_color)
    color2 = colors.GetColor3d(axis2_color)
    color3 = colors.GetColor3d(axis3_color)

    cube_axes_actor = vtk.vtkCubeAxesActor()
    cube_axes_actor.SetBounds(bounds)
    cube_axes_actor.SetCamera(camera)
    cube_axes_actor.GetTitleTextProperty(0).SetColor(color1)
    cube_axes_actor.GetTitleTextProperty(0).SetFontSize(fontsize)
    cube_axes_actor.GetLabelTextProperty(0).SetColor(color1)

    cube_axes_actor.GetTitleTextProperty(1).SetColor(color2)
    cube_axes_actor.GetTitleTextProperty(1).SetFontSize(fontsize)
    cube_axes_actor.GetLabelTextProperty(1).SetColor(color2)

    cube_axes_actor.GetTitleTextProperty(2).SetColor(color3)
    cube_axes_actor.GetTitleTextProperty(2).SetFontSize(fontsize)
    cube_axes_actor.GetLabelTextProperty(2).SetColor(color3)

    cube_axes_actor.DrawXGridlinesOn()
    cube_axes_actor.DrawYGridlinesOn()
    cube_axes_actor.DrawZGridlinesOn()
    cube_axes_actor.SetGridLineLocation(cube_axes_actor.VTK_GRID_LINES_FURTHEST)

    cube_axes_actor.XAxisMinorTickVisibilityOff()
    cube_axes_actor.YAxisMinorTickVisibilityOff()
    cube_axes_actor.ZAxisMinorTickVisibilityOff()

    cube_axes_actor.SetFlyModeToStaticEdges()

    return cube_axes_actor


def cmap2color_transfer_function(vmin=0, vmax=1, cmap='viridis'):
    """
    """
    cmap_colors = plt.get_cmap(cmap).colors

    color_tf = vtk.vtkColorTransferFunction()

    # the vectorized approach does not work --- there must be an issue
    # in how the vtk arrays are created
    # x = numpy_to_vtk(np.linspace(vmin, vmax, len(cmap_colors)))
    # color_tf.AddRGBPoints(x, numpy_to_vtk(cmap_colors))
    for x, color in zip(np.linspace(vmin, vmax, len(cmap_colors)), cmap_colors):
        color_tf.AddRGBPoint(x, color[0], color[1], color[2])
    return color_tf
