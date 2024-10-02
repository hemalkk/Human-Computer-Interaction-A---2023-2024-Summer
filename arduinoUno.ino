// Button Control Code for Play/Pause, Volume Mute/Unmute, Full Screen On/Off

// Pin assignments for the buttons
const int buttonPin1 = 2;     // Pin for Play/Pause button
const int buttonPin2 = 3;     // Pin for Mute/Unmute button
const int buttonPin3 = 4;     // Pin for Full Screen button

// Variables to store the last state of each button
int lastButtonState1 = HIGH;  // Last state of Play/Pause button
int lastButtonState2 = HIGH;  // Last state of Mute/Unmute button
int lastButtonState3 = HIGH;  // Last state of Full Screen button

// Setup function runs once when the program starts
void setup() {
  // Set buttons as inputs with pull-up resistors enabled
  pinMode(buttonPin1, INPUT_PULLUP);  // Play/Pause button setup
  pinMode(buttonPin2, INPUT_PULLUP);  // Mute/Unmute button setup
  pinMode(buttonPin3, INPUT_PULLUP);  // Full Screen button setup

  // Initialize serial communication at 9600 baud rate for debugging
  Serial.begin(9600);
}

// Loop function runs repeatedly
void loop() {
  // Read the current state of each button
  int buttonState1 = digitalRead(buttonPin1);  // Read Play/Pause button
  int buttonState2 = digitalRead(buttonPin2);  // Read Mute/Unmute button
  int buttonState3 = digitalRead(buttonPin3);  // Read Full Screen button

  // Check if the Play/Pause button was pressed (LOW means pressed)
  if (buttonState1 == LOW && lastButtonState1 == HIGH) {
    // Send "PLAY_PAUSE" message via serial for external control
    Serial.println("PLAY_PAUSE");
    delay(300);  // Debounce delay to prevent multiple triggers
  }
  lastButtonState1 = buttonState1;  // Update last state of Play/Pause button

  // Check if the Mute/Unmute button was pressed
  if (buttonState2 == LOW && lastButtonState2 == HIGH) {
    // Send "MUTE_UNMUTE" message via serial for external control
    Serial.println("MUTE_UNMUTE");
    delay(300);  // Debounce delay to prevent multiple triggers
  }
  lastButtonState2 = buttonState2;  // Update last state of Mute/Unmute button

  // Check if the Full Screen button was pressed
  if (buttonState3 == LOW && lastButtonState3 == HIGH) {
    // Send "FULL_SCREEN" message via serial for external control
    Serial.println("FULL_SCREEN");
    delay(300);  // Debounce delay to prevent multiple triggers
  }
  lastButtonState3 = buttonState3;  // Update last state of Full Screen button
}
