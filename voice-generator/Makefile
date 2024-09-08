# Ansi colors
ifneq ($(MAKE_TERMOUT),"")
	RED    := \033[1;31m
	GREEN  := \033[1;32m
	YELLOW := \033[1;33m
	CYAN   := \033[1;36m
	RESET  := \033[0m
else
	RED    :=
	GREEN  :=
	YELLOW :=
	CYAN   :=
	RESET  :=
endif

.PHONY: setup run clean

VENV_DIR := $(shell realpath .venv)

run:
	@$(VENV_DIR)/bin/python3 voice_generator.py -f ../src/locales/quotes.json -o ../public/sounds

clean:
	@$(VENV_DIR)/bin/python3 voice_generator.py -f ../src/locales/quotes.json -o ../public/sounds --clean

setup:
	@/usr/bin/echo -e "🔧 ${YELLOW}Environment setup${RESET}"
	@./build/setup.sh $(VENV_DIR)
	@/usr/bin/echo -e "🔧 ${GREEN}Environment setup complete successfully !${RESET}"
