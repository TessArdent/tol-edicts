# Mini Patch v3.0.2: 3rd Anniversary Event + Draggables

- Date: 2020-09-30 15:52:51 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/mini-patch-v3-0-2-3rd-anniversary-event-draggables/84133.html
- Original: https://forum.imperium42.com/t/mini-patch-v3-0-2-3rd-anniversary-event-draggables/84133
- Replies by other users left out: 0

---

[![AVATAR_KINGSLAYER_2020-512](https://fol-archive.netlify.app/uploads/default/optimized/3X/d/c/dccad214405692ce40e07965c1ab6364631d2280_2_375x375.png)](https://fol-archive.netlify.app/uploads/default/original/3X/d/c/dccad214405692ce40e07965c1ab6364631d2280.png "AVATAR_KINGSLAYER_2020-512")

## Event: 3rd Anniversary

- To celebrate our 3rd anniversary, @ those that login within the next 2~3 weeks, you will be rewarded with an exclusive, progressive title and avatar similar to the previous anniversary rewards.
- [![image](https://fol-archive.netlify.app/uploads/default/original/3X/e/8/e84a8653730cda9b7368d3ab257e1779decd011a.jpeg)](https://fol-archive.netlify.app/uploads/default/original/3X/e/8/e84a8653730cda9b7368d3ab257e1779decd011a.jpeg "image")
- To those that hang out within our Discord ( <https://discord.gg/tol> ) shortly after this patch launches, you will receive an exclusive/colored `Kingslayer III` role that will never be handed out again. We will do a small purge before we hand out this role, so be sure you’ve participated at least once within the past month!
- Ends Oct 31

## Event: Moon Festival

![moonFestivalBanner](https://fol-archive.netlify.app/uploads/default/original/3X/8/b/8b268ccd3aea19d85e342d37828ee2931d5a5357.jpeg)

- Ends Oct 31

## New/Impr

- ~~You now have the ability to **disable** chat clicky links in options. Although it says glossary links, this also applies to class card links in chat.~~ (Requires further testing for a future update)
- When you click your class portrait at the top-left, it will now always open *your class* card. Pressing TAB will continue “resuming” whatever the previous class card was.
- Tutorial now mentions the **glossary** for acronyms.
- Added a new “draggable” cursor (the compass-like one) for things draggable.
- Added new draggable goodies (that, like chat, reset each game):
  - Whisper panel
  - Pardon/Execute panel
  - “Step Forward” button (the outside area)
- Allowed the chat to resize larger and wider (ability buttons on top).
- Chat resizer is now less “wonky” (for lack of a better word) after exceeding max thresholds.
- Draggables demo:
  ![image](https://fol-archive.netlify.app/uploads/default/original/3X/a/e/ae66169a784014d0eb1ab410297271a4f578d46d.png)
  ![image](https://fol-archive.netlify.app/uploads/default/original/3X/2/9/2946b46ef90c26e82137c583e4e4a2b36c80ac50.jpeg)

## Fixes

- Sorc’s day abils should be more consistent.
- You can no longer see friends online that are in different regions to prevent confusion when joining/inviting would fail.
- You can no longer receive queued invites from those in another region (it would fail, anyway, if accepted - this is just less confusing).
- Fixed garbled class card description when you clicked a link before your normally entering class cards.
- Emotes buttons fixed.
- Suicide *“are you sure?”* panel will no longer show preemptively.
- Fix a style typo for “Poison ended your life” feedback to King.
- More of a workaround than a fix: *Spectator Mode* has been temporarily disabled while we fix the bugs that are preventing matches from starting.
- Fixed Snare Trap abil that was literally showing %TARGET% instead of target name.
- Fixed bad translation key for MVP panel for starting King (eg, “B\_D\_KING–SOMETHING”).
- You may now click-thru the winner banner when the game is ending
- Potentially fixed early-game “fake disconnects” that now check for a heartbeat at NIGHT 1 instead of day 1 (perhaps some folks loaded in slow).
- Potentially fixed disconnected players’ death that would sometimes occur the *following* night (bug) instead of the immediate night (intended).
- MVP no longer awards bonus gp in private matches (sorry folks, ancient bug).
- Name selection, when changing names, will now correctly show the old<>new names.
- Merc’s extra brilders will now offer the bonus gp promised.
- Fixed tutorial journal button that should now properly open the journal, once it’s enabled (outside the normal force click).

## Chinese Only

僅中文 (Click to Expand)

## 僅中文

1. 因應中文玩家反映，白天時間由90秒延長至110秒。（由於中文輸入較英文耗時，因此調整以便配合英語地區的節奏）
2. 移除中文職業名稱旁的英文名稱。（主要方便作者在中文版本測試間，能更快解決bug而設）
3. 修正MVP及玩家介面的中文化bug。
4. 修正結算版面 開始及終結 時的職業中文名稱。
5. 修正由中文玩家 #feedback所報告的漢化問題。（感謝中文玩家的報告！請繼續協助我們找出更多漢化出現的問題）
6. 修正玩家介面中，首王的顯示錯誤 （例如：“B\_D\_KING–SOMETHING”）
7. 我們在2019年時發現並向開發團隊報告了一項，當輸入中文並轉換成英文時所造成的[IME bug](https://forum.unity.com/threads/tmp-breaking-chinese-bugs-for-traditional-zhuyin-bopomofo-taiwan-locale.717308/#post-6343383)，開發團隊將會在未來數天內完成修正，並盡快提出修正。

謝謝 `@bAo` 的翻譯！

## Chinese Only (English)

- **Day timer increased from 90s >> 110s** by popular demand (takes longer to type Chinese than English, so this should better match the English region’s pace).
- English class names next to the Chinese ones have been removed (mostly used during Chinese alpha to resolve bugs faster as an English speaker).
- MVP and player panel localization bugs fixed.
- End screen start/final classes list is now localized.
- Misc English localizations now in Chinese that were reported to [#feedback:](https://fol-archive.netlify.app/c/feedback/12) Thanks! Please report more unexpected English, as seen.
- Fixed bad translation key for player panel for starting King (eg, “B\_D\_KING–SOMETHING”).
- We are aware of the IME bug that messes up typing Chinese and swaps to English: [This is a **unity** bug](https://forum.unity.com/threads/tmp-breaking-chinese-bugs-for-traditional-zhuyin-bopomofo-taiwan-locale.717308/#post-6343383) for a bug report we submitted in 2019. The dev claims they will have a patch ready “within the next few days”. As soon as it’s available (see above link for updates), we’ll patch it in.

---

## Recent Discord Poll Result

[![image](https://fol-archive.netlify.app/uploads/default/original/3X/6/d/6d542aee1fa0ec209e7e42331502148ab1ed2f29.png)](https://fol-archive.netlify.app/uploads/default/original/3X/6/d/6d542aee1fa0ec209e7e42331502148ab1ed2f29.png "image")

---

## Related

- [Mini Patch v3.0.1: Clicky Links](https://fol-archive.netlify.app/t/mini-patch-v3-0-1-clicky-links/83893)
- [Patch v3.0.0: Major Balance / 中文 Chinese Localization](https://fol-archive.netlify.app/t/patch-v3-0-0-major-balance-chinese-localization/83299)

---

### Follow-up #2 by í42-Xblade (2020-10-05)

Live!
