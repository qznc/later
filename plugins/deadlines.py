"""
This plugin calculated a schedule.
It uses the issue properties deadline, manhours, and dependencies to do that.
"""

from datetime import timedelta, datetime

_HOOKS=None

MANHOURS_PER_DAY = 1
def parse_datetime(string):
   return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")

def manhours2timedelta(manhours):
   return timedelta(manhours / MANHOURS_PER_DAY)

def schedule():
   deadlined = list()
   toschedule = list()
   imap = dict()
   # init
   for guid in _HOOKS.be_all_guids():
      issue = _HOOKS.be_load_issue(guid)
      if issue.properties["status"] == "closed":
         continue
      imap[issue.guid] = issue
      if "deadline" in issue.properties:
         issue.ideadline = parse_datetime(issue.properties["deadline"])
         deadlined.append(issue)
      else:
         issue.ideadline = None
         toschedule.append(issue)
   # read dependencies
   for issue in imap.values():
      issue.idependencies = list()
      guids = issue.properties.get("dependencies", "").split()
      for guid in guids:
         issue.idependencies.append(imap[guid])
   # schedule
   while deadlined:
      deadi = deadlined.pop()
      delta = manhours2timedelta(deadi.properties.get("manhours", 1))
      start = deadi.ideadline - delta
      for depi in deadi.idependencies:
         if depi.ideadline and depi.ideadline < start:
            continue
         depi.ideadline = start
         deadlined.append(depi)
   # return sorted
   def ideadline_cmp(a, b):
      if a.ideadline == None:
         return 1
      if b.ideadline == None:
         return -1
      return cmp(a.ideadline, b.ideadline)
   return sorted(imap.values(), ideadline_cmp)

def cmd_schedule(args):
   """Output a schedule of all issues.
Argument is how many manhours per day
should be calculated. Default is '1'."""
   if len(args) > 1:
      error("at most one argument: how many manhours per day")
   if args:
      global MANHOURS_PER_DAY
      MANHOURS_PER_DAY = float(args[0])
   
   print datetime.now().strftime("%Y-%m-%d\n==========")
   
   for issue in schedule():
      if issue.ideadline:
         print issue.ideadline.strftime("%Y/%m/%d"),
      else:
         print "          ",
      print issue.shortString()

def plugin_init(hooks):
   global _HOOKS
   hooks["cmd_schedule"] = cmd_schedule
   _HOOKS = hooks

