import os

_HOOKS = None

def rev_file():
	"""
	Get path of revision file
	"""

	revs = os.path.join(_HOOKS.be_get_data_dir(), 'revisions')

	if not os.path.isfile(revs):
		fh = open(revs, 'w')
		fh.write('')
		fh.close()

	return revs

def avail_name(name):
	"""
	Check that it is an available name (does not exist anymore)
	"""

	rev = rev_file()
	if not rev: return True

	fh = open(rev)
	for l in fh:
		if name.strip() == l.strip():
			return False
	return True

def all_issues():
	return (_HOOKS.be_load_issue(g) for g in _HOOKS.be_all_guids())

def pending_issues():
	return [iss for iss in all_issues() if not iss.properties.get('revision') and iss.properties.get('status')!='reported']

def revision_list():
	"""
	List all revisions
	"""

	rev = rev_file()
	if not rev: return

	revs = [' '+l.strip() for l in open(rev).readlines() if l.strip()]
	if revs:
		print 'Revision (latest on top):'
		print '\n'.join(revs)
	else:
		print 'No revisions available'

def revision_new(name):
	"""
	revision new <rev_name>		Add closed issues to <rev_name>
	"""
	
	if not avail_name(name):
		print 'Cannot use %s, already taken'%name
		return 

	issues = [iss for iss in pending_issues() if iss.properties['status']=='closed']
	
	if not len(issues):
		print 'Error. Nothing to add to revision', name
		return

	print 'Issues under revision %s:'%name
	for iss in issues:
		iss.properties['revision'] = name
		_HOOKS.be_store_issue(iss)
		print iss.shortString()
	
	rev = rev_file()
	revs = [l.strip() for l in open(rev).readlines() if l.strip()]

	fh = open(rev, 'w')
	fh.write('\n'.join([name]+revs))
	fh.close()

def revision_show(name):
	if avail_name(name):
		print '%s does not exist, did you get the name right?'%name
		return
	
	issues = [iss.shortString() for iss in all_issues() if iss.properties.get('revision')==name]
	
	if not len(issues):
		print 'There is nothing in revision', name
		return

	print 'Issues under revision %s:'%name
	print '\n'.join(issues)

def revision_rollback():
	try: 
		revs = open(rev_file()).readlines()
		rev = revs[-1].strip()
		assert (rev)
	except IndexError, AssertionError:
		print 'No revision available'
		return
	
	for iss in all_issues(): 
		if iss.properties.get('revision')==rev:
			iss.properties['revision'] = None
			_HOOKS.be_store_issue(iss)

	revs = [rev.strip() for rev in revs[:-1] if rev.strip()]

	fh = open(rev_file(), 'w')
	fh.write('\n'.join(revs)+'\n')
	fh.close()

	print 'Revision %s removed'%rev

def revision_status():
	issues =  pending_issues() 

	if not issues:
		print 'There is nothing to add to your revision'

	for iss in issues:
		print iss.shortString()

def revision_help():
	print _HOOKS.get('cmd_revision').__doc__

def cmd_revision(args):
	"""
revision list				List all revisions
revision new <rev_name>		Add newly closed issues to <rev_name>
revision rollback			Remove all issues from most recent
revision status				Show issues queued for next revision
revision show <rev_name>	Show issues in <rev_name>
	"""

	if not len(args):
		return revision_help()

	cmd = args[0]
	args = args[1:]
	
	if cmd=='list':
		revision_list()
	elif cmd=='new':
		if not len(args):
			print 'Please insert valid revision name'
			print revision_new.__doc__
			return
		
		revision_new(' '.join(args))
	elif cmd=='show':
		if not len(args):
			print 'Please insert valid revision name'
			print revision_show.__doc__
			return

		revision_show(' '.join(args))
	elif cmd=='rollback':
		revision_rollback()
	elif cmd=='status':
		revision_status()
	else:
		print 'Error: unrecognized command\n'
		return revision_help()


def plugin_init(hooks):
	global _HOOKS
	hooks['cmd_revision'] = cmd_revision
	_HOOKS = hooks
