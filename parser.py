from bs4 import BeautifulSoup as Bs
from pathlib import Path
import duckduckgo_search
import yagooglesearch
import search_engines
import urllib.parse
import rich.console
import datetime
import requests
import sys

    
c = rich.console.Console()
proj_path = Path(__file__).parent.resolve()
errors_path = proj_path.joinpath('errors')
lists_path = proj_path.joinpath('lists')
deler_emails_path = lists_path.joinpath('deler_emails.txt')
emails_only_path = lists_path.joinpath('emails_only.txt')
delerships_path = lists_path.joinpath('delerships.txt')

if sys.argv[-1].isdigit():
    startfrom = int(sys.argv[-1])
else:
    startfrom = 0


def pretty(
    link: str,
) -> str:
    link = urllib.parse.unquote(
        link
    )
    for trash in (
        'https://',
        'http://',
        'www.',
    ):
        link = link.replace(
            trash,
            '',
        )
    link = link.rstrip('/')
    return link


def write_error() -> str:
    max_errors_in_dir = 30
    errors_path.mkdir(
        exist_ok = True,
        parents = True,
    )
    all_errors = list(
        errors_path.iterdir()
    )
    all_errors.sort()
    while len(
        all_errors
    ) >= max_errors_in_dir:
        all_errors[0].unlink()
        all_errors.remove(all_errors[0])
    file_date = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M")
    test_error_path = errors_path.joinpath(file_date)
    error_path = Path(
        f'{test_error_path}.txt'
    )
    index = 2
    while error_path.exists():
        error_path = Path(
            f'{test_error_path}_{index}.txt'
        )
        index += 1
    with open(
        error_path,
        'w',
        encoding = "utf-8",
    ) as file:
        c_error = rich.console.Console(
            width = 80,
            file = file,
        )
        c_error.print_exception(
            show_locals = True
        )
    c.log(f'error written to {error_path}')
    return str(error_path)


class Searcher:
    def __init__(
        self,
        deler: str,
    ):
        self.deler: str = deler
        self.deler_spaces = ' '.join(deler.split('_'))
        self.done: set = set()
        self.email: str = ''

    def ddg(
        self,
    ) -> None:
        c.log(f'searching duck duck go for {self.deler_spaces}')
        with duckduckgo_search.DDGS() as ddgs:
            for result in ddgs.text(
                keywords = self.deler_spaces,
                region = 'ru-ru',
                safesearch = 'off',
                timelimit = '5',
            ):
                link = result.get('href', '')
                if not link:
                    continue
                if link in self.done:
                    continue
                link = pretty(link)
                self.parse_page(link)
                if self.email:
                    return

    def google(
        self,
    ) -> None:
        c.log(f'searching google for {self.deler_spaces}')
        client = yagooglesearch.SearchClient(
            query = self.deler_spaces,
            max_search_result_urls_to_return = 10,
            verbosity = 0,
            verbose_output = False,
        )
        client.assign_random_user_agent()
        results_list = client.search()
        if results_list:
            for result in results_list:
                link = pretty(result)
                if link in self.done:
                    continue
                self.parse_page(link)

    def bing(
        self,
    ) -> None:
        c.log(f'searching bing for {self.deler_spaces}')
        bing = search_engines.Bing(
            timeout = 5
        )
        results = bing.search(
            query = self.deler,
            pages = 1,
        )
        for link in results.links():
            self.parse_page(
                pretty(link)
            )
            if self.email:
                return

    def parse_page(
        self,
        link: str,
    ) -> None:
        try:
            if 'bing.com/ck/a' in link:
                self.done.add(link)
                response = requests.get(
                    'https://' + link,
                    timeout = 5,
                )
                soup = Bs(
                    response.text,
                    'html.parser',
                )
                text = str(soup.find('script'))
                start = text.find('var u = "') + 9
                end = text.find('"', start)
                link = pretty(
                    text[start:end]
                )
            self.done.add(link)
            c.log(
                f'searching for emails in {link}'
            )
            response = requests.get(
                'https://' + link,
                timeout = 5,
            )
            soup = Bs(
                response.text,
                'html.parser',
            )
            for email in soup.text.split():
                if '@' in email and '.' in email and '/' not in email:
                    c.log(f'[bold green]found email {email}')
                    self.email = email
                    if emails_only_path.exists():
                        with open(
                            emails_only_path,
                            'r',
                        ) as file:
                            if email in file.read():
                                c.log('already writed')
                                return
                    with open(
                        emails_only_path,
                        'a',
                    ) as file:
                        file.write(
                            self.email + '\n',
                        )
                    with open(
                        deler_emails_path,
                        'a',
                    ) as file:
                        file.write(
                            f'{self.deler} - {self.email}\n',
                        )
                    return
        except KeyboardInterrupt as ki:
            raise ki
        except Exception:
            write_error()


def search_deler_emails(
    deler: str
) -> None:
    searcher = Searcher(deler)
    for search_engine in (
        searcher.ddg,
        searcher.google,
        searcher.bing,
    ):
        try:
            search_engine()
            if searcher.email:
                return
        except KeyboardInterrupt as ki:
            raise ki
        except Exception:
            write_error()
            continue
    if not searcher.email:
        with open(
            deler_emails_path,
            'a',
        ) as file:
            file.write(
                f'{searcher.deler} - none\n',
            )
        return


def main():
    with open(
        delerships_path,
        'r',
    ) as file:
        for index, line in enumerate(file):
            try:
                if index >= startfrom:
                    c.log(f'reading line {index}')
                    splitted = line.rsplit('/', 2)
                    deler = splitted[-2]
                    search_deler_emails(deler)
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                write_error()


main()

