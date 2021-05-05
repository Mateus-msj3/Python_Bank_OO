import os
import sys
import icons_window
import sqlite3
import time


from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtWidgets import *

# os.system('pyrcc5 icons_window.qrc -o icons_window.py')


# Functions
def toggle_menu(self, maxWidth, enable):

    if enable:
        width = view_bank.left_side_menu.width()
        maxExtend = maxWidth
        standard = 50

        if width == 50:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        view_bank.animation = QPropertyAnimation(
            view_bank.left_side_menu, b"minimumWidth")
        view_bank.animation.setDuration(400)
        view_bank.animation.setStartValue(width)
        view_bank.animation.setEndValue(widthExtended)
        view_bank.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        view_bank.animation.start()


def show_login_response(response_message):
    # Container de login
    view_bank.login_response_frame.show()
    # label msg
    view_bank.label_msg.setText(response_message)


def close_login_response():
    view_bank.login_response_frame.close()


def validate_login_fields():
    # variaveis de estilos css
    sucess_style = "border: 3px solid rgb(0, 255, 255); border-radius: 10px;"
    error_style = "border: 3px solid rgb(255, 0, 0); border-radius: 10px;"

    # Check username
    if not view_bank.lineEdit_username.text():
        username_response = " User cant not be Empyt. "
        view_bank.lineEdit_username.setStyleSheet(error_style)
    else:
        username_response = ""

    # Check password
    if not view_bank.lineEdit_password.text():
        password_response = " Password cant not be Empyt. "
        view_bank.lineEdit_password.setStyleSheet(error_style)
    else:
        password_response = ""

    # View responses

    if password_response != "" or username_response != "":
        login_response = username_response + password_response
        show_login_response(login_response)
        # view_bank.show_login_response(login_response)
    else:

        # Correct username and password
        correct_username = "mateus"
        correct_password = "123"

        # check if the user name is correct
        if view_bank.lineEdit_username.text() == correct_username:
            username_response = ""
            view_bank.lineEdit_username.setStyleSheet(sucess_style)
        else:
            username_response = "Incorrect username"
            view_bank.lineEdit_username.setStyleSheet(error_style)

        # check if the password is correct
        if view_bank.lineEdit_password.text() == correct_password:
            password_response = ""
            view_bank.lineEdit_password.setStyleSheet(sucess_style)
        else:
            password_response = "Incorrect password "
            view_bank.lineEdit_password.setStyleSheet(error_style)

        # Create response msg
        if password_response == "" and username_response == "":
            login_response = "Login Sucessful."
            show_login_response(login_response)
            view_bank.stackedWidget.setCurrentWidget(view_bank.home_page)
            view_bank.lineEdit_username.setText("")
            view_bank.lineEdit_password.setText("")
            view_bank.pushButton_contas.setEnabled(True)
            view_bank.pushButton_funcionarios.setEnabled(True)
            view_bank.login_response_frame.hide()

        elif password_response != "" and username_response != "":
            login_response = username_response + " and " + password_response
            show_login_response(login_response)

        else:
            login_response = username_response + password_response
            show_login_response(login_response)
    

def msg_box_confirmation():

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText('Conta cadastrada com sucesso!')
    msg_box.setWindowTitle('Sucess')
    msg_box.setStandardButtons(QMessageBox.Ok)

    returnValue = msg_box.exec()
    if returnValue == QMessageBox.Ok:
        view_bank.stackedWidget.setCurrentWidget(view_bank.page_new_conta)


def create_new_conta():
    # Pegando os dados dos capmos da tela
    tipo_conta = view_bank.comboBox_tipo_conta.currentText()
    numero = view_bank.lineEdit_numero.text()
    titular = view_bank.lineEdit_titular.text()
    saldo_inicial = view_bank.lineEdit_saldo.text()
    limite = view_bank.lineEdit_limite.text()

    try:
        # Criando a conexão com o database
        data_base = sqlite3.connect('data_base_bank.sqlite')
        cursor = data_base.cursor()
        cursor.execute("INSERT INTO conta VALUES (NULL, '"+tipo_conta +
                       "', '"+numero+"', '"+titular+"', '"+saldo_inicial+"', '"+limite+"')")
        data_base.commit()
        data_base.close()
        print('Conta inserida com sucesso')
    except sqlite3.Error as erro:
        print('Erro ao inserir os dados: ', erro)

    # Limpando os dados dos capmos da tela
    numero = view_bank.lineEdit_numero.clear()
    titular = view_bank.lineEdit_titular.clear()
    saldo_inicial = view_bank.lineEdit_saldo.clear()
    limite = view_bank.lineEdit_limite.clear()


def list_contas():

    data_base = sqlite3.connect('data_base_bank.sqlite')
    cursor = data_base.cursor()
    cursor.execute("SELECT * FROM conta")
    return_dados_database = cursor.fetchall()

    view_bank.tableWidget.setRowCount(len(return_dados_database))
    view_bank.tableWidget.setColumnCount(6)

    for i in range(0, len(return_dados_database)):
        for j in range(0, 6):
            view_bank.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(return_dados_database[i][j])))
                
# End Functions


# instancia
app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(":/icons/icons/bank.png"))


# Load da GUI principal
view_bank = uic.loadUi("view_bank.ui")
view_bank.comboBox_tipo_conta.addItems(["Conta Poupança", "Conta Corrente"])


# Actions PushButtons

# Menu toggle
view_bank.pushButton_toggle.clicked.connect(
    lambda: toggle_menu(toggle_menu, 170, True))

# StackedWidgets pages principais
view_bank.stackedWidget.setCurrentWidget(view_bank.home_page)

view_bank.pushButton_home.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.home_page))

view_bank.pushButton_login.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.login_page))
# End StackedWidgets pages principais


# Page Contas
view_bank.pushButton_contas.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.contas_page))

view_bank.pushButton_nova_conta.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.page_new_conta))

view_bank.pushButton_create_conta.clicked.connect(create_new_conta)

view_bank.pushButton_create_conta.clicked.connect(msg_box_confirmation)

view_bank.pushButton_listar_conta.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.page_list_conta))

view_bank.pushButton_listar_conta.clicked.connect(list_contas)
# End pages contas

# Page Funcionarios
view_bank.pushButton_funcionarios.clicked.connect(
    lambda: view_bank.stackedWidget.setCurrentWidget(view_bank.funcionarios_page))
# End Funcionarios

# Pop-up de login
view_bank.login_response_frame.hide()

view_bank.pushButton_Ok.clicked.connect(
    lambda: view_bank.login_response_frame.hide)
# End pop-up login


# Botão que valida o login
view_bank.pushButton_login_validate.clicked.connect(validate_login_fields)
view_bank.pushButton_Ok.clicked.connect(close_login_response)


# Executando a aplicação
view_bank.show()
app.exec()