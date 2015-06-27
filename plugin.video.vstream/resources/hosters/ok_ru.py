from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2
import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Ok.ru'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'ok_ru'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def getHostAndIdFromUrl(self, sUrl):
        sPattern = 'http:\/\/((?:(?:ok)|(?:odnoklassniki))\.ru)\/.+?\/([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        v = self.getHostAndIdFromUrl(self.__sUrl)
        sId = v[1]
        sHost = v[0]
        web_url = 'http://' + sHost + '/dk?cmd=videoPlayerMetadata&mid=' + sId
        
        #print web_url
        
        oRequest = cRequestHandler(web_url)
        sHtmlContent = oRequest.request()
        
        sHtmlContent = sHtmlContent.decode('unicode-escape')
        sHtmlContent = sHtmlContent.encode("utf-8")
        
        sPattern = '"name":"([^"]+?)","url":"(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #print aResult
        
        api_call = False

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]
                    
        #print api_call

        if (api_call):
            return True, api_call
            
        return False, False