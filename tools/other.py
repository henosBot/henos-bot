import time
import traceback

def is_booster(member):
    if member in member.guild.premium_subscribers:
        return True
    else:
        return False

def date(target, clock=True):
    if not clock:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

def timetext(name):
    return f"{name}_{int(time.time())}.txt"

def tracebacker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"
