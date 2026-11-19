// gta6-meme-reddit-01 entrypoint (Node 22, standard library only).
//
// The entry is the Reddit post itself: the house reads the post from Reddit
// (its first picture, title and text) and hands that to the judge. This
// program only has to hand the house the post's address, by copying the
// repository's POST.json into the output directory, where the gate reads it.
//
// POST.json holds {"url": "https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/"}.
// Until the meme is actually posted on Reddit it holds the placeholder
// address from the starter; the gate refuses that (valid 0) until the real
// post's address replaces it.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const POST_FILE = "POST.json";

// Read POST.json first so a malformed file fails loudly here, with a
// message that names the file, instead of silently copying a bad entry.
const raw = readFileSync(join(BOT_DIR, POST_FILE), "utf8");
let post: unknown;
try {
  post = JSON.parse(raw);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post !== "object" || post === null || Array.isArray(post)) {
  console.error("POST.json must be a JSON object with a url field.");
  process.exit(1);
}

const url = (post as { url?: unknown }).url;
if (typeof url !== "string" || url.length === 0) {
  console.error("POST.json must be a JSON object with a non-empty url string.");
  process.exit(1);
}

// The starter's placeholder is not a post: warn loudly instead of letting
// a placeholder slip into a submission unnoticed. Copying still proceeds —
// the gate, not this program, is what refuses a placeholder.
if (url.includes("<subreddit>") || url.includes("<id>")) {
  console.warn(
    "WARNING: POST.json still holds the placeholder address; " +
      "replace it with the real Reddit post address before submitting.",
  );
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, POST_FILE), join(OUTPUT_DIR, POST_FILE));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

console.log(`POST.json copied to ${OUTPUT_DIR} (url: ${url})`);
