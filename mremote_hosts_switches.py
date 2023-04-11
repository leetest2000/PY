import os
import json
import sys
import csv
import time

try:
    with open('sshlist_switches.csv', newline='') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        file = open(f"switches.xml", "a")
        file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n")
        file.write("<mrng:Connections xmlns:mrng=\"http://mremoteng.org\" Name=\"Connections\" Export=\"false\" EncryptionEngine=\"AES\" BlockCipherMode=\"GCM\" KdfIterations=\"1000\" FullFileEncryption=\"false\" Protected=\"q2YhWc2+Uz45kDBEEH6K18aj6lY9DzpWWKKxQaJDt9FbEfteNwBRBuiYcugnrjpLEp6C0zl2f3K4/4YRuYNTIGRp\" ConfVersion=\"2.6\">" + "\n")
        for row in data:
            site = row[0]
            print(site)
            host = row[1]
            ip_addr = row[2]
            if 'host' != 'Name':
                file.write("        <Node Name=\"" + host + "\" Type=\"Connection\" Descr=\"\" Icon=\"mRemoteNG\" Panel=\"General\" Id=\"518b59a7-9362-4fff-a618-341366bb3fe9\" Username=\"\" Domain=\"\" Password=\"\" Hostname=\"" + ip_addr + "\" Protocol=\"SSH2\" PuttySession=\"Default Settings\" Port=\"22\" ConnectToConsole=\"false\" UseCredSsp=\"true\" RenderingEngine=\"IE\" ICAEncryptionStrength=\"EncrBasic\" RDPAuthenticationLevel=\"NoAuth\" RDPMinutesToIdleTimeout=\"0\" RDPAlertIdleTimeout=\"false\" LoadBalanceInfo=\"\" Colors=\"Colors16Bit\" Resolution=\"FitToWindow\" AutomaticResize=\"true\" DisplayWallpaper=\"false\" DisplayThemes=\"false\" EnableFontSmoothing=\"false\" EnableDesktopComposition=\"false\" CacheBitmaps=\"false\" RedirectDiskDrives=\"false\" RedirectPorts=\"false\" RedirectPrinters=\"false\" RedirectSmartCards=\"false\" RedirectSound=\"DoNotPlay\" SoundQuality=\"Dynamic\" RedirectKeys=\"false\" Connected=\"false\" PreExtApp=\"\" PostExtApp=\"\" MacAddress=\"\" UserField=\"\" ExtApp=\"\" VNCCompression=\"CompNone\" VNCEncoding=\"EncHextile\" VNCAuthMode=\"AuthVNC\" VNCProxyType=\"ProxyNone\" VNCProxyIP=\"\" VNCProxyPort=\"0\" VNCProxyUsername=\"\" VNCProxyPassword=\"\" VNCColors=\"ColNormal\" VNCSmartSizeMode=\"SmartSAspect\" VNCViewOnly=\"false\" RDGatewayUsageMethod=\"Never\" RDGatewayHostname=\"\" RDGatewayUseConnectionCredentials=\"Yes\" RDGatewayUsername=\"\" RDGatewayPassword=\"\" RDGatewayDomain=\"\" InheritCacheBitmaps=\"false\" InheritColors=\"false\" InheritDescription=\"false\" InheritDisplayThemes=\"false\" InheritDisplayWallpaper=\"false\" InheritEnableFontSmoothing=\"false\" InheritEnableDesktopComposition=\"false\" InheritDomain=\"false\" InheritIcon=\"false\" InheritPanel=\"false\" InheritPassword=\"true\" InheritPort=\"false\" InheritProtocol=\"false\" InheritPuttySession=\"false\" InheritRedirectDiskDrives=\"false\" InheritRedirectKeys=\"false\" InheritRedirectPorts=\"false\" InheritRedirectPrinters=\"false\" InheritRedirectSmartCards=\"false\" InheritRedirectSound=\"false\" InheritSoundQuality=\"false\" InheritResolution=\"false\" InheritAutomaticResize=\"false\" InheritUseConsoleSession=\"false\" InheritUseCredSsp=\"false\" InheritRenderingEngine=\"false\" InheritUsername=\"true\" InheritICAEncryptionStrength=\"false\" InheritRDPAuthenticationLevel=\"false\" InheritRDPMinutesToIdleTimeout=\"false\" InheritRDPAlertIdleTimeout=\"false\" InheritLoadBalanceInfo=\"false\" InheritPreExtApp=\"false\" InheritPostExtApp=\"false\" InheritMacAddress=\"false\" InheritUserField=\"false\" InheritExtApp=\"false\" InheritVNCCompression=\"false\" InheritVNCEncoding=\"false\" InheritVNCAuthMode=\"false\" InheritVNCProxyType=\"false\" InheritVNCProxyIP=\"false\" InheritVNCProxyPort=\"false\" InheritVNCProxyUsername=\"false\" InheritVNCProxyPassword=\"false\" InheritVNCColors=\"false\" InheritVNCSmartSizeMode=\"false\" InheritVNCViewOnly=\"false\" InheritRDGatewayUsageMethod=\"false\" InheritRDGatewayHostname=\"false\" InheritRDGatewayUseConnectionCredentials=\"false\" InheritRDGatewayUsername=\"false\" InheritRDGatewayPassword=\"false\" InheritRDGatewayDomain=\"false\" />" + "\n")
        file.write("</mrng:Connections>")           	
    time.sleep(2)      
except Exception as e:
    print(e)
    
