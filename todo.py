# Tkinterをtkという名前でインポート
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.messagebox as tkm
# ほか必要なものをインポート
from tkcalendar import Calendar
import datetime
import csv
import os

# Tk()はトップレベルウィンドウを生成
root = tk.Tk()
# タイトルを設定
root.title("ToDo app")
# 画面サイズを設定(xは小文字のエックス)
root.geometry("470x400")

# トップレベルウィンドウはメインの画面で、閉じるとアプリ自体を終了する。
# pack/grid/placeを混在させるためのフレームを作成
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)

# 実行時にリストを作成
task_list = []
# リストボックスの中身
var_listbox = tk.StringVar(value=task_list)

# -------処理---------
def load_task():
    global task_list
    if os.path.exists("task_list_csv.csv"):
        try:
            with open("task_list_csv.csv", "r", encoding="utf-8") as file:
                data = csv.DictReader(file)
                task_list.clear()  # 既存のタスクリストをクリア
                for row in data:
                    task_list.append(f"{row['日付']}:{row['タスク']} {row['時間']} - {row['状態']}")
        except Exception as e:
            tkm.showerror("エラー", f"タスクリストファイルの読み込み中にエラーが発生しました: {e}")
    else:
        tkm.showerror("エラー", "タスクリストファイルが見つかりません。")

    update_task()

def add_task():
    data = cal_entry.get()
    task_information = task_entry.get()
    time = times_hour_minutes.get()
    if not data or not task_information or not time:
        tkm.showerror("エラー", "日付・タスク・時間のどれか一つが入力されていません")
    else:
        task_list.append(f"{data}:{task_information} {time} - ❌")
        var_listbox.set(task_list)
        update_task()
        save_csv(data, task_information, time, "❌")

        cal_entry.delete(0, tk.END)
        task_entry.delete(0, tk.END)
        times_hour_minutes.delete(0,tk.END)

def deleted_task():
    try:
        selected_indices = listbox.curselection()
        if not selected_indices:
            raise ValueError

        for index in reversed(selected_indices):
            del task_list[index]

        update_task()
        save_all_tasks()  # CSVを更新

    except ValueError:
        tkm.showerror("エラー", "削除するタスクが選択されていません。")

def checks_task():
    try:
        selected_indices = listbox.curselection()
        if not selected_indices:
            raise ValueError
        
        for index in selected_indices:
            task_list[index] = task_list[index].replace("❌", "✅")

        update_task()
        save_all_tasks()  # CSVを更新
    except ValueError:
        tkm.showerror("エラー", "タスクが選択されていません。")

def update_task():
    var_listbox.set(task_list)

def get_calender():
    cal_entry.delete(0, tk.END)
    
    now_days = datetime.date.today()
    year = now_days.year
    month = now_days.month
    day = now_days.day + 1

    cal_entry.insert(0,f"{year}/{month}/{day}")

    calender_window = tk.Toplevel(root)
    calender_window.title("カレンダー")
    calender_window.geometry("350x220")

    calender = Calendar(
        calender_window,
        selectmode='day',
        year=year,
        month=month,
        day=day
    )
    calender.pack()

    cal_data = tk.Button(
        calender_window,
        text="確定",
        command=lambda: get_cal(calender,calender_window)
    )

    cal_data.pack()

def get_cal(calender,calender_window):
    cal_entry.delete(0, tk.END)
    calender_item = calender.get_date()
    cal_entry.insert(0, calender_item)
    calender_window.destroy()

def open_clock():
    times_hour_minutes.delete(0, tk.END)

    clocked_window = tk.Toplevel(root)
    clocked_window.title("時計")
    clocked_window.geometry("235x80")
    # 時間と分のリストを作成
    hour = [str(i).zfill(2) for i in range(24)]
    minute = [str(i).zfill(2) for i in range(60)]

    # ------------------
    times_hour_label = tk.Label(
        clocked_window,
        text="時間"
    )

    times_hour_label.grid(row=0, column=0, padx=5, pady=5)

    # 時間のboxを作成
    hour_box = ttk.Combobox(
        clocked_window,
        values=hour,
        width=5
    )
    hour_box.grid(row=0, column=1, padx=5, pady=5)

    times_minutes_label = tk.Label(
        clocked_window,
        text="分"
    )
    times_minutes_label.grid(row=0, column=2, padx=5, pady=5)

    # 分のboxを作成
    minute_box = ttk.Combobox(
        clocked_window,
        values=minute,
        width=5
    )
    minute_box.grid(row=0, column=3, padx=5, pady=5)

    # 時間と分をclock_entryに追加
    add_clock = tk.Button(
        clocked_window,
        text="確定",
        command=lambda: add_clock_entry(hour_box.get(), minute_box.get(), clocked_window)
    )
    add_clock.grid(row=1, column=0, columnspan=5, pady=5)

def add_clock_entry(hours, minutes, clocked_window):
    if "" == hours or "" == minutes:
        tkm.showerror("エラー","時間または分が入力されていません")
    else:
        times_hour_minutes.insert(0, f"{hours}時{minutes}分")
        clocked_window.destroy()

def save_csv(data, info, time, condition):
    with open("task_list_csv.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([data, info, time, condition])

def save_all_tasks():
    with open("task_list_csv.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["日付", "タスク", "時間", "状態"])  # ヘッダーを書き込む
        for task in task_list:
            parts = task.split(':')
            date = parts[0]
            rest = parts[1].split(' ')
            task_info = rest[0]
            time_info = rest[1].strip('()')  # 状態を除去
            state = "❌" if "❌" in task else "✅"
            writer.writerow([date, task_info, time_info, state])

# --------------------
# 保存されたタスク履歴をリストに入れる
load_task()

# ---------ウィンドウ内部---------
task_label = tk.Label(
    frame1,
    text="タスク一覧"
)

# リストボックスの作成
listbox = tk.Listbox(
    frame1,
    listvariable=var_listbox,
    selectmode=tk.MULTIPLE,
    width=50
)

# カレンダー
cal_label = tk.Label(
    frame2,
    text="YYYY/MM/DD"
)

cal_button = tk.Button(
    frame2,
    text="🗓️",
    command=get_calender
)

cal_entry = tk.Entry(
    frame2,
    width=10
)
cal_entry.insert(0, "日付を入力")

# タスクの書き込み
task_l = tk.Label(
    frame2,
    text="予定"
)
task_entry = tk.Entry(
    frame2,
    width=20
)

# 時間
time_label = tk.Label(
    frame2,
    text="時間"
)
times_hour_minutes = tk.Entry(
    frame2,
    width=10
)
times_hour_minutes.insert(0, "時間を入力")

clock_times = tk.Button(
    frame2,
    text="🕛",
    command=open_clock
)

# 記述した上記三つをリストに格納
task_Button = tk.Button(
    frame3,
    text="追加",
    command=add_task
)

# タスクにチェックをつける
task_check = tk.Button(
    frame3,
    text="完了",
    command=checks_task
)

# タスクを削除する
task_deleted_button = tk.Button(
    frame3,
    text="タスクの削除",
    command=deleted_task
)

# ------------------------------

# ウィンドウ内部のウィジェット配置
task_label.pack()
listbox.pack()

# カレンダーのエントリとボタンを配置
cal_label.grid(row=0, column=0, sticky="ew")
cal_entry.grid(row=0, column=1, sticky="ew")
cal_button.grid(row=0, column=2, sticky="ew")

# タスクのエントリを配置
task_l.grid(row=1, column=0)
task_entry.grid(row=1, column=1)

# 時間のエントリとボタンを配置
time_label.grid(row=2, column=0, sticky="ew")
times_hour_minutes.grid(row=2, column=1, sticky="ew")
clock_times.grid(row=2, column=2, sticky="ew")

# タスクを追加するボタン
task_Button.pack()
task_check.pack()
task_deleted_button.pack()

frame1.pack()
frame2.pack()
frame3.pack()

# トップレベルウィンドウの処理を開始
root.mainloop()