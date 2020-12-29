# encoding: utf-8

from __future__ import division, print_function, unicode_literals
from GlyphsApp import *
from GlyphsApp import objcObject
from GlyphsApp.plugins import *
from GlyphsApp.plugins import pathForResource
from AppKit import NSButton, NSUserDefaultsController, NSTexturedRoundedBezelStyle, NSImageOnly, NSImageScaleNone, NSToggleButton, NSRectFill, NSNotificationCenter
import traceback

class ShowUnderline(GeneralPlugin):
	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({'en': u'Show Underline', 'de': u'Unterstrichen'})
	@objc.python_method
	def start(self):
		#Glyphs.addCallback(self.addUnderlineButton_, TABDIDOPEN)
		#Glyphs.addCallback(self.removeUnderlineButton_, TABWILLCLOSE)
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, "addUnderlineButton:", TABDIDOPEN, objc.nil)
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, "removeUnderlineButton:", TABWILLCLOSE, objc.nil)
		Glyphs.addCallback(self.drawUnderline, DRAWBACKGROUND)
		Glyphs.addCallback(self.drawUnderline, DRAWINACTIVE)

		# load icon from bundle
		iconPath = pathForResource("underLineTemplate", "pdf", __file__)
		self.toolBarIcon = NSImage.alloc().initWithContentsOfFile_(iconPath)
		self.toolBarIcon.setTemplate_(True)

	def addUnderlineButton_(self, notification):
		Tab = notification.object()
		if hasattr(Tab, "addViewToBottomToolbar_"):
			button = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 18, 14))
			button.setBezelStyle_(NSTexturedRoundedBezelStyle)
			button.setBordered_(False)
			button.setButtonType_(NSToggleButton)
			button.setTitle_("")
			button.cell().setImagePosition_(NSImageOnly)
			button.cell().setImageScaling_(NSImageScaleNone)
			button.setImage_(self.toolBarIcon)
			Tab.addViewToBottomToolbar_(button)
			try:
				Tab.tempData["underlineButton"] = button # Glyphs 3
			except:
				Tab.userData["underlineButton"] = button # Glyphs 2
			userDefaults = NSUserDefaultsController.sharedUserDefaultsController()
			button.bind_toObject_withKeyPath_options_("value", userDefaults, objcObject("values.GeorgSeifert_showUnderline"), None)
			userDefaults.addObserver_forKeyPath_options_context_(Tab.graphicView(), objcObject("values.GeorgSeifert_showUnderline"), 0, 123)

	def removeUnderlineButton_(self, notification):
		Tab = notification.object()
		try:
			button = Tab.tempData["underlineButton"] # Glyphs 3
		except:
			button = Tab.userData["underlineButton"] # Glyphs 2
		if button != None:
			button.unbind_("value")
			userDefaults = NSUserDefaultsController.sharedUserDefaultsController()
			userDefaults.removeObserver_forKeyPath_(Tab.graphicView(), "values.GeorgSeifert_showUnderline")

	@objc.python_method
	def drawUnderline(self, layer, options):
		try:
			if Glyphs.boolDefaults["GeorgSeifert_showUnderline"]:
				master = layer.associatedFontMaster()
				thinkness = master.customParameters["underlineThickness"]
				position = master.customParameters["underlinePosition"]
				if thinkness != None and position != None:
					thinkness = float(thinkness)
					position = float(position)
					rect = NSMakeRect(0, position - (thinkness * 0.5), layer.width, thinkness)
					NSColor.colorWithDeviceRed_green_blue_alpha_(64.0/255.0, 79.0/255.0, 104.0/255.0, 1).set()
					NSRectFill(rect)
		except:
			NSLog(traceback.format_exc())
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
