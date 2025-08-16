FROM openjdk:22-jdk-alpine
# ARG JAR_FILE=target/*.jar
# COPY ${JAR_FILE} app.jar
# ENTRYPOINT ["java","-jar","/app.jar"]

WORKDIR /app
ENTRYPOINT ["./gradlew","bootRun"]