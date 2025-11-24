import matplotlib.colors


def get_color(name):
    """
    """
    return tuple([x for x in matplotlib.colors.to_rgb(name)])
