#!/usr/bin/env python3

import aws_cdk as cdk

from serverless_ffmpeg.serverless_ffmpeg_stack import ServerlessFfmpegStack


app = cdk.App()
ServerlessFfmpegStack(app, "serverless-ffmpeg")

app.synth()
