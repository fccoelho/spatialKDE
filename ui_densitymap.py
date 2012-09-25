# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_densitymap.ui'
#
# Created: Tue Sep 25 19:00:07 2012
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
        DensityMap.resize(276, 213)
        self.verticalLayout = QtGui.QVBoxLayout(DensityMap)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.layerComboBox = QtGui.QComboBox(DensityMap)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.gridLayout.addWidget(self.layerComboBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(DensityMap)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.bwEdit = QtGui.QLineEdit(DensityMap)
        self.bwEdit.setEnabled(True)
        self.bwEdit.setToolTip(_fromUtf8(""))
        self.bwEdit.setObjectName(_fromUtf8("bwEdit"))
        self.gridLayout.addWidget(self.bwEdit, 1, 1, 1, 1)
        self.autobwCheckBox = QtGui.QCheckBox(DensityMap)
        self.autobwCheckBox.setChecked(True)
        self.autobwCheckBox.setObjectName(_fromUtf8("autobwCheckBox"))
        self.gridLayout.addWidget(self.autobwCheckBox, 1, 2, 1, 1)
        self.label = QtGui.QLabel(DensityMap)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(DensityMap)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.rasterEdit = QtGui.QLineEdit(DensityMap)
        self.rasterEdit.setObjectName(_fromUtf8("rasterEdit"))
        self.gridLayout.addWidget(self.rasterEdit, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(DensityMap)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.sizeSpinBox = QtGui.QSpinBox(DensityMap)
        self.sizeSpinBox.setMaximum(1000)
        self.sizeSpinBox.setSingleStep(10)
        self.sizeSpinBox.setProperty("value", 400)
        self.sizeSpinBox.setObjectName(_fromUtf8("sizeSpinBox"))
        self.gridLayout.addWidget(self.sizeSpinBox, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(DensityMap)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DensityMap)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DensityMap.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DensityMap.reject)
        QtCore.QMetaObject.connectSlotsByName(DensityMap)

    def retranslateUi(self, DensityMap):
        DensityMap.setWindowTitle(QtGui.QApplication.translate("DensityMap", "Kernel Density Map", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DensityMap", "Bandwith:", None, QtGui.QApplication.UnicodeUTF8))
        self.autobwCheckBox.setText(QtGui.QApplication.translate("DensityMap", "auto", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DensityMap", "Point layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DensityMap", "File Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.rasterEdit.setText(QtGui.QApplication.translate("DensityMap", "kde.tif", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DensityMap", "Size (pixels):", None, QtGui.QApplication.UnicodeUTF8))

