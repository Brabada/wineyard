from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
import collections
import argparse


def get_wineyard_year():
    WINEYARD_FOUNDING_YEAR = 1920
    return datetime.now().year - WINEYARD_FOUNDING_YEAR


def get_year_declension(year):
    """Returns declension of word 'years' by year number"""

    if 5 < year < 21:
        return 'лет'

    year_word = ''
    last_year_digit = year % 10
    if last_year_digit == 1:
        year_word = 'год'
    elif 1 < last_year_digit < 5:
        year_word = 'года'
    elif last_year_digit == 0 or last_year_digit >= 5:
        year_word = 'лет'

    return year_word


def main():
    parser = argparse.ArgumentParser(description='This program running '
                                                 'site with wineyard and '
                                                 'load data from excel file '
                                                 'for template.')
    parser.add_argument('excel_db',
                        help='Name of excel_db file',
                        type=str,
                        default='wine.xlsx')
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    drinks_excel = pandas.read_excel(args.excel_db,
                                     na_values=None,
                                     keep_default_na=False)

    drinks = drinks_excel.to_dict(orient='records')
    drinks_by_category = collections.defaultdict(list)
    for drink in drinks:
        buffer = {
                'Картинка': drink['Картинка'],
                'Название': drink['Название'],
                'Сорт': drink['Сорт'],
                'Цена': drink['Цена'],
                'Акция': drink['Акция'],
        }
        drinks_by_category[drink['Категория']].append(buffer)

    wineyard_year = get_wineyard_year()
    rendered_page = template.render(
        wineyard_year=f'{wineyard_year} {get_year_declension(wineyard_year)}',
        drinks=drinks_by_category
    )

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
