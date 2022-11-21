import google_sheets_api
import bot

def main():
    google_sheets_api.start_refreshing_all_tables()
    bot.start()

if __name__ == '__main__':
    main()
