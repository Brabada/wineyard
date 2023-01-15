from jinja2 import Environment, FileSystemLoader, select_autoescape

from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime


def get_wineyard_year():
    return datetime.now().year - datetime(year=1920, month=1, day=1).year


def year_declension(year):
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


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

wineyard_year = get_wineyard_year()
rendered_page = template.render(
    wineyard_year=f'{wineyard_year} {year_declension(wineyard_year)}'
)


with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
print(1)
server.serve_forever()
