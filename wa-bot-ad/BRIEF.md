# AIA Bot: 20s WhatsApp video ad

4:5 vertical, 1080×1350, 30fps, 20.0s. Built for Meta feed (FB/IG) and LinkedIn feed video ads, where 4:5
takes the most screen space in feed. Designed to read with sound off (Meta and LinkedIn autoplay muted);
the score adds WhatsApp-style send/receive pops when unmuted.

Audience: founders, owners and MDs of Tally-using SMBs who wait on their CA or accountant for numbers.

| Time | Beat | On screen |
|---|---|---|
| 0.0–3.25 | HOOK (real founder photo) | Full-bleed photo: a frustrated, hopeless Indian founder staring dead into camera, slow push-in. Top right, WhatsApp notifications from "CA Sharma ji" stack up with escalating excuses: Mon "Sir, shaam tak bhej dunga 🙏", Wed "Sir, thoda busy hoon. Kal pakka.", Sat "Sir, month-end ke baad pakka 🙏". Reels-style caption: "Day 9 of waiting for ONE number from my CA." At 2.6s: punch-in, desaturate, record scratch, a beat of dead air, hard cut. |
| 3.25–4.75 | FLIP | Hard cut to white. "Now just ask your Tally." + green chat bubble "On WhatsApp." |
| 3.25–4.75 | FLIP | White wipe out of his phone. "Now just ask your Tally." + green chat bubble "On WhatsApp." |
| 4.75–11.4 | BOT CHAT (light mode) | "Cash. Dues. Sales." lights up word by word as the bot answers: "kitna cash hai?", "Who hasn't paid me yet?", "Aaj ki sales?" (Hinglish reply). Chips: ~10 sec reply, English · Hindi · Hinglish, 24x7 |
| 11.4–14.25 | BILL UPLOAD | "Forward the bill. We'll do the entry." Crumpled bill photo scanned, fields boxed, "Sent to Needs Review" |
| 14.25–17.6 | BENEFITS | ~~Tally login.~~ ~~Month-end wait.~~ Just WhatsApp. + the same founder, now relieved (photo card "Ab koi wait nahi.") → "Ask as many times as you like. Questions? Free forever." + Unlimited asks, Up to 10 companies, Your whole team |
| 17.6–20.0 | END CARD | A-Star, "Chat with your accounting data. Right inside WhatsApp.", CTA "Say "Hi" to get started", "Free forever for the first 100 users", +91 63665 75567 |

Notes
- Bill upload is never called free; only questions are ("Questions? Free forever").
- Answers are labelled "As per last Tally sync" (no real-time claim).
- All figures and party names are illustrative.
- WhatsApp colours are used only for the chat UI and the CTA; brand indigo #314DD0 marks the AI moments.
- No WhatsApp logo is used.


Re-render: `cd wa-bot-ad && python3 audio/gen_score.py && npx hyperframes@0.8.140 render --quality high --video-bitrate 10M -o renders/aia-bot-whatsapp-ad-4x5.mp4`

## Founder photos (drop-in)

The hook needs two photos. Replace the placeholders and re-render; nothing else changes.

| File | Size | What |
|---|---|---|
| `assets/founder.jpg` | 2160×2700 (4:5), min 1080×1350 | Frustrated founder, subject centre-left, top-right third left empty for the notifications, lower 20% calm for captions |
| `assets/founder-happy.jpg` | 1200×1200 (1:1) | Same man, same outfit and office, relieved and smiling |

Usage rights: use an AI-generated person, a licensed stock photo with a model release (Shutterstock, Getty, Adobe Stock) or your own shoot.
Do not use a lookalike of an actor or film character.

### Image prompt: frustrated (`founder.jpg`)
Photorealistic vertical portrait, 4:5. A 50-year-old Indian businessman, heavy-set with a round belly, balding with
grey hair on the sides, thick black-and-grey moustache, round metal-frame glasses, maroon Nehru jacket over a cream kurta.
He stands in his cluttered small-business office in India (steel almirah, stacks of files, wall calendar, tubelight,
a Tally screen on an old monitor, blurred). He stares directly into the camera, completely deadpan, exhausted and
hopeless, slight frown, eyebrows pinched, arms crossed, a smartphone in one hand. Chest-up framing, subject centre-left
in the lower two-thirds; the top-right third of the frame is soft out-of-focus background with no detail. 50mm lens,
f/1.8, shallow depth of field, warm tungsten practical light, subtle film grain, natural skin texture and pores,
documentary realism, Indian ad film look. No text, no logos, no watermark.

### Image prompt: relieved (`founder-happy.jpg`)
Same man, same outfit and same office as the reference image, square 1:1. He is looking at his smartphone and breaking
into a big, relieved, genuine smile, shoulders relaxed, a glass of cutting chai in the other hand. Same lens, light and
grade. No text, no logos, no watermark.
