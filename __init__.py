# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DensityMap
                                 A QGIS plugin
 This plugin calculates 2D gaussian kernel density from a point layer
                             -------------------
        begin                : 2012-09-20
        copyright            : (C) 2012 by Flávio Codeco Coelho - Fundacão Getulio Vargas
        email                : fccoelho@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "2d Kernel Density Map"
def description():
    return "This plugin calculates 2D gaussian kernel density from a point layer"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.8"
def classFactory(iface):
    # load DensityMap class from file DensityMap
    from densitymap import DensityMap
    return DensityMap(iface)
