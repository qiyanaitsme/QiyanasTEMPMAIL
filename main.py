import sys
import aiohttp
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextBrowser
from PyQt5.QtGui import QIcon

class EmailManager:
    def __init__(self):
        self.email_list = []

    async def generate_emails(self, count):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(count):
                task = self.generate_single_email(session)
                tasks.append(task)
            self.email_list = await asyncio.gather(*tasks)

    async def generate_single_email(self, session):
        api_url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]
            else:
                print(f"Ошибка: {response.status} - {await response.text()}")
                return None

    async def check_mail(self, email):
        login, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    messages = await response.json()
                    return messages
                else:
                    print(f"Ошибка: {response.status} - {await response.text()}")
                    return None

    async def delete_mail(self, email):
        login, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=deleteMailbox&login={login}&domain={domain}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"Ошибка: {response.status} - {await response.text()}")
                    return False

    async def run(self, num_emails):
        await self.generate_emails(num_emails)
        if self.email_list:
            for email in self.email_list:
                print(email)

class TempMailApp(QWidget):
    def __init__(self):
        super().__init__()

        self.email_manager = EmailManager()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowIcon(QIcon('qiyanka.ico'))
        self.setFixedSize(400, 300)

        self.label = QLabel('Адрес временной почты:')
        self.email_input = QLineEdit(self)
        layout.addWidget(self.label)
        layout.addWidget(self.email_input)

        self.get_email_button = QPushButton('Получить временную почту', self)
        self.get_email_button.clicked.connect(self.get_temp_email)
        layout.addWidget(self.get_email_button)

        self.check_mail_button = QPushButton('Проверить почту', self)
        self.check_mail_button.clicked.connect(self.check_mail)
        layout.addWidget(self.check_mail_button)

        self.result_browser = QTextBrowser(self)
        layout.addWidget(self.result_browser)

        self.author_button = QPushButton('АВТОР', self)
        self.author_button.clicked.connect(self.open_author_page)
        layout.addWidget(self.author_button)

        self.delete_mail_button = QPushButton('Удалить почту', self)
        self.delete_mail_button.clicked.connect(self.delete_mail)
        layout.addWidget(self.delete_mail_button)

        self.setLayout(layout)

    def get_temp_email(self):
        asyncio.run(self.email_manager.generate_emails(1))
        if self.email_manager.email_list:
            self.email_input.setText(self.email_manager.email_list[0])
            self.result_browser.clear()
            self.result_browser.append(f"Сгенерированная почта: {self.email_manager.email_list[0]}")

    def check_mail(self):
        email = self.email_input.text().strip()
        if email:
            messages = asyncio.run(self.email_manager.check_mail(email))
            if messages:
                self.result_browser.clear()
                self.result_browser.append(f"Сообщения для {email}:")
                for message in messages:
                    self.result_browser.append(str(message))
            else:
                self.result_browser.clear()
                self.result_browser.append(f"Сообщений нет для {email}")
        else:
            self.result_browser.clear()
            self.result_browser.append("Введите адрес электронной почты для проверки.")

    def open_author_page(self):
        import webbrowser
        webbrowser.open('https://zelenka.guru/sataraitsme/')

    def delete_mail(self):
        email = self.email_input.text().strip()
        if email:
            success = asyncio.run(self.email_manager.delete_mail(email))
            if success:
                self.result_browser.clear()
                self.result_browser.append(f"Почта {email} успешно удалена.")
            else:
                self.result_browser.clear()
                self.result_browser.append(f"Не удалось удалить почту {email}. Попробуйте позже.")
        else:
            self.result_browser.clear()
            self.result_browser.append("Введите адрес электронной почты для удаления.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TempMailApp()
    ex.setWindowTitle('QIYANAS TEMPMAIL')
    ex.show()
    sys.exit(app.exec_())
