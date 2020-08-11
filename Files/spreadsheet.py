import os
import gspread
from dotenv import load_dotenv
from datetime import date

# env
load_dotenv()
users = [os.getenv("DISCRIMINATOR_1"), os.getenv("DISCRIMINATOR_2")]
SPREADSHEET_NUM = int(os.getenv("SPREADSHEET_NUM"))
sheet = gspread.service_account(filename=os.getenv("PATH_TO_CREDENTIALS"))\
    .open(os.getenv("SPREADSHEET_NAME")).get_worksheet(SPREADSHEET_NUM)

# constants
discriminator_col = {users[0]: 'B', users[1]: 'H'}
a = 65


def verify_spreadsheet_num_is_correct():
    row_1 = sheet.row_values(1)
    if len(row_1) < 11:
        raise AssertionError(f"you seem to be on the wrong spreadsheet: row length is less than 11")
    for i in range(4):
        if row_1[i] == row_1[i + 6]:
            pass
        else:
            raise AssertionError(f"you seem to be on the wrong spreadsheet: {row_1[i]} != {row_1[i + 6]}")


def get_last_open_row(sent_by):
    char = ord(discriminator_col[sent_by])
    str_list = list(filter(None, sheet.col_values(char - a + 1)))
    row_num = len(str_list) + 1
    return [f"{chr(char - 1)}{row_num}", f"{chr(char + 3)}{row_num}"]


def is_entry_from_today_present(sent_by):
    char = ord(discriminator_col[sent_by])
    date_col = list(filter(None, sheet.col_values(char - a)))
    return str(date.today()) in date_col


def process_date_info(info):
    upload_info = info
    if is_entry_from_today_present(f"{info[0]}"):
        upload_info[0] = ""
    else:
        upload_info[0] = str(date.today())
    return upload_info


def update_spreadsheet(info):
    verify_spreadsheet_num_is_correct()
    update_cells = get_last_open_row(f"{info[0]}")
    upload_info = process_date_info(info)
    cell_list = sheet.range(":".join(update_cells))
    for i in range(len(upload_info)):
        cell_list[i].value = upload_info[i]
    sheet.update_cells(cell_list)
    return f"Added \"{upload_info[1]}\" by {upload_info[2]} to the spreadsheet."
