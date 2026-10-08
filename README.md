# AI Accountant — 20s launch film

A 20-second, 16:9 (1920×1080, 30fps) product-launch film for **AIAccountant.com**, built with
[HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP → MP4).

- `launch-film/index.html` — the composition (8 scenes on one seekable GSAP timeline)
- `launch-film/audio/gen_score.py` — synthesises the original, hit-synced score (`assets/score.wav`)
- `launch-film/renders/aiaccountant-launch.mp4` — rendered film
- `launch-video/BRIEF.md` — creative brief and beat sheet
- `brand/` — official A-Star logo SVGs

## Edit / re-render

```bash
cd launch-film
python3 audio/gen_score.py            # only if you change the score
npx hyperframes preview               # Studio preview / timeline editing
npx hyperframes render --quality delivery --output renders/aiaccountant-launch.mp4
```

# AIA Bot: 20s WhatsApp video ad (`wa-bot-ad/`)

4:5 (1080×1350, 30fps) WhatsApp-themed ad for Meta and LinkedIn feeds. See `wa-bot-ad/BRIEF.md`.
Render: `wa-bot-ad/renders/aia-bot-whatsapp-ad-4x5.mp4`
