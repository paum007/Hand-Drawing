# Theory behind the commands

## Contents
- [GestureRecogniserOptions](#gesturerecogniseroptions)
- [Asynchronous](#asynchronous)



## GestureRecogniserOptions
**GestureRecognizerOptions** is just a configuration object — it bundles together all the settings MediaPipe needs before it can create the recognizer. Think of it like filling out a form before starting a job.

It takes three things here:

base_options — the foundational setting, which is just pointing to the model file. This tells MediaPipe *which brain to use.*

running_mode — tells MediaPipe how you're going to feed it data. There are three modes:
- IMAGE — one-off static images
- VIDEO — a pre-recorded video file
- LIVE_STREAM — a continuous real-time feed, which is what you're using

result_callback — only required in LIVE_STREAM mode. Because results come back asynchronously, MediaPipe needs to know where to deliver them. In IMAGE or VIDEO mode you don't need this because results come back synchronously.

So essentially this line is saying: *"use this model, expect a continuous live feed, and when results are ready deliver them to print_result."*

## Asynchronous

Normally when your code runs a function, it stops and waits for that function to finish before moving on. That's synchronous — one thing at a time, in order.

Asynchronous means don't wait, keep going. You hand something off and continue with your own work, and you'll be notified when it's done.

In your script, the reason this matters is that gesture recognition takes time. MediaPipe needs to analyse the frame, run it through the neural network, and produce a result. If your loop had to wait for that every frame, it would slow down and your camera feed would stutter.

Instead, **recognize_async** says *"here's a frame, process it whenever you're ready"* and returns immediately. Your loop keeps grabbing frames and displaying them smoothly, while MediaPipe is working in the background on its own thread.

When MediaPipe finishes, it fires the callback — that's its way of tapping you on the shoulder and saying *"I'm done, here's the result."*

So in your script at any given moment there are effectively **two things happening in parallel:**

- Your loop, running continuously, grabbing frames and displaying text
- MediaPipe, processing frames in the background and updating text via the callback

That's the essence of asynchronous programming.