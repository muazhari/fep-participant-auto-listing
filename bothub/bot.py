# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel
from bothub_client.decorators import command

from inspect import getfullargspec

import requests
from datetime import datetime

from bothub.feplist_cleaner import cleaner


class Bot(BaseBot):
    """Represent a Bot logic which interacts with a user.

    BaseBot superclass have methods belows:

    * Send message
      * self.send_message(message, chat_id=None, channel=None)
    * Data Storage
      * self.set_project_data(data)
      * self.get_project_data()
      * self.set_user_data(data, user_id=None, channel=None)
      * self.get_user_data(user_id=None, channel=None)
    * Channel Handler
      from bothub_client.decorators import channel
      @channel('<channel_name>')
      def channel_handler(self, event, context):
        # Handle a specific channel message
    * Command Handler
      from bothub_client.decorators import command
      @command('<command_name>')
      def command_handler(self, event, context, args):
          # Handle a command('/<command_name>')
    * Intent Handler
      from bothub_client.decorators import intent
      @intent('<intent_id>')
      def intent_result_handler(self, event, context, answers):
          # Handle a intent result
          # answers is a dict and contains intent's input data
            {
              "<intent slot id>" : <entered slot value>
              ...
            }
    """
    batch_list = {
        'a': '22 - 27 JULI 2019',
        'b': '29 JULI - 3 AGUSTUS 2019',
        'c': '5 - 10 AGUSTUS 2019',
        'd': '19 - 24 AGUSTUS 2019',
        'e': '26 - 03 SEPTEMBER 2019',
    }

    command_prefix = '.'

    @channel()
    def default_handler(self, event, context):
        """Handle a message received

        event is a dict and contains trigger info.

        {
           "trigger": "webhook",
           "channel": "<name>",
           "sender": {
              "id": "<chat_id>",
              "name": "<nickname>"
           },
           "content": "<message content>",
           "raw_data": <unmodified data itself webhook received>
        }
        """

        # self.send_message('Echo: {}'.format(event['content']))
        self.command(event)

    def add(self, args):
        if len(args) == 5:
            data = {
                'batch': args[0],
                'name': args[1],
                'campus': args[2],
                'room': args[3],
                'user_id': args[-1]
            }

            self.set_store(data)
            self.view([args[0], args[-1]])
            # self.send_message('Done!')
            self.backup_store('silent')
        else:
            self.send_message(Bot.command_prefix
                              + 'add <batch> <name> <campus> <room>')

    def update(self, args):
        if len(args) == 6:
            data = {
                'batch': args[0],
                'num': args[1],
                'name': args[2],
                'campus': args[3],
                'room': args[4],
                'user_id': args[-1]
            }

            self.update_store(data)
            self.send_message('Done!')
            self.backup_store('silent')
        else:
            self.send_message(Bot.command_prefix
                              + 'upd <batch> <number> <name> <campus> <room>')

    def delete(self, args):
        if len(args) == 3:
            data = {
                'batch': args[0],
                'num': args[1],
                'user_id': args[-1]
            }
            self.delete_store(data)
            self.send_message('Done!')
            self.backup_store('silent')
        else:
            self.send_message(Bot.command_prefix
                              + 'del <batch> <number>')

    def view(self, args):
        if len(args) <= 2:
            data = {
                'batch': args[0],
                'user_id': args[-1]
            }
            store = self.get_project_data('fep')

            if len(args) == 1:
                selected_batch = sorted(store.keys())
            else:
                selected_batch = [data['batch'].lower()]

            header = 'FEP BINUSIAN IT\n(Nama - Kampus - Nomor Ruangan)\n\n'

            if store != None:
                # for batch in store.keys():
                #     msg += '{}. {}\n'.format(batch.upper(), Bot.batch_list[batch])
                #     for user, i in zip(store[batch].keys(), range(1, len(store[batch].keys()) + 1)):
                #         msg += '{}. {} - {} - {}\n'.format(
                #             i,  store[batch][user]['name'], store[batch][user]['campus'], store[batch][user]['room'])
                #
                #     msg += '\n'

                for batch in selected_batch:
                    msg = header + \
                        '{}. {}\n'.format(batch.upper(), Bot.batch_list[batch])
                    for i in range(0, len(store[batch])):
                        msg += '{}. {} - {} - {}\n'.format(
                            i + 1, store[batch][i][0], store[batch][i][1], store[batch][i][2])

                    msg += '\n'
                    self.send_message(msg)
        else:
            self.send_message(Bot.command_prefix
                              + 'view <batch>')

    def set_store(self, data):
        if data['batch'].lower() in Bot.batch_list.keys():

            store = self.get_project_data('fep')

            # if data['batch'] not in store.keys():
            #     store[data['batch']] = {}
            #
            # selected_user_data = {key: data[key]
            #                       for key in data.keys() if key not in ['batch', 'user_id']}
            #
            # store[data['batch']][data['user_id']] = selected_user_data

            if data['batch'] not in store.keys():
                store[data['batch']] = []

            # selected_user_data = {key: data[key]
            #                       for key in data.keys() if key not in ['batch', 'user_id']}
            selected_user_data = [data['name'], data['campus'], data['room']]

            store[data['batch']].append(selected_user_data)

            self.set_project_data({'fep': store})

    def update_store(self, data):
        if data['batch'].lower() in Bot.batch_list.keys():
            store = self.get_project_data('fep')
            # if data['batch'] not in store.keys():
            #     store[data['batch']] = {}
            #
            # selected_user_data = {key: data[key]
            #                       for key in data.keys() if key not in ['batch', 'user_id']}
            #
            # store[data['batch']][data['user_id']] = selected_user_data

            try:
                selected_user_data = [data['name'],
                                      data['campus'], data['room']]

                store[data['batch']][int(
                    data['num']) - 1] = selected_user_data

                self.set_project_data({'fep': store})

            except KeyError:
                self.set_store(data)

    def delete_store(self, data):
        store = self.get_project_data('fep')
        # for key in store.keys():
        #     if data['user_id'] in store[key]:
        #         store[key].pop(data['user_id'], None)
        #         self.set_project_data(store)
        # store[data['batch']].pop(int(data['num']) - 1)

        store[data['batch']].pop(int(data['num']) - 1)
        if len(store[data['batch']]) == 0:
            store.pop(data['batch'], None)

        self.set_project_data({'fep': store})

    def reset_store(self):
        store = self.get_project_data()

        self.set_project_data({'fep': {}})
        self.send_message('Done!')

    def pre_store(self, args):
        if len(args) <= 2:
            default_url = 'https://gist.githubusercontent.com/muazhari/38a5819eb228a20a693db0516e76bedb/raw/108e665e24b63184f92444436b83142a4bf1fb0b/feplist'

            data = {
                'url': default_url if len(args) == 1 else args[0],
                'user_id': args[-1]
            }

            feplc = cleaner(data['url'])
            feplc.run()
            store = feplc.store
            self.set_project_data({'fep': store})
            self.send_message('Done!')
        else:
            self.send_message(Bot.command_prefix
                              + 'pre_store <url>')

    def backup_store(self, args=None):
        headers = {'Content-type': 'application/json'}

        store = self.get_project_data('fep')
        backup_store = self.get_project_data('backup')

        if backup_store is None:
            backup_store = {'fep': []}
        else:
            backup_store = backup_store['fep'][-20:]

        response = requests.post(
            'https://paste.c-net.org/', headers=headers, data=store)

        if args is None or args != 'silent':
            self.send_message('Done!\n{}'.format(response.text))

        backup_store['fep'].append({datetime.now(): response})
        self.set_project_data({'fep': store, 'backup': backup_store})

    def command(self, event):
        command_list = {'add': self.add,
                        'upd': self.update,
                        'del': self.delete,
                        'view': self.view,
                        'reset_store': self.reset_store,
                        'pre_store': self.pre_store,
                        'backup_store': self.backup_store
                        }

        content_splitted = event['content'].split(' ')

        content_prefix = content_splitted[0][0]
        content_command = content_splitted[0][1:]

        content_args = content_splitted[1:]

        content_args.append(event['sender']['id'])

        if content_prefix == Bot.command_prefix and content_command in command_list.keys():
            if len(getfullargspec(command_list[content_command]).args) > 1:
                if '' not in content_args:
                    command_list[content_command](content_args)
            else:
                command_list[content_command]()
