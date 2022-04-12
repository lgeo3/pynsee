
import pandas as pd
import math
from shapely.affinity import translate as trs
from shapely.affinity import rotate
from shapely.geometry import Point, LineString
import warnings
import sys
from shapely.errors import ShapelyDeprecationWarning

from pynsee.geodata._rescale_geom import _rescale_geom
from pynsee.geodata._get_center import _get_center
        
def zoom(self, 
        departement = ['75','92', '93','94'], #'91', '78', '77', '95'
        center = (-133583.39, 5971815.98),
        radius = 650000,
        angle = math.pi * (1 - 2.5 * 1/9),
        factor = 2):   
        
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)        
        df = self
        if all([x in df.columns for x in ['insee_dep', 'geometry']]):

            zoomDep = df[df['insee_dep'].isin(departement)].reset_index(drop=True)

            zoomDep = _rescale_geom(df = zoomDep, factor = factor)
            end = Point(center[0] + radius, center[1])
            line = LineString([center, end])

            line = rotate(line, angle, origin=center, use_radians=True)
            endPoint = Point(line.coords[1])
            center = _get_center(zoomDep)

            xoff = endPoint.coords.xy[0][0] - center[0] 
            yoff = endPoint.coords.xy[1][0] - center[1] 

            zoomDep['geometry'] = zoomDep['geometry'].apply(lambda x: trs(x, xoff=xoff, yoff=yoff))
            df = pd.concat([self, zoomDep]).reset_index(drop=True)         
        return df