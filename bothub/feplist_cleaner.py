import requests


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


class cleaner:
    def __init__(self, url):
        self.file = requests.get(url).text.splitlines()
        self.store = {}

    def set_store(self, data):
        if data['batch'] not in self.store.keys():
            self.store[data['batch']] = []

        selected_user_data = [data[key]
                              for key in data.keys() if key not in ['batch']]

        self.store[data['batch']].append(selected_user_data)

    def run(self):
        for line in range(0, len(self.file)):
            if len(self.file[line]) > 0 and not hasNumbers(self.file[line][0]):
                batch = self.file[line][0].lower()
                continue

            lstrip = self.file[line].strip()
            lsplit = self.file[line].split('-')

            args = []
            for i in lsplit:
                args.append(i.strip())

            for i in args[0]:
                if hasNumbers(i):
                    args[0] = args[0].replace(i, '').strip()

            if len(args) >= 1 and '' not in args:
                if args[0][0] == '.':
                    args[0] = args[0][1:].strip()
                data = {
                    'batch': batch,
                    'name': args[0],
                    'campus': args[1],
                    'room': '' if len(args) < 3 else args[2],
                }
                self.set_store(data)
