import flet as fl
import sqlite3

def main(page: fl.Page):
    page.theme_mode = 'dark'
    page.vertical_alignment = fl.MainAxisAlignment.CENTER

    page.window.width = 600
    page.window.height = 400
    page.window_resizable = False


    def register(event):
        db = sqlite3.connect('myusers.db')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INEGER PRIMARY KEY,
                            login TEXT,
                            password TEXT
                       )""")

        
        cursor.execute(f"INSERT INTO users VALUES(NULL, '{user_login_field.value}', '{user_password_field.value}')")

        cursor.close()
        db.close()

        user_login_field.value = ''
        user_password_field.value = ''

        page.update()


    def validate(event):
        if all([user_login_field.value, user_password_field.value]):
            confirm_button.disabled = False
        else:
            confirm_button.disabled = True
        page.update()
        

    user_login_field = fl.TextField(label='Имя пользователя', width=200, on_change=validate)
    user_password_field = fl.TextField(label='Пароль', width=200, on_change=validate)
    confirm_button = fl.OutlinedButton(text='Подтвердить', disabled=True, on_click=register)

    page.add(
        fl.Row(
            [
                fl.Column(
                    [
                        fl.Text('Регистрация'),
                        user_login_field,
                        user_password_field,
                        confirm_button
                    ]
                )
            ],
            alignment=fl.MainAxisAlignment.CENTER
        )
    )

fl.app(target=main)