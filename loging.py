import datetime


def printl(*string):
    try:
        s = ''
        for i in string:
            s = f'{s} {str(i)}'
        with open('log.txt', 'a') as file:
            file.write(f'{s}\t{datetime.datetime.now()}\n')
            file.close()
    except ValueError as e:
        print(f'Не удалось сделать запись в log {e}')
