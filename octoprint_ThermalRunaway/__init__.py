# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import logging
import threading
import time

_logger = logging.getLogger('octoprint.plugins.ThermalRunaway')

class ThermalRunawayPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        global bHighTemp
        bHighTemp = 0.0
        _logger.debug('bHighTemp = ')
        _logger.debug(bHighTemp)
        _logger.debug('reached end on on_after_startup')
        return

    def killPrint():
        octoprint.printer.PrinterInterface.cancel_print()
        _logger.debug('KilledPrint')
        return
    
    ##~~ SettingsPlugin mixin

##    def get_settings_defaults(self):
##        return dict(
##            # put your plugin's default settings here
##        )

    ##~~ AssetPlugin mixin

##    def get_assets(self):
##        # Define your plugin's asset files to automatically include in the
##        # core UI here.
##        return dict(
##            js=["js/ThermalRunaway.js"],
##            css=["css/ThermalRunaway.css"],
##            less=["less/ThermalRunaway.less"]
##        )


    ##~~ Temperatures received hook

    def check_temps(self, temps):
        global bHighTemp
        _logger.debug('reached start of check_temps')
        TMaxOffTemp = 250.0
        BMaxOffTemp = 60.0
        TMaxDiff = 25.0
        BMaxDiff = 10.0
        BTemps = temps["B"]
        TTemps = temps["T0"]
        BCurrentTemp = BTemps[0]
        _logger.debug('BCurrentTemp = ')
        _logger.debug(BCurrentTemp)
        TCurrentTemp = TTemps[0]
        BSetTemp = BTemps[1]
        _logger.debug('BSetTemp = ')
        _logger.debug(BSetTemp)
        TSetTemp = TTemps[1]
        _logger.debug('old bHighTemp = ')
        _logger.debug(bHighTemp)
        bHighTemp += 1.0
        if (BSetTemp > 0.0):
            BMaxTemp = BSetTemp + BMaxDiff
            _logger.debug('BMaxTemp = ')
            _logger.debug(BMaxTemp)
        if (TSetTemp > 0.0):
            TMaxTemp = TSetTemp + TMaxDiff
            _logger.debug('TMaxTemp = ')
            _logger.debug(TMaxTemp)
        if (BCurrentTemp > BMaxTemp):
            _logger.debug('KillPrint()')
            killPrint()
        if (TCurrentTemp > TMaxTemp):
            _logger.debug('KillPrint()')
        return

    def get_temps(self, comm, parsed_temps):
        temps = parsed_temps
        if (temps == parsed_temps):
            _logger.debug('Spawning new thread...')
            t = threading.Timer(0,self.check_temps,[temps])
            t.start()
            _logger.debug('Spawned new thread.')
        return parsed_temps

    
    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            ThermalRunaway=dict(
                displayName="Thermalrunaway Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="AlexVerrico",
                repo="Octoprint-ThermalRunaway",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/AlexVerrico/Octoprint-ThermalRunaway/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
##__plugin_name__ = "Thermalrunaway Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ThermalRunawayPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.temperatures.received": __plugin_implementation__.get_temps
    }
