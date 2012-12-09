#import os
import sys
import xbmcaddon
import xbmc
import xbmcgui
from time import sleep
import threading

Addon = xbmcaddon.Addon('script.web.tvwanderlust')
__addon_name__ = Addon.getAddonInfo('name')
__version__ = Addon.getAddonInfo('version')
ADDON_PATH = Addon.getAddonInfo('path').decode('utf-8')

import resources.lib.scraper as scraper

def log(text):
    xbmc.log('%s: %s' % (__addon_name__, text))

class ViewerWindow(xbmcgui.WindowXML):
    CONTROL_EXIT = 104
    CONTROL_REFRESH = 105
    CONTROL_SETTINGS = 106
    
    #found action numbers with action.getId() in onAction function
    ACTION_SELECT_ITEM = 7
    ACTION_PREVIOUS_MENU = 10

    def __init__(self, skin_file, addon_path):
        log('script.__init__ started')
        self.isreloading=False
        
    def onInit(self):
        log('script.onInit started')
        #self.getControl(self.CONTROL_EXIT).setLabel("QExit")

        self.bob=scraper.scraper()
        
        self.thread = threading.Thread(target=self.thread_method)
        self.thread.setDaemon(True)
        self.wait(4)
        print 'Starting thread'
        self.thread.start()

        log('script.onInit finished')
        
    def thread_method( self ):
        print 'Thread started'
        while True:
            self.refresh()
            secs=int(Addon.getSetting('interval'))
            if secs<60:
                secs=60
            self.wait(secs)
            
    def wait(self, secs):          #thx ronie!
        while (not xbmc.abortRequested) and secs > 0:
          secs -= 1
          sleep(1)
                       
    def refresh(self):
        if self.isreloading == True:
            print "Already refreshing!"
            return
        self.isreloading=True
        self.getControl(self.CONTROL_REFRESH).setEnabled(False)
        
        self.bob.load(Addon.getSetting('station'))
        data={}       
        data=self.bob.parse()
        for h in range(3):
            for i in range(3):
                lid=1000+(1000*h)+i
                self.getControl(lid).setLabel(data[h][i])
        self.getControl(self.CONTROL_REFRESH).setEnabled(True)
        self.isreloading=False

        
    def onAction(self, action):
        if action == self.ACTION_SELECT_ITEM:
            Addon.openSettings()
        if action == self.ACTION_PREVIOUS_MENU:
            self.close()
            
    def onClick(self, controlId):
        if controlId == self.CONTROL_REFRESH:
            self.refresh()
        if controlId == self.CONTROL_SETTINGS:
            Addon.openSettings()
        if controlId == self.CONTROL_EXIT:
            #xbmcgui.Dialog().ok('s','Hello world')
            self.close()



if (__name__ == '__main__'):
    w = ViewerWindow('script-Tvwanderlust-main.xml', ADDON_PATH)
    print 'inited with python ver %d %d' % (sys.version_info[0], sys.version_info[1])
    w.doModal()
    del w
    sys.modules.clear()

