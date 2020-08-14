import os
import sys
import urllib.request
import urllib.parse
import logging
import posixpath
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from contextlib import closing

from tqdm import tqdm

logger = logging.getLogger('pyviz3d.blue_marble')


"""
From readme.pdf:

1.1 Map projection

The BMNG dataset is gridded at the following spatial resolutions: 15,
60 and 240 arc-seconds (500m, 2km, and 8km approximate spacing at the
equator). It uses a geographic (Plate Carr\'{e}e) projection, which is
based on an equal latitude-longitude grid spacing (not an equal area
projection!). The projection datum is WGS84.

1.5 Citation of the BMNG

R. St\:{o}ckli, E. Vermote, N. Saleous, R. Simmon and D. Herring
(2005). The Blue Marble Next Generation - A true color earth dataset
including seasonal dynamics from MODIS. Published by the NASA Earth
Observatory. Corresponding author: rstockli@climate.gsfc.nasa.gov
"""

"""
Note, files are for June.
"""
URL_MAP = {
    'low':    'http://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74368/world.topo.200406.3x5400x2700.png',
    'medium': 'http://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74368/world.topo.200406.3x21600x10800.png'
}


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    # See https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def fetch(path,
          resolution='medium',
          block_size=8192):
    """
    """
    try:
        url = URL_MAP[resolution]
    except IndexError:
        raise ValueError('resolution must be one of: {}'.format(' '.join(sorted(URL_MAP))))
    fname = posixpath.split(urllib.parse.urlparse(url).path)[1]
    local_fname = os.path.join(path, fname)
    if os.path.isfile(local_fname):
        logger.info('{} exists --- not downloading'.format(local_fname))
    else:
        logger.info('fetching {} and storing to {}'.format(url,
                                                           local_fname))
        with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
              desc=url.split('/')[-1]) as t:  # all optional kwargs
            urllib.request.urlretrieve(url, filename=local_fname,
                                       reporthook=t.update_to, data=None)
    return local_fname


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = ArgumentParser('Fetch Blue Marble image.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('path',
                        type=str,
                        help='path to store image file')
    parser.add_argument('--resolution',
                        '-r',
                        choices=sorted(URL_MAP),
                        default='low',
                        type=str,
                        help='resolution of image to download (low is 8 [km] and medium is 2 [km] at the equator)')
    args = parser.parse_args(argv[1:])

    fetch(args.path,
          resolution=args.resolution)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
