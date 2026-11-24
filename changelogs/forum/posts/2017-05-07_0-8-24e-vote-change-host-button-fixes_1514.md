# 0.8.24e - Vote Change Host Button Fixes

- Date: 2017-05-07 14:21:10 UTC
- Author: í42-Xblade
- Archived copy: https://fol-archive.netlify.app/t/0-8-24e-vote-change-host-button-fixes/1514.html
- Original: https://forum.imperium42.com/t/0-8-24e-vote-change-host-button-fixes/1514
- Replies by other users left out: 1

---

## **0.8.24e Changelog**

**Originally -** Voting to remove a host and give it to someone new originally only toggled between the first and 2nd players. This would mean two trolls or AFKers would forever hold a room “hostage”. I realized I had more fixes than I thought, so wrote up a changelog:

### Changes

1. Host can now only be host of a room **one time**.
2. If a host is voted off, the next host will be by seniority.
3. Voting for a new host will now circulate across the entire room.
4. To prevent breakage and weirdness, if for whatever reason every single person ends up being a host at least once, the list resets and the original host can once again become host :stuck\_out\_tongue:
5. [Potentially] fixed the visual glitch that would always show **0/4 votes**: It should now update properly. I hope. Ping me, if it does not.
