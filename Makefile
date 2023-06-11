docker-image:
	docker build -t telegram-commons:latest .

clean:
	rm -rf build
	rm -rf *.egg-info
