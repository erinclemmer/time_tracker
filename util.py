from typing import List, Dict
from datetime import datetime, timedelta
import pandas as pd
import tkinter as tk

def pretty_time(d: timedelta) -> str:
    return str(d).split(".")[0]

def append_df(df, row):
    return pd.concat([df, pd.DataFrame.from_records([row])])   

def str_to_datetime(d: str) -> datetime:
    return datetime.strptime(d, '%y-%m-%d %H:%M:%S.%f')

def datetime_to_str(d: datetime) -> str:
    return d.strftime('%y-%m-%d %H:%M:%S.%f')

def pretty_duration(d):
    split = str(d).split('.')[0].split(':')
    return split[0] + ':' + split[1]

def double_digit_num(num: int) -> str:
    return str(num) if num > 9 else f'0{num}'

def get_number(title, prompt, min_num, max_num):
    num_str = tk.simpledialog.askstring(title, prompt)
    if num_str is None:
        return None
    try:
        num = int(num_str)
        if num < min_num or num > max_num:
            less_more = "more" if num < min_num else "less"
            n = min_num if num < min_num else max_num
            cont = tk.messagebox.askyesno('Error', f'Error: number must be {less_more} than {n}, try again?')
            if not cont:
                return None
            return get_number(title, prompt, min_num, max_num)
    except:
        cont = tk.messagebox.askyesno('Error', 'Error parsing number, try again?')
        if not cont:
            return None
        return get_number(title, prompt, min_num, max_num)
    return num

def ask_time(title):
    hour = get_number(title, 'Hour', 0, 23)
    if hour is None:
        return None
    minute = get_number(title, 'Minute', 0, 59)
    if minute is None:
        return None
    today = datetime.now()
    year_str = str(today.year)[2:]
    return str_to_datetime(f'{year_str}-{double_digit_num(today.month)}-{double_digit_num(today.day)} {double_digit_num(hour)}:{double_digit_num(minute)}:00.000000')