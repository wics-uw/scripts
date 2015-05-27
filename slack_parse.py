#!/usr/bin/python
#
# Copyright (C) 2015 Elana Hashman
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import json
import re
import sys

# Import the user id <-> nick dict
users = {}
try:
    with open('users.json', 'r') as user_file:
        data = json.load(user_file)
        for user in data:     # preface with '@'
            users[user["id"]] = "@%s" % user["name"]
except IOError:
    print "Couldn't find the users.json file, terminating."
    sys.exit(1)

# Import the channel id <-> channel name dict
channels = {}
try:
    with open('channels.json', 'r') as channels_file:
        data = json.load(channels_file)
        for channel in data:        # preface with '#'
            channels[channel["id"]] = "#%s" % channel["name"]
except IOError:
    print "Couldn't find the channels.json file, terminating."
    sys.exit(1)

# Usage info
if len(sys.argv) <= 1 or sys.argv[1] == "--help":
    print "Usage: slack_export filename_to_parse.json"
    sys.exit(0)


# Helpers
def timestamp(value):
    "Turns a decimal UNIX timestamp into an 'HH:MM' string"
    # "- 18000" <-- sketchy timezone conversion to EST
    ts = datetime.fromtimestamp(int(float(value)) - 18000)
    return datetime.strftime(ts, "%H:%M")


def parse_line(line):
    "Parses a line of JSON into a line of text"
    line_type = line["type"]
    if line_type == "message":
        subtype = line.get("subtype")

        if subtype == "bot_message":
            # TODO: Not implemented
            return
        elif subtype == "channel_purpose":
            print "%s -!- Channel Purpose: %s" % \
                (timestamp(line["ts"]), replace_with_special(line["text"]))
        elif subtype == "channel_join":
            print "%s -!- %s has joined the channel" % (timestamp(line["ts"]),
                                                        users[line["user"]])
        elif subtype == "channel_topic" or subtype == "file_share":
            print "%s -!- %s" % (timestamp(line["ts"]),
                                 replace_with_special(line["text"]))
        else:
            print "%s <%s> %s" % (timestamp(line["ts"]),
                                  users[line["user"]],
                                  replace_with_special(line["text"]))


def replace_with_special(text):
    "Substitutes user ids with nicks, channel ids with channels, escaped chars"
    users_pass = re.sub(r"<@(U[0-9A-Z]{8})(\|[^>]*)?>",
                        lambda x: users[x.group(1)],
                        text)
    channels_pass = re.sub(r"<#(C[0-9A-Z]{8})>",
                           lambda x: channels[x.group(1)],
                           users_pass)
    amp_pass = re.sub(r"&amp;", "&", channels_pass)
    lt_pass = re.sub(r"&lt;", "<", amp_pass)
    gt_pass = re.sub(r"&gt;", ">", lt_pass)
    return re.sub("\n", "   ", gt_pass)


# "main": Load the file and give it a go, print to stdout
try:
    raw_log = open(sys.argv[1], 'r')
    data = json.load(raw_log)

    for line in data:
        parse_line(line)

except IOError:
    print "Failed to open file " + sys.argv[1] + ", terminating."
    sys.exit(1)
