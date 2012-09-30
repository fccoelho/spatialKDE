# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DensityMapDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_densitymap import Ui_DensityMap
# create the dialog for zoom to point
class DensityMapDialog(QtGui.QDialog):
    dialog_opened = QtCore.pyqtSignal()
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_DensityMap()
        self.ui.setupUi(self)
