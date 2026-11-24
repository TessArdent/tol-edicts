# Patch v2.5.1 (LIVE): Bug Fixes/Stability

- Date: 2020-02-25 13:03:25 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/patch-v2-5-1-live-bug-fixes-stability/80431.html
- Original: https://forum.imperium42.com/t/patch-v2-5-1-live-bug-fixes-stability/80431
- Replies by other users left out: 14

---

![teemo-128-anim-v5](https://fol-archive.netlify.app/uploads/default/original/3X/8/1/81b8af0deaf6b64409dd1eb7d7288889935c86b7.gif)
v2.5.1 is mostly a bugfix patch - some recent, some overdue.

## Class Bug Fixes/Improvements

- Fixed King’s *Decide Fate (Slam)* abil that was grayed out when it shouldn’t be.
- In addition to the *Decide Fate*, there were several other day abilities that were fixed in a similar way involving being grayed out or enabled when they weren’t supposed to (opposite of what’s expected). Day abilities will need a revamp, one day, but this bandaid should hold fine.
- *Pocket Dimension* abil fixed for immediate attacks.
- Fixed Maid’s *Matchmake* abil involving targeting Mastermind day <4 (when supposed to be disguised) + also when matched with Sellsword that should now display as expected.
- Fixed Enforcer’s *Protection* abil that was set to 0 targets instead of 1, therefore not doing anything upon click.
- Fixed a series of major “semi-permanent bugs” all involving a group of events where certain status flags would NOT reset until you reboot the game if you hosted the next one, causing tons of confusion (thx [@Stoneage](https://fol-archive.netlify.app/u/stoneage)):
  - Fixed bleed immune “Inoc Virus” bug that was causing a bleed-immune user to be perma immune the rest of his session throughout multiple games.
  - Fixed Cult/Unseen chat that would sometimes “leak” if you weren’t supposed to see it the rest of the session.
  - Fixed temporary death immunities that would permanently go away for the rest of the session once gone (eg, *Armored*).
  - Fixed *Royal Blood* randomly showing as true/false for the rest of the session.
- ~~*Assassinate* abil was inadvertently setting targets *unhealable*, so anyone *except* reaper would see opposite effects and cause confusion.~~ Set to revert next patch: Seems like this caused an issue rather than fixed.
- ~~Sellsword didn’t used to win with auto-resolve (1 BD alive): SS should now win if bd doesn’t win.~~ (Needs further testing – this is extremely difficult to test. Someone said it worked, and someone else said it didn’t)
- *Gaze*, *Bat Eyelashes*, and *Probe* abils can no longer indirectly target the King (eg, redirect): it will show a “King found” feedback instead of an actual reveal. Memos updated.
- Butler should no longer see night UI when pending suicide.
- Invoker’s *Strings of Mithras* abil now allows same-target.
- Overlook’s *action word* is now *overlook* instead of *survey* when using the ability.
- Pocket Dimension’s “could have been…” feedback tip removed *suicide* from a possibility.
- More *Pretender* mentions from feedback tips were removed (such as silence abils).
- Added memos to redirection abils to clarify that *redirection conflicts may fail* (eg, a double-redirect such as with a self-redirect double redirection).

## General Bug Fixes

- Several lobby improvements when it comes to button enable/disable flow: Spamming the join button too early after leaving a room may have contributed to infinite loading screens and weirdness. Weird things happen when you spam the network servers.
- You can no longer change your name while you’re joining a room through a particular combo of events.
- Changing your name will no longer desync you from games, which would originally require a restart. This may have other domino-fixes, too, since a name desync isn’t good~
- Text input “Caret” will no longer “shift up vertically” when no text is entered.
- Double gp weekend rich text field fixed.
- Upgraded to a new Text engine version, fixing a bunch of random bugs, mostly involving Unicode.
- Lobby store now loads async for shorter freeze transition from login screen.
- Friends beyond the 1st 8 now loads/refreshes async, too.
- Fixed some desync recovery in lobby (if you were still in a group, some settings weren’t being reset).
- Desyncing from a game during loading screen should no longer show a placeholder name through the lobby UI.
- Joining between spectators<>players shouldn’t lock you inside, anymore.
- Fixed the “deduction panel” sometimes showing incorrect values when <16 players.
- Fixed some shader issue that always appears in logs that I… have no idea what this will actually fix O\_o

## Quality of Life

- Blacklisted *hate slurs* (*not* swears) are no longer `****` asterisk censored as we swap to an improved system:
  - Sentences that would normally censor now only shows to the **local player** (from their end, it looks like everyone saw it).
  - The idea is for trolls to stop trying different ways to bypass the hate slang filter until it works and for end-users to not even see messages that contain these. Trolls will wait for a reaction only to find … no one cares - maybe they’ll get bored. In the future, we will likely add an auto-report system for open-and-close cases like this.
  - If you used one of these blacklisted slangs, you probably were off-topic and ill-intentioned, anyway.
- Players that leave the room due to desync will be more prone to leaving behind a system message letting users know they were kicked by system.
- When you join a room, you’ll now auto-focus the chat.
- When you get to name selection, you’ll now auto-focus your IGN selection.
- When you choose your IGN, you’ll now auto-focus name selection chat.
- When the game starts, you’ll now auto-focus the main chat.
- You can now name yourself *Pretender* (by oddly-popular request :P)
- Settings resolution selection is now vertically centered.
- Quit confirm panel is no longer off-centered.
- Settings resolution dropdown dupes now display the refresh rate Hz.
- Quit button and quit confirm pane panel are now more-polished.

## Localization 中文

- Fixed the `<u></u>` bug that would wrap around text while using Chinese IME text selection popup.
- Fixed the deathnote small text.
- Plugged in a bunch of random localization. Tutorial and ability feedback next!

---

## Added While Testing

Now merged above, but just in case you already saw these notes both before/after testing:

- Lobby store now loads async for shorter freeze transition from login screen.
- Friends beyond the 1st 8 now loads/refreshes async, too.
- Fixed some desync recovery in lobby (if you were still in a group, some settings weren’t being reset).
- Desyncing from a game during loading screen should no longer show a placeholder name through the lobby UI.
- Joining between spectators<>players shouldn’t lock you inside, anymore.
- Fixed the “deduction panel” sometimes showing incorrect values when <16 players.
- Fixed some shader issue that always appears in logs that I… have no idea what this will actually fix O\_o

---

### Follow-up #3 by í42-Xblade (2020-02-25)

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/orangeandblack5/40/33172_2.png) orangeandblack5:

> If the player isn’t notified of this, that needs to be done.

The “f” word, among others, is not censored and everyone will see it. Only over-the-top words that no one uses, anyway. Players that actually play the game rarely get censored, if at all. Not notifying them prevents them spamming combinations until it works and satisfies the troll, thinking everyone saw it: Another gamedev suggested it and I was intrigued. The only notable words were censor are “ni–” and “fa–”, really.

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/orangeandblack5/40/33172_2.png) orangeandblack5:

> Plus, that makes it much easier to know who is actively bypassing the filter.

We won’t need to know if they never saw it and never got reported.

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/orangeandblack5/40/33172_2.png) orangeandblack5:

> This is significantly less likely if the blacklist is entirely slurs, not swears, but either way this notification should be made.

Correct - hate slurs only. I’ll clarify OP. In theory, this should lower the number of reports and trigger less people while even satisfying (or boring) the troll.

---

### Follow-up #7 by í42-Xblade (2020-02-25)

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/nuclearburrito/40/4723_2.png) NuclearBurrito:

> Will it still send the rest of the message besides the slur?

It sends the entire message to only the local player - uncensored - as if it sent to everyone [but no one else sees it].

---

### Follow-up #17 by í42-Xblade (2020-02-28)

## Added:

- Lobby store now loads async for shorter freeze transition from login screen.
- Friends beyond the 1st 8 now loads/refreshes async, too.
- Fixed some desync recovery in lobby (if you were still in a group, some settings weren’t being reset).
- Desyncing from a game during loading screen should no longer show a placeholder name through the lobby UI.
- Joining between spectators<>players shouldn’t lock you inside, anymore.
- Fixed the “deduction panel” sometimes showing incorrect values when <16 players.
- Fixed some shader issue that always appears in logs that I have no idea what will actually fix :stuck\_out\_tongue:

---

### Follow-up #18 by í42-Xblade (2020-03-04)

Now live ~
