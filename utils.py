import functools

import pymel.core as pm


def preserve_huds(func):
    """Preserve current huds' visibility, positions and delete any huds created within `func`."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # store current huds' names, visibility and positions
        old_huds = pm.headsUpDisplay(listHeadsUpDisplays=True) or []
        old_visibility = [get_hud_visibility(hud) for hud in old_huds]
        old_positions = [get_hud_position(hud) for hud in old_huds]

        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # delete new huds
            all_huds = pm.headsUpDisplay(listHeadsUpDisplays=True) or []
            for hud in all_huds:
                if hud not in old_huds:
                    pm.headsUpDisplay(hud, remove=True)

            # restore huds' visibility
            for hud, visible in zip(old_huds, old_visibility):
                pm.headsUpDisplay(hud, e=True, visible=visible)

            # restore hud positions
            for hud, (section, block) in zip(old_huds, old_positions):
                pm.headsUpDisplay(hud, e=True, section=section, block=block)

    return wrapper


def get_hud_visibility(hud):
    return pm.headsUpDisplay(hud, q=True, visible=True)


def get_hud_position(hud):
    section = pm.headsUpDisplay(hud, q=True, section=True)
    block = pm.headsUpDisplay(hud, q=True, block=True)
    return section, block


# line: 63 u'E     \x1b[0m\x1b[1m\x1b[36mleft:  \x1b[0m\x1b[1m\x1b[32m3\x1b[0m'
# line: 63 u'E     {reset}{bright}{cyan}left:  {reset}{bright}{geeen}3{reset}'

# line: 65 u'E     \x1b[0m\x1b[1m\x1b[36mright: \x1b[0m\x1b[1m\x1b[31m4\x1b[0m'
# line: 65 u'E     {reset}{bright}{cyan}right: {reset}{bright}{red}4{reset}'

# reset = "\x1b[0m"
# bright = "\x1b[1m"
# dim = "\x1b[2m"
# underscore = "\x1b[4m"
# blink = "\x1b[5m"
# reverse = "\x1b[7m"
# hidden = "\x1b[8m"

# black = "\x1b[30m"
# red = "\x1b[31m"
# green = "\x1b[32m"
# yellow = "\x1b[33m"
# blue = "\x1b[34m"
# magenta = "\x1b[35m"
# cyan = "\x1b[36m"
# white = "\x1b[37m"

# BGblack = "\x1b[40m"
# BGred = "\x1b[41m"
# BGgreen = "\x1b[42m"
# BGyellow = "\x1b[43m"
# BGblue = "\x1b[44m"
# BGmagenta = "\x1b[45m"
# BGcyan = "\x1b[46m"
# BGwhite = "\x1b[47m"
