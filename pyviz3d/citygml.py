import vtk


def gml_actors(gml_fname, lod=1):
    """
    """
    reader = vtk.vtkCityGMLReader()
    reader.SetFileName(gml_fname)
    reader.SetLOD(lod)
    #reader.SetNumberOfBuildings(10)
    # print(reader.LOD)
    reader.Update()
    mb = reader.GetOutput()

    #print(reader.GetNumberOfBuildings())

    actors = []
    it = mb.NewIterator()
    #breakpoint()
    while not it.IsDoneWithTraversal():
        print('it')
        it.GoToNextItem()
        poly = it.GetCurrentDataObject()
        if poly:
            field_data = poly.GetFieldData()
            texture = field_data.GetAbstractArray('texture_uri')
            diffuse = field_data.GetAbstractArray('diffuse_color')

            #print(field_data.GetNumberOfArrays(), field_data.GetNumberOfComponents(), field_data.GetNumberOfTuples())
            for i in range(field_data.GetNumberOfArrays()):
                print(field_data.GetArrayName(i))

            scale = (1)
            transform = vtk.vtkTransform()
            transform.Scale(scale)

            transformFilter = vtk.vtkTransformPolyDataFilter()
            transformFilter.SetInputConnection(reader.GetOutputPort())
            transformFilter.SetTransform(transform)
            transformFilter.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(transformFilter.GetOutputPort())

            if diffuse:
                breakpoint()

                specular = poly.GetFieldData().GetAbstractArray('specular_color')
                transparency = poly.GetFieldData().GetAbstractArray('transparency')
                diffuseColor = [diffuse.GetValue(0),
                                diffuse.GetValue(1),
                                diffuse.GetValue(2)]
                mapper.SetDiffuse(diffuseColor)
                if specular:
                    specularColor = [specular.GetValue(0),
                                     specular.GetValue(1),
                                     specular.GetValue(2)]
                    mapper.SetSpecular(1.0)
                    mapper.SetSpecularColor(specularcolor)
                if transparency:
                    transparencyValue = transparency.GetValue(0)
                    mapper.SetOpacity(1 - transparencyValue)

            actors.append(vtk.vtkActor())
            actors[-1].SetMapper(mapper)
    return actors


if __name__ == '__main__':
    gml_fname = 'Part-4-Buildings-V4-one.gml'
    lod = 3

    # gml_fname = 'illinois-17019-000.gml'
    # lod = 1

    # gml_fname = 'DA1_3D_Buildings_Merged.gml'
    # lod = 2

    # gml_fname = 'lod1_3_f0_h3.gml'
    # lod = 1

    actors = gml_actors(gml_fname, lod=lod)
    print(len(actors))

    from pyviz3d.viz import Renderer

    ren = Renderer(earth=False,
                   position_camera=False,
                   size=(1920, 1200))

    # def dummyfunc1(obj, ev):
        # print('hmm')

    # iren.removeobservers('leftbuttonpressevent')
    # iren.addobserver('leftbuttonpressevent', dummyfunc1, 1.0)

    #ren.ren.resetcamera()
    # ren.ren.getactivecamera().azimuth(90)
    # ren.ren.getactivecamera().roll(-90)
    # ren.ren.getactivecamera().zoom(1.5)

    # ren.iren.removeobservers('leftbuttonpressevent')
    # ren.iren.addobserver('charevent', dummyfunc1, 1.0)
    # ren.iren.addobserver('leftbuttonpressevent', dummyfunc2, -1.0)

    # for actor in actors:
        # ren.ren.addactor(actor)

    # ren.camera.setposition(0, 0, 0)
    # ren.camera.setfocalpoint(0, 0, 0)
    # ren.camera.setviewup(0, 0, 1)

    def DummyFunc1(obj, ev):
        print("Before Event")
    ren.iren.AddObserver('CharEvent', DummyFunc1, 1.0)

    ren.start()
