.PHONY: run clean

# ELEVENLABS_API_KEY must be set; quotes.json "spoken" holds the respelled
# text said when it differs from the displayed one.
run:
	@python3 voice_generator.py -f ../src/locales/quotes.json -o ../public/sounds

clean:
	@python3 voice_generator.py -f ../src/locales/quotes.json -o ../public/sounds --clean
