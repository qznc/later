"""
This plugin provides a delete and a delete-closed command,
to clean up an issue database.
"""

_HOOKS=None

def cmd_delete(args):
	"""Delete a specific issue permanently."""
	if not args:
		error("need guid argument")
	guid = _HOOKS.be_complete_guid(args[0])
	if not guid:
		return
	_HOOKS.be_delete_issue(guid)

def cmd_delete_closed(args):
	"""Delete all closed issues permanently."""
	assert len(args) == 0
	for guid in _HOOKS.be_all_guids():
		cmd_delete([guid])

def plugin_init(hooks):
	global _HOOKS
	hooks["cmd_delete"] = cmd_delete
	hooks["cmd_delete-closed"] = cmd_delete_closed
	_HOOKS = hooks

