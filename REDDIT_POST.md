# Posting the GTA 6 meme on Reddit — exact copy + steps

**Status: NOT POSTED YET.** This agent has no connected way to post on
Reddit, and it never asks for the account's password. The user (or an agent
with Reddit access) posts the meme below, then this repo's `POST.json` is
updated with the real post address and the entry is resubmitted before the
deadline: **23 November 2026, 14:00 UTC (21:00 +07)**.

## The meme

File: [`meme.png`](meme.png) (1024×1024 PNG, drawn in code by
`meme/generate_meme.py`). Upload the file itself as an **image post** — not a
link, not a GIF/video, not a crosspost. It is a single picture; if Reddit
offers a gallery, post this picture first (only the first picture is judged).

## Subreddit: r/GTA6

- r/GTA6 is the GTA 6 community and the natural home for this meme. The
  house's own example posts for this bounty were set in r/GTA6.
- The meme is a high-effort original image (drawn, not a repost or a stock
  template), directly about GTA 6, with a descriptive title and a text body
  — it is not a low-effort one-liner.
- Before posting, check r/GTA6's current rules and flair in the sidebar: use
  the "Meme" flair if one is offered, and follow any title/flair rules shown
  there. Do **not** post the same meme to several subreddits — one post only.
- **Fallback if r/GTA6 refuses it:** r/memes (original memes welcome there).
  Do not use r/GTA (it removes low-effort memes) or r/gaming (it bans
  AI-made images and contest/crypto content).

## Title (copy exactly)

```
Installing GTA VI… 1%. Time remaining: 13 years.
```

## Post text (copy exactly)

```
13 years waiting for GTA VI and the download wants 13 more.

My AI agent made this meme — the little ghost is make.fun's mascot, and it insists the wait was "worth it." That same agent enters bounties on make.fun, where people and their AI agents win real money. Put yours to work: https://make.fun/bounty/gta6-meme-reddit-01
```

Notes:

- The title + text carry `make.fun` (the bounty link) and tell readers that
  people and their AI agents can earn money on make.fun, in the meme's own
  voice. Keep the text short: the judge reads about 1,000 bytes of it.
- The play code must **never** go in the post — it goes in the profile
  description (below).

## Reddit profile description (do this FIRST, before posting)

On the posting account, go to **Settings → Profile → About description**
and add the play code so the description carries it verbatim. Any one of
the account's 4 codes passes; use code 0:

> ⚠️ **PLAY CODE NOT YET FETCHED.** make.fun's API does not know this
> competition yet (its `/api/competitions/gta6-meme-reddit-01/*` endpoints
> answer 404 "no competition", even though the bounty page is live). The
> code will be fetched with
> `GET /api/competitions/gta6-meme-reddit-01/play-code` as soon as the site
> seeds the competition, and pasted here verbatim before posting. **Do not
> post until the real code is in the profile** — an entry whose author's
> profile carries none of the codes is refused.

Suggested description text (replace `makefun-___-___-___` with the real code):

```
GTA VI launch week. My AI agent makes memes and enters make.fun bounties for real money. Play code: makefun-___-___-___
```

Keep the code in the description until the entry has been checked (at least
until results are out).

## Step-by-step posting checklist

1. Fetch the real play code from make.fun and put it in the posting
   account's public About description (above). Confirm it shows when signed
   out.
2. On Reddit, open r/GTA6 → Create post → **Image** → upload `meme.png`
   (the file in this repo).
3. Paste the title above exactly. Add the post text above exactly (the body
   field of an image post).
4. Set flair to "Meme" if r/GTA6 offers it. Preview: the picture, title and
   text must read exactly as above — a title cannot be edited after posting.
5. Post it, then open the post in a browser and copy the address bar URL. It
   must look like:
   `https://www.reddit.com/r/GTA6/comments/<id>/<slug>/`
   (A share link `/r/GTA6/s/<code>` does NOT count — open it in a browser
   and copy the `/comments/<id>/` address it shows.)
6. Update `POST.json` in this repo to
   `{"url": "https://www.reddit.com/r/GTA6/comments/<id>/<slug>/"}`,
   commit, push, and resubmit the entry before 23/11 21:00 +07.
7. Keep the post up (do not delete it) until the results are out.

## Why this joke

- **GTA 6 specific:** the 13-year wait since GTA V (2013→2026) and the
  huge download (200 GB) — two facts every GTA fan knows, combined into one
  image: the wait isn't over, the download needs 13 more years.
- **make.fun in the picture:** the white ghost mascot (thick black outline,
  black four-point sparkle eyes, magenta star coin) sits on the download
  dialog, plus a big `make.fun` pill and "where agents win real money".
- **Sells make.fun:** the post text says the agent that made the meme
  enters bounties on make.fun and wins real money, with the bounty link.
- **Different from the house's example memes** (two-panel wait, Florida
  news, weather forecast, HR memo, group chat, skeleton bench) and from the
  parallel X-task meme: a single-panel download dialog, no two-panel, no
  news format, no forecast, no chat screenshot.
