/*
 * View model for OctoPrint-Kronos-Data-Collector
 *
 * Author: Michael Paniagua
 * License: All Rights Reserved
 */
allBound = false;
$(function() {
    function KronosViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
         //self.loginStateViewModel = parameters[0];
         self.settingsViewModel = parameters[0];

         self.onAllBound = function(){
             setTimeout(function() {
                 allBound = true;
             },500)
         }
    }



    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: KronosViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel", "wizardViewModel"],
        // Elements to bind to, e.g. #settings_plugin_cogniprint, #tab_plugin_cogniprint, ...
        elements: [ "#settings_plugin_kronos_data_collector",  "#wizard_plugin_kronos_data_collector"]
    });
});
