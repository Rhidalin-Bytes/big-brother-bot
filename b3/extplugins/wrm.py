#*************************************************************************************
#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# WRM (Wolfsbanes Realism Mod) (www.1stsfss.org)      
#
# This program is free software and licensed under the terms of
# the GNU General Public License (GPL), version 2.
#
# http://www.gnu.org/copyleft/gpl.html
#
# This plugin is designed to be used with WRM.
#
# WRM Download Locations
#*************************************************************************************
# http://www.1stsfss.org/viewtopic.php?t=1947 
# http://callofduty.filefront.com/file/Wolfsbanes_CoD2_Realism_Mod;55086
#*************************************************************************************
#
# Installation:
#*************************************************************************************
# NOTE: Playerinfo-PI moved to countryfilter.py / countryfilter.xml
# 1. Place wrm.py  in the folder [../b3/extplugins]
# 2. Place wrm.xml in the folder [../b3/extplugins/conf]
# 3. Modify the wrm.xml commands to your desiered settings
# 4. Modify the b3.xml to include the path of the plugin
# Example: <plugin name="wrm" priority="15" config="@b3/extplugins/conf/wrm.xml"/>
#*************************************************************************************
#
# Requirements:
#*************************************************************************************
# Call of Duty 2 server
# B3 version 1.1.0 or higher
#*************************************************************************************
#
#Changelog
#*************************************************************************************
#v1.0.0         : Initial Release - 01-19-2006 (Version 6.5c)
#v1.1.0         : Change Release -  05-07-2006 (Version 6.5d)
#*************************************************************************************
#
#Created By: Senator aka SoggyOreo 
#Date      : 05-07-2006
#Email     : senatorreturns@hotmail.com
#Website   : www.the82ndab.com

__version__ = '1.1.0'
__author__  = 'Senator'

import sys, re, b3, threading, string
#import b3, re, string
import b3.events
import b3.functions
import b3.clients
import b3.extplugins.countryfilter
#import b3.extplugins.GeoIP.PurePythonGeoIP
#from b3.extplugins.GeoIP.PurePythonGeoIP import GeoIP

#-------------------------------------------------------------
class WrmPlugin(b3.plugin.Plugin):
  _adminPlugin = None
  _parseUserCmdRE = re.compile(r'^(?P<cid>\'[^\']{2,}\'|[0-9]+|[^\s]{2,}|@[0-9]+)\s?(?P<parms>.*)$')
  cf_country_print_mode = 'name'  
  gi = None

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
    
#    self.gi = GeoIP.open('@b3\extplugins\GeoIP\GeoIP.dat', GeoIP.GEOIP_STANDARD)
    self.registerEvent(b3.events.EVT_CLIENT_AUTH)
    self.debug('Started')
    
    # register our commands
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
    
  def parseUserCmd(self, cmd, req=False):
		m = re.match(self._parseUserCmdRE, cmd)

		if m:
			cid = m.group('cid')
			parms = m.group('parms')

			if req and not len(parms): return None

			if cid[:1] == "'" and cid[-1:] == "'":
				cid = cid[1:-1]

			return (cid, parms)
		else:
			return None
  
  def findClientPrompt(self, id, client=None):
		matches = self.console.clients.getByMagic(id)
		if matches:
			if len(matches) > 1:
				names = []
				for p in matches:
					names.append('[^2%s^7] %s' % (p.cid, p.name))

				if client:
					client.message(self.getMessage('players_matched', id, string.join(names, ', ')))
				return False
			else:
				return matches[0]
		else:
			if client:
				client.message(self.getMessage('no_players', id))
			return None

  def onEvent(self, event):
    """\
    Handle intercepted events
    """    

#**START OF WRM COMMANDS**

  def cmd_wrmvsclan(self, data, client, cmd=None):
    """\
    <tags> - Set the clan tags for a clan vs. match (colors excluded)  
    """
    # we need the cvar of the clan tags
    var_vsclan = self.console.getCvar('wrm_clanTags')[0]
    if not data:         
         if not var_vsclan:
               # it hasnt been set in the config yet, no problem                
               client.message('^7No clan set yet, use !help wrmvsclan for usage')
               return False
         else:
               cmd.sayLoudOrPM(client, '^7Current clan tags: ^1%s' % var_vsclan)
               return False
    else:
      # check to see what they entered
      if data == 'none':
           self.console.setCvar( 'wrm_clanTags','')
           self.console.say('^9Clan tags set to : ^1none')
      else:
           self.console.setCvar( 'wrm_clanTags','%s' % data )
           self.console.say('^9Clan tags set to : ^1%s' % data)
    return True
    
  def cmd_wrmceasefire(self, data, client, cmd=None):
    """\
    <on/off> - Put server into cease fire mode
    """
    # we need the cvar of the cease fire mode
    var_cfmode = self.console.getCvar('wrm_ceaseFire')[0]    
    if not data:         
         if not var_cfmode:
               # it hasnt been set in the config yet, no problem                
               client.message('^7Unable to find Cease Fire mode value')
               return False
         else:
               cmd.sayLoudOrPM(client, '^7Cease Fire Value: ^1%s' % var_cfmode)
               return False
    else:
      # check to see what they entered
      if data == 'on':
           self.console.setCvar( 'wrm_ceaseFire','0')
           self.console.setCvar( 'wrm_ceaseFire','1')
           self.console.say('^9Cease Fire Mode : ^1ON')
      else:
           self.console.setCvar( 'wrm_ceaseFire','0')
           self.console.say('^9Cease Fire Mode : ^1OFF')
    return True 
     
  def cmd_wrmpractice(self, data, client, cmd=None):
    """\
    <on/off> - Turn practice mode on/off
    """
    # we need the cvar of the practice mode
    var_practice = self.console.getCvar('wrm_practiceMode')[0]
    var_practicedefault = self.console.getCvar('wrm_practiceMode')[1]    
    if not data:         
         if not var_practicedefault:
               # it hasnt been set in the config yet, no problem                
               client.message('^7Unable to find WRM cvar')
               return False
         else:
               cmd.sayLoudOrPM(client, '^7Practice mode : ^1%s' % var_practice)               
               return False
    else:
      # check to see what they entered
      if data == 'on':           
           self.console.setCvar( 'wrm_practiceMode', '1')
           self.console.say('^9Practice Mode: ^1ON')
      else:                     
           self.console.setCvar( 'wrm_practiceMode', '0')
           self.console.say('^9Practice Mode: ^1OFF')
    return True
    
  def cmd_wrmtest(self, data, client, cmd=None):
    """\
    <on/off> - Turn test weapons mode on/off
    """
    # we need the cvar of the practice mode
    var_testweapons = self.console.getCvar('wrm_testWeapons')[0]
    var_testweaponsdefault = self.console.getCvar('wrm_testWeapons')[1]    
    if not data:         
         if not var_testweaponsdefault:
               # it hasnt been set in the config yet, no problem                
               client.message('^7Unable to find WRM cvar')
               return False
         else:
               cmd.sayLoudOrPM(client, '^7Weapons Mode: ^1%s' % var_testweapons)               
               return False
    else:
      # check to see what they entered
      if data == 'on':           
           self.console.setCvar( 'wrm_testWeapons', '1')
           self.console.say('^9Weapons Mode: ^1ON')
      else:                     
           self.console.setCvar( 'wrm_testWeapons', '0')
           self.console.say('^9Weapons Mode: ^1OFF')
    return True
      
  def cmd_wrmnades(self, data, client, cmd=None):
    """\
    <on/off> - Turn nades on/off
    """
    # we need the cvar of the frag info
    var_rifle = self.console.getCvar('wrm_riflefrags')[0]
    var_rifledefault = self.console.getCvar('wrm_riflefrags')[1]
    var_sniper = self.console.getCvar('wrm_sniperfrags')[0]
    var_sniperdefault = self.console.getCvar('wrm_sniperfrags')[1]
    var_support = self.console.getCvar('wrm_supportfrags')[0]
    var_supportdefault = self.console.getCvar('wrm_supportfrags')[1]
    var_assault = self.console.getCvar('wrm_assaultfrags')[0]
    var_assaultdefault = self.console.getCvar('wrm_assaultfrags')[1]
    if not data:         
         if not var_assaultdefault:
               # it hasnt been set in the config yet, no problem                
               client.message('^7Unable to find WRM nade values')
               return False
         else:
               cmd.sayLoudOrPM(client, '^7Rifle Frags : ^1%s' % var_rifle)
               cmd.sayLoudOrPM(client, '^7Sniper Frags: ^1%s' % var_sniper)
               cmd.sayLoudOrPM(client, '^7Support Frags: ^1%s' % var_support)
               cmd.sayLoudOrPM(client, '^7Assault Frags: ^1%s' % var_assault)
               return False
    else:
      # check to see what they entered
      if data == 'on':
           self.console.say('^9Turning nades ^1on ^9... please wait a moment')
           self.console.setCvar( 'wrm_rifleFrags', var_rifledefault)
           self.console.setCvar( 'wrm_sniperFrags', var_sniperdefault)
           self.console.setCvar( 'wrm_supportFrags', var_supportdefault)
           self.console.setCvar( 'wrm_assaultFrags', var_assaultdefault)
           self.console.say('^9Nades : ^1ON')
      else:
           self.console.say('^9Turning nades ^1off ^9... please wait a moment')
           self.console.setCvar( 'wrm_rifleFrags', '0')
           self.console.setCvar( 'wrm_sniperFrags', '0')
           self.console.setCvar( 'wrm_supportFrags', '0')
           self.console.setCvar( 'wrm_assaultFrags', '0')
           self.console.say('^9Nades : ^1OFF')
    return True
  
  def cmd_wrmvsteam(self, data, client, cmd=None):                         
    """\                                                                   
    <team> - Set the clan team for a versus match (allies, axis, none)
    """         
    # we need the cvar of the clan tags                               
    var_vsteam = self.console.getCvar('wrm_clanTeam')[0]
    if not data:
         if not var_vsteam:                                              
               # it hasnt been set in the config yet, no problem           
               client.message('^7No team set yet, use !help wrmvsteam for usage')      
               return False                                                
         else:                                                             
               cmd.sayLoudOrPM(client, '^7Current clan team: ^1%s' % var_vsteam)      
               return False                                                
    else:                                                                  
      # check to see what they entered                                     
      if data == 'axis' or data == 'allies':                                                   
           self.console.setCvar( 'wrm_clanTeam','%s' % data )
           self.console.say('^9Clan versus team set to : ^1%s' % data)
      else:
           self.console.setCvar( 'wrm_clanTeam','')
           self.console.say('^9Clan versus team set to : ^1off')
    return True
    
  def cmd_wrmsdtype(self, data, client, cmd=None):                         
    """\                                                                   
    <sdtype> - Set the type of S&D (random, kingofthehill, allies, axis)
    """         
    # we need the cvar of the clan tags                               
    var_sdtype = self.console.getCvar('wrm_attackingTeam')[0]
    if not data:
         if not var_sdtype:                                              
               # it hasnt been set in the config yet, no problem           
               client.message('^7No sd type found, use !help wrmsdtype for usage')      
               return False                                                
         else:                                                             
               cmd.sayLoudOrPM(client, '^7Current attacking team: ^1%s' % var_sdtype)      
               return False                                                
    else:                                                                  
      # check to see what they entered                                     
      if data not in ('axis','allies','random'):                                                   
           self.console.setCvar( 'wrm_attackingTeam','kingofthehill')
           self.console.say('^9S&D type set to : ^1kingofthehill')
      else:           
           self.console.setCvar( 'wrm_attackingTeam','%s' % data )
           self.console.say('^9S&D type set to : ^1%s' % data) 
    return True  
    
  def cmd_gametype(self, data, client, cmd=None):                         
    """\                                                                   
    <gametype> - Set the gametype for the next map
    """         
    # we need the cvar of the gametype                              
    var_curgametype = self.console.getCvar('g_gametype')[0]
    if not data:
         if not var_curgametype:                                              
               # it hasnt been set in the config yet, no problem           
               client.message('^7Error in finding gametype, check cvar in b3 code!')      
               return False                                                
         else:                                                             
               cmd.sayLoudOrPM(client, '^7Current gametype: ^1%s' % var_curgametype)      
               return False                                                
    else:                                                                  
      # check to see what they entered                                     
      if data == 'sd':                                                   
           self.console.setCvar( 'g_gametype','%s' % data )
           self.console.say('^9Gametype will be changed to ^1Search and Destroy^9 upon restarting')
      elif data == 'ctf':                                                   
           self.console.setCvar( 'g_gametype','%s' % data )
           self.console.say('^9Gametype will be changed to ^1Capture the Flag^9 upon restarting')
      elif data == 'dm':                                                   
           self.console.setCvar( 'g_gametype','%s' % data )
           self.console.say('^9Gametype will be changed to ^1Deathmatch^9 upon restarting')     
      elif data == 'tdm':                                                   
           self.console.setCvar( 'g_gametype','%s' % data )
           self.console.say('^9Gametype will be changed to ^1Team Deathmatch^9 upon restarting')
      elif data == 're':                                                   
           self.console.setCvar( 'g_gametype','%s' % data )
           self.console.say('^9Gametype will be changed to ^1Retrieval^9 upon restarting')
      else:           
           self.console.say('^9Error: ^3Valid values are (sd, dm, tdm, ctf)')
    return True
    
  def cmd_mp(self, data, client, cmd=None):                         
    """\                                                                   
    Displays the current MP in charge
    """         
    # we need the cvar of the clan tags                               
    var_mp = self.console.getCvar('_b3_mp')[0]
    
    if not var_mp:                                              
       # it hasnt been set in the config yet, no problem           
       client.message('^7No MP has been set yet at the moment, however they may be present on the server regardless')
       return False
    else:
       cmd.sayLoudOrPM(client, '^7Current MP in charge: ^1%s' % var_mp)
       return False
    
    return True
    
    #Not Needed
#    def cmd_playerinfo(self, data, client, cmd=None):
#      """\
#      <player> - Find a player info
#      """
#
#      input = self._adminPlugin.parseUserCmd(data)
#      if input[0] == '':
#        cmd.sayLoudOrPM(client,'Incorrect player searched')
#        return True
#      elif input[0]:
#        # input[0] is the player id
#        sclient = self._adminPlugin.findClientPrompt(input[0], client)
#
#      if not sclient:
#            # a player matchin the name was not found, a list of closest matches will be displayed
#            # we can exit here and the user will retry with a more specific player
#        return False
#      else:
#        countryId = self.gi.id_by_addr(str(sclient.ip))
#        countryCode = GeoIP.id_to_country_code(countryId)
#        country = self.idToCountry(countryId)
#        cmd.sayLoudOrPM(client,'^1%s (%s) ^9guid: ^1%s ^9country: ^1%s ^9ip: ^1%s ^9lvl: ^1%s' % (sclient.exactName, str(sclient.id), str(sclient.guid), str(country), str(sclient.ip), str(sclient.maxLevel)))
          
  def cmd_setmp(self, data, client, cmd=None):                         
    """\                                                                   
    <person> - Set the MP cvar (leave blank for self)
    """
    
    m = self.parseUserCmd(data)
    
    if data:    
         sclient = self.findClientPrompt(m[0], client)
         
         if sclient:            
              self.console.setCvar('_b3_mp','%s' % sclient.exactName)
              self.console.say('^9MP has changed to: ^1%s' % sclient.exactName) 
              return False
         else:
              client.message('^7Unable to locate requested player')
              return False
    else:                                          
         self.console.setCvar('_b3_mp','%s' % client.exactName)
         self.console.say('^9MP has changed to: ^1%s' % client.exactName) 
         return False
    return True  
  
  def cmd_maprestart(self, data, client, cmd=None):
    """\
    - restart the map
    """
    
    self.console.say('^7Restarting the map.....')    
    self.console.write('fast_restart')

  def cmd_mapreload(self, data, client, cmd=None):
    """\
    - reload the map
    """
    
    self.console.say('^7Reloading the map.....')    
    self.console.write('map_restart')

#  Not Needed  
#  def idToCountry(self, countryId):
#    """\
#    Convert country id to country representation.
#    """
#    if 'code3' == self.cf_country_print_mode:
#      return GeoIP.id_to_country_code3(countryId)
#    elif 'name' == self.cf_country_print_mode:
#      return GeoIP.id_to_country_name(countryId)
#    else: # 'code' (default)
#      return GeoIP.id_to_country_code(countryId)