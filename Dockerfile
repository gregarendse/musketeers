FROM azul/zulu-openjdk-alpine:17 as build
WORKDIR /workspace/app

ARG DEPENDENCY=target/dependency

ADD target target
RUN mkdir -p ${DEPENDENCY} && (cd ${DEPENDENCY}; jar -xf ../*.jar)

FROM azul/zulu-openjdk-alpine:17-jre-headless

RUN addgroup -S spring && adduser -S spring -G spring

EXPOSE 8080

ARG DEPENDENCY=/workspace/app/target/dependency
ARG JAVA_OPTS=""

COPY --from=build ${DEPENDENCY}/BOOT-INF/lib        /app/lib
COPY --from=build ${DEPENDENCY}/META-INF            /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes    /app

USER spring

ENTRYPOINT ["sh", "-c", "java \
-cp app:app/lib/* \
-noverify \
-XX:TieredStopAtLevel=1 \
${JAVA_OPTS} \
za.co.entelect.training.musketeers.MusketeersApplication \
${0} \
${@}"]

