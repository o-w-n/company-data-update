import multiprocessing
from multiprocessing import Pool, freeze_support

from script import get_company_data
from config import create_companies_list, kill_by_process, save_json, timed


@timed
def main() -> dict:
    main_dict = {}
    url_list = create_companies_list('db_local.csv')
    with Pool(processes=8) as pool:
        try:
            for company_dict in pool.imap_unordered(get_company_data, url_list):
                main_dict.update(company_dict)
        except Exception as ex:
            print(str(ex))
            pass
    # kill_by_process()
    return main_dict


if __name__ == '__main__':
    freeze_support()
    save_json(main())
