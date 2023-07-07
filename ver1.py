import tkinter as tk
import ctypes
import wmi
import json

#c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")

class battery_c():
    def __init__(self):
        pass

    def updatebatterystats(self):
        batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
        for i, b in enumerate(batts):
            self.full = b.FullChargedCapacity
            break

        batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batts):
            self.discharge = b.DischargeRate
            # print '\nBattery %d ***************' % i
            # print 'Tag:               ' + str(b.Tag)
            # print 'Name:              ' + b.InstanceName

            # print 'PowerOnline:       ' + str(b.PowerOnline)
            # print 'Discharging:       ' + str(b.Discharging)
            # print 'Charging:          ' + str(b.Charging)
            # print 'Voltage:           ' + str(b.Voltage)
            # print 'DischargeRate:     ' + str(b.DischargeRate)
            # print 'ChargeRate:        ' + str(b.ChargeRate)
            self.remainecapacity = b.RemainingCapacity
            # print 'Active:            ' + str(b.Active)
            # print 'Critical:          ' + str(b.Critical)
            self.percent = round( (self.remainecapacity/self.full)*100, 2)
            break

    def label(self):
        self.updatebatterystats()
        str = f'{self.percent}%, {int(self.discharge/1000)}'
        return str  # label str


battery = battery_c()

def F1():
    # batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
    # for i, b in enumerate(batts):
    #     print ('Battery %d Fully Charged Capacity: %d mWh' % 
    #         (i, b.FullChargedCapacity))

    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    
    for i, b in enumerate(batts):
        return str(b.DischargeRate/1000)
        # print '\nBattery %d ***************' % i
        # print 'Tag:               ' + str(b.Tag)
        # print 'Name:              ' + b.InstanceName

        # print 'PowerOnline:       ' + str(b.PowerOnline)
        # print 'Discharging:       ' + str(b.Discharging)
        # print 'Charging:          ' + str(b.Charging)
        # print 'Voltage:           ' + str(b.Voltage)
        # print 'DischargeRate:     ' + str(b.DischargeRate)
        # print 'ChargeRate:        ' + str(b.ChargeRate)
        # print 'RemainingCapacity: ' + str(b.RemainingCapacity)
        # print 'Active:            ' + str(b.Active)
        # print 'Critical:          ' + str(b.Critical)
    

def add_window_to_alt_tab():
    # Получаем хэндл окна
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    # Добавляем окно в список Alt+Tab
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    extended_style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    extended_style = extended_style | WS_EX_APPWINDOW
    extended_style = extended_style & ~WS_EX_TOOLWINDOW
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, extended_style)


#def F1():
    # Ваш код для функции F1
#    return "Привет, мир!"

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def move_window(event):
    root.geometry(f"+{event.x_root - root_width // 2}+{event.y_root - root_height // 2}")
    save_window_config()


def changetop():
    root.attributes("-topmost", not root.attributes("-topmost"))  # Изменяем атрибут "topmost" окна



root = tk.Tk()
root.overrideredirect(True)  # Убираем заголовок окна
root_width = 70
root_height = 25
root.geometry(f"{root_width}x{root_height}")  # Размер окна 20x50 пикселей
root.attributes("-topmost", not root.attributes("-topmost"))

label = tk.Label(root, text="", width=20, height=5)  # Создаем метку для вывода текста
label.configure(bg="black", fg="white")
label.pack()

# Создаем контекстное меню

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Поверх всех окон", command=changetop)
context_menu.add_command(label="Пункт 2")
context_menu.add_command(label="Пункт 3")

root.bind("<Button-3>", show_context_menu)  # При нажатии правой кнопкой мыши показываем контекстное меню
root.bind("<ButtonPress-1>", lambda event: root.geometry(f"+{event.x_root - root_width // 2}+{event.y_root - root_height // 2}"))
root.bind("<B1-Motion>", move_window)


def update_label():
    label.config(text=battery.label())
    root.after(1000, update_label)  # Вызываем функцию каждую секунду
update_label()

root.after(100, add_window_to_alt_tab)


#========================= config +++++++++++++++++++++++
CONFIG_FILE = 'battery.txt'
def save_window_config():
    config = {
        "x": root.winfo_x(),
        "y": root.winfo_y()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_window_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        return None        

# Загрузка конфигурации окна
config = load_window_config()
if config:
    root.geometry(f"+{config['x']}+{config['y']}")


#================ popup ==============
# def show_popup(event):
#     popup = tk.Toplevel(root)
#     popup.title("Всплывающее окно")
#     popup.geometry("200x100")
#     popup.resizable(False, False)

#     label = tk.Label(popup, text="Привет, это всплывающее окно!")
#     label.pack(pady=20)

#     popup.focus_force()  # Перенаправляем фокус на всплывающее окно



# root.bind("<Enter>", show_popup)  # Отображаем всплывающее окно при наведении мыши
# root.bind("<Leave>", hide_popup)  # Скрываем всплывающее окно при убирании мыши

#==================================================================


root.mainloop()
