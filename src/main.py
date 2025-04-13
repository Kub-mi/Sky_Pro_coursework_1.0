from src.views import main_info

if __name__ == '__main__':
    date_request = '2018-03-20 15:30:00'
    result_views = main_info(date_request)
    print(result_views)