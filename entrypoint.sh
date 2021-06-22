#!/bin/sh -l
python /main.py --message $1 --message-type $2 --slack-token $3 --slack-channel-id $4
