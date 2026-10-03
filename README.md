# SpaceSnap AI — What's Happening in This Space Image?

**Pipeline:** Image → Feature Detection → Explanation

## Approach (≈120 words)
SpaceSnap AI loads a NASA or Earth-observation image, shrinks it, and classifies every pixel using HSV colour-space rules. Rules separate bright low-saturation clouds from bluish ice, blue ocean, green forest, tan desert, red-orange fires, night-time city lights, and grey rocky or cratered terrain. Each detected feature is blended with a colour overlay and labelled at its centroid, with its percentage of the image shown. Features under 3% are ignored as noise. A template-based generator then turns the detected set into plain-language text, for example "a cloud system over the ocean near a coastline". The web demo (spacesnap.html) runs entirely in the browser, and spacesnap.py provides the same logic for command-line use.

## Run
- Demo: open `spacesnap.html`, use a sample or upload an image.
- Code: `pip install pillow numpy && python spacesnap.py image.jpg`

## Sample output (Earth sample scene)
Detected: clouds, ocean, forest / vegetation, ice / snow, land / desert.
Explanation: This image shows a cloud system over the ocean near a coastline, with ice or snow at high latitudes.

## Dataset / image source
Built-in samples are generated programmatically. For real images use NASA Worldview (worldview.earthdata.nasa.gov), NASA Earth Observatory (earthobservatory.nasa.gov) or NASA Image Library (images.nasa.gov), and credit NASA.

## To finish your submission
1. Push these files to a GitHub repo.
2. Add 2–3 real NASA images to a `samples/` folder.
3. Run the demo on them and take screenshots of the detection and explanation.
