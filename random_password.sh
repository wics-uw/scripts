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


# Generates some random passwords.
# If no number of passwords is specified on the command line, generates
# just one password.
# i.e.
#       ./random_password.sh
#       ./random_password.sh 5

if [ $# == 0 ]; then
 NUM='1'
else
 NUM="$1"
fi

cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n "$NUM"
