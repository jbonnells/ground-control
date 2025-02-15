.PHONY: run clean

gcs = GCS

run_python: $(gcs).py networking.py
	python3 $(gcs).py

clean:
	rm -rf $(fsw).o __pycache__
