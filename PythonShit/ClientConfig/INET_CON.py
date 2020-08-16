STATUS_ENABLED = 0
STATUS_PROMPT = 1
STATUS_DISABLED = 3
STATUS_HIGH_SAFETY = 65536
STATUS_AUTO_CURRENT_LOGON = 0

# Microsoft support article
# https://support.microsoft.com/en-us/help/182569/internet-explorer-security-zones-registry-entries-for-advanced-users
zones = {
    "2402": (".NET Framework: Loose XAML", STATUS_ENABLED),
    "2400": (".NET Framework: XAML browser applications", STATUS_ENABLED),
    "2401": (".NET Framework: XPS documents", STATUS_ENABLED),
    "2007": (".NET Framework: Permissions for Components with Manifests", STATUS_HIGH_SAFETY),
    "2004": (".NET Framework: Run components not signed with Authenticode", STATUS_ENABLED),
    "2001": (".NET Framework: Run components signed with Authenticode", STATUS_ENABLED),
    # USED TO OVERRIDE ALL ACTIVEX CONTROLS - SHOULD BE DISABLED
    "120A": (
        "ActiveX controls: ActiveX controls and plug-ins: Override Per-Site ActiveX restrictions", STATUS_DISABLED),

    "2702": ("ActiveX controls: Allow ActiveX Filtering", STATUS_DISABLED),
    "1208": ("ActiveX controls: Allow previously unused ActiveX controls to run without prompt", STATUS_ENABLED),
    "1209": ("ActiveX controls: Allow Scriptlets", STATUS_ENABLED),
    "2201": ("ActiveX controls: Automatic prompting for ActiveX controls", STATUS_ENABLED),
    "2000": ("ActiveX controls: Binary and script behaviors", STATUS_ENABLED),
    "1001": ("ActiveX controls: Download signed ActiveX controls", STATUS_ENABLED),
    "1004": ("ActiveX controls: Download unsigned ActiveX controls", STATUS_ENABLED),
    "1201": (
        "ActiveX controls: Initialize and script ActiveX controls not marked as safe for scripting", STATUS_ENABLED),
    # USED TO OVERRIDE ALL ACTIVEX CONTROLS - DOMAIN BASED - NOT MANDATORY
    # "120B": ("ActiveX controls: Override Per-Site (domain-based) ActiveX restrictions", STATUS_DISABLED),

    "1200": ("ActiveX controls: Run ActiveX controls and plug-ins", STATUS_ENABLED),
    # COULD NOT FIND IN DOCUMENTATIONS
    "270C": ("ActiveX Controls: Run Antimalware software on ActiveX controls", STATUS_DISABLED),

    "1405": ("ActiveX controls: Script ActiveX controls marked as safe for scripting", STATUS_ENABLED),
    "1A05": ("Allow 3rd party persistent cookies", STATUS_ENABLED),
    "1A06": ("Allow 3rd party session cookies", STATUS_ENABLED),
    # Not available in GUI
    # "180E": ("Allow OpenSearch queries in Windows Explorer", STATUS_ENABLED),
    # "1A03": ("Allow per-session cookies (not stored)", STATUS_ENABLED),
    # "1A02": ("Allow persistent cookies that are stored on your computer", STATUS_ENABLED),
    # "180F": ("Allow previewing and custom thumbnails of OpenSearch query results in Windows Explorer", STATUS_ENABLED)
    # # # # # # # # # # # # # # # # # #
    "2200": ("Downloads: Automatic prompting for file downloads", STATUS_ENABLED),
    ##################################################################################
    "1803": ("Downloads: File Download", STATUS_ENABLED),
    "1604": ("Downloads: Font download", STATUS_ENABLED),
    "2600": ("Enable .NET Framework setup", STATUS_ENABLED),
    # Not available in GUI
    #
    # "1C00": ("Java permissions", STATUS_ENABLED),
    # "1805": ("Launching programs and files in webview", STATUS_ENABLED),
    # # # # # # # # # # # # # #
    "1406": ("Miscellaneous: Access data sources across domains", STATUS_ENABLED),
    "2709": ("Miscellaneous: Allow dragging of content between domains into separate windows", STATUS_DISABLED),
    # Not mandatory
    # "2708": ("Miscellaneous: Allow dragging of content between domains into the same window", STATUS_ENABLED),
    "1608": ("Miscellaneous: Allow META REFRESH", STATUS_ENABLED),
    "2102": ("Miscellaneous: Allow script initiated windows without size or position constraints", STATUS_ENABLED),
    "1206": ("Miscellaneous: Allow scripting of Internet Explorer Web browser control", STATUS_ENABLED),
    # Not mandatory
    # "2300": ("Miscellaneous: Allow webpages to use restricted protocols for active content", STATUS_ENABLED),
    "2104": ("Miscellaneous: Allow websites to open windows without address or status bars", STATUS_ENABLED),
    "1609": ("Miscellaneous: Display mixed content", STATUS_ENABLED),
    "1A04": (
        "Miscellaneous: Don't prompt for client certificate selection when no certificates exists", STATUS_ENABLED),
    "1802": ("Miscellaneous: Drag and drop or copy and paste files", STATUS_ENABLED),
    "160A": ("Miscellaneous: Include local directory path when uploading files to a server", STATUS_ENABLED),
    "1800": ("Miscellaneous: Installation of desktop items", STATUS_ENABLED),
    "1806": ("Miscellaneous: Launching applications and unsafe files", STATUS_ENABLED),
    "1804": ("Miscellaneous: Launching programs and files in an IFRAME", STATUS_ENABLED),
    "1607": ("Miscellaneous: Navigate sub-frames across different domains", STATUS_ENABLED),
    "2100": ("Miscellaneous: Open files based on content), not file extension", STATUS_ENABLED),
    "270B": ("Miscellaneous: Render legacy filters", STATUS_ENABLED),
    # Not documented, assumes as not mandatory.
    # "1E05": ("Miscellaneous: Software channel permissions", STATUS_ENABLED),
    "1601": ("Miscellaneous: Submit non-encrypted form data", STATUS_ENABLED),
    "2301": ("Miscellaneous: Use Phishing Filter", STATUS_DISABLED),
    "1809": ("Miscellaneous: Use Pop-up Blocker", STATUS_DISABLED),
    "1606": ("Miscellaneous: Userdata persistence", STATUS_ENABLED),
    "2101": (
        "Miscellaneous: Web sites in less privileged web content zone can navigate into this zone", STATUS_ENABLED),
    "1A10": ("Privacy Settings", STATUS_ENABLED),
    # "1207":"Reserved", STATUS_ENABLED),
    # "1408":"Reserved", STATUS_ENABLED),
    # "180A":"Reserved", STATUS_ENABLED),
    # "180B":"Reserved", STATUS_ENABLED),
    # "180C":"Reserved", STATUS_ENABLED),
    # "180D":"Reserved", STATUS_ENABLED),
    # "1807":"Reserved", STATUS_ENABLED),
    # "1808":"Reserved", STATUS_ENABLED),
    # "1F00":"Reserved", STATUS_ENABLED),
    "1605": ("Run Java", STATUS_ENABLED),
    "1400": ("Scripting: Active scripting", STATUS_ENABLED),
    "1407": ("Scripting: Allow Programmatic clipboard access", STATUS_ENABLED),
    "2103": ("Scripting: Allow status bar updates via script", STATUS_ENABLED),
    "2105": ("Scripting: Allow websites to prompt for information using scripted windows", STATUS_ENABLED),
    "1409": ("Scripting: Enable XSS Filter", STATUS_DISABLED),
    "1402": ("Scripting: Scripting of Java applets", STATUS_ENABLED),
    "2500": ("Turn on Protected Mode [Vista only setting]", STATUS_DISABLED),
    "1A00": ("User Authentication: Logon", STATUS_AUTO_CURRENT_LOGON)
}

advanced_tab = {
    "Anchor Underline": "yes",
    "Cache_Update_Frequency": "yes",
    "Disable Script Debugger": "yes",
    "DisableScriptDebuggerIE": "yes",
    "Display Inline Images": "yes",
    # "Do404Search": "hex:01,00,00,00",
    # "Local Page": "%11%\\blank.htm",
    "Save_Session_History_On_Exit": "no",
    # "Search Page": "http://go.microsoft.com/fwlink/?LinkId=54896",
    # "Show_FullURL": "no",
    # "Show_StatusBar": "yes",
    # "Show_ToolBar": "yes",
    "Show_URLinStatusBar": "yes",
    "Show_URLToolBar": "yes",
    "Use_DlgBox_Colors": "yes",
    # "UseClearType": "no",
    "XMLHTTP": "1",
    "Enable Browser Extensions": "no",
    "Play_Background_Sounds": "yes",
    "Play_Animations": "yes",
    # "Start Page": "http://go.microsoft.com/fwlink/p/?LinkId=255141",
    # "OperationalData": "hex(b):0d,02,00,00,00,00,00,00",
    "CompatibilityFlags": "0",
    "FullScreen": "no",
    # "Window_Placement": "",
    # "ImageStoreRandomFolder": "kjgz3n2",
    # "DownloadWindowPlacement": "",
    "News Feed First Run Experience": "0",
    "Error Dlg Displayed On Every Error": "no",
    "Print_Background": "yes",
    "AllowWindowReuse": "yes",
    "SearchBandMigrationVersion": "1",
    "Use FormSuggest": "no",
    "FormSuggest PW Ask": "no",
    "UseSWRender": "0",
    "Expand Alt Text": "no",
    "Move System Caret": "no",
    # "PlaySounds": "0",
    "NscSingleExpand": "0",
    "UseThemes": "1",
    "GotoIntranetSiteForSingleWordEntry": "1",
    "HideNewEdgeButton": "1",
    "HideOpenWithEdgeInContextMenu": "0",
    "NotifyDownloadComplete": "yes",
    "Friendly http errors": "yes",
    # "Check_Associations": "yes",
    "SmoothScroll": "1",
    "EnableAlternativeCodec": "yes",
    "Enable AutoImageResize": "yes",
    "Show image placeholders": "0",
    "MixedContentBlockImages": "0",
    # "Isolation64Bit": "0",
    "DOMStorage": "1",
    # "Isolation": "PMIL",
    "DoNotTrack": "0"

}
