import matplotlib.colors


def get_color(name):
    """
    """
    return tuple([int(x) for x in matplotlib.colors.to_rgb(name)])
