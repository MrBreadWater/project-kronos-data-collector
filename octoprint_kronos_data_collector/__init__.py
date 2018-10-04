# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import urllib
import random
import string
import boto3
from botocore.client import Config
import os
import base64

class KronosDataCollector(octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.EventHandlerPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.RestartNeedingPlugin,
                             octoprint.plugin.WizardPlugin):
    def is_wizard_required(self):
        return True
    def get_wizard_version(self):
        return 2.2
    def on_after_startup(self):
        self._logger.info("Plugin Succesfully running!")
    def get_settings_defaults(self):
                return dict(
                    enablePlugin=False
                )
    def get_template_configs(self):
                return [
                dict(type='settings', custom_bindings=False, template='fail_data_settings.jinja2')
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

    def upload_file(self, file, filename, pic = True):
        self._logger.info('Uploading to S3 Server...')
        if pic == False:
                try:
                        scram_a = 'QUtJQUk0UFlVRVVNVFJCTVRNT1E='
                        scram_s = 'YzBTQW9uL3YvZWNnb1hOV2NObGllMVY2YXdXSCtiZVo4M20rRzlzdQ=='
                        s3 = boto3.client('s3', aws_access_key_id=base64.b64decode(scram_a), aws_secret_access_key=base64.b64decode(scram_s))
                        bucket_name = '3dprintdetectionuploads'
                        s3.upload_file(file, bucket_name, 'prints/' + filename)
                        self._logger.info('Uploaded timelapse to S3 Server!')
                except Exception as e:
                        self._logger.info(str(e))
                        self._logger.info("error")
        elif pic == True:
                try:
                        scram_a = 'QUtJQUk0UFlVRVVNVFJCTVRNT1E='
                        scram_s = 'YzBTQW9uL3YvZWNnb1hOV2NObGllMVY2YXdXSCtiZVo4M20rRzlzdQ=='
                        s3 = boto3.client('s3', aws_access_key_id=base64.b64decode(scram_a), aws_secret_access_key=base64.b64decode(scram_s))
                        bucket_name = '3dprintdetectionuploads'
                        s3.upload_file(file, bucket_name, 'print_pics/' + filename)
                        self._logger.info('Uploaded photo to S3 Server!')
                except Exception as e:
                        self._logger.info(str(e))
                        self._logger.info("error")

    def upload_picture(self):
        enablePlugin = self.enablePlugin
        if enablePlugin:
                snapshot_url = self._settings.global_get(["webcam", "snapshot"])
                random_filename = str(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])) + '.jpg'
                urllib.urlretrieve (snapshot_url, random_filename)
                self._logger.info('Uploading image to S3 Sever...')
                self.upload_file(random_filename, random_filename, pic = True)
                os.remove(random_filename)
    def upload_timelapse(self, payload):
        enablePlugin = self.enablePlugin
        if enablePlugin:
                path = payload['movie']
                file_name = payload['movie_basename']
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



#__plugin_implementation__ = KronosDataCollector()

#__plugin_hooks__ = {
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
#}

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = KronosDataCollector()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
