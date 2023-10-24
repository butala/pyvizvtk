import logging

import vtk
import numpy as NP


def spherical_grid_spokes(r1,
                          r2,
                          N_theta,
                          N_phi):
    """
    """
    theta_vec = NP.linspace(0, NP.pi, N_theta + 1)[1:-1]
    phi_vec = NP.linspace(0, 2*NP.pi, N_phi, endpoint=False) + NP.pi / N_phi

    thetas, phis = NP.meshgrid(theta_vec, phi_vec)
    thetas = NP.concatenate(thetas)
    phis = NP.concatenate(phis)

    r1s = NP.full_like(thetas, r1)
    r2s = NP.full_like(thetas, r2)

    x1s = r1s * NP.sin(thetas) * NP.cos(phis)
    y1s = r1s * NP.sin(thetas) * NP.sin(phis)
    z1s = r1s * NP.cos(thetas)

    x2s = r2s * NP.sin(thetas) * NP.cos(phis)
    y2s = r2s * NP.sin(thetas) * NP.sin(phis)
    z2s = r2s * NP.cos(thetas)

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    for i, (x1, y1, z1, x2, y2, z2) in enumerate(zip(x1s, y1s, z1s,
                                                     x2s, y2s, z2s)):
        points.InsertNextPoint((x1, y1, z1))
        points.InsertNextPoint((x2, y2, z2))
        lines.InsertNextCell(2)
        lines.InsertCellPoint(2*i)
        lines.InsertCellPoint(2*i + 1)

    # vertical spokes
    points.InsertNextPoint((0, 0, r1))
    points.InsertNextPoint((0, 0, r2))
    points.InsertNextPoint((0, 0, -r1))
    points.InsertNextPoint((0, 0, -r2))
    lines.InsertNextCell(2)
    lines.InsertCellPoint(2*len(x1s))
    lines.InsertCellPoint(2*len(x1s) + 1)
    lines.InsertNextCell(2)
    lines.InsertCellPoint(2*len(x1s) + 2)
    lines.InsertCellPoint(2*len(x1s) + 3)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def spherical_grid_rings(r1,
                         r2,
                         N_r,
                         N_theta,
                         N_phi,
                         resolution=50):
    """
    """
    # circles with z normal
    r_vec = NP.linspace(r1, r2, N_r + 1)
    theta_vec = NP.linspace(0, NP.pi, N_theta, endpoint=False) + NP.pi / N_theta

    rs, thetas = NP.meshgrid(r_vec, theta_vec)
    rs = NP.concatenate(rs)
    thetas = NP.concatenate(thetas)

    x = rs * NP.sin(thetas)
    z = rs * NP.cos(thetas)

    apd = vtk.vtkAppendPolyData()
    for x_i, z_i in zip(x, z):
        arc = vtk.vtkArcSource()
        arc.UseNormalAndAngleOn()
        arc.SetPolarVector(x_i, 0, 0)
        arc.SetNormal(0, 0, 1)
        arc.SetAngle(360)
        arc.SetResolution(resolution)
        arc.Update()
        tf = vtk.vtkTransformPolyDataFilter()
        transform = vtk.vtkTransform()
        tf.SetInputConnection(arc.GetOutputPort())
        transform.Translate(0, 0, z_i)
        tf.SetTransform(transform)
        apd.AddInputConnection(tf.GetOutputPort())

    # circles rotated about z axis
    phi_vec = NP.linspace(0, 2*NP.pi, N_phi, endpoint=False) + NP.pi / N_phi

    rs, phis = NP.meshgrid(r_vec, phi_vec)
    rs = NP.concatenate(rs)
    phis = NP.concatenate(phis)

    for r_i, cos_phi_i, sin_phi_i in zip(rs, NP.cos(phis), NP.sin(phis)):
        arc = vtk.vtkArcSource()
        arc.UseNormalAndAngleOn()
        arc.SetPolarVector(0, 0, r_i)
        arc.SetNormal(sin_phi_i, cos_phi_i, 0)
        arc.SetAngle(180)
        arc.SetResolution(resolution)
        arc.Update()
        apd.AddInputConnection(arc.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(apd.GetOutputPort())
    rings_actor = vtk.vtkActor()
    rings_actor.SetMapper(mapper)
    return rings_actor


def spherical_grid_actor(r1,
                         r2,
                         N_r,
                         N_theta,
                         N_phi,
                         arc_resolution=50):

    """
    """
    spherical_grid = vtk.vtkAssembly()
    spherical_grid.AddPart(spherical_grid_spokes(r1, r2, N_theta, N_phi))
    spherical_grid.AddPart(spherical_grid_rings(r1, r2, N_r, N_theta, N_phi))
    return spherical_grid


def spherical_voxel_actor(r1,
                          r2,
                          theta1,
                          theta2,
                          phi1,
                          phi2,
                          N_r=10,
                          N_theta=10,
                          N_phi=10):
    """
    """
    if r1 > r2:
        r1, r2 = r2, r1
    if phi1 > phi2:
        phi1, phi2 = phi2, phi1
    if theta1 > theta2:
        theta1, theta2 = theta2, theta1

    # surface 1: r = r1
    phi_vec = NP.linspace(phi1, phi2, N_phi)
    theta_vec = NP.linspace(theta1, theta2, N_theta)

    phi, theta = NP.meshgrid(phi_vec, theta_vec)

    x_r = NP.sin(theta) * NP.cos(phi)
    y_r = NP.sin(theta) * NP.sin(phi)
    z_r = NP.cos(theta)

    points = vtk.vtkPoints()

    for x_r_i, y_r_i, z_r_i in zip(x_r.flat, y_r.flat, z_r.flat):
        p = (r1 * x_r_i,
             r1 * y_r_i,
             r1 * z_r_i)
        points.InsertNextPoint(p)

    quads = []

    I, J = phi.shape

    for i in range(I - 1):
        for j in range(J - 1):
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, i*N_phi + j)
            quad.GetPointIds().SetId(1, (i + 1)*N_phi + j)
            quad.GetPointIds().SetId(2, (i + 1)*N_phi + j + 1)
            quad.GetPointIds().SetId(3, i*N_phi + j + 1)
            quads.append(quad)

    # surface 2: r = r2
    for x_r_i, y_r_i, z_r_i in zip(x_r.flat, y_r.flat, z_r.flat):
        p = (r2 * x_r_i,
             r2 * y_r_i,
             r2 * z_r_i)
        points.InsertNextPoint(p)

    K = I * J

    for i in range(I - 1):
        for j in range(J - 1):
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, i*N_phi + j + K)
            quad.GetPointIds().SetId(3, i*N_phi + j + 1 + K)
            quad.GetPointIds().SetId(2, (i + 1)*N_phi + j + 1 + K)
            quad.GetPointIds().SetId(1, (i + 1)*N_phi + j + K)
            quads.append(quad)


    # surface 3: phi = phi1
    for i in range(N_theta - 1):
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, i*N_phi)
        quad.GetPointIds().SetId(1, i*N_phi + K)
        quad.GetPointIds().SetId(2, (i + 1)*N_phi + K)
        quad.GetPointIds().SetId(3, (i + 1)*N_phi)
        quads.append(quad)


    # surface 4: phi = phi2
    for i in range(N_theta - 1):
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, i*N_phi + N_phi - 1)
        quad.GetPointIds().SetId(1, (i + 1)*N_phi + N_phi - 1)
        quad.GetPointIds().SetId(2, (i + 1)*N_phi + K + N_phi - 1)
        quad.GetPointIds().SetId(3, i*N_phi + K + N_phi - 1)
        quads.append(quad)

    # surface 5: theta = theta2
    for j in range(N_phi - 1):
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, j)
        quad.GetPointIds().SetId(1, j + K)
        quad.GetPointIds().SetId(2, j + 1 + K)
        quad.GetPointIds().SetId(3, j + 1)
        quads.append(quad)

    # surface 6: theta = theta2
    for j in range(N_phi - 1):
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, j + N_phi * (N_theta - 1))
        quad.GetPointIds().SetId(1, j + 1 + N_phi * (N_theta - 1))
        quad.GetPointIds().SetId(2, j + 1 + K + N_phi * (N_theta - 1))
        quad.GetPointIds().SetId(3, j + K + N_phi * (N_theta - 1))
        quads.append(quad)

    # build unstructured grid
    voxel = vtk.vtkUnstructuredGrid()
    voxel.Allocate(len(quads), len(quads))
    for quad in quads:
        voxel.InsertNextCell(quad.GetCellType(),
                             quad.GetPointIds())
    voxel.SetPoints(points)
    voxel_mapper = vtk.vtkDataSetMapper()
    voxel_mapper.SetInputData(voxel)
    voxel_actor = vtk.vtkActor()
    voxel_actor.SetMapper(voxel_mapper)
    return voxel_actor


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    r1 = 2
    r2 = 5

    N_r = 3
    N_theta = 4
    N_phi = 5

    spherical_grid = spherical_grid_actor(r1, r2, N_r, N_theta, N_phi)

    from .viz import Renderer

    ren = Renderer(position_camera=False)

    ren.ren.AddActor(spherical_grid)


    r_vec = NP.linspace(r1, r2, N_r + 1)
    theta_vec = NP.linspace(0, NP.pi, N_theta, endpoint=False) + NP.pi / N_theta
    phi_vec = NP.linspace(0, 2*NP.pi, N_phi, endpoint=False) + NP.pi / N_phi

    I, J, K = 1, 1, 3

    r1 = r_vec[I]
    r2 = r_vec[I + 1]

    theta1 = theta_vec[J]
    theta2 = theta_vec[J + 1]

    phi1 = phi_vec[K]
    phi2 = phi_vec[K + 1]

    voxel = spherical_voxel_actor(r1,
                                  r2,
                                  theta1,
                                  theta2,
                                  phi1,
                                  phi2)

    voxel.GetProperty().SetOpacity(.5)
    voxel.GetProperty().SetColor(1, 0, 0)


    ren.ren.AddActor(voxel)

    # Axes
    axes = vtk.vtkAxesActor()
    transform = vtk.vtkTransform()
    transform.Translate(0.0, 0.0, 0.0)
    axes.SetUserTransform(transform)

    ren.ren.AddActor(axes)

    ren.camera.SetPosition(20, 20, 0)
    ren.camera.SetFocalPoint(0, 0, 0)
    ren.camera.SetViewUp(0, 0, 1)

    ren.start()
