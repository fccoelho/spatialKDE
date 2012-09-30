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
import types
import pdb

def refresh(self,event):
    self.dialog_opened.emit()
    

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
        
        self.dlg.showEvent = types.MethodType(refresh, self.dlg)
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
        self.dlg.dialog_opened.connect(self.set_it_all_up)
        self.set_it_all_up()
#        self.progress = QProgressDialog("Calculating Density...","Wait",0,4)
#        self.progress.setWindowModality(Qt.WindowModal);
#        self.progress.setWindowTitle("2D KDE")
        self.update_dialog(True)
        self.update_bw()
        self.update_attribute_combo()
   

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/densitymap/icon.png"), \
            u"Kernel Density", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        # Connect the autobw signal
        self.dlg.ui.autobwCheckBox.stateChanged.connect(self.update_bw)
        #Connect layer selection signal to 
        self.dlg.ui.layerComboBox.currentIndexChanged.connect(self.update_attribute_combo)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Kernel Density", self.action)
        
    def set_it_all_up(self):
        """
        Reads data and updates dialog
        """
        self.update_dialog()
        self.update_bw()
        self.update_attribute_combo()

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
            # do the calculations
#            self.progress.open()
#            self.progress.setLabelText("Setting up analysis...")
            points,values = self.collectData(self.collectOptions())
            print len(points['X']),min(points['X']),max(points['X'])
            try:
                bw = float(self.dlg.ui.bwEdit.text())
            except:
                bw = None
            if values != []:
                k = Kernel2d(np.array(points['X']), np.array(points['Y']),np.array(values),bw,self.dlg.ui.sizeSpinBox.value())
            else:
                k = Kernel2d(np.array(points['X']), np.array(points['Y']),bw=bw,size=self.dlg.ui.sizeSpinBox.value())
            k.run()
#            self.progress.setValue(3)
#            self.progress.setLabelText("Saving GeoTiff...")
            k.to_geotiff(str(self.dlg.ui.rasterEdit.text()), self.epsg)
#            self.progress.setValue(4)
        
    def read_kde(self,fname):
        """
        Loads the generated tiff file and shows on the canvas.
        """
        fileName = fname
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.baseName()
        rlayer = QgsRasterLayer(fileName, baseName)
        if not rlayer.isValid():
            QMessageBox.critical(self.dlg, "Kernel Density Map plugin", "Layer failed to load.")
        #Adding layer to the registry:
        QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        
    def update_bw(self,i=0):
        """
        Enable/disable bandwith specification box
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
            

    #~ @pyqtSlot(int, name="on_layerComboBox_currentIndexChanged")
    def update_attribute_combo(self,i=0):
        """
        Fills the zcomboBox based on the attributes of the layer chosen
        """
        if len(self.layermap) == 0:
            return
        # the line means: catch the address of the layer which full name has the index in combobox.
        layer = self.layermap[self.layer_list[self.dlg.ui.layerComboBox.currentIndex()]]
        provider = layer.dataProvider()
        fieldmap = provider.fields()
        self.dlg.ui.zcomboBox.clear()
        self.dlg.ui.zcomboBox.addItem("None")
        for (k,attr) in fieldmap.iteritems():
          self.dlg.ui.zcomboBox.addItem(attr.name())
        
    def collectData(self, opt):
        """
        Extracts geometries from selected layer.
        """
        xDict = []
        yDict = []
        values = []
        geomData = {'X': xDict,  'Y': yDict}
        # use QGis tools to extract info from layer
        layer = opt["io"]["layerpointer"]
        provider = layer.dataProvider()
        # get Spatial reference system
        srs = layer.srs()
        self.epsg = srs.epsg()
        self.srid = srs.srsid()
        # get selected ids
        sel_features = layer.selectedFeatures() #may use selectedFeaturesIds() to minimize memory usage
        print "Selected: ", len(sel_features)
#        pyqtRemoveInputHook()
#        pdb.set_trace()
        allAttrs = provider.attributeIndexes()
        fields = provider.fields()
        fieldID = None
        for (k, v) in fields.iteritems():
            if v.name() == opt["io"]["zvalue"]: 
                fieldID = k 
        if self.dlg.ui.selectedCheckBox.isChecked():
            print "Selected: ",layer.selectedFeatureCount()
            return self.collect_selected_data(sel_features, geomData, 
                                              values, fieldID)
        print "Doing the Whole dataset"
        provider.select(allAttrs)
        feat = QgsFeature()
        while provider.nextFeature(feat):
            geom = feat.geometry()
            pointmp = geom.asPoint()
            xDict.append(pointmp.x())
            yDict.append(pointmp.y())
            attrs = feat.attributeMap()
            try:
                for (k,attr) in attrs.iteritems(): # i.e., for each pair key-value of the attributes of that feature
                    if k == fieldID:
                        at = str(attr.toString())
                        if not at:
                            at = np.nan
                        else:
                            v = float(at)
                        values.append(v)
            except ValueError:
                QMessageBox.critical(self.dlg, "Kernel Density Map plugin",
                                     "Can't convert value '%s' to floats please choose a numeric variable"%at)
#        self.progress.setValue(2)
#        self.progress.setLabelText("Calculating Kernel...")
        return geomData, values

    def collect_selected_data(self, sel_feat, geomdata, values, fieldID):
        """
        Collect only selected points
        """
        print "Doing selected points "
        for feat in sel_feat:
            geom = feat.geometry()
            pointmp = geom.asPoint()
            geomdata['X'].append(pointmp.x())
            geomdata['Y'].append(pointmp.y())
            attrs = feat.attributeMap()
            try:
                for (k,attr) in attrs.iteritems(): # i.e., for each pair key-value of the attributes of that feature
                    if k == fieldID:
                        at = str(attr.toString())
                        if not at:
                            at = np.nan
                        else:
                            v = float(at)
                        values.append(v)
            except ValueError:
                QMessageBox.critical(self.dlg, "Kernel Density Map plugin",
                                     "Can't convert value '%s' to floats please choose a numeric variable"%at)
        return geomdata,values
        
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
        opt["io"]["zvalue"] = str(self.dlg.ui.zcomboBox.currentText()) #layer with z values for the points
        #print opt
#        self.progress.setValue(1)
#        self.progress.setLabelText("Loading data...")
        return opt
