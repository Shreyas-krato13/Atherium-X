#!/bin/sh
export XDG_CURRENT_DESKTOP=Openbox
export GTK_THEME=Atherium-X
if command -v dbus-run-session >/dev/null 2>&1; then
    exec dbus-run-session -- openbox-session
else
    exec openbox-session
fi
