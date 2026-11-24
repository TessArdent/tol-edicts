# Patch v2.5.3 - Newcomer system, class fixes, Unity 2020

- Date: 2020-03-26 15:35:30 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/patch-v2-5-3-newcomer-system-class-fixes-unity-2020/80918.html
- Original: https://forum.imperium42.com/t/patch-v2-5-3-newcomer-system-class-fixes-unity-2020/80918
- Replies by other users left out: 1

---

## Class Fixes

- *Matchmaking* abil feedback chaos should now be fixed (after reverting a failed scalability revamp).
- Maid no longer has a chance to have herself be the starting *Matchmake* abil target.
- “Couldn’t heal” message from *Heal* abilities have been fixed and should show the correct message, which was especially affecting Knight (*poor Knight*).
- Mystic’s *Conduit* abil fixed, no longer able to target *King*.
- There are now more-aggressive checks for neutral win checks (with eyes on objective-based classes, sellsword, etc).
- Inquisitor *Heathen* icon should now -only- show to the Inquisitor when using *Interrogate*.
- *Tornado* and *Teleportation* redirection abils:
  - Will no longer be able to target the same person 2x.
  - Can now also target self in 2nd slot instead of only 1st (both not both).
- Fixed *Disguise/Defile* abils that, when combo’d with the same target being converted, would cause desyncs or “incomplete” converts due to unintended errors.
  - This should fix *some* feedback-on-convert bugs that were missing (although there are likely additional causes of the bug).
  - This also fixed Scorned *Disguise* working on someone that died during a convert attempt to the same target.
  - Since this likely caused bugs elsewhere, this may magically fix other bugs in an unknown fashion.

## Newcomer

Now that we have a newcomer flag, we can start adding some goodies to start building good habits, such as additional system messages (Thx [@Stoneage](https://fol-archive.netlify.app/u/stoneage)). These messages are customized per-faction, then also customized per-class for some Neutral.

- Whenever a user is *imprisoned*, they will be instructed how to handle Prince interrogation.
  - For BD, you’ll be notified that the Prince is a trusted ally and that you should quickly reveal your class + logs to gain his trust.
  - For Cultseen, you’ll be notified how dangerous an adversary the Prince is - and that you should offer FAKE claim/logs to gain his trust.
  - (…etc)
- Whenever a user is *on trial*, they will be instructed similarly ^ for how to handle a viable defense.
- At the beginning of each day, there will be a reminder to update your logbook with recent actions + results.
- Fixed 2019 anniversary gifts still leaking out to new players.

## General

- Upgraded to Unity 2020: Tested throughout, but there may be some unexpected bugs (or improvements!). The main point of this was to reap the benefits of improved editor performance (previously sluggish) and fix some editor bugs I’ve been waiting for. This will also allow us to use the new graphics pipeline in the future. Let me know if you get a performance boost!
- I can confirm Win7 works with this Unity 2020 port.
- Swapped lighting over to an experimental “GPU”-based schema (previously CPU-based): This may improve performance.
- Some glitchy walls were magically fixed after the Unity 2020 upgrade.
- Added some code to prep for *Sloof Lirpa* (more later).
- Settings *Logs Preset* button is now layered *behind* the *Texture Quality* dropdown list.
- Slightly adjusted color hues after Unity 2020 rendered them “grayish”: Let me know if you like it better or worse (if noticed):

<https://i.imgur.com/CgBJtmZ.jpg>

^ I noticed that some death hallways are stupidly bright. I’ll fix it soon, but figured bug fixes trumped this in priority.

I was playing around with Unity 2020 features and had some nice “light hazing” on the Windows, but of course reverted because that was just a small test and would’ve broken consistency. One day, *everything* involving light needs to be revamped - I know it’s not pretty.

## Test Realm (Beta)

Test realm is only up occasionally before a patch - it’s not persistent. However, when it is up, it’s best to streamline some stuff:

- Players will now auto-lock-in their *username* as their IGN.
- Player classes will now be revealed at the beginning of each match with a new *welcome to test realm* message to better discover combos to test.

## Dev Notes

- Bugs are bad, mmkay. There are still bugs unfixed, but I gotta patch a little at a time to deliver what we have instead of hoard them all for a giant patch that could potentially cause more bugs - I decided to focus on the ones that had the best bang for the buck of notable impact and speed to fix (some bugs take wayy too long to test and I really wanted to fix a LIST of bugs instead of just like 1 or 2 that will get more love later).
- In one of the fixes above, there was a HUGE bug involving converting + disguise together that would just destroy silently games (for the rest of the match). This fix will have positive ripple effects on what else it fixed. Let’s keep an eye this patch what was “magically” fixed. If you notice something fixed not in patch notes, let me know!
- I am still stupidly close to finishing localization. Next patch may be a bit boring so I can wrap this up. Localization to a native English speaker sounds boring, but opening the doors to new markets means higher budget: The more we make and the more globally-popular we are, the better things that arrive to *Throne*! We’ve demonstrated for years we always reinvest in *Throne of Lies*. Localization means better things for all of us.

---

## More

<https://forum.imperium42.com/t/mini-patch-v2-5-4-testing/81011>

---

–Xblade
<https://discord.gg/tol>

---

### Follow-up #2 by í42-Xblade (2020-03-27)

Added:

## Newcomer

Now that we have a newcomer flag, we can start adding some goodies to start building good habits, such as additional system messages (Thx [@Stoneage](https://fol-archive.netlify.app/u/stoneage)). These messages are customized per-faction, then also customized per-class for some Neutral.

- Whenever a user is *imprisoned*, they will be instructed how to handle Prince interrogation.
  - For BD, you’ll be notified that the Prince is a trusted ally and that you should quickly reveal your class + logs to gain his trust.
  - For Cultseen, you’ll be notified how dangerous an adversary the Prince is - and that you should offer FAKE claim/logs to gain his trust.
  - (…etc)
- Whenever a user is *on trial*, they will be instructed similarly ^ for how to handle a viable defense.
- At the beginning of each day, there will be a reminder to update your logbook with recent actions + results.

---

### Follow-up #4 by í42-Xblade (2020-03-28)

Added:

- Maid no longer has a chance to have herself be the starting *Matchmake* abil target.
- Settings *Logs Preset* button is now layered *behind* the *Texture Quality* dropdown list.
- I can confirm Win7 works with this Unity 2020 port.

---

### Follow-up #5 by í42-Xblade (2020-03-29)

Live!
