# Auto-start Atherium-X JARVIS HUD desktop on TTY1 login
if [ -z "${DISPLAY:-}" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec startx -- -keeptty >/tmp/xorg-session.log 2>&1
fi
