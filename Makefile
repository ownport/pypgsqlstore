
.PHONY: clean
clean:
	@ echo "[INFO] Cleaning files: *.pyc" && \
		find . -name "*.pyc" -delete

.PHONY: post-clean
post-clean: clean
	@ echo "[INFO] Cleaning build directories" && \
		rm -rf $(shell pwd)/*.egg-info

	@ echo "[INFO] Cleaning cache files" && \
		find . -name "__pycache__" -delete

	@ echo "[INFO] Cleaning coverage files"
	@ rm -rf \
		$(shell pwd)/.coverage.* \
		$(shell pwd)/report.xml

.PHONY: test
test: 
	@ drone exec --build-event test

.PHONY: test-in-droneci
test-in-droneci:
	@ PYTHONDONTWRITEBYTECODE=1 pytest \
		--cov=pypgsqlstore \
		-p no:cacheprovider \
		--junitxml=report.xml \
		--cov-report=term-missing \
		--cov-config=.coveragerc

.PHONY: build-dev-image
build-dev-image:
	docker build -t ownport/pypgsqlstore-dev .
