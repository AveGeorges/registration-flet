import flet as fl
import sqlite3

def main(page: fl.Page):
    page.title = 'User LogIn system'
    page.theme_mode = 'dark'
    page.vertical_alignment = fl.MainAxisAlignment.CENTER

    page.window.width = 400
    page.window.height = 500
    page.window_resizable = False


    def register(event):
        db = sqlite3.connect('myusers.db')
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            login TEXT,
                            password TEXT
                       )""")

        
        cursor.execute(f"INSERT INTO users VALUES(NULL, '{user_login_field.value}', '{user_password_field.value}')")

        cursor.close()
        db.commit()
        db.close()

        user_login_field.value = ''
        user_password_field.value = ''

        page.update()


    def validate(event):
        if all([user_login_field.value, user_password_field.value]):
            confirm_reg_button.disabled = False
            confirm_auth_button.disabled = False
        else:
            confirm_reg_button.disabled = True
            confirm_auth_button.disabled = True
        page.update()
        

    def authorization(event):
        db = sqlite3.connect('myusers.db')
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM users WHERE login = '{user_login_field.value}' AND password = '{user_password_field.value}'")
        user_data = cursor.fetchone()
        if user_data != None:
            user_login_field.value = ''
            user_password_field.value = ''
            page.snack_bar = fl.SnackBar(fl.Text('Вы успешно вошли!'))
            page.snack_bar.open = True
            
            if len(page.navigation_bar.destinations) == 2:
              page.navigation_bar.destinations.append(fl.NavigationBarDestination(
                icon=fl.icons.BOOK,
                label='Кабинет',
                selected_icon=fl.icons.BOOKMARK
              ))
            
            page.update()
        else:
            page.snack_bar = fl.SnackBar(fl.Text('Введены неверные данные'))
            page.snack_bar.open = True
            page.update()

        cursor.close()
        db.commit()
        db.close()


    def navigate(event):
      page.clean()
      
      if page.navigation_bar.selected_index == 0:
        page.add(panel_register)
        
      elif page.navigation_bar.selected_index == 1:
        page.add(panel_auth)
        
      elif page.navigation_bar.selected_index == 2:
        user_list.controls.clear()
        
        db = sqlite3.connect('myusers.db')
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM users ")
        result = cursor.fetchall()
        
        if result != None:
          for user in result:
            user_list.controls.append(fl.Row([
              fl.Text(f'User {user[1]}'),
              fl.Icon(fl.icons.VERIFIED_USER_ROUNDED)
            ]
                                             ))
            
        cursor.close()    
        db.commit()
        db.close()
        
        page.add(panel_cabinet)
        
        
    user_login_field = fl.TextField(label='Имя пользователя', width=200, on_change=validate)
    user_password_field = fl.TextField(label='Пароль', width=200, on_change=validate)
    confirm_reg_button = fl.OutlinedButton(text='Подтвердить', width=200, disabled=True, on_click=register)
    confirm_auth_button = fl.OutlinedButton(text='Войти', width=200, disabled=True, on_click=authorization)
    
    panel_start = fl.Row(
          [fl.Text('Добро пожаловать в YourApp!')], alignment=fl.MainAxisAlignment.CENTER
        )
       
    user_list = fl.ListView(spacing=10, padding=20)
    
    panel_register = fl.Row(
            [
                fl.Column(
                    [
                        fl.Text('Регистрация'),
                        user_login_field,
                        user_password_field,
                        confirm_reg_button
                    ]
                )
            ],
            alignment=fl.MainAxisAlignment.CENTER
        )
    
    panel_cabinet = fl.Row(
            [
                fl.Column(
                    [
                        fl.Text('Личный кабинет'),
                        user_list
                    ]
                )
            ],
            alignment=fl.MainAxisAlignment.CENTER
        )
    
    panel_auth = fl.Row(
            [
                fl.Column(
                    [
                        fl.Text('Авторизация'),
                        user_login_field,
                        user_password_field,
                        confirm_auth_button
                    ]
                )
            ],
            alignment=fl.MainAxisAlignment.CENTER
        )
    
    page.navigation_bar = fl.NavigationBar(
      destinations=[
        fl.NavigationBarDestination(icon=fl.icons.VERIFIED_USER, label='Регистрация'),
        fl.NavigationBarDestination(icon=fl.icons.VERIFIED_USER_OUTLINED, label='Авторизация'),
      ], on_change=navigate
    )
    
    page.add(panel_start)

fl.app(target=main)

# https://www.youtube.com/watch?v=JJCjAUmNXBs
