from src.utils import get_correct_dates, PATH_TO_EXCEL
from src.utils import get_period

def main_info(date_time):
    start_date, end_date = get_correct_dates(date_time)
    sorted_df = get_period(PATH_TO_EXCEL, start_date, end_date)

    return {
        "start_date": start_date,
        "end _date": end_date,
        "sorted_df": sorted_df
    }
