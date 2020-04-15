import functools

import maya.cmds as cmds


def preserve_huds(func):
    """
    Temporarily hide and preserve the current heads up displays in position and visibility.
    Works with the assumption that huds are moved only down in their sections.
    Does NOT cover edge cases of moving up or left and right.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # store current huds' names, position and visibility
        old_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True) or []
        old_huds_visibility = [hud_visibility(hud) for hud in old_huds]
        sections = {i: {} for i in range(10)}
        for hud in old_huds:
            section, block = get_hud_position(hud)
            sections[section][block] = hud

        # hide all huds
        for hud in old_huds:
            cmds.headsUpDisplay(hud, e=True, visible=False)

        try:
            return func(*args, **kwargs)
        except:
            raise
        finally:
            # delete new huds
            new_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True) or []
            for hud in new_huds:
                if hud not in old_huds:
                    cmds.headsUpDisplay(hud, remove=True)

            # restore huds' visibility
            for hud, visibility in zip(old_huds, old_huds_visibility):
                cmds.headsUpDisplay(hud, e=True, visible=visibility)

            # restore huds' positions
            for section, blocks in sections.items():
                for block, hud in sorted(blocks.items()):
                    cmds.headsUpDisplay(hud, e=True,
                                        section=section, block=block)
    return inner


def hud_visibility(hud):
    return cmds.headsUpDisplay(hud, q=True, visible=True)


def get_hud_position(hud):
    section = cmds.headsUpDisplay(hud, q=True, section=True)
    block = cmds.headsUpDisplay(hud, q=True, block=True)
    return section, block
