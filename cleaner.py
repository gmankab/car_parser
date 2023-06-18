from pathlib import Path
import rich.console
import sys

c = rich.console.Console()
proj_path = Path(__file__).parent.resolve()
errors_path = proj_path.joinpath('errors')
lists_path = proj_path.joinpath('lists')
full_mails_path = lists_path.joinpath('full_mails.txt')
cleaned_path = lists_path.joinpath('cleaned.txt')
exceptions_path = lists_path.joinpath('exceptions.txt')


if sys.argv[-1].isdigit():
    startfrom = int(sys.argv[-1])
else:
    startfrom = 0


def remove_bad_chars(
    email: str,
) -> str: 
    result = ''
    chars_to_remove = '1234567890#№-'
    for char in email:
        if char not in chars_to_remove:
            result += char
    return result


def write(
    email: str,
    file_path: Path,
):
    if file_path.exists():
        with open(
            file_path,
            'r',
        ) as file:
            if email in file.read():
                return
    with open(
        file_path,
        'a',
    ) as file:
        file.write(
            email + '\n'
        )


def contains_bad_characters(
    email: str,
) -> bool | str:
    whitelist = 'abcdefghijklmnopqrstuvwxyz01234567890@-_.'
    for char in email:
        if char.lower() not in whitelist:
            return char.lower()
    return False


def clean(
    email: str,
) -> None:
    old_email = email
    # 1. если строчка начинается с цифры - удалить из строчки все цифры и знаки "-", при этом в середине строки цифры могут быть, главное чтобы не начинались с них
    if email[0].isdigit():
        email = remove_bad_chars(email)
        c.log(f'runned 1: {email}')
        
    # 1.1. если в емейле перед @ были только цифры, и после их удаления в начале емейла осталась только собачка, то цифры не убираем и пишем в отдельный файл
    if email[0] == '@':
        c.log(f'runned 1.1: {old_email}')
        write(
            old_email,
            exceptions_path,
        )
        return

    # 2. если есть знаки "№" или "#" - удалить эти знаки + удалить все цифры из строки
    for char in '#№':
        if char in email:
            email = remove_bad_chars(email)
            c.log(f'runned 2: {email}')
            break

    # 3. если в строке есть больше одной "@" - закинуть в отдельный файл, я руками переберу
    if email.count('@') > 1:
        c.log('runned 3')
        write(
            email,
            exceptions_path,
        )
        return

    # 4. если в строке есть знак "+" - закинуть в отдельный файл
    if '+' in email:
        c.log('runned 4')
        write(
            email,
            exceptions_path,
        )
        return

    # 5. если в строке есть левые символы (аля таких ����ǽ��g�s��{��.$O) - закинуть в отдельный файл
    bad_character = contains_bad_characters(email)
    if bad_character:
        c.log(f'runned 5, bad character "{bad_character}"')
        write(
            email,
            exceptions_path,
        )
        return

    # 6. строка также не может начинаться с "-", такие закинуть в отдельный файл
    if email[0] == '-':
        c.log('runned 6')
        write(
            email,
            exceptions_path,
        )
        return

    # 7. если заканчивается или начинается на точку, убрать ее
    if email[0] == '.' or email[-1] == '.':
        email = email.strip('.')
        c.log(f'runned 7: {email}')

    write(
        email,
        cleaned_path,
    )


def main():
    exceptions_path.unlink(
        missing_ok = True
    )
    cleaned_path.unlink(
        missing_ok = True
    )
    with open(
        full_mails_path,
        'r',
    ) as file:
        for index, line in enumerate(file):
            if index >= startfrom:
                email = line.strip()
                c.log(f'reading line {index}: {email}')
                clean(email)

main()

