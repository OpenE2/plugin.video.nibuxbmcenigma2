'''
EnigmaData Class
Created on 10.08.2011
@author: NiBuDev
'''
import xbmc, xbmcplugin, xbmcgui, urllib, urllib2, sys, xml.dom.minidom

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

class EnigmaData(object):
    """Class thats handle the communicate between xbmc and the Dreambox Enigma 2 Webinterface
    """
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__" ].__plugin__
    
    def __init__(self, handle):
        self.handle = handle
        self.dreamboxip = self.__settings__.getSetting("dreamboxhost")
        self.dreamboxport = self.__settings__.getSetting("dreamboxport")
        self.debug = self.__settings__.getSetting("debug")
      
    def basicmenu(self):
        menu = [
            { "name":self.__language__( 30101 ), "mode": "tv" },
            { "name":self.__language__( 30102 ), "mode": "radio" },
            { "name":self.__language__( 30103), "mode": "movies" },
        ]
        for item in menu:
            li = xbmcgui.ListItem(item["name"])
            url = sys.argv[0] + '?' + urllib.urlencode({"mode":item["mode"]})
            xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True, totalItems=len(menu))
        xbmcplugin.endOfDirectory(handle=self.handle, succeeded=True)
    
    def getBougetListTV(self):
        # Get Bouquet list
        data = urllib2.urlopen("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/getservices?" + urllib.urlencode({"sRef": '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25)FROM BOUQUET "bouquets.tv" ORDER BY bouquet'}))
        e2servicelist = xml.dom.minidom.parse(data)
        data.close()

        servicelist = e2servicelist.getElementsByTagName("e2service")
        for service in servicelist:
            data = {}
            for element in service.childNodes:
                data[element.localName] = getText(element.childNodes)

            cmd = {}
            cmd["mode"] ="readservice"
            cmd["e2servicename"] = data["e2servicename"].encode("utf-8")
            cmd["e2servicereference"] = data["e2servicereference"].encode("utf-8")

            li = xbmcgui.ListItem(data["e2servicename"])            
            url = sys.argv[0] + '?' + urllib.urlencode(cmd)
            xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True, totalItems=len(servicelist))

        # Get provider list
        data = {
            "mode":"playservice",
            "e2servicename":"Provider",
            "e2servicereference":"1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM PROVIDERS ORDER BY name"
        }
        li = xbmcgui.ListItem(data["e2servicename"])
        url = sys.argv[0] + '?' + urllib.urlencode(data)
        xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True, totalItems=len(servicelist))

        xbmcplugin.endOfDirectory(handle=self.handle, succeeded=True)
    
    def getBougetListRadio(self):
        # Get Bouquet list
        data = urllib2.urlopen("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/getservices?" + urllib.urlencode({"sRef": '1:7:2:0:0:0:0:0:0:0:(type == 2)FROM BOUQUET "bouquets.radio" ORDER BY bouquet'}))
        e2servicelist = xml.dom.minidom.parse(data)
        data.close()

        servicelist = e2servicelist.getElementsByTagName("e2service")
        for service in servicelist:
            data = {}
            for element in service.childNodes:
                data[element.localName] = getText(element.childNodes)

            cmd = {}
            cmd["mode"] ="readservice"
            cmd["e2servicename"] = data["e2servicename"].encode("utf-8")
            cmd["e2servicereference"] = data["e2servicereference"].encode("utf-8")

            li = xbmcgui.ListItem(data["e2servicename"])
            url = sys.argv[0] + '?' + urllib.urlencode(cmd)
            xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True, totalItems=len(servicelist))

        # Get provider list
        data = {
            "mode":"playservice",
            "e2servicename":"Provider",
            "e2servicereference":"1:7:2:0:0:0:0:0:0:0:(type == 2) FROM PROVIDERS ORDER BY name"
        }
        li = xbmcgui.ListItem(data["e2servicename"])
        url = sys.argv[0] + '?' + urllib.urlencode(data)
        xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True, totalItems=len(servicelist))
        xbmcplugin.endOfDirectory(handle=self.handle, succeeded=True)
    
    def GetMovieList(self):
        data = urllib2.urlopen("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/movielist")
        e2movielist = xml.dom.minidom.parse(data)
        data.close()

        movieList = e2movielist.getElementsByTagName("e2movie")
        for movie in movieList:
            data = {}
            for element in movie.childNodes:
                data[element.localName] = getText(element.childNodes)

            li = xbmcgui.ListItem(data["e2title"], data["e2description"])
            labels = {
                "size":int(data["e2filesize"]), 
                "plot":data["e2description"], 
                "title":data["e2title"]
            }
            li.setInfo("video", labels)
            url = sys.argv[0] + '?' + urllib.urlencode({"mode":"ts", "e2servicename":data["e2title"].encode("utf-8"), "e2filename":data["e2filename"].encode("utf-8"), "e2servicereference":data["e2servicereference"].encode("utf-8")})
            xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=False, totalItems=len(movieList))
        xbmcplugin.endOfDirectory(handle=self.handle, succeeded=True)
    
    def readService(self, data):
        servicereference = data["e2servicereference"][0].decode("utf-8")
        data = urllib2.urlopen("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/epgnow?" + urllib.urlencode({"bRef": servicereference.encode("utf-8")}))
        e2eventlist = xml.dom.minidom.parse(data)
        data.close()

        e2event = e2eventlist.getElementsByTagName("e2event")
        
        i=1
        for event in e2event:
            data = {}
            for element in event.childNodes:
                data[element.localName] = getText(element.childNodes)
            servicereference = data["e2eventservicereference"].split(":")
            attr = int(servicereference[1])
            mode = int(servicereference[2])
            cmd = {}
            eventname=""
            eventbeschreibung=""
            eventlangbeschreibung=""
            try:
                eventname = data["e2eventtitle"]                                           
            except:
                pass
            try:
                eventbeschreibung = data["e2eventdescription"]                                          
            except:
                pass
            try:
                eventlangbeschreibung = data["e2eventdescriptionextended"]                                          
            except:
                pass           
            
            if attr & 4:
                cmd["mode"] ="readservice"
                isFolder = True
            else:
                cmd["mode"] ="playservice"
                isFolder = False            
                                
            cmd["e2eventservicename"] = data["e2eventservicename"].encode("utf-8")
            cmd["e2eventservicereference"] = data["e2eventservicereference"].encode("utf-8")
            
            li = xbmcgui.ListItem(data["e2eventservicename"] + ' - ' + eventname)            
            mediatype = ""
            if mode == 1:
                mediatype = "video"
            elif mode == 2:
                mediatype = "music"
            if mediatype:
                li.setInfo(mediatype, {'title': data["e2eventservicename"] + ' - ' + eventname ,"plot":eventlangbeschreibung,"PlotOutline":eventbeschreibung})
                
            url = sys.argv[0] + '?' + urllib.urlencode(cmd)
            xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=isFolder, totalItems=len(e2event))
            i=i+1
            
        xbmcplugin.endOfDirectory(handle=self.handle, succeeded=True)
   
    def playService(self, data):
        servicename = data["e2eventservicename"][0].decode("utf-8")
        servicereference = data["e2eventservicereference"][0].decode("utf-8")
        reference = servicereference.split(":")
        mode = int(reference[2])
        
        #Umschalten
        request = urllib2.Request("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/zap?" + urllib.urlencode({"sRef": servicereference.encode("utf-8")}))
        socket = urllib2.urlopen(request)
        socket.close();
        
        data = urllib2.urlopen("http://" + self.dreamboxip + ":" + self.dreamboxport + "/web/stream.m3u?" + urllib.urlencode({"ref": servicereference.encode("utf-8")}))
        playlist = data.readlines()
        data.close()

        li = xbmcgui.ListItem(servicename)
        mediatype = ""
        if mode == 1:
            mediatype = "video"
        elif mode == 2:
            mediatype = "music"
        if mediatype:
            li.setInfo(mediatype, {'Title': servicename })
        xbmc.Player().play(playlist[-1], li)
    
    def tsStream(self, data):
        servicename = data["e2servicename"][0].decode("utf-8")
        filename = data["e2filename"][0].decode("utf-8")
        servicereference = data["e2servicereference"][0].decode("utf-8")
        reference = servicereference.split(":")
        mode = int(reference[2])
        
        url = "http://" + self.dreamboxip + ":" + self.dreamboxport +  "/file?file=" + filename.replace("/", "%2F").replace(" ", "%20")

        li = xbmcgui.ListItem(servicename)
        mediatype = ""
        if mode == 1:
            mediatype = "video"
        elif mode == 2:
            mediatype = "music"
        if mediatype:
            li.setInfo(mediatype, {'Title': servicename })
        xbmc.Player().play(url, li)
        
    def showDebugMessage(self,text=''):
        if  self.debug == true:
            print (text)

