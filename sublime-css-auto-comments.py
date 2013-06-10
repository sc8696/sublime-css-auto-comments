import sublime, sublime_plugin

class CssautocommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# get the nearest css property
		cssProp = self.findCss()

		# enter edit mode
		self.editMode(edit, cssProp)

	def getCursor(self):
		cursorReg = self.view.sel()[0]
		return cursorReg

	def findCss(self):
		cssProp = self.view.substr(self.view.find(".*\{", self.getCursor().begin()))
		cssName = cssProp = cssProp[:-1].strip()
		cssType = ''

		if (cssProp[0] == '.'):
			cssType = 'class'
			cssName = cssProp[1:]
		elif (cssProp[0] == '#'):
			cssType = 'id'
			cssName = cssProp[1:]
		else:
			cssType = 'element'	

		relatedCss = self.findRelatedCss(cssProp)

		return {
			'name' : cssName,
			'type' : cssType,
			'related' : relatedCss
		}

	def findRelatedCss(self, cssProp):
		relatedCss = self.view.find_all(cssProp + "(\.|\:).+\{")
		
		for i in range(0,len(relatedCss)):
			relatedCss[i] = self.view.substr(relatedCss[i])[len(cssProp):-1].strip()

		print relatedCss
		return relatedCss


	def editMode(self, edit, cssAttr):

		markup = ''

		cssName = cssAttr['name']
		cssType = cssAttr['type']
		relatedCss = cssAttr['related']

		if(cssType == 'class'):
			markup = '<div class="' + cssName + '">markup</div>'
		elif(cssType == 'id'):
			markup = '<div id="' + cssName + '">markup</div>'
		elif(cssType == 'element'):
			markup = '<' + cssName + '>Markup</' + cssName + '>'


		# replace the current cursor with a comment block and auto fill in all the attributes
		cursor =  self.getCursor()
		line = self.view.line(cursor)
		self.view.insert(edit, cursor.begin(), '/**\n')
		self.view.insert(edit, self.getCursor().begin(), '  * @name ' + cssName.title() + '\n')
		self.view.insert(edit, self.getCursor().begin(), '  * @description Style for the ' + cssName + ' ' + cssType + '\n')

		for i in range(0, len(relatedCss)):
			self.view.insert(edit, self.getCursor().begin(), '  * @state ' + relatedCss[i] + ' - ' + relatedCss[i][1:] + ' state\n')

		self.view.insert(edit, self.getCursor().begin(), '  * @markup\n')
		self.view.insert(edit, self.getCursor().begin(), '  *   ' + markup + '\n')
		self.view.insert(edit, self.getCursor().begin(), '  */\n')

