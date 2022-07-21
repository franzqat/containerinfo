FROM bitnami/kubectl as kubectl
FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
ADD app .

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

COPY --from=kubectl /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/

RUN apk update \
 && apk add --no-cache curl jq \
 && rm -rf /var/cache/apk/*

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["/app/main.py"]