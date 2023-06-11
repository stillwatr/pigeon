docker-image:
	docker build -t telegram.commons .

clean:
	rm -rf build
	rm -rf *.egg-info
