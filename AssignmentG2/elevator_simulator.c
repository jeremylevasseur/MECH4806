/*
=================================================================
=================================================================
===== MECH 4806 - MECHATRONICS - ASSIGNMENT 2 - ACTIVITY 5 ======


======================= FOUR-STORY ELEVATOR =====================

=========================== Description =========================

Use a microcontroller to simulate the operation of a simple elevator in a four-story building.
Use Tinkercad to code and simulate the behaviour of the microcontroller. Use LEDs to show 
where the elevator is and use four small switches next to each LED to control the elevator. 
Program the microcontroller, such that:
a) When the elevator reaches a specific floor (or stays on), the related LED should stay on. 

b) When the elevator is moving up or down, the LEDs for each floor on the way would turn on 
and off as the elevator passes those intermediate floors.

c) For the simulator, it only takes 1.5 seconds to pass from one floor to another.

d) If someone presses other buttons, then the elevator stops on those floors if they are in 
the same direction, and if not will catch them on the way back.

e) If no button is pressed, the elevator always comes back to the first floor (floor 1).

f) You may make more assumptions and make the behaviour of the elevator more realistic.

g) Attach your microcontroller program with proper comments to your pre-lab report.

=================================================================
=================================================================
*/


// Button pin numbers
const int buttonPin1 = 2;	// The pin number associated with button 1
const int buttonPin2 = 4;	// The pin number associated with button 2
const int buttonPin3 = 6;	// The pin number associated with button 3
const int buttonPin4 = 8;	// The pin number associated with button 4

// LED pin numbers
const int ledPin1 = 3;		// The pin number associated with led 1
const int ledPin2 = 5;		// The pin number associated with led 2
const int ledPin3 = 7;		// The pin number associated with led 3
const int ledPin4 = 9;		// The pin number associated with led 4

// Global variables that will handle the states of the buttons
int stateOfButton1 = 0;
int stateOfButton2 = 0;
int stateOfButton3 = 0;
int stateOfButton4 = 0;

// Global variables
int i, j, k;						// Iteration variables
int numberOfFloors = 4;				// Number of floors in the building
int floors[] = {1, 0, 0, 0}; 		// Variable that will be used for elevator system
int currentFloor = 1;				// Variable that will be used to keep track of the current floor the elevator is at
String queuedRequests = String("");	// Setting a String object that will be used for floor requests

int elevatorSpeed = 1500; 			// The length of time it takes for the elevator to move from one floor to another (in milliseconds)
int elevatorWaitSpeed = 3000;		// The length of time that the elevator waits for someone at a requested floor (in milliseconds)

void setup()
{
  // Setting up the console
  Serial.begin(9600);
  
  // Initializing the button pins as inputs
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
  
  // Initializing the led pins as outputs
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  
  // Starting the elevator at floor 1, turning led 1 output state to HIGH
  digitalWrite(ledPin1, HIGH);
  
}


/*
Desc:
	This function finds the floor that the elevator is currently at.
    It searches the floors array for the element that has the value of 1.

Inputs:
	None
    
Outputs:
	None
*/
int findCurrentFloor() {
  for (i = 0; i < numberOfFloors; i++) {
    if (floors[i] == 1) {
      return i + 1;
    }
  }
  return -1;
}


/*
Desc:
	This function turns the state of an LED pin to HIGH.

Inputs:
	floorNumber		=>		An integer that represents the floor number of the led pin that needs to be turned on.
    
Outputs:
	None
*/
void turnFloorLightOn(int floorNumber) {
  
  if (floorNumber == 1) {
    digitalWrite(ledPin1, HIGH);
  } else if (floorNumber == 2) {
    digitalWrite(ledPin2, HIGH);
  } else if (floorNumber == 3) {
    digitalWrite(ledPin3, HIGH);
  } else if (floorNumber == 4) {
    digitalWrite(ledPin4, HIGH);
  }
  
  return;
}


/*
Desc:
	This function turns the state of an LED pin to LOW.

Inputs:
	floorNumber		=>		An integer that represents the floor number of the led pin that needs to be turned off.
    
Outputs:
	None
*/
void turnFloorLightOff(int floorNumber) {
  
  if (floorNumber == 1) {
    digitalWrite(ledPin1, LOW);
  } else if (floorNumber == 2) {
    digitalWrite(ledPin2, LOW);
  } else if (floorNumber == 3) {
    digitalWrite(ledPin3, LOW);
  } else if (floorNumber == 4) {
    digitalWrite(ledPin4, LOW);
  }
  
  return;
}


/*
Desc:
	This function looks through the string that contains the requested floor numbers for the specified floor.

Inputs:
	floorNumber		=>		An integer that represents a floor number.
    
Outputs:
	boolean			=>		A boolean that represents whether the specified floor number has been requested or not.
*/
bool checkForRequests(int floorNumber) {
  // Looping through the requested floors and looking for the specified floor number
  
  for (j = 0; j < queuedRequests.length(); j++) {
    // Subtracting '0' from a char casts it into an integer
    if (floorNumber == queuedRequests.charAt(j) - '0') {
      // The specified floor number is in the queue
      queuedRequests.remove(j); // Removing it from the queue
      return true;
    }
  }
  
  // The specified floor number was not found, returning false.
  return false;
}


/*
Desc:
	This function contains the logic to move to a specified floor.

Inputs:
	destinationFloor		=>		An integer that represents the floor number of the desired destination.
    
Outputs:
	None
*/
void moveToAnotherFloor(int destinationFloor) {
  
  currentFloor = findCurrentFloor();
  
  if (currentFloor < destinationFloor) {
    
    // Need to move up
    waitAndListenForRequests(elevatorSpeed);
    
    for (i = currentFloor; i < destinationFloor; i++) {
      
      turnFloorLightOff(i);
      turnFloorLightOn(i + 1);
      
      floors[i - 1] = 0;
      floors[i] = 1;
      
      if (checkForRequests(i + 1)) {
        
        // Somebody requested this floor, must wait longer.
        Serial.print("Waiting for passengers at floor " + String(i + 1) + ".\r\n");
        waitAndListenForRequests(elevatorWaitSpeed);
        
      } else {
        // Nobody requested this floor, may continue.
        waitAndListenForRequests(elevatorSpeed);
      }
      
    }
    
  } else if (currentFloor > destinationFloor) {
	// Need to move down
   	
    waitAndListenForRequests(elevatorSpeed);
    
    for (i = currentFloor; i > destinationFloor; i--) {
      
      turnFloorLightOff(i);
      turnFloorLightOn(i - 1);
      
      floors[i - 1] = 0;
      floors[i - 2] = 1;
      
      if (checkForRequests(i - 1)) {
        
        // Somebody requested this floor, must wait longer.
        Serial.print("Waiting for passengers at floor " + String(i - 1) + ".\r\n");
        waitAndListenForRequests(elevatorWaitSpeed);
        
      } else {
        
        // Nobody requested this floor, may continue.
        waitAndListenForRequests(elevatorSpeed);
          
      }
      
    }
    
  }
  
  return;
  
}


/*
Desc:
	The purpose of this function is to wait for a desired amount of time while also listening to the button states.

Inputs:
	waitingTime		=>		An integer that represents the length of the wait time desired.
    
Outputs:
	None
*/
void waitAndListenForRequests(int waitingTime) {

  int totalWaitTime = 0;
  int waitIncrements = 30;	// Size of the incremental waiting times
  
  while (totalWaitTime < waitingTime) {
    delay(waitIncrements);
    totalWaitTime += waitIncrements;
    
    // Listening for requests
    stateOfButton1 = digitalRead(buttonPin1);
    stateOfButton2 = digitalRead(buttonPin2);
    stateOfButton3 = digitalRead(buttonPin3);
    stateOfButton4 = digitalRead(buttonPin4);

    // Applying logic to the current button states
    if (stateOfButton1 == HIGH) {

      // Making sure that floor 1 isn't in the queue already
      if (queuedRequests.indexOf('1') == -1) {
        // Adding floor 1 to the queue
        Serial.print("Floor 1 has been requested.\r\n");
        queuedRequests += String("1");
      }

    } else if (stateOfButton2 == HIGH) {

      // Making sure that floor 2 isn't in the queue already
      if (queuedRequests.indexOf('2') == -1) {
        // Adding floor 2 to the queue
        Serial.print("Floor 2 has been requested.\r\n");
        queuedRequests += String("2");
      }

    } else if (stateOfButton3 == HIGH) {

      // Making sure that floor 3 isn't in the queue already
      if (queuedRequests.indexOf('3') == -1) {
        // Adding floor 3 to the queue
        Serial.print("Floor 3 has been requested.\r\n");
        queuedRequests += String("3");
      }

    } else if (stateOfButton4 == HIGH) {

      // Making sure that floor 4 isn't in the queue already
      if (queuedRequests.indexOf('4') == -1) {
        // Adding floor 4 to the queue
        Serial.print("Floor 4 has been requested.\r\n");
        queuedRequests += String("4");
      }

    }
    
  }
  
  return;
  
}


/*
Desc:
	The function that loops indefinitely.

Inputs:
	None
    
Outputs:
	None
*/
void loop()
{
  // Getting the current floor value
  currentFloor = findCurrentFloor();
  
  // Reading in the current button states
  stateOfButton1 = digitalRead(buttonPin1);
  stateOfButton2 = digitalRead(buttonPin2);
  stateOfButton3 = digitalRead(buttonPin3);
  stateOfButton4 = digitalRead(buttonPin4);
  
  // Applying logic to the current button states
  if (stateOfButton1 == HIGH) {
    
    // Making sure that floor 1 isn't in the queue already
    if (queuedRequests.indexOf('1') == -1) {
      // Adding floor 1 to the queue
      //Serial.print("Floor 1 has been requested.\r\n");
      queuedRequests += String("1");
    }
    
  } else if (stateOfButton2 == HIGH) {
    
    // Making sure that floor 2 isn't in the queue already
    if (queuedRequests.indexOf('2') == -1) {
      // Adding floor 2 to the queue
      //Serial.print("Floor 2 has been requested.\r\n");
      queuedRequests += String("2");
    }
    
  } else if (stateOfButton3 == HIGH) {
    
    // Making sure that floor 3 isn't in the queue already
    if (queuedRequests.indexOf('3') == -1) {
      // Adding floor 3 to the queue
      //Serial.print("Floor 3 has been requested.\r\n");
      queuedRequests += String("3");
    }
    
  } else if (stateOfButton4 == HIGH) {
    
    // Making sure that floor 4 isn't in the queue already
    if (queuedRequests.indexOf('4') == -1) {
      // Adding floor 4 to the queue
      //Serial.print("Floor 4 has been requested.\r\n");
      queuedRequests += String("4");
    }
    
  }
  
  if (queuedRequests.length() > 0) {
    // Need to move floors
    int tempFloor = queuedRequests.charAt(0) - '0';
    queuedRequests.remove(0); // Removing this floor from the queue because it will be in progress
    
    // Moving to requested floor
    Serial.print("Moving to floor " + String(tempFloor) + ".\r\n");
    moveToAnotherFloor(tempFloor);
    
    // Wait at the requested floor
    waitAndListenForRequests(elevatorWaitSpeed - elevatorSpeed);
    
    // Moving back down to the first floor
    moveToAnotherFloor(1);
  }
  
  delay(50); // Listening for button presses every 200 ms
}