# Patch v5.0.0: Gfx Revamp (pt1) + Bye Faction Rotations

- Date: 2021-08-24 09:47:15 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953.html
- Original: https://forum.imperium42.com/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953
- Replies by other users left out: 4

---

## Major Gfx Revamp (Part 1)

**Early Access:** This is essentially a live beta test of our graphics revamp (part 1), that we’re happy to share!

Mystic New (GIF):

[![](https://cdn.discordapp.com/attachments/580380189079502868/879307181999128626/mystic-anim.gif)](https://cdn.discordapp.com/attachments/580380189079502868/879307181999128626/mystic-anim.gif)

Mystic Old:

[![](https://cdn.discordapp.com/attachments/580380189079502868/879307206149943316/unknown.png)](https://cdn.discordapp.com/attachments/580380189079502868/879307206149943316/unknown.png)

King New:

[![](https://cdn.discordapp.com/attachments/580380189079502868/879621181559414784/unknown.png)](https://cdn.discordapp.com/attachments/580380189079502868/879621181559414784/unknown.png)

King Old:

[![](https://cdn.discordapp.com/attachments/580380189079502868/879621198592479252/unknown.png)](https://cdn.discordapp.com/attachments/580380189079502868/879621198592479252/unknown.png)

**Part 1, Live Now:**

- Ground-up lighting/shading/particle revamps for every day/night/death room.
- Added shadows, god rays and environmental dust.
- Darker environment, but brighter focus points with better color differences.
- Added some environmental texture upgrades.
- HDR support.
- Optimization - Should still have decent FPS!
- **@ Veterans:** If you have the tag with the crystal *flair*, you got a visual upgrade:
  <https://cdn.discordapp.com/attachments/580380189079502868/879316269315276810/ezgif.com-gif-maker_1.gif>

- Known bugs to be hotfixed:
  - Some areas have Bloom intensity too high, like Sellsword/Merc room.
  - Some areas are too dark (or the character is too dark).
  - Part 1 has “dev tweaks”. Part 2 will have “*actual artist*” tweaks.

**Part 2+, Roadmap:**

1. Lighting is actually *too* dark right now: We will tweak this.
2. Camera angle improvements.
3. More textures (armor + weapons).
4. Reflective surfaces (armor/weapons/windows).
5. Additional prop varieties (like furniture).
6. Potential fixes for previously-disabled weapons+executions.
7. Better idle/sitting animations.
8. Significant optimization boost (baked lights).

---

## Faction Rotations GONE!

We’re back to *classic mode*, for now! :tada:

[![](https://cdn.discordapp.com/attachments/643778163402342420/879662484091441162/classicmodereturns.gif)](https://cdn.discordapp.com/attachments/643778163402342420/879662484091441162/classicmodereturns.gif)

In the future, we’ll likely add optional rotation modes to *100% private* games, \*\*if you really feel like an Unseen or Cult game, specifically.

---

## Major Fixes

1. Fixed crash when typing `<` or `>` in chat.
2. Fixed some `<styles>` being revealed during select class card hovers.
3. Fixed buggy text selection (when trying to copy text from chat) - it should now work similarly to a text editor, where you can drag to select / double click to highlight the word / triple click to highlight the entire sentence.
4. Potentially fixed quest progression bug for executing players.

\**These are early access fixes, at least working in Unity — let us know if it worked for you!*

## Minor Improvements

1. Fixed some class card consistency issues, like with Marshal/Seeker’s *Expose*.
2. Seems like *Voidstone of Corax* execution was missing an entire particle layer - fixed.
3. Fixed stacking text: The moment the player dies in an execution, we’ll hide the name above their head (so both players’ names don’t jarble together).
4. Death reveals no longer **bold** the name of Neutral classes.
5. Tutorial night ability description has returned.
6. Made the names above your head prettier.

---

## Hotfixes

This had some MAJOR changes, both front and backend – here come the hotfixes (thanks for the awesome bug reports :clap: )!

## Hotfix v5.0.0a

[Patch Notes](https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953/5)

## Hotfix v5.0.0b

[Patch Notes](https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953/5)

## Hotfix v5.0.1

[Patch Notes](https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953/7)

## v5.0.1a

[Patch Notes](https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953/5)

## v5.0.1b

[Patch Notes](https://fol-archive.netlify.app/t/patch-v5-0-0-gfx-revamp-pt1-bye-faction-rotations/88953/11)

---

—Xblade @ <https://discord.gg/tol>

---

### Follow-up #2 by í42-Xblade (2021-08-24)

By popular request, here is the Merc/Sellsword room:

[![image](https://fol-archive.netlify.app/uploads/default/optimized/3X/7/9/7994c0e8dbcd537760fb24adfaef82826dbd1a2f_2_690x384.jpeg)](https://fol-archive.netlify.app/uploads/default/original/3X/7/9/7994c0e8dbcd537760fb24adfaef82826dbd1a2f.jpeg "image")

(^ However, this has the “bloom fix” that will arrive next hotfix. The current one is over-bloomed)

Old:

[![image](https://fol-archive.netlify.app/uploads/default/optimized/3X/f/e/fe8d968335ac8cc1b4ee96eb55c20389510ac13b_2_690x388.jpeg)](https://fol-archive.netlify.app/uploads/default/original/3X/f/e/fe8d968335ac8cc1b4ee96eb55c20389510ac13b.jpeg "image")

---

### Follow-up #3 by í42-Xblade (2021-08-24)

**Bug** : Tutorial may not progress past N1. We’ll hotfix this soon. Keep the feedback coming for non-tutorial games

[![image](https://fol-archive.netlify.app/uploads/default/optimized/3X/b/7/b7dd970077b50daaae048e4abffbf5e1bcf365e7_2_620x500.jpeg)](https://fol-archive.netlify.app/uploads/default/original/3X/b/7/b7dd970077b50daaae048e4abffbf5e1bcf365e7.jpeg "image")

There will be more bugs, for sure – please report them to Discord.

---

### Follow-up #5 by í42-Xblade (2021-08-26)

## Hotfix v5.0.0a

Thanks for testing our early access patch and reporting all the bugs! As promised, here’s a quick hotfix.

## Gameplay Fixes

- Fixed breaking issues when transitioning rooms.
- Fixed tutorial breaking timer freeze and missing Unseen room.
- Fixed FPS issues in graveyard, scorned room, a couple dead rooms and several others caused by inefficient fog and terrain.

## Visual Improvements

- Text is crisper with more clarity.
- Fixed several rooms having “overbloom” and misplaced dust particles.
- Swapped out *most* old pixelated torch particles with the new style (more later).
- Fixed bright graveyard (among other similar issues).
- Fixed one of the dead room’s awkward camera positions.
- Improved Sorc room’s lighting.
- Made Sheriff’s room less “orange”.
- Fixed some random ultra-glowing of select parchments (which gave the Unseen table “knife in parchment” a really cool shadowed-knife-glowing-hilt effect).
- Hunter and Merc/Sellsword walls got a mini texture upgrade (placeholder).

## Other Improvements

- Fixed new player lobby “Welcome Screen” text placement.
- Renamed lobby “Knowledgebase” tab to “Learn”
- Hovering over a lobby friend button has less text overlap and more clarity.
- Left lobby “Patch Notes banner” with link has returned.

---

## Hotfix v5.0.0b

- Fixed many things :wink:

---

## Hotfix v5.0.1

We’re out of early access! Things are looking stable.

## Major Bug Fixes

- Fixed a major desync bug that was also affecting text in strange ways.
- Sorcerer room fixed.
- “Send Selection” logbook bug fixes:
  - “Send Selection” is once again fixed to sending across multiple lines.
  - `CTRL+A` now sets “Send Selection” text.
  - Fixed “Send Selection” not setting when you partially highlight text.
- Chat input text is more-legible and consistent with game chat.
- Quest Bug Fixes:
  - “Execute a Player” type quests may now progress.
  - “Execute a Player” tier 2 now requires 2 executions instead of 1 (no longer the same goal as tier 1).
- Fixed some armor desyncs.
- The floor is no longer swallowing players.

## Minor Fixes

- Fixed some light gaps in day scene walls/floors.
- Fixed tutorial/dev/backer sword missing textures.
- Fixed Abaddon Axe missing textures during execution.
- Fixed missing trident weapon textures.
- Fixed some minor issues with name selection chat button.
- Additional optimization between game over and end screen.
- Assassin class card tips now have clickable class links.
- Less-awkward top-right lobby spacing between “Learn” and “Code of Conduct”.
- Fixed some unsync’d Welcome Screen panels/buttons.
- Made Sellsword/Hunter room less “red”.
- Swapped out some more old torches with new style.

—Xblade @ <https://discord.gg/tol>

---

### Follow-up #7 by í42-Xblade (2021-09-01)

Added to OP:

## Hotfix v5.0.1

We’re out of early access! Things are looking stable.

## Major Bug Fixes

- Fixed a major desync bug.
- Sorcerer room fixed.
- “Send Selection” logbook bug fixes:
  - “Send Selection” is once again fixed to sending across multiple lines.
  - `CTRL+A` now sets “Send Selection” text.
  - Fixed “Send Selection” not setting when you partially highlight text.
- Chat input text is more-legible and consistent with game chat.
- Quest Bug Fixes:
  - “Execute a Player” type quests may now progress.
  - “Execute a Player” tier 2 now requires 2 executions instead of 1 (no longer the same goal as tier 1).
- Fixed some armor desyncs.
- The floor is no longer swallowing players.

## Minor Fixes

- Fixed some light gaps in day scene walls/floors.
- Fixed tutorial/dev/backer sword missing textures.
- Fixed Abaddon Axe missing textures during execution.
- Fixed missing trident weapon textures.
- Fixed some minor issues with name selection chat button.
- Additional optimization between game over and end screen.
- Assassin class card tips now have clickable class links.
- Less-awkward top-right lobby spacing between “Learn” and “Code of Conduct”.
- Fixed some unsync’d Welcome Screen panels/buttons.
- Made Sellsword/Hunter room less “red”.
- Swapped out some more old torches with new style.

—Xblade @ <https://discord.gg/tol>

---

### Follow-up #10 by í42-Xblade (2021-09-05)

![](https://fol-archive.netlify.app/user_avatar/forum.throneoflies.com/planterror/40/9678_2.png) Planterror:

> how did it take 5 months to finally revert a change nobody liked

This particular decision was out of my control, unfortunately~ Perhaps it would’ve been decent if we had more new players for this to benefit; or swapped [bi]hourly (so new players could prep for the encounter, where hourly doesn’t make things stale).

---

### Follow-up #11 by í42-Xblade (2021-09-07)

Added to OP:

## v5.0.1a

- Fixed Prince + King bugs
- Fixed room bugs
- Fixed several FPS issues
- Small anti-spam upgrades in pre-game chat

## v5.0.1b

- Elected King room fixes
- *Present Drop* exec fixes
- Significantly-slower Chrono room for the movement-sickness players.
