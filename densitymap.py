# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DensityMap
                                 A QGIS plugin
 This plugin calculates 2D gaussian kernel density from a point layer
                              -------------------
        begin                : 2012-09-20
        copyright            : (C) 2012 by Flávio Codeço Coelho - Fundação Getulio Vargas
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from densitymapdialog import DensityMapDialog
from kernel import Kernel2d
import numpy as np

class DensityMap:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # Create the dialog and keep reference
        self.dlg = DensityMapDialog()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/densitymap"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/densitymap_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        self.layermap = QgsMapLayerRegistry.instance().mapLayers()
        self.layer_list = []
        self.layer_pointer_list = []
        self.update_dialog()
   

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/densitymap/icon.png"), \
            u"Kernel Density", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        QObject.connect(self.dlg.ui.autobwCheckBox,SIGNAL("stateChanged"),self.update_bw)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Kernel Density", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Kernel Density",self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            data = self.collectData(self.collectOptions())
            k = Kernel2d(np.array(data['X']), np.array(data['Y']),float(self.dlg.ui.bwEdit.text()))
            k.run()
            k.to_geotiff(str(self.dlg.ui.rasterEdit.text()), self.epsg)
        
    def read_kde(self):
        """
        Loads the generated tiff file and shows on the canvas.
        """
        fileName = "/path/to/raster/file.tif"
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.baseName()
        rlayer = QgsRasterLayer(fileName, baseName)
        if not rlayer.isValid():
            QMessageBox.critical(self.dlg, "Kernel Density Map plugin", "Layer failed to load.")
        #Adding layer to the registry:
        QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        
          
    
    def update_bw(self):
        """
        """
        if self.dlg.ui.autobwCheckBox.isChecked():
            self.dlg.ui.bwEdit.setEnabled(False)
        else:
            self.dlg.ui.bwEdit.setEnabled(True)
            
    def update_dialog(self, silent=False): 
        """
        Refreshes/loads layers in ComboBox, looking up in Legend NOT IN CANVAS
        """
        self.dlg.ui.layerComboBox.clear()
        for name, layer in self.layermap.iteritems():
            if layer.type() == layer.VectorLayer and layer.geometryType() == QGis.Point:
                self.dlg.ui.layerComboBox.addItem(layer.name()) # loads display name
                self.layer_list.append(layer.getLayerID()) # fills the list with full timestamped name
                self.layer_pointer_list.append(layer)

        if self.dlg.ui.layerComboBox.count() == 0 and not silent:
            QMessageBox.critical(self.dlg, "Kernel Density Map plugin", "No point layers available! Load at least one and re-run.")
            #~ self.emit(SIGNAL("rejected"), self.close)
            #~ self.kill()

    def collectData(self, opt):
        """
        Extracts geometries from selected layer.
        """
        idDict = []
        xDict = []
        yDict = []
        geomData = {'X': xDict,  'Y': yDict}
        # use QGis tools to extract info from layer
        layer = opt["io"]["layerpointer"]
        provider = layer.dataProvider()
        srs = layer.srs()
        self.epsg = srs.epsg()
        self.srid = srs.srsid()
        allAttrs = provider.attributeIndexes()
        fields = provider.fields()
        provider.select(allAttrs)
        feat = QgsFeature()
        while provider.nextFeature(feat):
            geom = feat.geometry()
            pointmp = geom.asPoint()
            xDict.append(pointmp.x())
            yDict.append(pointmp.y())

        return geomData

    def collectOptions(self):
        """
        Collects all options in a dictionary.
        """
        opt = {}
        # input settings
        opt["io"] = {}
        opt["io"]["layer"] = "%s" % self.layer_list[self.dlg.ui.layerComboBox.currentIndex()]
        opt["io"]["layerpointer"] = self.layer_pointer_list[self.dlg.ui.layerComboBox.currentIndex()]
        opt["io"]["layername"] = "%s" % self.layer_pointer_list[self.dlg.ui.layerComboBox.currentIndex()].name()
        opt["io"]["bandwidth"] = self.dlg.ui.bwEdit.text()
        print opt
        return opt
