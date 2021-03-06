# -*- coding: utf-8 -*-
import tkinter
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import messagebox
from AssistedController import AssistedController
from LoginController import LoginController

assisted_controller = AssistedController()
user_controller = LoginController()


class Ui_FormBackup(object):
    password_visible = False

    def btn_show_password_clicked(self):
        if self.password_visible is True:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
            new_icon = QtGui.QIcon.fromTheme("hint")
            self.btn_show_password.setIcon(new_icon)
            self.password_visible = False
        else:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.Normal)
            new_icon = QtGui.QIcon.fromTheme("view-hidden")
            self.btn_show_password.setIcon(new_icon)
            self.password_visible = True

    def btn_execute_clicked(self):
        this_window = QtWidgets.QApplication.activeWindow()
        user = self.txt_user.text().strip()
        password = self.txt_password.text().strip()

        if user_controller.count_user(user) < 1:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror(
                'ERRO', 'ERRO!!! O Usuário informado não existe.\nTente outro usuário')
            tkinter.Tk().destroy()
        else:
            historic_message = ''
            active_user = assisted_controller.select_active_user()

            if self.radio_export.isChecked():
                if password == user_controller.select_user(user)[1]:
                    if user == active_user[1]:
                        historic_message = 'EXPORTOU dados utilizando o próprio login'
                    else:
                        historic_message = f'EXPORTOU dados utilizando o login <{user}>'

                    assisted_controller.export_data()
                    assisted_controller.register_changes(
                        active_user[0], historic_message)
                    this_window.close()
                else:
                    root = tkinter.Tk()
                    root.withdraw()
                    messagebox.showerror(
                        'ERRO', f'ERRO!!! A senha para o usuário <{user}> está incorreta')
                    tkinter.Tk().destroy()
            else:
                if user_controller.select_user(user)[2] != 'ADMINISTRADOR':
                    root = tkinter.Tk()
                    root.withdraw()
                    messagebox.showerror(
                        'ERRO', 'ERRO!!! Apenas usuários com categoria ADMINISTRADOR podem IMPORTAR dados.\nInsira um usuário com a categoria de <ADMINISTRADOR> e tente novamente.')
                    tkinter.Tk().destroy()
                else:
                    if password == user_controller.select_user(user)[1]:
                        import platform
                        import os
                        path = ''

                        if platform.system() == 'Linux':
                            path = os.path.expanduser(
                                "~") + '/Documentos/GERENCIAMENTO_DE_ASSISTIDOS_AELMAC/BACKUPS/'
                        else:
                            path = os.path.expanduser(
                                "~") + '\\Documents\\GERENCIAMENTO_DE_ASSISTIDOS_AELMAC\\BACKUPS\\'

                        dialog = QtWidgets.QFileDialog()
                        file = dialog.getOpenFileName(
                            dialog, 'Selecionar arquivo de backup', path, 'Arquivo de Banco de Dados (*.db)')

                        if file[0] != '':
                            root = tkinter.Tk()
                            root.withdraw()
                            choice = messagebox.askquestion(
                                'ATENÇÃO', 'Ao confirmar esta ação, TODOS os dados salvos anteriormente serão substituidos.\nDeseja continuar?')
                            tkinter.Tk().destroy()

                            if choice == 'yes':
                                if user == active_user[1]:
                                    historic_message = 'IMPORTOU dados utilizando o próprio login'
                                else:
                                    historic_message = f'IMPORTOU dados utilizando o login de {active_user[0]}'

                                assisted_controller.register_changes(
                                    active_user[0], historic_message)
                                assisted_controller.gen_historic()
                                assisted_controller.import_data(file[0])
                                QtWidgets.QApplication.quit()
                    else:
                        root = tkinter.Tk()
                        root.withdraw()
                        messagebox.showerror(
                            'ERRO', f'ERRO!!! A senha para o usuário <{user}> está incorreta')
                        tkinter.Tk().destroy()

    def setupUi(self, FormBackup):
        FormBackup.setObjectName("FormBackup")
        FormBackup.resize(500, 405)
        FormBackup.setMaximumSize(QtCore.QSize(500, 405))
        FormBackup.setWindowTitle("GERENCIADOR DE BACKUPS")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/aelmac_white_16.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormBackup.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(FormBackup)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 481, 121))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setTitle("OPERAÇÃO")
        self.groupBox.setObjectName("groupBox")
        self.radio_export = QtWidgets.QRadioButton(self.groupBox)
        self.radio_export.setGeometry(QtCore.QRect(36, 60, 171, 22))
        self.radio_export.setText("EXPORTAR Dados")
        self.radio_export.setObjectName("radio_export")
        self.radio_import = QtWidgets.QRadioButton(self.groupBox)
        self.radio_import.setGeometry(QtCore.QRect(280, 60, 161, 22))
        self.radio_import.setText("IMPORTAR Dados")
        self.radio_import.setObjectName("radio_import")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 481, 211))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle("AUTENTICAÇÃO")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(15, 47, 445, 21))
        self.label.setText("USUÁRIO")
        self.label.setObjectName("label")
        self.txt_user = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_user.setGeometry(QtCore.QRect(15, 70, 450, 32))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txt_user.setFont(font)
        self.txt_user.setInputMask("")
        self.txt_user.setObjectName("txt_user")
        self.txt_password = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_password.setGeometry(QtCore.QRect(15, 150, 410, 32))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txt_password.setFont(font)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password.setObjectName("txt_password")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(15, 127, 445, 21))
        self.label_2.setText("SENHA")
        self.label_2.setObjectName("label_2")
        self.btn_show_password = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_show_password.setGeometry(QtCore.QRect(430, 150, 32, 32))
        self.btn_show_password.setText("")
        icon = QtGui.QIcon.fromTheme("hint")
        self.btn_show_password.setIcon(icon)
        self.btn_show_password.setFlat(True)
        self.btn_show_password.setObjectName("btn_show_password")
        self.btn_show_password.clicked.connect(self.btn_show_password_clicked)
        self.btn_execute = QtWidgets.QPushButton(self.centralwidget)
        self.btn_execute.setGeometry(QtCore.QRect(10, 360, 481, 34))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_execute.setFont(font)
        self.btn_execute.setText("EXECUTAR TRANSAÇÃO")
        self.btn_execute.setObjectName("btn_execute")
        self.btn_execute.clicked.connect(self.btn_execute_clicked)
        FormBackup.setCentralWidget(self.centralwidget)

        if assisted_controller.count_assisted() < 1:
            self.radio_export.setEnabled(False)
            self.radio_import.setEnabled(True)
        else:
            self.radio_export.setEnabled(True)
            self.radio_import.setEnabled(True)

        QtCore.QMetaObject.connectSlotsByName(FormBackup)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormBackup = QtWidgets.QMainWindow()
    ui = Ui_FormBackup()
    ui.setupUi(FormBackup)
    FormBackup.show()
    sys.exit(app.exec_())
