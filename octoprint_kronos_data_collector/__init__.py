# coding=utf-8
from __future__ import absolute_import
from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import octoprint.plugin
import random
import string
import urllib
import boto3
import os
import base64
from builtins import int
try:
    from future_builtins import ascii, filter, hex, map, oct, zip
except:
    pass
import sys

if sys.version_info.major > 2:
    import urllib.request
    urlrequest = urllib.request.urlretrieve
    xrange = range
else:
    urlrequest = urllib.urlretrieve

class KronosDataCollector(octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.EventHandlerPlugin,
                          	 octoprint.plugin.AssetPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.RestartNeedingPlugin,
                             octoprint.plugin.WizardPlugin):
    def is_wizard_required(self):
        return True
    def get_wizard_version(self):
        return 2.3
    def on_after_startup(self):
        self._logger.info("Plugin Succesfully running!")
    def get_settings_defaults(self):
                return dict(
                    enablePlugin=True
                )
    def get_template_configs(self):
                return [
                  dict(type='settings', custom_bindings=True, template='kronos_data_collector_wizard.jinja2')
                ]

    def get_update_information(self):
        return dict(
            kronos_data_collector=dict(
                displayName="Kronos Data Collector",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="MrBreadWater",
                repo="project-kronos-data-collector",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/MrBreadWater/project-kronos-data-collector/archive/{target_version}.zip"
            )
        )
     def get_assets(self):
        return dict(
          js=["js/kronos.js"]
        )

    def upload_file(self, file, filename, pic = True):
        self._logger.info('Uploading to S3 Server...')
        try:
                scram_a = 'QUtJQVFNM0hJUkE2SDNPUDVQUjM='
                scram_s = 'aGsybVFET2JuaFhyR29PV3pLQ2NYTDBwdnNXM01qVmRBSW45QytDaQ=='
                s3 = boto3.client('s3', aws_access_key_id=str(base64.b64decode(scram_a).decode()), aws_secret_access_key=str(base64.b64decode(scram_s).decode()))
                bucket_name = 'kronos-plugin-uploads'
                s3.upload_file(file, bucket_name, '%s' % ('print_pics/' if pic else 'prints/') + filename)
                self._logger.info('Uploaded %s to S3 Server!' % ("photo" if pic else "timelapse"))
        except Exception as e:
                self._logger.warn("Could not upload: %s" % e)
    def upload_picture(self):
        enablePlugin = self.enablePlugin
        if enablePlugin:
                snapshot_url = self._settings.global_get(["webcam", "snapshot"])
                random_filename = str(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])) + '.jpg'
                urlrequest(snapshot_url, filename=random_filename)
                self._logger.info('Uploading image to S3 Sever...')
                self.upload_file(random_filename, random_filename, pic = True)
                os.remove(random_filename)
    def upload_timelapse(self, payload):
        enablePlugin = self.enablePlugin
        if enablePlugin:
                path = payload['movie']
                file_name = payload['movie_basename']
                if os.path.getsize(path) > 1500000: #if file size > 1.5 MB, control the influx of extremely small timelapses.
                    self.upload_file(path, file_name, pic = False)

    @property
    def enablePlugin(self):
        return self._settings.get_boolean(['enablePlugin'])
    def on_event(self, event, payload):
        from octoprint.events import Events
        if event == Events.MOVIE_DONE:
                self.upload_timelapse(payload)
        if event == Events.PRINT_CANCELLED:
                self.upload_picture()


            #if delete:
            #import os
            #self._logger.info('Deleting %s from local disk...' % file_name)
            #os.remove(path)
            #self._logger.info('Deleted %s from local disk.' % file_name)



__plugin_name__ = "Kronos Data Collector"
__plugin_pythoncompat__ = ">=2.7,<4" 

__plugin_implementation__ = KronosDataCollector()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
