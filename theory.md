# Theory behind the commands

## Contents
- [GestureRecogniserOptions](#gesturerecogniseroptions)
- [Asynchronous](#asynchronous)
- [Camera Buffer and FPS](#camera-buffer-and-fps)
- [Timestamps](#timestamps)
- [Frame Flipping](#frame-flipping)
- [LAB Colour Space](#lab-colour-space)
- [CLAHE](#clahe)
- [Landmark Coordinates](#landmark-coordinates)
- [Canvas Blending](#canvas-blending)



## GestureRecogniserOptions
**GestureRecognizerOptions** is just a configuration object. It bundles together all the settings MediaPipe needs before it can create the recognizer. Think of it like filling out a form before starting a job.

It takes three things here:

base_options is the foundational setting, which is just pointing to the model file. This tells MediaPipe *which brain to use.*

running_mode tells MediaPipe how you are going to feed it data. There are three modes:
- IMAGE: one-off static images
- VIDEO: a pre-recorded video file
- LIVE_STREAM: a continuous real-time feed, which is what you are using

result_callback is only required in LIVE_STREAM mode. Because results come back asynchronously, MediaPipe needs to know where to deliver them. In IMAGE or VIDEO mode you do not need this because results come back synchronously.

So essentially this line is saying: *"use this model, expect a continuous live feed, and when results are ready deliver them to print_result."*

## Asynchronous

Normally when your code runs a function, it stops and waits for that function to finish before moving on. That is synchronous: one thing at a time, in order.

Asynchronous means do not wait, keep going. You hand something off and continue with your own work, and you will be notified when it is done.

In your script, the reason this matters is that gesture recognition takes time. MediaPipe needs to analyse the frame, run it through the neural network, and produce a result. If your loop had to wait for that every frame, it would slow down and your camera feed would stutter.

Instead, **recognize_async** says *"here is a frame, process it whenever you are ready"* and returns immediately. Your loop keeps grabbing frames and displaying them smoothly, while MediaPipe is working in the background on its own thread.

When MediaPipe finishes, it fires the callback. That is its way of tapping you on the shoulder and saying *"I am done, here is the result."*

So in your script at any given moment there are effectively **two things happening in parallel:**

- Your loop, running continuously, grabbing frames and displaying text
- MediaPipe, processing frames in the background and updating text via the callback

That is the essence of asynchronous programming.

## Camera Buffer and FPS

When you open a camera with OpenCV, it maintains an internal buffer. This is a small queue of frames it has already captured and is holding in memory, ready for you to read.

By default this buffer holds several frames. That means when you call `feed.read()`, you might get a frame that was captured a moment ago rather than the most recent one. In a drawing app this creates noticeable lag, because your hand has moved but the frame you are processing is stale.

Setting `CAP_PROP_BUFFERSIZE` to `1` tells OpenCV to only hold one frame at a time. Every time you call `read()` you get the freshest frame available.

`CAP_PROP_FPS` sets the target frame rate, in this case 20 frames per second. This controls how fast the camera captures, keeping processing load manageable while still feeling smooth.

## Timestamps

MediaPipe's async mode requires a timestamp with every frame you send it. This is because frames arrive out of order relative to when results come back. The timestamp is how MediaPipe keeps track of which result belongs to which frame, and ensures it processes them in the right sequence.

The timestamp is tracked manually in milliseconds. Each time a frame is grabbed, the timestamp increments by `1000 / fps`, which is the number of milliseconds one frame takes at the current frame rate. This gives MediaPipe a consistent, monotonically increasing clock to work with.

## Frame Flipping

Raw webcam footage shows you as others see you. If you raise your right hand, it appears on the left side of the screen. This is unintuitive for a drawing app because your movements feel reversed.

`cv2.flip(frame, 1)` mirrors the frame horizontally, so the image behaves like a mirror. When you move your hand right, the drawing moves right. This is why the hand labels in two-hand mode appear swapped. MediaPipe detects your actual left hand, but because the frame is flipped it appears on the right side of the screen.

## LAB Colour Space

Most images are stored in BGR (Blue, Green, Red), which mixes three colour channels together. The problem is that brightness is baked into all three channels at once, so you cannot adjust it cleanly without affecting the colours.

LAB is a different way of representing colour that separates brightness from colour information:
- **L**: Lightness, how bright the pixel is
- **A**: colour axis from green to red
- **B**: colour axis from blue to yellow

Converting to LAB lets you touch *only* the brightness of the image without disturbing the colours at all. In this project that is exactly what is needed. The goal is to enhance the contrast of the hand without shifting its hue, so MediaPipe can detect it more reliably in poor lighting.

## CLAHE

CLAHE stands for **Contrast Limited Adaptive Histogram Equalization**. To understand it, start with the simpler version: regular histogram equalization.

A histogram of an image shows how many pixels exist at each brightness level. If most pixels are clustered in a narrow range, for example mostly dark, the image looks flat and low contrast. Histogram equalization spreads those pixels out across the full brightness range, making the image more vivid and easier to interpret.

The problem with basic histogram equalization is that it looks at the whole image at once. If one corner is very bright and the rest is dark, the global adjustment can make parts of the image look unnatural or washed out.

**Adaptive** histogram equalization solves this by dividing the image into a grid of small tiles (in this case 8x8) and equalizing each tile independently. Each region gets its own local contrast boost, so a dark hand against a bright background can both be enhanced appropriately.

**Contrast Limited** adds one more refinement: it caps how aggressively any tile can be equalized. Without this, flat uniform regions like a plain wall get over-enhanced and develop ugly noise. The `clipLimit=2.0` parameter sets this cap.

In this project CLAHE is applied only to the **L channel** of the LAB image, the lightness channel, so only contrast is improved and not colour. The result is a frame where hands are clearer and better defined, helping MediaPipe's landmark detection work more reliably across different lighting conditions.

## Landmark Coordinates

When MediaPipe detects a hand it returns 21 landmarks, one for each key point on the hand such as fingertips, knuckles, and the wrist. Each landmark has `x`, `y`, and `z` coordinates.

Crucially, these are **normalised**. They are not pixel positions. Instead they are values between 0.0 and 1.0 representing a proportion of the frame dimensions. An `x` of 0.5 means the point is halfway across the frame, regardless of the actual resolution.

To draw on the canvas you need real pixel positions, so you multiply:
```
pixel_x = landmark.x * frame_width
pixel_y = landmark.y * frame_height
```

Landmark 8 is the **index fingertip**, which is what this project tracks for drawing and erasing.

## Canvas Blending

The drawing happens on a separate black surface, which is a NumPy array filled with zeros, rather than directly on the camera frame. This keeps the drawing persistent across frames, since the camera frame is replaced every loop but the drawing surface is not.

To display them together, `cv2.addWeighted` combines the two images:

```python
cv2.addWeighted(frame, 1.0, drawing_surface, 1.0, 0)
```

Each argument after the image is a weight. Here both are `1.0`, meaning the camera feed and the drawing are shown at full opacity. The final `0` is a scalar added to every pixel, which is not needed here so it is zero.

The result is a single blended frame: the live camera feed with the drawing overlaid on top of it.
