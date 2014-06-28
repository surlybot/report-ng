# Wasar
# Copyright (c) 2014 Marcin Woloszyn (@hvqzao)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import wx
import base64
import cStringIO

from resources.icon import icon
from report import Report
from scan import Scan

#import datetime ; print datetime.datetime.ctime(datetime.datetime.now())


class GUI(object):
    title = 'Wasar'
    long_title = 'Web Application Security Assessment Reporting'
    version = '0.2.8'
    c = 'Copyright (C) 2014 Marcin Woloszyn (@hvqzao)'
    url = 'https://github.com/hvqzao/wasar'
    license = 'Distributed under GNU General Public License, Version 2, June 1991'
    about = '''
    Generate reports based on HP WebInspect, BurpSuite Pro scans,
    own custom data, knowledge base and Microsoft Office Word templates.
    '''
    date = 'Sat Jun 28 10:04:28 2014'
    changelog = '''
    0.3.0 - Sat Jun 28 10:04:28 2014
    - content formatting fixes
    
    0.2.9 - Sat Jun 28 00:21:41 2014
    - added conditional root blocks in content
    - counter capability added to findings summary
    
    0.2.8 - Thu Jun 27 17:34:49 2014
    - minor formatting issues
    - added conditional blocks within findings
    
    0.2.7 - Sun May  4 23:02:01 2014
    - documentation updates
    
    0.2.6 - Fri May  2 16:13:22 2014
    - added: command-line support
    - added: License information
    
    0.2.5 - Mon Apr 28 02:11:00 2014
    - FIX: html/ihtml sections should now land correctly in summary table cells
    
    0.2.4 - Sat Apr 26 11:27:01 2014
    - added: Template structure preview

    0.2.3 - Thu Apr 24 22:12:09 2014
    - FIX: <img src="..."> is now relative to template file directory
    - html/ihtml sections are now more error proof
    - source code has been reorganized into smaller pieces
    - source has been cleaned up a bit

    0.2.2 - Mon Apr 21 03:01:05 2014
    - HP WebInspect and Burp Suite Pro scans are now supported
    - pseudo-html is now supported as an input for template
    - added: Changelog
    '''
    #'0.2.1 Sun Apr 13 21:17:13 2014'
    #'0.2.0 Sun Apr  6 20:03:13 2014'
    #'0.1.9 Sun Apr  6 12:47:31 2014'
    #'0.1.8 Sat Apr  5 19:06:10 2014'
    #'0.1.7 Fri Apr  4 23:41:16 2014'
    #'0.1.6 Sun Mar 23 14:01:58 2014'
    usage = '''
    # Web Application Security Assessment Reporting

    The idea behind is to speed up the preparation stage of penetration
    testing and dynamic scanning reports as well as make it more uniform.

    ## Basics

    Microsoft Office Word is being used to prepare report templates.
    HP WebInspect and BurpSuite Pro scan exports might be used as input
    data for the report as well.
    XML, Yaml and Json are used as input formats.
    Report in Openxml format is the final product of this application.

    Error traceback is on. If you will work with templating and wont stick
    to the rules presented below, you will very likely encounter it.

    ## GUI Interface

    Main application window contains four fields that act as an input
    (drag & drop is supported):
    - Template - Word report template
    - Content - additional data that should be automatically propagated
      to the report
    - Scan - HP WebInspect / Burp Suite Pro scan
    - Knowledge base - knowledge base that could be used to reinforce
      final report customization

    Double click on given text area will popup the content on larger area.

    ## CLI Interface

    Command-line support has been added in order to allow bulk generation
    of report-files. Application currently supports one set of switches:
    
    -t template-file [-c content-file] [-k kb-file] [-s scan-file]
    -r report-file

    ## Word Template Preparation

    This application was tested with Office 2010 Word documents saved with
    Word XML Document format.

    To prepare a template Developer tab must be enabled on Word's Ribbon.
    Rich Text Content Control on Developer tab is used to mark parts that
    should be used for templating. All Rich Text Controls in order to be
    properly recognized must have Title property set using Properties.
    Design Mode is also handy.

    Before I start with templating, few introductionary words: Word document
    itself is organized in an xml structure which more or less sticks to the
    HTML layout principles. There are paragraphs (p), inline text (run ~ span),
    tables, table rows (tr), table row columns (tc) and others. When content
    is marked using Rich Text Content Control it gets encapsulated. So when
    you encapsulate a whole line - it will work as paragraph, part of inline
    text - will work as a span etc. When during templating you will use multi
    line content, it will be splitted and added in multiple tags. Therefore,
    one should keep in mind that while paragraphs will work as expected, span
    blocks will just be contatenated. Margin settings for paragraphs will be
    propagated across each line of template content. Run parent might be run,
    paragraph or another element.

    I strongly advise to prepare your template using method of small steps.
    If you encounter some unexpected error, you will be able to revert back
    easily. Also take a look at Tools / Template structure preview wchich
    should aid you during some issues analysis.
    
    The following titles are reserved for the purpose of automated template
    population:
    
    Required fields:
    - Finding - finding template, it should include other Finding.* tags
      - Finding.Name
      - Finding.Severity - allowed: Critical, High, Medium, Low, Informational
        Best Practices

    Optional fields:
    - Finding.* - other fields
    - Findings.Chart - chart with all findings will be filled automatically
    - Findings.Critical - placeholder for critical findings
    - Findings.High
    - Findings.Medium
    - Findings.Low
    - Findings.Informational
    - Findings.BestPractices
    - Summary.Critical - must be a row
    - Summary.Critical.Finding - will be filled with finding name
    - Summary.Critical.* - optional fields, will be put in finding template
    - Summary.High
    - Summary.High.Finding
    - Summary.High.*
    - Summary.Medium
    - Summary.Medium.Finding
    - Summary.Medium.*
    - Summary.Low
    - Summary.Low.Finding
    - Summary.Low.*
    - Summary.Informational
    - Summary.Informational.Finding
    - Summary.Informational.*
    - Summary.BestPractices
    - Summary.BestPractices.Finding
    - Summary.BestPractices.*
    - *.*.*
    - *.*
    - *

    It is recommended to arrange data in structures, e.g.:
    - Report.Name - paragraph
    - Report.Owner - span
    ...

    It is possible to prepare table templates as well, e.g.:
    - History - table row
    - History.Version - table column (or span within table column)
    - History.Date - table column
    ...
    It applies to both data and Finding structures.

    Conditionals

    Conditional blocks have been introduced to findings in the following ways:
    - Surrounding template data within e.g. Finding.Critical?
      causes block to appear only for critical findings.
    - If finding includes some tag, e.g. Finding.Description, conditional
      block Finding.Description? could be added to the template. Content will
      only be rendered if finding have Finding.Description set.

    It is now also possible to add root conditional blocks for content itself.
    Example use would be e.g. adding Pentest? conditional block and few tags,
    like Pentest.Name, Pentest.Version etc. If at least one Pentest.* will
    be present and filled, block will be left, otherwise it will be removed
    from generated report.

    Counters

    When needed, summary.[finding].property# counter could be added to show
    lists volume. 

    ## Content and Knowledge Base preparation

    Content could be provided in yaml or json format. Values could be one of
    three kinds:
    - plain text
    - Regular pseudo-html data: <html>...</html>
    - Inline pseudo-html data: <ihtml>...</ihtml> - keep in mind that it
      might have some limitations and it could cause problems.

    Additionally, Knowledge Base file could be also used. It should basically
    look like findings section of content. Name and Severity fields are mandatory,
    all other are optional. If content will not provide appropiate value for
    given section, it will be taken from knowlege base, if such section will be
    available there.

    ## Inline pseudo-html allowed tags

    Following tags are available:
    - <b>...</b> - bold
    - <i>...</i> - italic
    - <y>...</y> (or <yellow>...</yellow) - yellow highlight
    - <r>...</r> (or <red>...</red> or <redwhite>...</redwhite>) - red
      highlight with white text
    - <a href="...">...</a> - link (remember to use scheme in url, e.g.
      http://)
    - <font [face="..."] [size="..."]>...</font> - font, size should be
      2x bigger (e.g. 22 instead 11px), no units just a numeric value

    ## Regular pseudo-html allowed tags

    All inline tags could be used. Additionally available are:
    - <ul><li>...</li>...</ul> - unnumbered list
    - <ol><li>...</li>...</ol> - numbered list
    - <xl>...</xl> - supplementary, indented only list item, e.g.:
      <ul><li>item</li><xl>item description</xl><li>...</li></ul>
    - <img src="..." [alt="..."] [width="..."] /> - image, no units for width,
      just a numerical value
    - <br/> - break line

    ## Scans

    HP WebInspect 10.1.177.0 and Burp Suite Pro 1.6beta2 were used during
    tests. To prepare source scan data within HP WebInspect, Export Scan
    Details (Full) with XML Export Format. For Burp use Report Selected
    Issues, select XML and pick Base64-encode requests and responses.

    ## License
    
    GNU General Public License, Version 2, June 1991
    '''

    def MainWindow(self):
        self.__MainWindow(application=self)

    class __MainWindow(wx.Frame):

        # Variables set during __init__

        #report
        #application
        #scan
        #template
        #icon
        #menu_file_open_c
        #menu_file_open_k
        #menu_file_generate_c
        #menu_file_generate_k
        #menu_file_generate_r
        #menu_file_save_t
        #menu_file_save_s
        #menu_file_save_k
        #menu_file_save_r
        #menu_tools_template_structure_preview
        #ctrl_st_t
        #ctrl_tc_t
        #ctrl_st_c
        #ctrl_tc_c
        #ctrl_st_s
        #ctrl_tc_s
        #ctrl_st_k
        #ctrl_tc_k
        #ctrl_st_r
        #ctrl_tc_r
        #color_tc_bg_e
        #color_tc_bg_d

        def __init__(self, application=None, parent=None, *args,
                     **kwargs):  #style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER

            #self.report = None
            self.report = Report()
            self.application = application
            self.scan = None
            wx.Frame.__init__(self, parent, title=self.application.title + ' ' + self.application.version, *args,
                              **kwargs)  #style=style
            self.Bind(wx.EVT_CLOSE, lambda x: self.Destroy())

            myStream = cStringIO.StringIO(base64.b64decode(icon))
            myImage = wx.ImageFromStream(myStream)
            myBitmap = wx.BitmapFromImage(myImage)
            self.icon = wx.EmptyIcon()
            self.icon.CopyFromBitmap(myBitmap)
            self.SetIcon(self.icon)

            # Menu arrangement

            menu = wx.MenuBar()

            class Index(object):
                def __init__(self, current):
                    self.__current = current - 1

                @property
                def current(self):
                    return self.__current

                @current.setter
                def current(self, x):
                    self.__current = x

                def next(self):
                    self.__current += 1
                    return self.__current

            index = Index(100)
            menu_file = wx.Menu()
            menu_file.Append(index.next(), 'Open Report &Template...')
            self.Bind(wx.EVT_MENU, self.Open_Template, id=index.current)
            self.menu_file_open_c = menu_file.Append(index.next(), 'Open &Content...')
            self.menu_file_open_c.Enable(False)
            self.Bind(wx.EVT_MENU, self.Open_Content, id=index.current)
            menu_file.Append(index.next(), 'Open &Scan...')
            self.Bind(wx.EVT_MENU, self.Open_Scan, id=index.current)
            self.menu_file_open_k = menu_file.Append(index.next(), 'Open &Knowledge Base...')
            self.menu_file_open_k.Enable(False)
            self.Bind(wx.EVT_MENU, self.Open_Knowledge_Base, id=index.current)
            #menu_file.AppendSeparator()
            #self.menu_file_generate_c = menu_file.Append(index.next(), '&Generate Content')
            #self.menu_file_generate_c.Enable(False)
            #self.Bind(wx.EVT_MENU, self.Generate_Content, id=index.current)
            #self.menu_file_generate_k = menu_file.Append(index.next(), 'G&enerate Knowledge Base')
            #self.menu_file_generate_k.Enable(False)
            #self.Bind(wx.EVT_MENU, self.Generate_Knowledge_Base, id=index.current)
            #self.menu_file_generate_r = menu_file.Append(index.next(), 'Ge&nerate Report')
            #self.menu_file_generate_r.Enable(False)
            #self.Bind(wx.EVT_MENU, self.Generate_Report, id=index.current)
            menu_file.AppendSeparator()
            self.menu_file_save_t = menu_file.Append(index.next(), '&Save Template As...')
            self.menu_file_save_t.Enable(False)
            self.Bind(wx.EVT_MENU, self.Save_Template_As, id=index.current)
            #self.menu_file_save_k = menu_file.Append(index.next(), 'S&ave Knowledge Base As...')
            #self.menu_file_save_k.Enable(False)
            #self.Bind(wx.EVT_MENU, self.Save_Knowledge_Base_As, id=index.current)
            self.menu_file_save_s = menu_file.Append(index.next(), 'Sa&ve Scan As...')
            self.menu_file_save_s.Enable(False)
            self.Bind(wx.EVT_MENU, self.Save_Scan_As, id=index.current)
            self.menu_file_save_r = menu_file.Append(index.next(), 'Save &Report As...')
            self.menu_file_save_r.Enable(False)
            self.Bind(wx.EVT_MENU, self.Save_Report_As, id=index.current)
            menu_file.AppendSeparator()
            menu_file.Append(wx.ID_EXIT, 'E&xit\tCtrl+Q', 'Exit application')
            self.Bind(wx.EVT_MENU, self.Exit, id=wx.ID_EXIT)
            menu.Append(menu_file, '&File')
            menu_view = wx.Menu()
            self.menu_view_c = menu_view.Append(index.next(), 'C&lean template', kind=wx.ITEM_CHECK)
            self.Bind(wx.EVT_MENU, self.Clean_template, id=index.current)
            self.menu_view_c.Check(True)
            menu_view.AppendSeparator()
            self.menu_view_y = menu_view.Append(index.next(), '&yaml', kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.Use_yaml, id=index.current)
            self.menu_view_j = menu_view.Append(index.next(), '&json', kind=wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.Use_json, id=index.current)
            self.menu_view_y.Check(True)
            menu.Append(menu_view, '&View')
            menu_tools = wx.Menu()
            self.menu_tools_template_structure_preview = menu_tools.Append(index.next(), 'Te&mplate structure preview')
            self.menu_tools_template_structure_preview.Enable(False)
            self.Bind(wx.EVT_MENU, self.Template_Structure_Preview, id=index.current)
            menu.Append(menu_tools, '&Tools')
            menu_help = wx.Menu()
            menu_help.Append(index.next(), '&Usage')
            self.Bind(wx.EVT_MENU, self.Usage, id=index.current)
            menu_help.Append(index.next(), '&Changelog')
            self.Bind(wx.EVT_MENU, self.Changelog, id=index.current)
            menu_help.AppendSeparator()
            menu_help.Append(wx.ID_ABOUT, '&About')
            self.Bind(wx.EVT_MENU, self.About, id=wx.ID_ABOUT)
            menu.Append(menu_help, '&Help')
            self.SetMenuBar(menu)

            # Frame layout arrangement

            class FileDropTarget(wx.FileDropTarget):
                def __init__(self, target, handler):
                    wx.FileDropTarget.__init__(self)
                    self.target = target
                    self.handler = handler

                def OnDropFiles(self, x, y, filenames):
                    self.handler(filenames)

            panel = wx.Panel(self)
            vbox = wx.BoxSizer(wx.VERTICAL)
            fgs = wx.FlexGridSizer(5, 2, 9, 25)

            # Template
            self.ctrl_st_t = wx.StaticText(panel, label='Template:')
            self.ctrl_st_t.Enable(False)
            self.ctrl_tc_t = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 3 * 17,))

            def ctrl_tc_t_OnFocus(e):
                self.ctrl_tc_t.ShowNativeCaret(False)
                # for unknown reason this refuse to work in wxpython 3.0
                e.Skip()

            def ctrl_tc_t_OnDoubleclick(e):
                if self.ctrl_st_t.IsEnabled():
                    self.application.TextWindow(self, title='Template Preview', content=self.ctrl_tc_t.GetValue())
                e.Skip()

            self.ctrl_tc_t.Bind(wx.EVT_SET_FOCUS, ctrl_tc_t_OnFocus)
            self.ctrl_tc_t.Bind(wx.EVT_LEFT_DCLICK, ctrl_tc_t_OnDoubleclick)

            def ctrl_tc_t_OnDropFiles(filenames):
                if len(filenames) != 1:
                    wx.MessageBox('Single file is expected!', 'Error', wx.OK | wx.ICON_ERROR)
                    return
                self._open_template(filenames[0])

            ctrl_tc_t_dt = FileDropTarget(self.ctrl_tc_t, ctrl_tc_t_OnDropFiles)
            self.ctrl_tc_t.SetDropTarget(ctrl_tc_t_dt)
            fgs.AddMany([(self.ctrl_st_t, 1, wx.EXPAND), (self.ctrl_tc_t, 1, wx.EXPAND)])

            # Content
            self.ctrl_st_c = wx.StaticText(panel, label='Content:')
            self.ctrl_st_c.Enable(False)
            self.ctrl_tc_c = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 3 * 17,))
            self.color_tc_bg_e = self.ctrl_tc_c.GetBackgroundColour()
            self.ctrl_tc_c.Enable(False)
            self.color_tc_bg_d = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
            self.ctrl_tc_c.SetBackgroundColour(self.color_tc_bg_d)

            def ctrl_tc_c_OnFocus(e):
                self.ctrl_tc_c.ShowNativeCaret(False)
                e.Skip()

            def ctrl_tc_c_OnDoubleclick(e):
                if self.ctrl_st_c.IsEnabled():
                    self.application.TextWindow(self, title='Content Preview', content=self.ctrl_tc_c.GetValue())
                e.Skip()

            self.ctrl_tc_c.Bind(wx.EVT_SET_FOCUS, ctrl_tc_c_OnFocus)
            self.ctrl_tc_c.Bind(wx.EVT_LEFT_DCLICK, ctrl_tc_c_OnDoubleclick)

            def ctrl_tc_c_OnDropFiles(filenames):
                if len(filenames) != 1:
                    wx.MessageBox('Single file is expected!', 'Error', wx.OK | wx.ICON_ERROR)
                    return
                self._open_content(filenames[0])

            ctrl_tc_c_dt = FileDropTarget(self.ctrl_tc_c, ctrl_tc_c_OnDropFiles)
            self.ctrl_tc_c.SetDropTarget(ctrl_tc_c_dt)
            fgs.AddMany([(self.ctrl_st_c, 1, wx.EXPAND), (self.ctrl_tc_c, 1, wx.EXPAND)])

            # Scan
            self.ctrl_st_s = wx.StaticText(panel, label='Scan:')
            self.ctrl_st_s.Enable(False)
            self.ctrl_tc_s = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 3 * 17,))

            def ctrl_tc_s_OnFocus(e):
                self.ctrl_tc_s.ShowNativeCaret(False)
                e.Skip()

            def ctrl_tc_s_OnDoubleclick(e):
                if self.ctrl_st_s.IsEnabled():
                    self.application.TextWindow(self, title='Scan Preview', content=self.ctrl_tc_s.GetValue())
                e.Skip()

            self.ctrl_tc_s.Bind(wx.EVT_SET_FOCUS, ctrl_tc_s_OnFocus)
            self.ctrl_tc_s.Bind(wx.EVT_LEFT_DCLICK, ctrl_tc_s_OnDoubleclick)

            def ctrl_tc_s_OnDropFiles(filenames):
                if len(filenames) != 1:
                    wx.MessageBox('Single file is expected!', 'Error', wx.OK | wx.ICON_ERROR)
                    return
                self._open_scan(filenames[0])

            ctrl_tc_s_dt = FileDropTarget(self.ctrl_tc_s, ctrl_tc_s_OnDropFiles)
            self.ctrl_tc_s.SetDropTarget(ctrl_tc_s_dt)
            fgs.AddMany([(self.ctrl_st_s, 1, wx.EXPAND), (self.ctrl_tc_s, 1, wx.EXPAND)])

            # Knowledge Base
            self.ctrl_st_k = wx.StaticText(panel, label='Knowledge Base:')
            self.ctrl_st_k.Enable(False)
            self.ctrl_tc_k = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 3 * 17,))
            self.ctrl_tc_k.Enable(False)
            self.ctrl_tc_k.SetBackgroundColour(self.color_tc_bg_d)

            def ctrl_tc_k_OnFocus(e):
                self.ctrl_tc_k.ShowNativeCaret(False)
                e.Skip()

            def ctrl_tc_k_OnDoubleclick(e):
                if self.ctrl_st_k.IsEnabled():
                    self.application.TextWindow(self, title='KB Preview', content=self.ctrl_tc_k.GetValue())
                e.Skip()

            self.ctrl_tc_k.Bind(wx.EVT_SET_FOCUS, ctrl_tc_k_OnFocus)
            self.ctrl_tc_k.Bind(wx.EVT_LEFT_DCLICK, ctrl_tc_k_OnDoubleclick)

            def ctrl_tc_k_OnDropFiles(filenames):
                if len(filenames) != 1:
                    wx.MessageBox('Single file is expected!', 'Error', wx.OK | wx.ICON_ERROR)
                    return
                self._open_kb(filenames[0])

            ctrl_tc_k_dt = FileDropTarget(self.ctrl_tc_k, ctrl_tc_k_OnDropFiles)
            self.ctrl_tc_k.SetDropTarget(ctrl_tc_k_dt)
            fgs.AddMany([(self.ctrl_st_k, 1, wx.EXPAND), (self.ctrl_tc_k, 1, wx.EXPAND)])

            # Report
            #self.ctrl_st_r = wx.StaticText(panel, label='Report:')
            #self.ctrl_st_r.Enable (False)
            #self.ctrl_tc_r = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(200, 3*17,))
            #self.ctrl_tc_r.Enable(False)
            #self.ctrl_tc_r.SetBackgroundColour (self.color_tc_bg_d)
            #def ctrl_tc_r_OnFocus (e):
            #    self.ctrl_tc_r.ShowNativeCaret (False)
            #    e.Skip()
            #self.ctrl_tc_r.Bind (wx.EVT_SET_FOCUS, ctrl_tc_r_OnFocus)
            #fgs.AddMany ([(self.ctrl_st_r, 1, wx.EXPAND), (self.ctrl_tc_r, 1, wx.EXPAND)])

            fgs.AddGrowableRow(0, 1)
            fgs.AddGrowableRow(1, 1)
            fgs.AddGrowableRow(2, 1)
            fgs.AddGrowableRow(3, 1)
            #fgs.AddGrowableRow (4, 1)
            fgs.AddGrowableCol(1, 1)
            vbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
            #data = wx.TextCtrl(panel)
            #hbox1 = wx.BoxSizer (wx.HORIZONTAL)
            #hbox1.Add(data, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, border=10)
            #vbox.Add (hbox1, 0, wx.ALL|wx.EXPAND, 0)
            panel.SetSizer(vbox)
            vbox.Fit(self)
            self.SetMinSize(self.GetSize())
            #panel = wx.Panel (self)
            #vbox = wx.BoxSizer (wx.VERTICAL)
            #hbox1 = wx.BoxSizer (wx.HORIZONTAL)
            ##st1 = wx.StaticText (panel, wx.ID_ANY, label='Not yet ready')
            #st1 = wx.StaticText (panel, wx.ID_ANY, label='Template:', size=(100, -1,))
            #hbox1.Add (st1, 0, wx.ALL, 5)
            #tc1 = wx.TextCtrl (panel, wx.ID_ANY, size=(300, -1,))
            #hbox1.Add (tc1, 1, wx.ALL|wx.EXPAND, 0)
            #vbox.Add (hbox1, 0, wx.ALL|wx.EXPAND, 0)
            #hbox2 = wx.BoxSizer (wx.HORIZONTAL)
            #st2 = wx.StaticText (panel, wx.ID_ANY, label='Scan:', size=(100, -1,))
            #hbox2.Add (st2, 0, wx.ALL, 5)
            #tc2 = wx.TextCtrl (panel, wx.ID_ANY, size=(300, -1,))
            #hbox2.Add (tc2, 1, wx.ALL|wx.EXPAND, 0)
            #vbox.Add (hbox2, 0, wx.ALL|wx.EXPAND, 0)
            ##vbox.Add (hbox1, 0, wx.CENTER, 5)
            #panel.SetSizer (vbox)
            #vbox.Fit (self)
            self.Center()
            self.Show()
            #print 'loaded'

        def Exit(self, e):
            self.Close()

        def About(self, e):
            dialog = wx.AboutDialogInfo()
            #dialog.SetIcon (wx.Icon('icon.ico', wx.BITMAP_TYPE_PNG))
            dialog.SetIcon(self.icon)
            dialog.SetName(self.application.long_title+' - '+self.application.title)
            dialog.SetVersion(self.application.version)
            dialog.SetCopyright(self.application.c)
            dialog.SetDescription('\n'.join(map(lambda x: x[4:], self.application.about.split('\n')[1:][:-1])))
            
            dialog.SetWebSite(self.application.url)
            dialog.SetLicence(self.application.license)
            wx.AboutBox(dialog)

        def Template_Structure_Preview(self, e):
            self.application.TextWindow(self, title=self.Usage.__name__, content=self.report.template_dump_struct())

        def Usage(self, e):
            self.application.TextWindow(self, title=self.Usage.__name__, content='\n'.join(
                map(lambda x: x[4:], self.application.usage.split('\n')[1:][:-1])))

        def Changelog(self, e):
            self.application.TextWindow(self, title=self.Changelog.__name__, content='\n'.join(
                map(lambda x: x[4:], self.application.changelog.split('\n')[1:][:-1])))

        def Destroy(self):
            map(lambda x: x.Close(), filter(lambda x: isinstance(x, wx.Frame), self.GetChildren()))
            wx.WakeUpIdle()
            #print 'destroying MainWindow'
            super(wx.Frame, self).Destroy()

        def Open_Template(self, e):
            openFileDialog = wx.FileDialog(self, 'Open Template', '', '', 'XML files (*.xml)|*.xml|All files (*.*)|*.*',
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self._open_template(openFileDialog.GetPath())

        def _open_template(self, filename):
            self.ctrl_st_t.Enable(False)
            self.ctrl_tc_t.SetValue('')
            self.ctrl_st_c.Enable(False)
            self.ctrl_tc_c.SetValue('')
            self.menu_file_open_k.Enable(False)
            self.menu_file_save_t.Enable(False)
            self.menu_file_save_r.Enable(False)
            self.menu_tools_template_structure_preview.Enable(False)
            #if self.report:
            #    del self.report
            #self.report = Report()
            #print self.report._skel
            self.report.template_load_xml(filename, clean=self.menu_view_c.IsChecked())
            if self.menu_view_y.IsChecked():
                self.ctrl_tc_t.SetValue(self.report.template_dump_yaml())
            else:
                self.ctrl_tc_t.SetValue(self.report.template_dump_json())
            self.ctrl_st_t.Enable(True)
            self.ctrl_tc_c.Enable(True)
            self.ctrl_tc_c.SetBackgroundColour(self.color_tc_bg_e)
            self.ctrl_tc_k.Enable(True)
            self.ctrl_tc_k.SetBackgroundColour(self.color_tc_bg_e)
            self.menu_file_open_k.Enable(True)
            self.menu_file_open_c.Enable(True)
            self.menu_file_save_t.Enable(True)
            self.menu_tools_template_structure_preview.Enable(True)
            if self.scan:
                self.menu_file_save_r.Enable(True)

        def Open_Content(self, e):
            openFileDialog = wx.FileDialog(self, 'Open Content', '', '',
                                           'Content files (*.yaml; *.json)|*.yaml;*.json|All files (*.*)|*.*',
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self._open_content(openFileDialog.GetPath())

        def _open_content(self, filename):
            self.ctrl_st_c.Enable(False)
            json_ext = '.json'
            if filename[-len(json_ext):] == json_ext:
                self.report.content_load_json(filename)
            else:
                self.report.content_load_yaml(filename)
            if self.menu_view_y.IsChecked():
                self.ctrl_tc_c.SetValue(self.report.content_dump_yaml())
            else:
                self.ctrl_tc_c.SetValue(self.report.content_dump_json())
            self.ctrl_st_c.Enable(True)
            self.menu_file_save_r.Enable(True)

        def Open_Scan(self, e):
            openFileDialog = wx.FileDialog(self, 'Open Scan', '', '',
                                           'Scan files (*.xml; *.yaml; *.json)|*.xml;*.yaml;*.json|All files (*.*)|*.*',
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self._open_scan(openFileDialog.GetPath())

        def _open_scan(self, filename):
            self.menu_file_save_s.Enable(False)
            if self.scan is not None:
                del self.scan
            self.scan = Scan(filename)
            if self.menu_view_y.IsChecked():
                self.ctrl_tc_s.SetValue(self.scan.dump_yaml())
            else:
                self.ctrl_tc_s.SetValue(self.scan.dump_json())
            self.ctrl_st_s.Enable(True)
            self.menu_file_save_s.Enable(True)
            self.menu_file_save_r.Enable(True)

        #def Open_Knowledge_Base (self, e):
        #    pass
        #def Generate_Content (self, e):
        #    pass
        #def Generate_Knowledge_Base (self, e):
        #    pass
        #def Generate_Report (self, e):
        #    pass
        def Save_Template_As(self, e):
            openFileDialog = wx.FileDialog(self, 'Save Template As', '', '',
                                           'Content files (*.yaml; *.json)|*.yaml;*.json|All files (*.*)|*.*',
                                           wx.FD_SAVE | wx.wx.FD_OVERWRITE_PROMPT)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            json_ext = '.json'
            filename = openFileDialog.GetPath()
            h = open(filename, 'w')
            if filename[-len(json_ext):] == json_ext:
                h.write(self.report.template_dump_json())
            else:
                h.write(self.report.template_dump_yaml())
            h.close()

        def Save_Scan_As(self, e):
            openFileDialog = wx.FileDialog(self, 'Save Scan As', '', '',
                                           'Content files (*.yaml; *.json)|*.yaml;*.json|All files (*.*)|*.*',
                                           wx.FD_SAVE | wx.wx.FD_OVERWRITE_PROMPT)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            json_ext = '.json'
            filename = openFileDialog.GetPath()
            h = open(filename, 'w')
            if filename[-len(json_ext):] == json_ext:
                h.write(self.scan.dump_json())
            else:
                h.write(self.scan.dump_yaml())
            h.close()

        #def Save_Knowledge_Base_As (self, e):
        #    pass
        def Save_Report_As(self, e):
            openFileDialog = wx.FileDialog(self, 'Save Report As', '', '',
                                           'XML files (*.xml)|*.xml|All files (*.*)|*.*',
                                           wx.FD_SAVE | wx.wx.FD_OVERWRITE_PROMPT)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            filename = openFileDialog.GetPath()
            if filename == self.report._template_filename:
                wx.MessageBox('For safety reasons, template overwriting with generated report is not allowed!', 'Error',
                              wx.OK | wx.ICON_ERROR)
                return
            self.report.scan = self.scan
            self.report.xml_apply_meta()
            self.report.save_report_xml(filename)

        def Clean_template(self, e):
            if self.ctrl_st_t.IsEnabled():
                self.report._template_reload(clean=self.menu_view_c.IsChecked())
                if self.ctrl_st_c.IsEnabled():
                    self.report._content_reload()
                self._refresh()

        def _refresh(self):
            if self.menu_view_y.IsChecked():
                self._Use_yaml()
            else:
                self._Use_json()

        def _Use_yaml(self):
            if self.ctrl_st_t.IsEnabled():
                self.ctrl_tc_t.SetValue(self.report.template_dump_yaml())
            if self.ctrl_st_c.IsEnabled():
                self.ctrl_tc_c.SetValue(self.report.content_dump_yaml())
            if self.ctrl_st_s.IsEnabled():
                self.ctrl_tc_s.SetValue(self.scan.dump_yaml())

        def Use_yaml(self, e):
            self._Use_yaml()

        def _Use_json(self):
            if self.ctrl_st_t.IsEnabled():
                self.ctrl_tc_t.SetValue(self.report.template_dump_json())
            if self.ctrl_st_c.IsEnabled():
                self.ctrl_tc_c.SetValue(self.report.content_dump_json())
            if self.ctrl_st_s.IsEnabled():
                self.ctrl_tc_s.SetValue(self.scan.dump_json())

        def Use_json(self, e):
            self._Use_json()

        def Open_Knowledge_Base(self, e):
            openFileDialog = wx.FileDialog(self, 'Open Knowledge Base', '', '',
                                           'Knowledge Base files (*.yaml; *.json)|*.yaml;*.json|All files (*.*)|*.*',
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self._open_kb(openFileDialog.GetPath())

        def _open_kb(self, filename):
            self.ctrl_st_k.Enable(False)
            json_ext = '.json'
            if filename[-len(json_ext):] == json_ext:
                self.report.kb_load_json(filename)
            else:
                self.report.kb_load_yaml(filename)
            if self.menu_view_y.IsChecked():
                self.ctrl_tc_k.SetValue(self.report.kb_dump_yaml())
            else:
                self.ctrl_tc_k.SetValue(self.report.kb_dump_json())
            self.ctrl_st_k.Enable(True)
            #self.menu_file_save_k.Enable (True)
            self.menu_file_save_r.Enable(True)

    class TextWindow(wx.Frame):

        def __init__(self, parent, content='', size=(500, 600,), *args, **kwargs):
            if parent is not None:
                for title in ['title']:
                    if title in kwargs:
                        kwargs[title] = parent.application.title + ' - ' + kwargs[title]
            wx.Frame.__init__(self, parent, size=size, *args, **kwargs)
            if parent is not None:
                self.SetIcon(parent.icon)
            self.Bind(wx.EVT_CLOSE, lambda x: self.Destroy())
            tc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

            def tc_OnFocus(e):
                tc.ShowNativeCaret(False)
                e.Skip()

            tc.Bind(wx.EVT_SET_FOCUS, tc_OnFocus)
            tc.SetValue(content)
            self.Center()
            self.Show()

        def Destroy(self):
            #print 'destroying TextWindow'
            super(wx.Frame, self).Destroy()

    def CLI(self):
        self.__CLI(application=self)
    
    class __CLI(wx.Frame):

        # application

        def __init__(self, application=None, *args, **kwargs):
            self.application = application
            wx.Frame.__init__(self, None, *args, **kwargs)
            self.Bind(wx.EVT_CLOSE, lambda x: self.Destroy())
            #self.Show()
            import sys

            def val (key):
                if key in sys.argv:
                    return sys.argv[sys.argv.index('-t')+1]
                else:
                    return None
                
            def is_yaml (filename):
                ext = '.yaml'
                return filename[-len(ext):] == ext
                
            template_file = val('-t')
            content_file = val('-c')
            kb_file = val('-k')
            scan_file = val('-s')
            report_file = val('-r')

            if template_file and report_file:
                report = Report()
                report.template_load_xml(template_file)
                if content_file:
                    if is_yaml(content_file):
                        report.content_load_yaml(content_file)
                    else:
                        report.content_load_json(content_file)
                if kb_file:
                    if is_yaml(kb_file):
                        report.kb_load_yaml(kb_file)
                    else:
                        report.kb_load_json(kb_file)
                if scan_file:
                    report.scan = Scan(scan_file)                
                report.xml_apply_meta()
                report.save_report_xml(report_file)
            else:
                print 'Usage: '
                print
                print '    '+self.application.title+'.exe'
                print '        start GUI application'
                print
                print '    '+self.application.title+'.exe -t template-file [-c content-file] [-k kb-file] [-s scan-file] -r report-file'
                print '        generate report'
                print
                print '    '+self.application.title+'.exe [any other arguments]'
                print '        display usage and exit'
            
            self.Close()

        def Destroy(self):
            #print 'destroying CLI'
            super(wx.Frame, self).Destroy()

    # GUI class

    def __init__(self):
        #wx_app = wx.App (redirect=False) # DEVELOPMENT
        wx_app = wx.App()
        #self.TextWindow(None, title='asdasd', content='bsdsdasd')
        import sys
        #sys.argv = [sys.argv[0], '--help']
        #sys.argv = [sys.argv[0], '-t', 'asdad']
        if len(sys.argv) > 1:
            self.CLI()
        else:
            self.MainWindow()
        wx_app.MainLoop()


if __name__ == '__main__':
    GUI()