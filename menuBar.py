from PyQt5.QtWidgets import QAction, QMenuBar, QMessageBox
from PyQt5.QtCore import Qt

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_menu()

    def init_menu(self):

        # Добавление разделов в меню-бар
        #view_menu = self.addMenu("Внешний вид")
        setting_menu = self.addMenu("Настройки")
        about_menu = self.addMenu("Справка")

        about_action = QAction("О программе", self)
        contacts_action = QAction("Об авторе", self)
        setting_action = QAction("Настройки метронома", self)

        about_menu.addAction(about_action)
        about_menu.addAction(contacts_action)
        setting_menu.addAction(setting_action)

        # Связываем действия с функциями
        about_action.triggered.connect(self.show_about)
        contacts_action.triggered.connect(self.show_contacts)
        setting_action.triggered.connect(self.setting_metronome)

    def show_about(self):
        """Показывает окно "О программе"."""
        about_box = QMessageBox(self)
        about_box.setWindowTitle("О программе")
        about_box.setTextFormat(Qt.RichText)  # Включаем поддержку HTML
        about_box.setText(
            "<b>Программа:</b> Виртуальное пианино<br>"
            "<b>Описание:</b> Программа создана в рамках выполнения автором "
            "курсовой работы по предмету 'Технологии и методы программирования'<br>"
            "<b>Автор:</b> Шестериков Б.В.<br>"
            "<b>Версия:</b> <i>1.0.0</i>"
        )
        about_box.setIcon(QMessageBox.Information)
        about_box.setStandardButtons(QMessageBox.Ok)
        about_box.exec_()

    def show_contacts(self):
        """Показывает окно "Об авторе"."""
        contacts_box = QMessageBox(self)
        contacts_box.setWindowTitle("Контакты")
        contacts_box.setTextFormat(Qt.RichText)  # Включаем поддержку HTML
        contacts_box.setText(
            "<b>Контакты:</b><br>"
            "<ul>"
            "<li><b>Имя:</b> Шестериков Б.В.</li>"
            "<li><b>Почта:</b> boris20033@gmail.com</li>"
            "<li><b>Telegram:</b> <a href='https://t.me/barman_555'>t.me/barman_555</a></li>"
            "</ul>"
        )
        contacts_box.setIcon(QMessageBox.Information)
        contacts_box.setStandardButtons(QMessageBox.Ok)
        contacts_box.exec_()

    def setting_metronome(self):
        pass
