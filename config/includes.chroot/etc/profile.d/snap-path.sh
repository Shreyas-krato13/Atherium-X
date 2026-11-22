# Ensure Snap binaries are on PATH in live sessions
case ":$PATH:" in
    *:/snap/bin:*) ;;
    *) export PATH="$PATH:/snap/bin" ;;
esac
