# Atherium-X Build Makefile
# Run inside Linux or WSL2 as root (e.g., sudo make build PHASE=phase-1)

BUILD_DIR ?= /var/tmp/atherium-x-build
ISO_OUT   ?= atherium-x.iso
PHASE     ?= phase-1

.PHONY: help build clean checksum verify size-report chart

help:
	@echo "Atherium-X Build System"
	@echo "  make build PHASE=phase-1       Build ISO in $(BUILD_DIR), copy to $(ISO_OUT), verify, and report size"
	@echo "  make clean                     Remove $(BUILD_DIR) and temporary build files"
	@echo "  make checksum                  Generate and verify $(ISO_OUT).sha256"
	@echo "  make verify                    Run static ISO integrity checks (no VM/QEMU)"
	@echo "  make size-report PHASE=phase-1 Generate ISO size + top-20 package report"
	@echo "  make chart                     Generate docs/boot_times.png from docs/boot_times.csv"

build:
	@if [ "$$(id -u)" -ne 0 ]; then \
		echo "ERROR: make build must run as root (needed by live-build/debootstrap)."; \
		exit 1; \
	fi
	@echo "==> Staging Atherium-X sources into $(BUILD_DIR)..."
	mkdir -p "$(BUILD_DIR)"
	rsync -a --delete --exclude='cache' --exclude='.build' --exclude='chroot' --exclude='binary' \
		auto config "$(BUILD_DIR)/"
	@if [ -d assets ]; then rsync -a --delete assets "$(BUILD_DIR)/"; fi
	@if [ -d assets/icons/Atherium-X-Icons ]; then \
		mkdir -p "$(BUILD_DIR)/config/includes.chroot/usr/share/icons"; \
		rsync -a assets/icons/Atherium-X-Icons "$(BUILD_DIR)/config/includes.chroot/usr/share/icons/"; \
	fi
	@if [ -f assets/wallpaper/atherium-hud.png ]; then \
		mkdir -p "$(BUILD_DIR)/config/includes.chroot/usr/share/backgrounds/atherium-x"; \
		cp -f assets/wallpaper/atherium-hud.png "$(BUILD_DIR)/config/includes.chroot/usr/share/backgrounds/atherium-x/"; \
	fi
	find "$(BUILD_DIR)/auto" "$(BUILD_DIR)/config" -type f ! -name '*.png' -exec sed -i 's/\r$$//' {} + 2>/dev/null || true
	chmod +x "$(BUILD_DIR)"/auto/*
	find "$(BUILD_DIR)/config/hooks" -type f -name '*.hook.*' -exec chmod +x {} + 2>/dev/null || true
	find "$(BUILD_DIR)/config/includes.chroot/usr/local/bin" -type f -exec chmod +x {} + 2>/dev/null || true
	@echo "==> Running live-build (lb clean && lb config && lb build) in $(BUILD_DIR)..."
	cd "$(BUILD_DIR)" && lb clean || true
	cd "$(BUILD_DIR)" && lb config && lb build
	@ISO_FOUND=$$(ls -1 "$(BUILD_DIR)"/live-image-*.hybrid.iso 2>/dev/null | head -n 1); \
	if [ -z "$$ISO_FOUND" ]; then \
		echo "ERROR: No hybrid ISO produced in $(BUILD_DIR)!"; \
		exit 1; \
	fi; \
	cp -f "$$ISO_FOUND" "$(ISO_OUT)"
	@$(MAKE) checksum
	@$(MAKE) verify
	@$(MAKE) size-report PHASE="$(PHASE)"

clean:
	rm -rf "$(BUILD_DIR)"
	rm -f "$(ISO_OUT)" "$(ISO_OUT).sha256"

checksum:
	sha256sum "$(ISO_OUT)" > "$(ISO_OUT).sha256"
	sha256sum -c "$(ISO_OUT).sha256"

verify:
	bash scripts/verify_iso.sh "$(ISO_OUT)"

size-report:
	bash scripts/size_report.sh "$(PHASE)" "$(ISO_OUT)" "$(BUILD_DIR)"

chart:
	python3 scripts/plot_boot_times.py docs/boot_times.csv docs/boot_times.png
