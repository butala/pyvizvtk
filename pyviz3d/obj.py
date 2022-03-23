import vtk

def obj_actor(obj_fname):
    """
    """
    reader = vtk.vtkOBJReader()
    reader.SetFileName(obj_fname)
    reader.Update()

    poly = reader.GetOutput()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

if __name__ == '__main__':
    # obj_fname = 'LOD1_3_F0_H3.obj'

    # actor = obj_actor(obj_fname)

    # from pyviz3d.viz import Renderer

    # ren = Renderer(earth=False,
    #                position_camera=False,
    #                size=(1920, 1200))

    # ren.ren.AddActor(actor)

    # # ren = Renderer(size=(1920, 1200))

    # def print_camera_pos(obj, ev):
    #     if obj.GetKeySym() == 'u':
    #         print(f'position {ren.camera.GetPosition()}')
    #         print(f'focal point {ren.camera.GetFocalPoint()}')
    #         print(f'view up {ren.camera.GetViewUp()}')
    #         print(f'view angle {ren.camera.GetViewAngle()}')

    # #xren.iren.AddObserver('CharEvent', print_camera_pos, 1.0)

    # ren.camera.SetPosition(-120, -120, 40)
    # ren.camera.SetFocalPoint(0, 0, 0)
    # ren.camera.SetViewUp(0, 0, 1)
    # ren.camera.SetViewAngle(30)

    # ren.start()

    # background_color = [x/255 for x in [90, 195, 57]]
    background_color = [x/255 for x in [83, 118, 106]]

    # obj_fname1 = 'Illinois-17019_reprojected.obj'
    obj_fname1 = 'Illinois-17019-000.obj'
    obj_fname2 = 'Illinois-17019-001.obj'

    actor1 = obj_actor(obj_fname1)
    actor2 = obj_actor(obj_fname2)

    from pyviz3d.viz import Renderer

    ren = Renderer(earth=False,
                   position_camera=False,
                   background_color=background_color,
                   size=(1920, 1200))

    ren.ren.AddActor(actor1)
    ren.ren.AddActor(actor2)

    # ren = Renderer(size=(1920, 1200))

    def print_camera_pos(obj, ev):
        if obj.GetKeySym() == 'u':
            print(f'position {ren.camera.GetPosition()}')
            print(f'focal point {ren.camera.GetFocalPoint()}')
            print(f'view up {ren.camera.GetViewUp()}')
            print(f'view angle {ren.camera.GetViewAngle()}')

    ren.iren.AddObserver('CharEvent', print_camera_pos, 1.0)

    # ren.camera.SetPosition(-0.030683627516548656, -0.047074913237692965, -0.0402042774611398)
    # ren.camera.SetFocalPoint(-0.03068373213937447, -0.04707487112360915, -0.040204276247962)
    # ren.camera.SetViewUp(-0.15832216587013923, -0.41906993046262536, 0.8940438944348529)
    # ren.camera.SetViewAngle(30)

    # ren.camera.Zoom(10)

    # print(1/111319.488)

    scale = (1, 1, 1/111319.488)
    transform = vtk.vtkTransform()
    transform.Scale(scale)

    ren.camera.SetModelTransformMatrix(transform.GetMatrix())

    # State Farm Center
    pos_lat = 40.0962
    pos_lon = -88.2359

    # Newmark Civil Engineering Laboratory
    # pos_lat = 40.114177
    # pos_lon = -88.226498

    # 2015 s. andderson
    # pos_lat = 40.091892
    # pos_lon = -88.199813

    ren.camera.SetPosition(pos_lon, pos_lat ,1)
    ren.camera.SetFocalPoint(pos_lon, pos_lat, 0)

    # cam_x = 48008 / 2
    # cam_y = 37552 / 2
    # cam_z = 1e3

    # ren.camera.SetPosition(cam_x, cam_y, cam_z)
    # ren.camera.SetFocalPoint(cam_x, cam_y, 0)

    def set_camera_pos(obj, ev):
        if obj.GetKeySym() == 'p':
            # Newmark Civil Engineering Laboratory
            pos_lat = 40.114177
            pos_lon = -88.226498

            ren.camera.SetPosition(pos_lon, pos_lat ,1)
            ren.camera.SetFocalPoint(pos_lon, pos_lat, 0)
            ren.ren.ResetCameraClippingRange()
            ren.ren_win.Render()

    ren.iren.AddObserver('CharEvent', set_camera_pos, 1.0)


    ren.start()
