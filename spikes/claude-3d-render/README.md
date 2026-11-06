# Spike: Claude-authored 3D animation, no Figma, no credits

Claude writes a Three.js scene as an HTML page. A Playwright script steps it frame by frame in headless Chromium, screenshots each frame, and FFmpeg encodes the MP4. Time is driven by frame number, not wall clock, so output is deterministic and frame-exact.

Result of first run (cloud container, 4 CPU, software WebGL):

| Clip | Frames | Render time | File |
| --- | --- | --- | --- |
| AI bubble, 1920x1080, 30 fps, 6 s | 180 | ~100 s | 1.1 MB |

A Mac with a GPU should be several times faster.

Run:

    npm install three@0.170.0
    node render.js
    ffmpeg -framerate 30 -i frames/%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4

Contract every scene follows: the page sets `window.__ready = true` and exposes `window.renderFrame(frameNumber)`. That is the interface the app's renderer will call.
