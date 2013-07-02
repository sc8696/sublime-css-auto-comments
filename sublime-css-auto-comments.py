import sublime, sublime_plugin
import re

class CssautocommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# get the nearest css property
		cssProp = self.findCss()

		if(cssProp != None):
			# enter edit mode
			self.writeOut(edit, cssProp)

	def getCursor(self):
		cursorReg = self.view.sel()[0]
		return cursorReg

	def findCss(self):
		regex = self.view.find(".*?(\n*\s*)\{", self.getCursor().begin());

		if(regex != None):

			cssProp = self.view.substr(regex)

			cssName = cssProp = cssProp[:-1].strip()
			cssType = ''
			cssAttrs = ''

			if (cssProp[0] == '.'):
				cssType = 'class'
				cssName = cssProp[1:]
			elif (cssProp[0] == '#'):
				cssType = 'id'
				cssName = cssProp[1:]
			else:
				cssType = 'element'

			attrs = re.match('(.*)(\[(.*)=(.*)\])', cssName)
			if attrs:
				cssAttrs = attrs.group(2)[1:-1]
				cssName = attrs.group(1)

			relatedCss = self.findRelatedCss(cssProp)
			relatedSass = self.findNestedCss(cssProp)

			# Combine all lists
			relatedCss = relatedCss + relatedSass
			# Remove dupes whilst preserving order
			relatedCss = [x for i,x in enumerate(relatedCss) if i==relatedCss.index(x)]
			#Remove empty elements
			relatedCss = filter(None, relatedCss)

			return {
				'name' : cssName,
				'type' : cssType,
				'attrs': cssAttrs,
				'related' : relatedCss
			}

		return None

	def findRelatedCss(self, cssProp):
		relatedCss = self.view.find_all(str(cssProp) + "(\.|\:)+.*(\n*\s*)\{")
		
		for i in range(0,len(relatedCss)):
			relatedCss[i] = self.view.substr(relatedCss[i])[len(cssProp):-1].strip()

		return relatedCss

	def findNestedCss(self, cssProp):
		relatedCss = self.view.find_all(cssProp + "(\.|\:)+.*(\n*\s*)\{")

		nestedCss = []
		
		recurseLimit = 100

		for i in range(0, len(relatedCss)):

			cssBlock = ""

			linelen = 0
			offset = 0
			bracketStack = []
			recurseAmount = 0
			firstBracketFound = False

			point = relatedCss[i].begin()

			line = self.getLineContents(self.view.line(point).begin())

			# Start with something on the bracket stack
			bracketStack.append('{')

			# Start building the CSS block to parse
			cssBlock += line.replace(" ","")

			#This is for keeping track of what line its on
			linelen = len(line)
			offset = offset + linelen + 1

			# Keep going when the brackets are unmatched
			while len(bracketStack) > 0 and recurseAmount < recurseLimit:		

				# Stack operations
				for j in range (0,line.count('{')):
					if firstBracketFound:
						bracketStack.append('{')

					if(line.count('{')):
						firstBracketFound = True					


				for j in range (0,line.count('}')):	
					bracketStack.pop()

				recurseAmount+=1

			# weird way of getting the next line. Start where the cursor began
			# and keep adding on the cumulative length of the next line and recurse
				line = self.getLineContents(self.view.line(point).begin() + offset)
				cssBlock += line.replace(" ","")
				linelen = len(line) + 1
				offset = offset + linelen

				if recurseAmount == 99:
					print "Recursion limit hit. Check your brackets are evenly matched for element " + self.view.substr(relatedCss[i])[:-1]

			bracketCount = 0
			fullClass = ""
			hookFound = True
			hookedClass = True
			# Go through the concatted css block to find stuff
			# Could probably do this in the while loop up there ^^^
			# Pretty funny logic. Don't try and follow it D:
			for j in range (0, len(cssBlock)):
				if cssBlock[j] == "{":
					bracketCount+=1

					if hookFound == True:
						hookedClass = True
					else:
						hookedClass = False

					hookFound = False

				if cssBlock[j] == "}":
					bracketCount-=1

					if bracketCount == 1:
						hookedClass = True

				if cssBlock[j] == "&":
					if hookedClass:
						hookFound =  True
						tempString = cssBlock[j+1:]
						if bracketCount == 1:
							fullClass = tempString.partition('{')[0]
						else:
							fullClass = fullClass + tempString.partition('{')[0]

						hookedClass = False

						nestedCss.append(fullClass)

		return nestedCss

	def getLineContents(self, line):
		return self.view.substr(self.view.line(line))


	def writeOut(self, edit, cssAttr):

		markup = ''

		cssName = cssAttr['name']
		cssType = cssAttr['type']
		cssAttrs = cssAttr['attrs']
		relatedCss = cssAttr['related']

		if cssAttrs:
			cssAttrs = ' ' + cssAttrs

		if(cssType == 'class'):
			markup = '<div class="' + cssName + cssAttrs + '">markup</div>'
		elif(cssType == 'id'):
			markup = '<div id="' + cssName + cssAttrs + '">markup</div>'
		elif(cssType == 'element'):
			markup = '<' + cssName + cssAttrs + '>Markup</' + cssName + '>'


		# replace the current cursor with a comment block and auto fill in all the attributes
		cursor =  self.getCursor()
		line = self.view.line(cursor)
		self.view.insert(edit, cursor.begin(), '/**\n')
		self.view.insert(edit, self.getCursor().begin(), '  * @name ' + cssName.title() + '\n')
		self.view.insert(edit, self.getCursor().begin(), '  * @description Style for the ' + cssName + ' ' + cssType + '\n')

		for i in range(0, len(relatedCss)):
			self.view.insert(edit, self.getCursor().begin(), '  * @state ' + relatedCss[i] + ' - ' + relatedCss[i].replace("."," ").replace(":"," ")[1:] + ' state\n')

		self.view.insert(edit, self.getCursor().begin(), '  * @markup\n')
		self.view.insert(edit, self.getCursor().begin(), '  *   ' + markup + '\n')
		self.view.insert(edit, self.getCursor().begin(), '  */\n')
