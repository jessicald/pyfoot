import message

import sys
import thread

class Network(object):
    def __init__(self, conf, irc):
        self.initial = True
        self.conf = conf
        self.irc = irc
        self.modules = []
        self.all_commands = []

        for modulename in conf.get('modules'):
            __import__('modules.'+modulename)
            module = sys.modules['modules.'+modulename]
            setattr(module.Module, 'name', modulename)
            self.modules.append(module.Module(self.irc, conf))
            self.all_commands.extend([c[0] for c in self.modules[-1].commands])

        for module in self.modules:
            module.all_commands = self.all_commands
            module.setDaemon(True)
            module.start()

    def dispatch(self, data):
        """ Deals with messages and sends modules the information they need. """
        if data == None:
            print ' :: no data'
            return None
        
        if data == '':
            print ' :: empty response, assuming disconnection\a' # alert
            sys.exit()

        for line in [line for line in data.split('\r\n') if len(line) > 0]:
            print '    %s' % line

            if line.startswith('PING :'):
                self.irc.pong(line)
            
            try:
                type = ''.join(line.split(':')[:2]).split(' ')[1]
            except(IndexError):
                type = None
            else:
                the_message = message.Message(line)
                
            if type == '353':
                # this is a channel names list
                pass

            if type == '324':
                # this is a list of channel modes
                splitline = line.split(' ')
                name = splitline[3]
                modelist = splitline[4]
                try:
                    self.irc.channels[name]['modes'] = modelist
                except KeyError:
                    self.irc.channels[name] = {}
                    self.irc.channels[name]['modes'] = modelist

            elif type == 'INVITE':
                channel = message.content(line)
                self.irc.join(channel)

            elif type == 'KICK':
                channel = message.content(line)
                self.irc.part(channel)

            elif type == 'NOTICE':
                pass

            elif type == 'NICK':
                pass

            elif type == 'MODE' and self.initial == True:
                for channel in self.conf.get('network_channels'):
                    self.irc.join(channel)

                self.initial = False

            elif type == 'PRIVMSG':
                for module in self.modules:
                    try:
                        module_blacklist = [c.lower for c in self.conf.get('module_blacklist')[module.name]]
                    except KeyError:
                        module_blacklist = []
                    
                    nick_blacklist = [n.lower() for n in self.conf.get('nick_blacklist')]

                    if the_message.source.lower() not in module_blacklist and the_message.nick.lower() not in self.conf.get('nick_blacklist'):
                        module.queue.put(the_message)
