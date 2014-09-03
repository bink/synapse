# -*- coding: utf-8 -*-
# Copyright 2014 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains constants from the specification."""


class Membership(object):

    """Represents the membership states of a user in a room."""
    INVITE = u"invite"
    JOIN = u"join"
    KNOCK = u"knock"
    LEAVE = u"leave"
    BAN = u"ban"
    LIST = (INVITE, JOIN, KNOCK, LEAVE, BAN)


class Feedback(object):

    """Represents the types of feedback a user can send in response to a
    message."""

    DELIVERED = u"delivered"
    READ = u"read"
    LIST = (DELIVERED, READ)


class PresenceState(object):
    """Represents the presence state of a user."""
    OFFLINE = u"offline"
    UNAVAILABLE = u"unavailable"
    ONLINE = u"online"
    FREE_FOR_CHAT = u"free_for_chat"


class JoinRules(object):
    PUBLIC = u"public"
    KNOCK = u"knock"
    INVITE = u"invite"
    PRIVATE = u"private"
