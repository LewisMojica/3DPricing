# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(399, 298)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.almacenamientoDeArchivosLabel = QtWidgets.QLabel(Form)
        self.almacenamientoDeArchivosLabel.setObjectName("almacenamientoDeArchivosLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.almacenamientoDeArchivosLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_3.addWidget(self.toolButton_2)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.baseDeDatosLabel = QtWidgets.QLabel(Form)
        self.baseDeDatosLabel.setObjectName("baseDeDatosLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.baseDeDatosLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.precioDeElectricidadLabel = QtWidgets.QLabel(Form)
        self.precioDeElectricidadLabel.setObjectName("precioDeElectricidadLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.precioDeElectricidadLabel)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox.setPrefix("")
        self.doubleSpinBox.setMaximum(99999999.99)
        self.doubleSpinBox.setSingleStep(0.01)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.precioDeTrabajoHumanoLabel = QtWidgets.QLabel(Form)
        self.precioDeTrabajoHumanoLabel.setObjectName("precioDeTrabajoHumanoLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.precioDeTrabajoHumanoLabel)
        self.precioDeTrabajoHumanoDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.precioDeTrabajoHumanoDoubleSpinBox.setMaximum(99999999.0)
        self.precioDeTrabajoHumanoDoubleSpinBox.setObjectName("precioDeTrabajoHumanoDoubleSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.precioDeTrabajoHumanoDoubleSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.almacenamientoDeArchivosLabel.setText(_translate("Form", "Almacenamiento de Archivos:"))
        self.toolButton_2.setText(_translate("Form", "..."))
        self.baseDeDatosLabel.setText(_translate("Form", "Base de datos:"))
        self.toolButton.setText(_translate("Form", "..."))
        self.precioDeElectricidadLabel.setText(_translate("Form", "Precio de electricidad:"))
        self.doubleSpinBox.setSuffix(_translate("Form", " $/kWh"))
        self.precioDeTrabajoHumanoLabel.setText(_translate("Form", "Precio de trabajo (humano):"))
        self.precioDeTrabajoHumanoDoubleSpinBox.setSuffix(_translate("Form", " $/h"))
        self.pushButton.setText(_translate("Form", "Descartar"))
        self.pushButton_2.setText(_translate("Form", "Guardar cambios"))