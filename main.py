#!/usr/bin/python
from collections import OrderedDict
from collections import Set
import re

# File names
RAW_FILENAME = 'raw.bib'
OUT_FILENAME = 'bib.bib'

# Regex
ENTRY_BEG = '^@(.+){(.+),'
ENTRY_DATA = '(\w+)\s*=\s*{(.+)}'

# Format
TAB_SIZE = 4
DATA_FORMAT = '%s = {%s},\n'

# Blacklist
blacklist = set([
					'category',
					'isbn',
					'issn',
					'doi',
					'month',
				])

formats =	{
				'year': ('(\d{4})', '%s'),
				'pages': ('(\d+)\D+(\d+)', '%s--%s'),
			}

# Raw file read
key = None
dataset = OrderedDict()
file = open(RAW_FILENAME, 'rb')
for n, line in enumerate(file):

	# Removing non-ascii characters
	line = ''.join(i for i in line if ord(i)<128)

	# Looking for new bib entry
	regex = re.findall(ENTRY_BEG, line)
	if len(regex) > 0 and len(regex[0]) >= 2:
			category	= regex[0][0].lower()
			key			= regex[0][1]
			dataset[key] = OrderedDict()
			dataset[key]['category'] = category

	# Looking for bib data
	regex = re.findall(ENTRY_DATA, line)
	if len(regex) > 0 and len(regex[0]) >= 2:
			category	= regex[0][0].lower()
			data		= regex[0][1]

			# Upper Case
			data = re.sub(r'{|}', r'', data)
			data = re.sub(r'([A-Z][A-Z]+)', r'{\1}', data)

			# Valid category
			if category not in blacklist:

				# Filtering 
				if category in formats:

					regex = re.findall(formats[category][0], data)
					if len(regex) > 0:
						data = formats[category][1] % regex[0]

				# Storing
				dataset[key][category] = data

file.close()

# Compiling output
buf = ''
for e in dataset:

	# Header
	buf += '@%s{%s,\n' % (dataset[e]['category'], e)

	# Contents
	for d in [d for d in dataset[e] if d != 'category']:

		# Tab
		buf += TAB_SIZE*' '

		# Data
		buf += DATA_FORMAT % (d, dataset[e][d])

	# Closing
	buf += '}\n\n'

# Filtered file writing
with open(OUT_FILENAME, 'wb') as file:
	file.write(buf)
