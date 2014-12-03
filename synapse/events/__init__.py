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

from frozendict import frozendict


def _freeze(o):
    if isinstance(o, dict):
        return frozendict({k: _freeze(v) for k,v in o.items()})

    if isinstance(o, basestring):
        return o

    try:
        return tuple([_freeze(i) for i in o])
    except TypeError:
        pass

    return o


class _EventInternalMetadata(object):
    def __init__(self, internal_metadata_dict):
        self.__dict__ = internal_metadata_dict

    def get_dict(self):
        return dict(self.__dict__)


def _event_dict_property(key):
        def getter(self):
            return self._event_dict[key]

        def setter(self, v):
            self._event_dict[key] = v

        def delete(self):
            del self._event_dict[key]

        return property(
            getter,
            setter,
            delete,
        )


class EventBase(object):
    def __init__(self, event_dict, signatures={}, unsigned={},
                 internal_metadata_dict={}):
        self.signatures = signatures
        self.unsigned = unsigned

        self._event_dict = event_dict

        self.internal_metadata = _EventInternalMetadata(
            internal_metadata_dict
        )

    auth_events = _event_dict_property("auth_events")
    content = _event_dict_property("content")
    event_id = _event_dict_property("event_id")
    hashes = _event_dict_property("hashes")
    origin = _event_dict_property("origin")
    prev_events = _event_dict_property("prev_events")
    prev_state = _event_dict_property("prev_state")
    room_id = _event_dict_property("room_id")
    sender = _event_dict_property("sender")
    state_key = _event_dict_property("state_key")
    type = _event_dict_property("type")
    user_id = _event_dict_property("sender")

    def get_dict(self):
        d = dict(self._original)
        d.update({
            "signatures": self._signatures,
            "unsigned": self._unsigned,
        })

        return d

    def get_internal_metadata_dict(self):
        return self.internal_metadata.get_dict()

    def get_pdu_json(self, time_now=None):
        pdu_json = self.get_dict()

        if time_now is not None and "age_ts" in pdu_json["unsigned"]:
            age = time_now - pdu_json["unsigned"]["age_ts"]
            pdu_json.setdefault("unsigned", {})["age"] = int(age)
            del pdu_json["unsigned"]["age_ts"]

        return pdu_json

    def __set__(self, instance, value):
        raise AttributeError("Unrecognized attribute %s" % (instance,))


class FrozenEvent(EventBase):
    def __init__(self, event_dict, signatures={}, unsigned={}):
        event_dict = dict(event_dict)

        signatures.update(event_dict.pop("signatures", {}))
        unsigned.update(event_dict.pop("unsigned", {}))

        frozen_dict = _freeze(event_dict)

        super(FrozenEvent, self).__init__(
            frozen_dict,
            signatures=signatures,
            unsigned=unsigned
        )

    @staticmethod
    def from_event(event):
        e = FrozenEvent(
            event.event_dict()
        )

        e.internal_metadata = event.internal_metadata

        return e
