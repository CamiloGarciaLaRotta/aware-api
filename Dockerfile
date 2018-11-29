FROM cegal/aware-base

COPY aware_api/ /aware_api
EXPOSE 8080
ENTRYPOINT ["waitress-serve", "--call", "aware_api:create_app"]
