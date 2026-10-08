"""Synthesise the 20s AIA Bot WhatsApp ad score, hit-synced to the edit in index.html.

Pure numpy, deterministic (seeded). 120 BPM grid anchored at the 4.25s drop.
Run:  python3 audio/gen_score.py   ->  assets/score.wav
"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

dry = np.zeros((N, 2))
pad_bus = np.zeros((N, 2))   # sidechained
verb_send = np.zeros((N, 2))


def t_arr(sec):
    return np.arange(int(sec * SR)) / SR


def place(buf, start, sig, gain=1.0, pan=0.0, send=0.0):
    i = int(start * SR)
    if i >= N:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], axis=1)
    n = min(len(sig), N - i)
    buf[i:i + n] += sig[:n] * gain
    if send:
        verb_send[i:i + n] += sig[:n] * gain * send


def env(n, a=0.002, d=0.2, curve=1.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d) ** curve
    return e


def lowpass(x, cutoff):
    # one-pole, cutoff may be array
    c = np.broadcast_to(np.asarray(cutoff, float), x.shape[:1])
    a = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.zeros_like(x)
    acc = np.zeros(x.shape[1:]) if x.ndim > 1 else 0.0
    for i in range(len(x)):
        acc = acc + a[i] * (x[i] - acc)
        y[i] = acc
    return y


def hp(x, cutoff):
    return x - lowpass(x, cutoff)


# ---------- instruments ----------
def kick(punch=1.0, length=0.45):
    t = t_arr(length)
    f = 45 + 140 * np.exp(-t / 0.035) * punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.16)
    s += 0.35 * rng.standard_normal(len(t)) * np.exp(-t / 0.004)
    return np.tanh(s * 1.6)


def sub_boom(length=1.6, f0=42):
    t = t_arr(length)
    f = f0 + 60 * np.exp(-t / 0.08)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (length / 3))
    return np.tanh(1.8 * s)


def noise_burst(length=0.6, decay=0.15, bright=6000):
    n = rng.standard_normal(int(length * SR))
    n = lowpass(n, bright)
    return n * env(len(n), 0.001, decay)


def hat(open_=False):
    length = 0.25 if open_ else 0.05
    n = rng.standard_normal(int(length * SR))
    n = hp(n, 7000)
    return n * env(len(n), 0.0005, 0.08 if open_ else 0.012)


def clap():
    length = 0.35
    n = lowpass(hp(rng.standard_normal(int(length * SR)), 900), 5000)
    t = t_arr(length)
    e = np.zeros_like(t)
    for off in (0, 0.011, 0.022):
        e += (t >= off) * np.exp(-np.maximum(t - off, 0) / 0.01)
    e += (t >= 0.03) * np.exp(-np.maximum(t - 0.03, 0) / 0.09)
    return n * e * 0.6


def thud(f0=95):
    t = t_arr(0.35)
    f = f0 * (0.55 + 0.45 * np.exp(-t / 0.05))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
    s += 0.5 * rng.standard_normal(len(t)) * np.exp(-t / 0.003)
    return np.tanh(2 * s)


def click(freq=2200, length=0.03):
    t = t_arr(length)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.006)


def blip(freq, length=0.09):
    t = t_arr(length)
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
    return s * env(len(t), 0.001, 0.025)


def pluck(freq, length=0.5):
    t = t_arr(length)
    s = sum(np.sin(2 * np.pi * freq * k * t) / k ** 1.3 for k in range(1, 6))
    return s * env(len(t), 0.001, 0.12) * 0.4


def bell(freq, length=2.5):
    t = t_arr(length)
    partials = [(1, 1.0, 1.2), (2.76, 0.5, 0.6), (5.4, 0.25, 0.3), (8.93, 0.12, 0.15)]
    s = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t / d) for r, a, d in partials)
    return s * 0.35


def saw(freq, t):
    ph = (freq * t) % 1.0
    return 2 * ph - 1


def supersaw_chord(freqs, length, cutoff):
    t = t_arr(length)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, -0.05, 0, 0.06, 0.13):
            s += saw(f * 2 ** (det / 12), t + rng.random())
    s /= len(freqs) * 5
    return lowpass(s, cutoff)


def whoosh(length=0.5, up=True, peak=0.7):
    n = rng.standard_normal(int(length * SR))
    t = np.linspace(0, 1, len(n))
    cut = 400 + 7000 * (t if up else 1 - t) ** 2
    shape = np.sin(np.pi * np.clip(t / peak, 0, 1) * 0.5) ** 2 * np.clip((1 - t) / (1 - peak), 0, 1) ** 0.6
    return lowpass(n, cut) * shape


def riser(length):
    t = t_arr(length)
    u = t / length
    n = lowpass(rng.standard_normal(len(t)), 300 + 9000 * u ** 2.2)
    f = 180 * 2 ** (u * 3.2)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4
    return (n * 0.8 + tone) * u ** 2.4


def note(n):  # midi -> hz
    return 440 * 2 ** ((n - 69) / 12)


# ---------- arrangement (20s cut) ----------
def pop_out():  # message sent: quick upward chirp
    t = t_arr(0.09)
    f = 700 + 900 * (t / 0.09)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.03)


def pop_in():  # message received: two soft tones
    a = blip(note(84), 0.12)
    b = blip(note(91), 0.16)
    s = np.zeros(int(0.25 * SR))
    s[:len(a)] += a
    i = int(0.07 * SR)
    s[i:i + len(b)] += b * 0.8
    return s


# HOOK 0 - 2.75: dark, ticking clock, unanswered messages
place(pad_bus, 0.0, supersaw_chord([note(n) for n in (45, 52, 57, 60)], 2.9, 600), 0.45, send=0.3)
place(dry, 0.0, sub_boom(1.6, 36), 0.5)
for k, t0 in enumerate(np.arange(0.0, 2.7, 0.25)):
    place(dry, t0, click(1800 if k % 2 else 2400, 0.02), 0.18)
for t0 in (0.25, 0.6, 0.95):
    place(dry, t0, pop_out(), 0.3, send=0.2)
place(dry, 1.55, pop_in(), 0.25, send=0.3)
place(dry, 1.95, thud(70), 0.8, send=0.4)
place(dry, 1.95, noise_burst(0.3, 0.06, 3000), 0.3)
tt = t_arr(0.35)
place(dry, 2.0, lowpass(saw(98, tt) * env(len(tt), 0.002, 0.15), 1100), 0.35)

# SLAM 2.75 - 4.25
place(dry, 2.6, riser(0.6), 0.6, send=0.3)
place(dry, 2.75, whoosh(0.45, up=True, peak=0.9), 0.45, send=0.3)
for t0, f in ((3.2, 1.2), (3.45, 1.2), (3.7, 1.5)):
    place(dry, t0, kick(f), 0.8)
    place(dry, t0, noise_burst(0.35, 0.06, 5000), 0.3, send=0.4)
place(dry, 3.7, pop_in(), 0.3, send=0.4)
place(dry, 4.0, whoosh(0.3, up=False, peak=0.2), 0.35)

# DROP 4.25 + groove to 13.75
DROP, GEND = 4.25, 13.75
place(dry, DROP, sub_boom(1.8, 36), 0.9)
place(dry, DROP, kick(1.5), 0.85)
place(dry, DROP, noise_burst(1.0, 0.3, 7000), 0.35, send=0.8)
place(dry, DROP, bell(note(81)), 0.3, send=0.6)
prog = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
bass_roots = [45, 41, 36, 43]
for b, t0 in enumerate(np.arange(DROP, GEND, 2.0)):
    ch = prog[b % 4]
    place(pad_bus, t0, supersaw_chord([note(n) for n in ch], 2.05, 2000), 0.45, send=0.35)
    root = note(bass_roots[b % 4])
    for k8 in range(8):
        if t0 + k8 * 0.25 >= GEND:
            break
        tt = t_arr(0.24)
        s = (saw(root, tt) + 0.6 * np.sin(2 * np.pi * root / 2 * tt)) * env(len(tt), 0.003, 0.12)
        place(pad_bus, t0 + k8 * 0.25, lowpass(s, 850), 0.5)
for t0 in np.arange(DROP, GEND, 0.5):
    place(dry, t0, kick(1.0), 0.6)
    place(dry, t0 + 0.25, hat(open_=(int((t0 - DROP) * 2) % 4 == 3)), 0.18, pan=0.25)
for t0 in np.arange(DROP + 0.5, GEND, 1.0):
    place(dry, t0, clap(), 0.32, send=0.25)
for t0 in np.arange(DROP, GEND, 0.125):
    place(dry, t0, hat(), 0.06, pan=-0.3)

# chat events
for t0 in (4.75, 7.05, 9.1, 11.15):
    place(dry, t0, pop_out(), 0.45, send=0.2)
for t0 in (5.65, 7.85, 9.85, 12.35):
    place(dry, t0, pop_in(), 0.42, send=0.35)
for t0 in (5.1, 7.35, 9.4):  # typing ticks
    for k in range(5):
        place(dry, t0 + 0.1 + k * 0.09, click(3000, 0.012), 0.08)
pent = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91]
for i, t0 in enumerate((5.9, 8.1, 10.1)):
    place(dry, t0 - 0.1, whoosh(0.25, up=True, peak=0.8), 0.25)
    place(dry, t0 + 0.05, pluck(note(pent[3 + 2 * i])), 0.35, send=0.4)
# bill scan
n = rng.standard_normal(int(0.7 * SR))
place(dry, 11.55, lowpass(n, 3000) * np.sin(np.linspace(0, np.pi, len(n))) * 0.15, 1.0, send=0.2)
place(dry, 11.75, blip(note(81), 0.08), 0.25)
place(dry, 12.1, blip(note(86), 0.08), 0.25)
place(dry, 12.75, bell(note(88), 1.2), 0.22, send=0.5)
place(dry, 13.3, whoosh(0.45, up=True, peak=0.9), 0.4, send=0.3)

# BENEFITS 13.75 - 17.1
for t0 in (13.8, 14.3):
    place(dry, t0, kick(1.3), 0.75)
    place(dry, t0, sub_boom(0.4, 50), 0.35)
for t0 in (14.1, 14.6):
    place(dry, t0, whoosh(0.15, up=False, peak=0.1), 0.4)
    place(dry, t0, thud(90), 0.45)
place(dry, 14.8, pop_in(), 0.45, send=0.4)
place(dry, 14.8, kick(1.4), 0.7)
place(pad_bus, 14.8, supersaw_chord([note(n) for n in (57, 64, 69, 72)], 1.0, 2400), 0.4, send=0.4)
place(dry, 15.4, whoosh(0.3, up=True, peak=0.9), 0.3)
place(dry, 15.65, kick(1.3), 0.75)
place(dry, 15.95, sub_boom(1.0, 40), 0.7)
place(dry, 15.95, kick(1.5), 0.8)
place(dry, 15.95, bell(note(84), 1.2), 0.25, send=0.6)
for i in range(3):
    place(dry, 16.25 + i * 0.09, pluck(note(pent[4 + i])), 0.35, send=0.4)
place(dry, 16.9, riser(0.25), 0.4)

# END CARD 17.1 - 20
place(dry, 17.15, sub_boom(2.4, 34), 0.85)
place(dry, 17.15, kick(1.4), 0.75)
place(dry, 17.15, noise_burst(1.4, 0.4, 6000), 0.3, send=0.9)
place(pad_bus, 17.15, supersaw_chord([note(n) for n in (57, 64, 69, 72, 76)], 2.85, 1800), 0.55, send=0.5)
place(dry, 17.85, pop_in(), 0.4, send=0.5)
place(dry, 18.5, bell(note(93), 1.5), 0.25, send=0.7)
place(dry, 19.2, blip(note(81), 0.12), 0.12, send=0.5)

# ---------- sidechain + reverb + master ----------
side = np.ones(N)
kick_times = [t for t in np.arange(DROP, GEND, 0.5)] + [13.8, 14.3, 14.8, 15.65, 15.95, 17.15]
tt = np.arange(int(0.35 * SR)) / SR
duck = 1 - 0.75 * np.exp(-tt / 0.09)
for k in kick_times:
    i = int(k * SR)
    n = min(len(duck), N - i)
    side[i:i + n] = np.minimum(side[i:i + n], duck[:n])
mix = dry + pad_bus * side[:, None]

ir_len = int(2.2 * SR)
ir_t = np.arange(ir_len) / SR
ir = rng.standard_normal((ir_len, 2)) * np.exp(-ir_t / 0.55)[:, None]
ir[:, 0] = lowpass(ir[:, 0], 6000)
ir[:, 1] = lowpass(ir[:, 1], 6000)
ir /= np.sqrt((ir ** 2).sum(axis=0))
L = N + ir_len
nfft = 1 << (L - 1).bit_length()
verb = np.stack([np.fft.irfft(np.fft.rfft(verb_send[:, c], nfft) * np.fft.rfft(ir[:, c], nfft), nfft)[:N]
                 for c in range(2)], axis=1)
mix += verb * 0.6

# fade tail
fade = np.ones(N)
fs = int(19.3 * SR)
fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
mix *= fade[:, None]

mix = np.tanh(mix * 1.1)
mix /= np.abs(mix).max() / 0.89

out = Path(__file__).resolve().parent.parent / "assets" / "score.wav"
pcm = (mix * 32767).astype("<i2")
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out)
