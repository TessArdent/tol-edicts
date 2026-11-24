# Patch v2.6.0b - Icons revamp, Class Fixes, Stats

- Date: 2020-04-12 13:43:58 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/patch-v2-6-0b-icons-revamp-class-fixes-stats/81245.html
- Original: https://forum.imperium42.com/t/patch-v2-6-0b-icons-revamp-class-fixes-stats/81245
- Replies by other users left out: 10

---

> **Patch v2.6.0:** *Tons of Good \*\*\*\**

# Summary

1. Tons of notable, class-specific bug fixes.
2. Added some basic stats to lobby “Account” section.
3. Revamped nearly *all* non-iconic icons.

---

## Class Fixes/Balance

- Fixed a bunch of *convert* abil bugs:
  - Both Observer/Princess night abils now show feedback upon convert.
  - Redirecting into someone being converted will now show feedback, as well.
  - Since this was a shared fix, there are likely other “feedback+convert” combo bugs that will magically resolve from this.
    ![image](https://fol-archive.netlify.app/uploads/default/original/3X/0/8/08b75e2384498386de200b758381646ed6451795.jpeg)
- Suicide toggle message no longer shows to evil King.
- Reaper’s *Gather Darkness* abil will no longer desync via a visual bug when attempting to cancel.
- The way day abilities cancel were backend-revamped, allowing more abilities to cancel and with proper feedback messages, as follows (some fixes, some additions):
  - Reaper’s *Gather Darkness* abil is now [properly] cancelable + displays cancel feedback msg.
  - Alchemist’s *Stoneskin* abil is now cancelable + displays cancel feedback msg.
  - Chronomancer’s *Pocket Dimension* abil is now cancelable + displays cancel feedback msg.
  - Physician/Ritualist/Herbalist’s *Exhume* abils are now cancelable + displays cancel feedback msg.
  - Mercenary’s *Don Armor* is now cancelable + displays cancel feedback msg.
  - *TrollBox* abils now displays cancel feedback msg.
  - …and probably others I forgot to list just for flavor text.
- Sellsword no longer wins with BD King.
- Maid’s *Nosy Servants* abil can now target reaped/soulless dead players.
- *Heal* abils will now properly say “did not require” instead of “could not” when healing someone being defended by a Knight.
- Aristocrat’s *Intrigue* abil no longer spam framed *Heal* abil feedback 2x. This will likely also fix related, gossip-like 2x spam bugs.
- Hunter’s *Bear Companion* abil priority lowered to ensure abils like *Defend* and *Safeguard* don’t take priority.
- Fixed Poss Facelift often [unintentionally] showing default disguise when canceling or changing beyond the 1st choice.
- Fixed *Debauchery*-type abils that was causing targets that had an active, targeted abil to randomly become redirect immune.
- Prince, Butler and possibly another [Hunter?] no longer announce *suicide* messages (from using a shared mechanic).
- Inquisitor’s *Holy Blessing* passive abil renamed to *Relentless Pursuit*.
- Removed the cringy salesman text for the Assassin’s *2-for-1* abil for *hovering*, but kept it in the full description.
- (More below @ v2.6a + v2.6b addendums)

## Stats

- There is now a stats summary section under “Account” (screenshot below).
- We will add on to this later. We actually track tons of per-class stats, but we haven’t tested them for accuracy, yet.
  ![](https://i.imgur.com/gSEX6pt.png)
  (The stats above are from test accounts, so ignore the math :stuck\_out\_tongue: )

## Class Cards, Text, Icons

- **Swapped out *most all* ability icons** for better, higher-quality, more-relevant ones (don’t worry – we kept the iconic ones). Demo below:
  ![image](https://fol-archive.netlify.app/uploads/default/original/3X/7/e/7e753c0047deb383e43ed0399525ad51196c4807.jpeg)
- Removed the bloaty *Hover* tab by popular request.
- Removed or swapped out some obsolete tips/class summaries.
- Swapped mentions of *Psychic* to *Mystic* in class card tips.
- Made the infinity symbol for # charges for less-awkward sizing/alignment compared to numbers.
- Got rid of the outline on # charges to look more “clean” (and ensured every icon corner has a dark corner area for visibility) + moved it to the bottom-right corner.
- Mass changed wording of “themself” to “themselves” in class cards and feedback because OCD.
- Updated tutorial to use the new icons/size/style.
- *Newcomer* tips will no longer be displayed in the tutorial since players don’t even get access to logs until later.

## Game Over

- Added a new victory and defeat theme song (30s) to make game over more satisfying.
- Faded in the winner screen background/text/logo on separate timers to look less '90s.
- Added the end screen music back (not sure when it went away).

## General

- Removed live game “disconnected/gray” names to prevent numerous forms of metagaming. ~~This is why we can’t have nice things.~~
- Online friends list buttons will now disable if they’re starting or in-game. You may still invite users at the end screen or login screen (showing just ‘Online’) to queue up an invite.
- *Newcomer* tips are now displayed by starting with an `*` asterisk and displayed in a gray-blue color.
- The daily *Newcomer* reminder tip to log actions+results now fits on 1 line for most default chat layouts to be less annoying while we burn this meta in new player minds :slight\_smile:
  ![image](https://fol-archive.netlify.app/uploads/default/original/3X/5/f/5f4f15290838ce50b829ef1364d68591a73098e1.png)
- Fixed lobby “Customize” header from showing the wrong highlighted header when swapping out and back in.
- Fixed class cards from showing up too early on the loading screen via TAB (that could cause issues if not fully loaded).
- Set max cap on tutorial whisper box to prevent freeze for someone who would oddly paste thousands of characters inside.

---

## More

See addendums below for hotfixes.

---

## Dev Notes

- Last patch fixed the FPS drops *and* we were able to keep the lighting quality upgrade, woot! Best of both worlds! One day, I’ll completely revamp lighting *completely* at minimal FPS cost (I know a way - just need the time to do it).
- This was supposed to be a pure bug fix patch, but distractions happen. Oops :slight\_smile: Hope you enjoy the sweet distractions on top of the bug fixes. We’re really excited about these new icons that actually fit way better than the old ones (no more Inquisitor attacking people with spears).

---

### Follow-up #2 by í42-Xblade (2020-04-12)

Additionally:

---

## v2.6a

- Fixed breaking bug for top-left panel.
- Removed “drawn” stat.
- Fixed tutorial “Assassinate” showing incorrect name/hover text.
- Some last-second icon changes.

---

## v2.6b

> v2.6.0~v2.6.0a Bugs

- Night abils now interact normally again after n2.
- Make v2.6’s new Victory theme song fanfare less abrupt.
- Suicide btn now shows correctly from v2.6
- Fixed negative win stat caching on loss (instead of losses++).
- More last-second icon changes.

> Live Bugs

- Fixed some ability spam exploits that would allow # of ability charges to go higher than what’s expected.
- Fixed several types of “Cannot Be Healed” <> “Does Not Require Healing” inconsistencies.
- Fixed an bug/exploit that allowed you to use both day abilities with the following combo:
  1. When using a day ability when you have 2 day abilities…
  2. And the ability selected is *cancelable*…
  3. And has no target panel.
  - For example, this fixed still being allowed to use Reaper’s *Icy Touch* after using *Gather Darkness*.
  - This also fixed abils that were *cancelable*, but would remove charges if you clicked it since it wasn’t technically supposed to be clickable at that time (eg, *Exhume* after you already used *Inoculate*).
- Possessor disguised as Cult will no longer trigger cult wins visual bug
- Handmaiden’s *Prying Servants* and similar abilities now allow targeting the dead Possessor body using his *Possess* abil.
- Corrected the color style for when a Butler ends your life via poison.
- Fixed incorrect Possessor class cards day tip info.
- Clamped class cards top left flags so they can’t drag.

---

## v2.6.1

<https://forum.imperium42.com/t/patch-v2-6-1-beta-testing/81687>

---

### Follow-up #3 by í42-Xblade (2020-04-12)



---

### Follow-up #4 by í42-Xblade (2020-04-18)



---

### Follow-up #12 by í42-Xblade (2020-04-23)

Alpha >> Beta testing

---

### Follow-up #13 by í42-Xblade (2020-04-27)

Beta Testing >> Live (Release Candidate)

---

### Follow-up #14 by í42-Xblade (2020-04-27)

Pending:

[https://forum.imperium42.com/t/patch-v2-6-0-live/81245/2?u=í42-xblade](https://forum.imperium42.com/t/patch-v2-6-0-live/81245/2?u=%C3%AD42-xblade)

EDIT: Reverted - back to testing.

---

### Follow-up #16 by í42-Xblade (2020-04-29)

These are all gameplay [beyond lobby] updates. Balance, you mean? New balance updates are pointless if core class bugs exist. In itself, it *is* balance since abilities will actually do what they say they’re supposed to do. We just added new mechanics [that should’ve existed, but didn’t] to about 10+ abilities!

## Balance Changes

- Observer/Princess night abils now show feedback upon converting! They can now finish their ability to get extra investigative info, giving an advantage to the Unseen.
- Redirecting additionally shows feedback, allowing better strategy next day.
- Suicide announcement is no longer seen by the King.
- Reaper’s abilities consume less souls, buffing him.
- Sellsword has less chance to win since can’t win with BD.
- Nosy Servants - new ability since it now works!

…The list goes on. Heck, Nosy Servants and some Reaper abils didn’t work at *all*. We can’t leave these kinds of bugs. Since I’m the only full-time dev, bug fixes are essential to progress the game, while balance before bug fixes only stirs a dirty bucket of water around. It’s not as exciting as new forms of balance, but it’s essential to the game’s stability to first knock these out.

## TL;DR

Class fixes *are* balance changes. If abils didn’t do what they said they’d do, it’s like adding completely new abilities once they are fixed. Or, at least, adding additional mechanics to them.

---

### Follow-up #20 by í42-Xblade (2020-05-04)

Release candidate for v2.6.0b due later today in off-peak

---

### Follow-up #21 by í42-Xblade (2020-05-04)

Release candidate being set live within the next few minutes!

---

### Follow-up #22 by í42-Xblade (2020-05-05)

Adding WIP known bugs for next hotfix

---

### Follow-up #23 by í42-Xblade (2020-05-10)

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/sabreoverdrive/40/19308_2.png) SabreOverdrive:

> *“Changed **Probe** Icon” Intensifies*

Here’s the irony. We changed most all icons *except* Probe!
