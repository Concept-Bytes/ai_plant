#include "thingProperties.h"
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const int soilPin = A7; // Pin connected to the Soil sensor
const int LDRPin = A5; // Pin connected to the Soil sensor


// Network credentials
const char* ssid = "";
const char* password = "";

WebServer server(80);
unsigned long previousMillis = 0;
const long interval = 60000;  // Interval set to 10 minutes (600,000 milliseconds)

String plant_name = "Sprout";
String plant_type = "Cactus";

String base_prompt = "You are a " + plant_type + " plant named " + plant_name + ". You are friendly and informative. You give advice about how to take care of you based on your sensor data. Be brief and respond in less than 30 words";
String full_prompt = "";
String response = "";



String getCompletion(const String& prompt, const String& model = "gpt-3.5-turbo") {
    HTTPClient http;
    const String apiKey = "";
    const String serverPath = "https://api.openai.com/v1/chat/completions";

    http.begin(serverPath);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + apiKey);

    StaticJsonDocument<200> doc;
    doc["model"] = model;
    JsonArray messages = doc.createNestedArray("messages");
    JsonObject message0 = messages.createNestedObject();
    message0["role"] = "user";
    message0["content"] = prompt;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    String response;

    if (httpResponseCode > 0) {
        response = http.getString();
    } else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
    }

    http.end();
    DynamicJsonDocument respDoc(1024);
    deserializeJson(respDoc, response);
    String text = respDoc["choices"][0]["message"]["content"].as<String>();
    return text;
}

void setup() {
  Serial.begin(9600);
  delay(1500);

  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  
  // Setup web server
  server.on("/", HTTP_GET, handleRoot);
  server.begin();
  
  response = getCompletion(base_prompt + "Say Hi!");
}

void loop() {
  ArduinoCloud.update();
  server.handleClient();
  unsigned long currentMillis = millis();
  //temperature =  analogRead(analogPin); // Read the input on analog pin A0
  soil_moisture = analogRead(soilPin); // Read the input on analog pin A7
  light_level = analogRead(LDRPin);
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    String soil_prompt = " Your soil Moisture level is: " + String(soil_moisture) + " This ranges from 0(dry) - 3000(moist)";
    String light_prompt = " Your light level is: " + String(light_level) + "This ranges from 0(dark) - 100(bright)";
    String temprature_prompt = " The current temperature is: " + String(temperature) + "degrees C";
    full_prompt= base_prompt + soil_prompt + light_prompt + temprature_prompt;
    response = getCompletion(full_prompt);
    Serial.println("Received response: " + response);
  }
  delay(1000);
}

void handleRoot() {
  server.send(200, "text/html", generateHTML());
}

String generateHTML() {
  String responseText = response;  // Example response text
  String html = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>Plant Dashboard</title>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"; // Viewport for responsive web design
  html += "<link href=\"https://fonts.googleapis.com/css2?family=Audiowide&display=swap\" rel=\"stylesheet\">";
  html += "<style>body { background-image: url('https://i.pinimg.com/originals/fc/36/fa/fc36fa7816fe1847b3dcbc352f227a0f.jpg'); background-size: cover; font-family: 'Audiowide', sans-serif; text-align: center; color: #fff; padding: 5%;} .progress { width: 90%; height: 40px; background-color: #ddd; border-radius: 20px; margin: 20px auto; border: 3px solid green;}.progress-bar { height: 100%; border-radius: 20px;}.moisture-bar { background-color: blue; width: " + String((soil_moisture / 4095.0) * 100) + "%;}.light-bar { background-color: yellow; width: " + String((light_level / 4095.0) * 100) + "%;}.temp, .label, .value, .callout-box { text-shadow: -1px -1px 0 #008000, 1px -1px 0 #008000, -1px 1px 0 #008000, 1px 1px 0 #008000; font-size: 24px;}.temp { font-size: 36px; margin-top: 30px;}.label, .value { margin-top: 20px; margin-bottom: 5px;}";
  html += "h1 { font-size: 48px; text-shadow: -2px -2px 0 #008000, 2px -2px 0 #008000, -2px 2px 0 #008000, 2px 2px 0 #008000;}";
  html += ".callout-box { border: 2px solid green; border-radius: 15px; padding: 20px; margin: 20px auto; width: 80%;}"; // Callout box styling
  html += "</style></head><body>";
  html += "<h1>Plant Name</h1><br>";
  html += "<div class=\"label\">Moisture Level</div><div class='progress'><div class='progress-bar moisture-bar'></div></div>";
  html += "<div class='value'>Moisture: " + String(soil_moisture) + "</div><br>";
  html += "<div class=\"label\">Light Level</div><div class='progress'><div class='progress-bar light-bar'></div></div>";
  html += "<div class='value'>Light: " + String(light_level) + "</div><br>";
  html += "<div class='temp'>Temperature: " + String(temperature) + " &deg;F</div><br>";
  html += "<div class='callout-box'><p>" + responseText + "</p></div>";  // Adding the callout box with response text
  html += "</body></html>";
  return html;
}
void onResponseMessageChange() {
  Serial.println("Response Message Changed: " + response_message);
}

void onLightLevelChange() {
  Serial.println("Light Level Changed: " + String(light_level));
}

void onSoilMoistureChange() {
  Serial.println("Soil Moisture Changed: " + String(soil_moisture));
}

void onTemperatureChange() {
  Serial.println("Temperature Changed: " + String(temperature));
}

