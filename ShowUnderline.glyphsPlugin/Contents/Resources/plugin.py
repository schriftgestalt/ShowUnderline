# encoding: utf-8

from GlyphsApp.plugins import *
from Foundation import NSClassFromString, NSLog
from AppKit import NSButton, NSTexturedRoundedBezelStyle, NSImageOnly, NSImageScaleNone, NSToggleButton
import traceback

class ShowUnderline(GeneralPlugin):
	def settings(self):
		self.name = Glyphs.localize({'en': u'Show Underline', 'de': u'Unterstrichen'})
	def start(self):
		try:
			Glyphs.addCallback(self.addUndelineButton, TABDIDOPEN)
			Glyphs.addCallback(self.removeUndelineButton, TABWILLCLOSE)
			Glyphs.addCallback(self.drawUndeline, DRAWBACKGROUND)
			Glyphs.addCallback(self.drawUndeline, DRAWINACTIVE)
			thisBundle = NSBundle.bundleForClass_(NSClassFromString("ShowUnderline"))
			if thisBundle != None:
				self.toolBarIcon = NSImage.alloc().initWithContentsOfFile_(thisBundle.pathForImageResource_("underLineTemplate.pdf"))
				self.toolBarIcon.setTemplate_(True)
		except:
			print traceback.format_exc()
	
	def addUndelineButton(self, notification):
		try:
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
				Tab.userData["underlineButton"] = button
				userDefaults = NSUserDefaultsController.sharedUserDefaultsController()
				button.bind_toObject_withKeyPath_options_("value", userDefaults, "values.GeorgSeifert_showUnderline", None)
				userDefaults.addObserver_forKeyPath_options_context_(Tab.graphicView(), "values.GeorgSeifert_showUnderline", 0, 123)
		except:
			NSLog(traceback.format_exc())
	
	def removeUndelineButton(self, notification):
		Tab = notification.object()
		button = Tab.userData["underlineButton"]
		if button != None:
			button.unbind_("value")
			userDefaults = NSUserDefaultsController.sharedUserDefaultsController()
			userDefaults.removeObserver_forKeyPath_(Tab.graphicView(), "values.GeorgSeifert_showUnderline")
	
	def drawUndeline(self, layer, options):
		try:
			if NSUserDefaults.standardUserDefaults().boolForKey_("GeorgSeifert_showUnderline"):
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