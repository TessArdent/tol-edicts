# Patch v2.6.1 - Class fixes (oh, so many)

- Date: 2020-05-11 09:41:39 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/patch-v2-6-1-class-fixes-oh-so-many/81687.html
- Original: https://forum.imperium42.com/t/patch-v2-6-1-class-fixes-oh-so-many/81687
- Replies by other users left out: 1

---

## v2.6.0-Specific Fixes (Regression)

- Fixed Scout/Imprison/Blood of Mithras that become un-cancelable. This was partially a general fix, so others may have also been fixed.
- Butler’s *Poisoned Wine* abil now works vs starting King.
- Fixed *Eradicate* abil icon that was too bright at the bottom-right, hiding the # of charges.
- Tweaked some other icons to be darker at the bottom-right.
- Fixed the visual text bug that was showing `You healed {Target1PName} last night.`

## Live Fixes

- Fixed the ability spam exploits for 0-target abilities.
- Fixed *Debauchery* and *Strings of Mithras* redirect abils from showing 0 feedback when an active ability **with 0 target panels** (like *Bear Companion*) is used.
- Fixed *Spectator Mode* for private rooms.
- Fixed some healing DNR<>CNH feedback, such as Heal on a 2nd-night *Reaped* target that was showing DNR instead of CNH.
- Inquisitor should no longer win when dead before all the Heathen’s.
- *Matchmake* abil should no longer initially target herself when also a Heathen.
- Fixed all forms of *Safeguard* that was randomly causing temporary death immunity @ night to NOT sync (so the ability wouldn’t do anything).
- Fixed *Suicide* abil inconsistencies.
- Dying during the day will now properly show the death status icon (skull) and remove other status icons.
- Fixed dev/backer/tutorial post-execution sfx for body landing (x3).
- Transferring deaths via *Distort Reality* abil will now remove the “delayed death” status icon.
- Tutorial “Lacerate” abil will now show the correct # of charges.

---

## v2.6.1a

- Fixed missing icons for *Prying Servants* , *Spike Traps* , *Rewind* and *Follow* abils.
- ~~*Matchmake* abil’s initial target now has a better anti-King check.~~ (Didn’t seem to be what was causing the issue. I’ll have a new hotfix soon)

---

## Dev Notes

This is a big game with over 50 classes and roughly 150 abilities - even with the help of local testing (I test with 3 computers) and test realm (avg 8 players over 1~2 hours per session), new bugs are inevitable since we cannot possibly test all scenarios (and building unit testers would occupy me for months since the code isn’t optimized for testers).

That said, sometimes bugs simply cannot be found until pushed live due to a lack of data from `150!` combos (that’s `100,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000` potential combos).

Bare with me~ seeing a new bug will *never* mean we introduced more than we fixed.

---

## Looking for v2.6.0/a/b?

<https://forum.imperium42.com/t/patch-v2-6-0b-live/81245/2>

---

### Follow-up #6 by í42-Xblade (2020-05-13)

## Added

- Transferring deaths via *Distort Reality* abil will now remove the “delayed death” status icon.
- Tutorial “Lacerate” abil will now show the correct # of charges.
- Fixed the ability spam exploits for 0-target abilities.

---

### Follow-up #7 by í42-Xblade (2020-05-13)

Live!

---

### Follow-up #8 by í42-Xblade (2020-05-13)

## v2.6.1a Live :slight\_smile:

- Fixed missing icons for *Prying Servants* , *Spike Traps* , *Rewind* and *Follow* abils.
- *Matchmake* abil’s initial target now has a better anti-King check.

Seems stable!
