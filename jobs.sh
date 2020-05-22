#!/bin/bash
/home/ubuntu/StreamerCap/venv/bin/python /home/ubuntu/StreamerCap/streamercap/manage.py update_twitch_streams

/home/ubuntu/StreamerCap/venv/bin/python /home/ubuntu/StreamerCap/streamercap/manage.py update_mixer_streams
