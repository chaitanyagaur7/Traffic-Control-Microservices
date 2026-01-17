# Use a lightweight Java image
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
# Copy the compiled jar (you must run 'mvn package' first)
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]