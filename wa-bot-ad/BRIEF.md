# AIA Bot: 20s WhatsApp video ad

4:5 vertical, 1080×1350, 30fps, 20.0s. Built for Meta feed (FB/IG) and LinkedIn feed video ads, where 4:5
takes the most screen space in feed. Designed to read with sound off (Meta and LinkedIn autoplay muted);
the score adds WhatsApp-style send/receive pops when unmuted.

Audience: founders, owners and MDs of Tally-using SMBs who wait on their CA or accountant for numbers.

| Time | Beat | On screen |
|---|---|---|
| 0.0–3.25 | HOOK (founder character) | Meme caption "POV: You asked your CA for one number." An original cartoon founder ("Seth ji": bald, big moustache, round glasses, Nehru jacket) taps his fingers on the desk while the clock spins and the calendar flips MON → THU ("3 days later"). His messages "Sales kitni hui?", "Cash kitna hai?", "Hello??" go unanswered, the CA replies "Will share after month-end closing." He turns red, steam from his ears, anger mark, comic burst "MONTH-END?!" (pressure-cooker whistle on the score). |
| 3.25–4.75 | FLIP | White wipe out of his phone. "Now just ask your Tally." + green chat bubble "On WhatsApp." |
| 4.75–11.4 | BOT CHAT (light mode) | "Cash. Dues. Sales." lights up word by word as the bot answers: "kitna cash hai?", "Who hasn't paid me yet?", "Aaj ki sales?" (Hinglish reply). Chips: ~10 sec reply, English · Hindi · Hinglish, 24x7 |
| 11.4–14.25 | BILL UPLOAD | "Forward the bill. We'll do the entry." Crumpled bill photo scanned, fields boxed, "Sent to Needs Review" |
| 14.25–17.6 | BENEFITS | ~~Tally login.~~ ~~Month-end wait.~~ Just WhatsApp. + the same founder, now smiling → "Ask as many times as you like. Questions? Free forever." + Unlimited asks, Up to 10 companies, Your whole team |
| 17.6–20.0 | END CARD | A-Star, "Chat with your accounting data. Right inside WhatsApp.", CTA "Say "Hi" to get started", "Free forever for the first 100 users", +91 63665 75567 |

Notes
- Bill upload is never called free; only questions are ("Questions? Free forever").
- Answers are labelled "As per last Tally sync" (no real-time claim).
- All figures and party names are illustrative.
- WhatsApp colours are used only for the chat UI and the CTA; brand indigo #314DD0 marks the AI moments.
- No WhatsApp logo is used.
- The founder is an original character, deliberately not a lookalike of any actor or film character (no implied celebrity endorsement).

Re-render: `cd wa-bot-ad && python3 audio/gen_score.py && npx hyperframes@0.8.140 render --quality high --video-bitrate 10M -o renders/aia-bot-whatsapp-ad-4x5.mp4`
