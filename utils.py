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
