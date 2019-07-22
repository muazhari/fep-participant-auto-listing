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

        if 'event_type' in event.keys():
            if event['event_type'] != 'message':
                self.send_message('Join event!')

        self.command_handler(event)

    def admin(self, args):
        data = {
            'event': args[-1]
        }
        event = data['event']
        if self.whitelist_check(event):
            self.send_message('privilage: {}'.format(event))

    def blacklist_check(self, event):
        sender = event['sender']

        blocked_ids = ['C7b132b65f0db5c28c4b7563bd348d168',
                       'C2a14eb4c73958925b6a299fe6798b67b']
        blocked_types = []

        validate = sender['id'] in blocked_ids or sender['name'] in blocked_types

        return validate

    def whitelist_check(self, event):
        sender = event['sender']

        allowed_ids = ['U016bfe22df53b903b404a80efdd8ec65', 'localuser']

        allowed_types = []

        validate_sender = sender['id'] in allowed_ids or sender['name'] in allowed_types

        return validate_sender

    def admin(self, args):
        data = {
            'event': args[-1]
        }
        event = data['event']
        if self.whitelist_check(event):
            self.send_message('privilage: {}'.format(event))

    def blacklist_check(self, event):
        sender = event['sender']

        blocked_ids = ['C7b132b65f0db5c28c4b7563bd348d168',
                       'C2a14eb4c73958925b6a299fe6798b67b']
        blocked_types = []

        validate = sender['id'] in blocked_ids or sender['name'] in blocked_types

        return validate

    def whitelist_check(self, event):
        sender = event['sender']

        allowed_ids = ['U016bfe22df53b903b404a80efdd8ec65', 'localuser']

        allowed_types = []

        validate_sender = sender['id'] in allowed_ids or sender['name'] in allowed_types

        return validate_sender

    def add(self, args):
        if len(args) == 5:
            data = {
                'batch': args[0],
                'name': args[1],
                'campus': args[2],
                'room': args[3],
                'user_id': args[-1]['sender']['id']
            }

            self.set_store(data)
            self.view([args[0], args[-1]])
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
                'user_id': args[-1]['sender']['id']
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
                'user_id': args[-1]['sender']['id']
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
                'user_id': args[-1]['sender']['id']
            }
            store = self.get_project_data('fep')

            if store is not None:

                if len(args) == 1:
                    selected_batch = sorted(store.keys())
                else:
                    selected_batch = [data['batch'].lower()]

                header = 'FEP BINUSIAN IT\n(Nama - Kampus - Nomor Ruangan)\n\n'

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

            if data['batch'] not in store.keys():
                store[data['batch']] = []

            selected_user_data = [data['name'], data['campus'], data['room']]

            store[data['batch']].append(selected_user_data)

            self.set_project_data({'fep': store})

    def update_store(self, data):
        if data['batch'].lower() in Bot.batch_list.keys():
            store = self.get_project_data('fep')

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
            default_url = 'https://gist.githubusercontent.com/muazhari/38a5819eb228a20a693db0516e76bedb/raw/5fe8b969ab5d3286f31026951edbb73ea030b460/feplist'

            data = {
                'url': default_url if len(args) == 1 else args[0],
                'user_id': args[-1]['sender']['id']
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

    def help(self):
        msg = '''
        add <batch> <name> <campus> <room> - .add a kamu Kemanggisan 000
        upd <batch> <number> <name> <campus> <room> - .upd a 1 kamu Kemanggisan 000
        del <batch> <number> - .del a 1
        view <batch> - .view a / .view
        '''
        self.send_message(msg)

    def command_handler(self, event):
        command_list = {'add': self.add,
                        'upd': self.update,
                        'del': self.delete,
                        'view': self.view,
                        'reset_store': self.reset_store,
                        'pre_store': self.pre_store,
                        'backup_store': self.backup_store,
                        ']]': self.admin,
                        'help': self.help,
                        }

        content_splitted = event['content'].split(' ')

        content_prefix = content_splitted[0][0]
        content_command = content_splitted[0][1:]

        content_args = list(map(str.strip, content_splitted[1:]))

        content_args.append(event)
        if content_prefix == Bot.command_prefix and content_command in command_list.keys():
            if len(getfullargspec(command_list[content_command]).args) > 1:
                command_list[content_command](content_args)
            else:
                command_list[content_command]()

    @command('bimay')
    def command_handlerbimay(self, event, context, args):
        pass

    @command('kurikulum')
    def command_kurikulum(self, event, context, args):
        pass

    @command('fep')
    def command_fep(self, event, context, args):
        pass

    @command('feprules')
    def command_feprules(self, event, context, args):
        pass

    @command('go')
    def command_go(self, event, context, args):
        pass

    @command('ao')
    def command_ao(self, event, context, args):
        pass

    @command('clo')
    def command_clo(self, event, context, args):
        pass

    @command('news')
    def command_news(self, event, context, args):
        pass

    @command('parttime')
    def command_parttime(self, event, context, args):
        pass

    @command('sat')
    def command_sat(self, event, context, args):
        pass

    @command('himti')
    def command_himti(self, event, context, args):
        pass

    @command(']]')
    def command_admin(self, event, context, args):
        self.send_message([event, context, args])
        pass
