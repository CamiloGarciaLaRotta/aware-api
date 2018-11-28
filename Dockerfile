FROM python:3.6-alpine

RUN apk add --no-cache --update python3-dev gcc build-base
# copying only requirements first avoids rebuilding
# the dependency layer when the source code changes
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY aware_api/ /aware_api
EXPOSE 8080
ENTRYPOINT ["waitress-serve", "--call", "aware_api:create_app"]
