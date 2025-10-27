import matplotlib.colors


def get_color(name):
    """
    """
    return tuple([int(x * 255) for x in matplotlib.colors.to_rgb(name)])
