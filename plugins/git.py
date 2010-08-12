import subprocess

def plugin_init(hooks):
	guess = hooks['guess_username']
	def git_guess_username():
		try:
			user_name = subprocess.Popen(["git", "config", "user.name"], stdout=subprocess.PIPE).communicate()[0].strip()
			user_mail = subprocess.Popen(["git", "config", "user.email"], stdout=subprocess.PIPE).communicate()[0].strip()
			if user_name != "" and user_mail != "":
				return "%s <%s>" % (user_name, user_mail)
			return
		except:
			pass
		return guess()
	hooks['guess_username'] = git_guess_username
	

