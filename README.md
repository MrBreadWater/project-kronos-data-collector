# Project Kronos Data Collector
A simple Octoprint Plugin to help collect a dataset of 3D Printing timelapses for Project Kronos. Project Kronos is an effort to create a webcam-based Neural Network to classify snapshots from a 3D Printer as "Failed" or "Successful". This will be implemented in real-time as an Octoprint plugin to automatically pause the printer and alert the user of the potential error, leading to far less wasted filament and a lower chance of printer damage.

# Install
Project Kronos Data Collector is in the Official Octoprint Plugin Repository, and can be installed automatically through the Plugin Manager by searching for the plugin.

Alternatively, install by going to Octoprint's plugin manager, clicking the "Get More" button at the bottom of the screen, and paste the following URL into it: https://github.com/MrBreadWater/project-kronos-data-collector/archive/master.zip

Simply follow the on screen directions from that point to finish the install.
# Upcoming Features
### 1. Usage incentive
The usage incentive will add a sign up form to the program to allow users to register themselves onto a list of contributors. The contributors will recieve an incentive (yet to be determined) at the end of the data collection period.
<br>
# Privacy Statement

By using this Plugin, you agree to allow for the anonymous collection of timelapses and photos generated by Octoprint. No identifying information will be attatched to the files, as they are entirely anonymous.

### What Data is Collected

The only data collected is snapshots of failed prints, and timelapses that Octoprint renders. Data is submitted for photos and timelapses upon cancellation of a print, and upon the rendering of a timelapse.

### Data Retention

The timelapses will be kept indefinitely, as is appropriate for each individual timelapse.

### Data Usage

The data is hand-sorted into a dataset, and used to generate a neural network. No timelapses will included as a part of the final neural network, only the variables generated by analysis of the overall dataset. No private timelapses will ever be released to the public. No third party companies will have access to the data. The data will only ever be stored on official Project Kronos computers/storage, and the server it's initially uploaded to.

### Disabling Data Collection and Uninstalling

To disable this plugin, go into your Octoprint settings, and on the side, click Project Kronos Daa Collector. Then, simply uncheck the "Enable?" checkbox and save your settings. 

To uninstall this plugin completely, go to your Octoprint settings and click on Plugin Manager. Simply find the plugin in the list of installed plugins, and click on the trash can to uninstall it. Follow any prompts that pop up.

# Contact Me

Email: mrbreadwater@yahoo.com

Reddit: MrBreadWater

Discord: MrBreadWater#4998

Twitter: https://twitter.com/MrBreadWater
