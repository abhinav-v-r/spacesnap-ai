"""SpaceSnap AI - detect features in a NASA/Earth image and explain them.
Usage: pip install pillow numpy ; python spacesnap.py image.jpg
Pipeline: Image -> Feature Detection (HSV classifier) -> Explanation."""
import sys, colorsys
import numpy as np
from PIL import Image, ImageDraw

FEATURES = {  # name: overlay colour
    "clouds": (255, 255, 255), "ice/snow": (155, 231, 255), "ocean": (30, 91, 255),
    "forest": (24, 192, 74), "land/desert": (224, 165, 58), "fires": (255, 45, 45),
    "urban lights": (255, 233, 77), "craters/rock": (179, 108, 255)}

def classify(rgb, dark):
    r, g, b = rgb / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if r > .78 and .2 < g < .69 and b < .35 and s > .6: return "fires"
    if dark and v > .55: return "urban lights"
    if v > .78 and s < .2: return "ice/snow" if b - r > .05 else "clouds"
    if 185 <= h <= 265 and s > .25: return "ocean"
    if 70 <= h < 185 and s > .2: return "forest"
    if 15 <= h < 70 and s > .2: return "land/desert"
    if s < .18 and .15 < v <= .78: return "craters/rock"
    return None

def analyze(path, out="result.png"):
    img = Image.open(path).convert("RGB"); img.thumbnail((300, 300))
    a = np.array(img); dark = a.mean() / 255 < .25
    h, w, _ = a.shape; labels = {}; over = a.copy().astype(float)
    for y in range(h):
        for x in range(w):
            k = classify(a[y, x], dark)
            if k:
                labels.setdefault(k, []).append((x, y))
                over[y, x] = (over[y, x] + FEATURES[k]) / 2
    res = Image.fromarray(over.astype("uint8")); d = ImageDraw.Draw(res)
    found = sorted(((k, len(v) / (h * w), v) for k, v in labels.items() if len(v) / (h * w) >= .03),
                   key=lambda t: -t[1])
    for k, _, pts in found:
        xs, ys = zip(*pts); d.text((sum(xs) / len(xs), sum(ys) / len(ys)), k, fill="white")
    res.save(out)
    names = [k for k, _, _ in found]
    text = f"Detected: {', '.join(names)}.\n"
    if "clouds" in names and "ocean" in names: text += "Explanation: A cloud system over the ocean."
    elif "urban lights" in names: text += "Explanation: City lights on the night side of Earth."
    elif "craters/rock" in names: text += "Explanation: A rocky, cratered surface."
    elif names: text += f"Explanation: Mostly {names[0]}."
    return text

if __name__ == "__main__":
    print(analyze(sys.argv[1]))
