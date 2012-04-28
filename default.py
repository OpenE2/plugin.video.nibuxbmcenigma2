'''
NiBuDev Enigma2 Viewer
Created on 10.08.2011
@author: NiBuDev
'''
import sys, cgi, xbmc, xbmcaddon

#Define Basic Vars for the Addon
__scriptname__  = "NiBuDev Enigma2 Viewer"
__credits__ = ""
__version__ = "0.0.1"
__plugin__ = "NiBuDev Enigma2 Viewer -" + __version__
__author__ = "NiBuDev Nicolai Burger"
__url__ = ""
__settings__ = xbmcaddon.Addon(id='plugin.video.nibuxbmcenigma2')
__language__ = __settings__.getLocalizedString

#Run the Addon
if (__name__ == "__main__" ):
    #Import the Enigma Class Module
    import EnigmaData
    
    handle = int(sys.argv[1])
    dreambd = EnigmaData.EnigmaData(handle)
    
    if not sys.argv[2]:
        dreambd.basicmenu()
    else:
        data = cgi.parse_qs(sys.argv[2][1:])
        mode = data["mode"][0]
        if mode == "movies": #Show the Movie List
            dreambd.GetMovieList()
        elif mode == "tv":  #Show the TV Bouget List
            dreambd.getBougetListTV()
        elif mode == "radio": #Show the Radio Bouget List
            dreambd.getBougetListRadio()
        elif mode == "readservice": #Read the Service from Bouget ID
            dreambd.readService(data)
        elif mode == "playservice": # Play the Service from Service ID
            dreambd.playService(data)
        elif mode == "ts": #Stream a Video File from the Dreambox
            dreambd.tsStream(data)
