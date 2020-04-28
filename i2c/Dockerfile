FROM arm32v6/alpine:3.10 as build

RUN apk add --update \
  gcc \
  musl-dev \
  make \
  linux-headers \
  && rm -rf /var/cache/apk/*

COPY src/ /tmp/src/

RUN \
  cd /tmp/src/ \
  && \
  make oled

FROM arm32v6/alpine:3.10

RUN \
  apk add --update \
  jq \
  && rm -rf /var/cache/apk/*

COPY --from=build /tmp/src/oled /oled

WORKDIR /

CMD /oled

