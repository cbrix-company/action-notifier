#!/bin/sh -l
msg="$4"
python /main.py --message-type $1 --slack-token $2 --slack-channel-id $3 --message '$msg'
