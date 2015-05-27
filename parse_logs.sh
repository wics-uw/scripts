#!/bin/bash
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


# Given root Slack export directory, create logs/ directory and
# search the current directory for all json files in
# dir/YYYY-MM-DD.json form. Create dir-YYYY-MM-DD.log in logs/.

mkdir -p logs
for file in `find . -name '[-0-9]*.json'`; do
    filename=${file:2}
    filename=${filename/\//-}
    ./slack_parse.py $file > logs/${filename%json}log
done
