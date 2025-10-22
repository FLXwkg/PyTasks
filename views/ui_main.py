# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.horizontalLayout = QHBoxLayout(self.tab_main)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sidebar = QWidget(self.tab_main)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMaximumWidth(350)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.searchBar = QLineEdit(self.sidebar)
        self.searchBar.setObjectName(u"searchBar")

        self.sidebarLayout.addWidget(self.searchBar)

        self.stateFilter = QComboBox(self.sidebar)
        self.stateFilter.addItem("")
        self.stateFilter.addItem("")
        self.stateFilter.addItem("")
        self.stateFilter.addItem("")
        self.stateFilter.addItem("")
        self.stateFilter.addItem("")
        self.stateFilter.setObjectName(u"stateFilter")

        self.sidebarLayout.addWidget(self.stateFilter)

        self.taskList = QListWidget(self.sidebar)
        self.taskList.setObjectName(u"taskList")

        self.sidebarLayout.addWidget(self.taskList)

        self.buttonContainer = QWidget(self.sidebar)
        self.buttonContainer.setObjectName(u"buttonContainer")
        self.buttonLayout = QHBoxLayout(self.buttonContainer)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.btnAdd = QPushButton(self.buttonContainer)
        self.btnAdd.setObjectName(u"btnAdd")

        self.buttonLayout.addWidget(self.btnAdd)

        self.btnDelete = QPushButton(self.buttonContainer)
        self.btnDelete.setObjectName(u"btnDelete")
        self.btnDelete.setEnabled(False)

        self.buttonLayout.addWidget(self.btnDelete)


        self.sidebarLayout.addWidget(self.buttonContainer)


        self.horizontalLayout.addWidget(self.sidebar)

        self.detailsPanel = QWidget(self.tab_main)
        self.detailsPanel.setObjectName(u"detailsPanel")
        self.detailsLayout = QVBoxLayout(self.detailsPanel)
        self.detailsLayout.setObjectName(u"detailsLayout")
        self.noSelectionLabel = QLabel(self.detailsPanel)
        self.noSelectionLabel.setObjectName(u"noSelectionLabel")
        self.noSelectionLabel.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.noSelectionLabel.setFont(font)

        self.detailsLayout.addWidget(self.noSelectionLabel)

        self.taskDetailsGroup = QGroupBox(self.detailsPanel)
        self.taskDetailsGroup.setObjectName(u"taskDetailsGroup")
        self.taskDetailsGroup.setVisible(False)
        self.taskDetailsLayout = QVBoxLayout(self.taskDetailsGroup)
        self.taskDetailsLayout.setObjectName(u"taskDetailsLayout")
        self.titleContainer = QWidget(self.taskDetailsGroup)
        self.titleContainer.setObjectName(u"titleContainer")
        self.titleLayout = QHBoxLayout(self.titleContainer)
        self.titleLayout.setObjectName(u"titleLayout")
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.labelTitle = QLabel(self.titleContainer)
        self.labelTitle.setObjectName(u"labelTitle")
        font1 = QFont()
        font1.setBold(True)
        self.labelTitle.setFont(font1)

        self.titleLayout.addWidget(self.labelTitle)

        self.titleEdit = QLineEdit(self.titleContainer)
        self.titleEdit.setObjectName(u"titleEdit")

        self.titleLayout.addWidget(self.titleEdit)


        self.taskDetailsLayout.addWidget(self.titleContainer)

        self.stateContainer = QWidget(self.taskDetailsGroup)
        self.stateContainer.setObjectName(u"stateContainer")
        self.stateLayout = QHBoxLayout(self.stateContainer)
        self.stateLayout.setObjectName(u"stateLayout")
        self.stateLayout.setContentsMargins(0, 0, 0, 0)
        self.labelState = QLabel(self.stateContainer)
        self.labelState.setObjectName(u"labelState")
        self.labelState.setFont(font1)

        self.stateLayout.addWidget(self.labelState)

        self.stateEdit = QComboBox(self.stateContainer)
        self.stateEdit.addItem("")
        self.stateEdit.addItem("")
        self.stateEdit.addItem("")
        self.stateEdit.addItem("")
        self.stateEdit.addItem("")
        self.stateEdit.setObjectName(u"stateEdit")

        self.stateLayout.addWidget(self.stateEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.stateLayout.addItem(self.horizontalSpacer)


        self.taskDetailsLayout.addWidget(self.stateContainer)

        self.datesContainer = QWidget(self.taskDetailsGroup)
        self.datesContainer.setObjectName(u"datesContainer")
        self.datesLayout = QHBoxLayout(self.datesContainer)
        self.datesLayout.setObjectName(u"datesLayout")
        self.datesLayout.setContentsMargins(0, 0, 0, 0)
        self.labelStartDate = QLabel(self.datesContainer)
        self.labelStartDate.setObjectName(u"labelStartDate")

        self.datesLayout.addWidget(self.labelStartDate)

        self.startDateEdit = QDateTimeEdit(self.datesContainer)
        self.startDateEdit.setObjectName(u"startDateEdit")
        self.startDateEdit.setCalendarPopup(True)

        self.datesLayout.addWidget(self.startDateEdit)

        self.labelEndDate = QLabel(self.datesContainer)
        self.labelEndDate.setObjectName(u"labelEndDate")

        self.datesLayout.addWidget(self.labelEndDate)

        self.endDateEdit = QDateTimeEdit(self.datesContainer)
        self.endDateEdit.setObjectName(u"endDateEdit")
        self.endDateEdit.setCalendarPopup(True)

        self.datesLayout.addWidget(self.endDateEdit)


        self.taskDetailsLayout.addWidget(self.datesContainer)

        self.labelDescription = QLabel(self.taskDetailsGroup)
        self.labelDescription.setObjectName(u"labelDescription")
        self.labelDescription.setFont(font1)

        self.taskDetailsLayout.addWidget(self.labelDescription)

        self.descriptionEdit = QTextEdit(self.taskDetailsGroup)
        self.descriptionEdit.setObjectName(u"descriptionEdit")
        self.descriptionEdit.setMaximumHeight(150)

        self.taskDetailsLayout.addWidget(self.descriptionEdit)

        self.taskActionsContainer = QWidget(self.taskDetailsGroup)
        self.taskActionsContainer.setObjectName(u"taskActionsContainer")
        self.taskActionsLayout = QHBoxLayout(self.taskActionsContainer)
        self.taskActionsLayout.setObjectName(u"taskActionsLayout")
        self.taskActionsLayout.setContentsMargins(0, 0, 0, 0)
        self.btnSave = QPushButton(self.taskActionsContainer)
        self.btnSave.setObjectName(u"btnSave")

        self.taskActionsLayout.addWidget(self.btnSave)

        self.btnClose = QPushButton(self.taskActionsContainer)
        self.btnClose.setObjectName(u"btnClose")

        self.taskActionsLayout.addWidget(self.btnClose)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.taskActionsLayout.addItem(self.horizontalSpacer_2)


        self.taskDetailsLayout.addWidget(self.taskActionsContainer)

        self.line = QFrame(self.taskDetailsGroup)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.taskDetailsLayout.addWidget(self.line)

        self.labelComments = QLabel(self.taskDetailsGroup)
        self.labelComments.setObjectName(u"labelComments")
        self.labelComments.setFont(font1)

        self.taskDetailsLayout.addWidget(self.labelComments)

        self.commentsList = QListWidget(self.taskDetailsGroup)
        self.commentsList.setObjectName(u"commentsList")
        self.commentsList.setMaximumHeight(200)

        self.taskDetailsLayout.addWidget(self.commentsList)

        self.commentInputContainer = QWidget(self.taskDetailsGroup)
        self.commentInputContainer.setObjectName(u"commentInputContainer")
        self.commentInputLayout = QHBoxLayout(self.commentInputContainer)
        self.commentInputLayout.setObjectName(u"commentInputLayout")
        self.commentInputLayout.setContentsMargins(0, 0, 0, 0)
        self.commentInput = QLineEdit(self.commentInputContainer)
        self.commentInput.setObjectName(u"commentInput")

        self.commentInputLayout.addWidget(self.commentInput)

        self.btnAddComment = QPushButton(self.commentInputContainer)
        self.btnAddComment.setObjectName(u"btnAddComment")

        self.commentInputLayout.addWidget(self.btnAddComment)


        self.taskDetailsLayout.addWidget(self.commentInputContainer)


        self.detailsLayout.addWidget(self.taskDetailsGroup)


        self.horizontalLayout.addWidget(self.detailsPanel)

        self.tabWidget.addTab(self.tab_main, "")
        self.tab_history = QWidget()
        self.tab_history.setObjectName(u"tab_history")
        self.historyLayout = QVBoxLayout(self.tab_history)
        self.historyLayout.setObjectName(u"historyLayout")
        self.historyLog = QTextEdit(self.tab_history)
        self.historyLog.setObjectName(u"historyLog")
        self.historyLog.setReadOnly(True)

        self.historyLayout.addWidget(self.historyLog)

        self.historyButtonsContainer = QWidget(self.tab_history)
        self.historyButtonsContainer.setObjectName(u"historyButtonsContainer")
        self.historyButtonsLayout = QHBoxLayout(self.historyButtonsContainer)
        self.historyButtonsLayout.setObjectName(u"historyButtonsLayout")
        self.historyButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.historyButtonsLayout.addItem(self.horizontalSpacer_3)

        self.btnClearHistory = QPushButton(self.historyButtonsContainer)
        self.btnClearHistory.setObjectName(u"btnClearHistory")

        self.historyButtonsLayout.addWidget(self.btnClearHistory)


        self.historyLayout.addWidget(self.historyButtonsContainer)

        self.tabWidget.addTab(self.tab_history, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyTasks - Gestionnaire de T\u00e2ches", None))
        self.searchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Rechercher une t\u00e2che...", None))
        self.stateFilter.setItemText(0, QCoreApplication.translate("MainWindow", u"Tous les \u00e9tats", None))
        self.stateFilter.setItemText(1, QCoreApplication.translate("MainWindow", u"\u00c0 faire", None))
        self.stateFilter.setItemText(2, QCoreApplication.translate("MainWindow", u"En cours", None))
        self.stateFilter.setItemText(3, QCoreApplication.translate("MainWindow", u"R\u00e9alis\u00e9", None))
        self.stateFilter.setItemText(4, QCoreApplication.translate("MainWindow", u"Abandonn\u00e9", None))
        self.stateFilter.setItemText(5, QCoreApplication.translate("MainWindow", u"En attente", None))

#if QT_CONFIG(tooltip)
        self.stateFilter.setToolTip(QCoreApplication.translate("MainWindow", u"Filtrer par \u00e9tat", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.taskList.setToolTip(QCoreApplication.translate("MainWindow", u"Liste des t\u00e2ches", None))
#endif // QT_CONFIG(tooltip)
        self.btnAdd.setText(QCoreApplication.translate("MainWindow", u"Ajouter", None))
        self.btnDelete.setText(QCoreApplication.translate("MainWindow", u"Supprimer", None))
        self.noSelectionLabel.setText(QCoreApplication.translate("MainWindow", u"S\u00e9lectionnez une t\u00e2che pour voir les d\u00e9tails", None))
        self.taskDetailsGroup.setTitle(QCoreApplication.translate("MainWindow", u"D\u00e9tails de la t\u00e2che", None))
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"Titre :", None))
        self.labelState.setText(QCoreApplication.translate("MainWindow", u"\u00c9tat :", None))
        self.stateEdit.setItemText(0, QCoreApplication.translate("MainWindow", u"\u00c0 faire", None))
        self.stateEdit.setItemText(1, QCoreApplication.translate("MainWindow", u"En cours", None))
        self.stateEdit.setItemText(2, QCoreApplication.translate("MainWindow", u"R\u00e9alis\u00e9", None))
        self.stateEdit.setItemText(3, QCoreApplication.translate("MainWindow", u"Abandonn\u00e9", None))
        self.stateEdit.setItemText(4, QCoreApplication.translate("MainWindow", u"En attente", None))

        self.labelStartDate.setText(QCoreApplication.translate("MainWindow", u"D\u00e9but :", None))
        self.labelEndDate.setText(QCoreApplication.translate("MainWindow", u"Fin :", None))
        self.labelDescription.setText(QCoreApplication.translate("MainWindow", u"Description :", None))
        self.btnSave.setText(QCoreApplication.translate("MainWindow", u"Enregistrer", None))
        self.btnClose.setText(QCoreApplication.translate("MainWindow", u"Cl\u00f4turer", None))
        self.labelComments.setText(QCoreApplication.translate("MainWindow", u"Commentaires :", None))
        self.commentInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ajouter un commentaire...", None))
        self.btnAddComment.setText(QCoreApplication.translate("MainWindow", u"Ajouter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), QCoreApplication.translate("MainWindow", u"T\u00e2ches", None))
        self.historyLog.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Les logs des actions appara\u00eetront ici...", None))
        self.btnClearHistory.setText(QCoreApplication.translate("MainWindow", u"Effacer l'historique", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), QCoreApplication.translate("MainWindow", u"Historique", None))
    # retranslateUi

