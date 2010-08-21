"""
This later plugin provides a "list-subdirs" command
as requested by bigfudge: http://news.ycombinator.com/item?id=1620445
"""

import os,sys

def find_dotlater(path):
	for p in os.listdir(path):
		p = os.path.join(path, p)
		if p.endswith("/.later"):
			yield p
		elif os.path.isdir(p):
			for sub in find_dotlater(p):
				yield sub

def cmd_list_subdirs(args):
	"""Shows an issue list in every subdirectory with a later database.
For details see "help list" """
	cmd = sys.argv[0]
	for path in find_dotlater("."):
		assert path.endswith("/.later")
		path = path[:-7]
		if len(path) > 2:
			path = path[2:]
		print ":"*10, path
		ret = os.getcwd()
		os.chdir(path)
		os.system("%s list %s" % (cmd, " ".join(args)))
		os.chdir(ret)

def plugin_init(hooks):
	hooks["cmd_list-subdirs"] = cmd_list_subdirs

