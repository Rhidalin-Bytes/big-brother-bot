
__version__ = '1.1'
__author__  = 'Vermicious Knid'

import b3, re
import b3.events
# Import the necessary libaries you need here, for example, I need random for the randomization of answers part of it.
import random
#--------------------------------------------------------------------------------------------------
#This lot doesn't need to be changed for simple commands, it gets the admin plugin and registers commands.
class ModPlugin(b3.plugin.Plugin):
    _adminPlugin = None

    def startup(self):
      """\
      Initialize plugin settings
      """

   # get the admin plugin so we can register commands
      self._adminPlugin = self.console.getPlugin('admin')
      if not self._adminPlugin:
      # something is wrong, can't start without admin plugin
        self.error('Could not find admin plugin')
        return False
    
    # register our commands (you can ignore this bit)
      if 'commands' in self.config.sections():
        for cmd in self.config.options('commands'):
          level = self.config.get('commands', cmd)
          sp = cmd.split('-')
          alias = None
          if len(sp) == 2:
            cmd, alias = sp

          func = self.getCmd(cmd)
          if func:
            self._adminPlugin.registerCommand(self, cmd, level, func, alias)

      self.debug('Started')


    def getCmd(self, cmd):
      cmd = 'cmd_%s' % cmd
      if hasattr(self, cmd):
        func = getattr(self, cmd)
        return func

      return None
#--------------------------------------------------------------------
# Your commands go under here

    def cmd_fail(self, data, client=None, cmd=None):
        """\
        <player> - Notify a player that they had an Epic Fail
        """

        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            self.console.say('^3That was an EPIC FAIL!')
            return False

        if m[0] == 'b3':
            self._adminPlugin.warnClient(client, 'Whatever b3 does = Epic Win', None, False, '', 1)
        else:
            sclient = self._adminPlugin.findClientPrompt(m[0], client)
            if sclient:
                self.console.say('^1%s, ^3that was an EPIC FAIL!' % sclient.exactName)