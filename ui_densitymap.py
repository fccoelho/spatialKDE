# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_densitymap.ui'
#
# Created: Thu Oct 11 10:21:10 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DensityMap(object):
    def setupUi(self, DensityMap):
        DensityMap.setObjectName(_fromUtf8("DensityMap"))
        DensityMap.resize(309, 288)
        self.formLayout = QtGui.QFormLayout(DensityMap)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(DensityMap)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.layerComboBox = QtGui.QComboBox(DensityMap)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.layerComboBox)
        self.selectedCheckBox = QtGui.QCheckBox(DensityMap)
        self.selectedCheckBox.setObjectName(_fromUtf8("selectedCheckBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.selectedCheckBox)
        self.label_5 = QtGui.QLabel(DensityMap)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.zcomboBox = QtGui.QComboBox(DensityMap)
        self.zcomboBox.setObjectName(_fromUtf8("zcomboBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.zcomboBox)
        self.label_2 = QtGui.QLabel(DensityMap)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.bwEdit = QtGui.QLineEdit(DensityMap)
        self.bwEdit.setEnabled(False)
        self.bwEdit.setToolTip(_fromUtf8(""))
        self.bwEdit.setObjectName(_fromUtf8("bwEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.bwEdit)
        self.autobwCheckBox = QtGui.QCheckBox(DensityMap)
        self.autobwCheckBox.setChecked(True)
        self.autobwCheckBox.setObjectName(_fromUtf8("autobwCheckBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.autobwCheckBox)
        self.label_3 = QtGui.QLabel(DensityMap)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_3)
        self.rasterEdit = QtGui.QLineEdit(DensityMap)
        self.rasterEdit.setObjectName(_fromUtf8("rasterEdit"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.rasterEdit)
        self.label_4 = QtGui.QLabel(DensityMap)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_4)
        self.sizeSpinBox = QtGui.QSpinBox(DensityMap)
        self.sizeSpinBox.setMinimum(-1)
        self.sizeSpinBox.setMaximum(10000)
        self.sizeSpinBox.setSingleStep(50)
        self.sizeSpinBox.setProperty("value", 400)
        self.sizeSpinBox.setObjectName(_fromUtf8("sizeSpinBox"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.sizeSpinBox)
        self.checkBox_2 = QtGui.QCheckBox(DensityMap)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.checkBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(DensityMap)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(DensityMap)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DensityMap.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DensityMap.reject)
        QtCore.QMetaObject.connectSlotsByName(DensityMap)

    def retranslateUi(self, DensityMap):
        DensityMap.setWindowTitle(QtGui.QApplication.translate("DensityMap", "Kernel Density Map", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DensityMap", "Point layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedCheckBox.setText(QtGui.QApplication.translate("DensityMap", "Only selected points", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DensityMap", "Values:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DensityMap", "Bandwith:", None, QtGui.QApplication.UnicodeUTF8))
        self.autobwCheckBox.setText(QtGui.QApplication.translate("DensityMap", "auto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DensityMap", "Output file:", None, QtGui.QApplication.UnicodeUTF8))
        self.rasterEdit.setText(QtGui.QApplication.translate("DensityMap", "kde.tif", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DensityMap", "Size (pixels):", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("DensityMap", "Load raster when done", None, QtGui.QApplication.UnicodeUTF8))

