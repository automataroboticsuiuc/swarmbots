#include <AFMotor.h>
#define COMMAND_MASK (B11000000)
#define CMD_SHIFT 6
#define HALT (0x00)
#define LINEAR (0x01)
#define ARC (0x02)
#define ROTATE (0x03)
#define FW (0x1)
#define BW (0x0)
#define CW (0x1)
#define CCW (0x0)
#define WHEELBASE (4)
#define DIRECTION_MASK (0x01)
#define RADIUS_SHIFT (1)
#define MAX_SPEED (255)
#define ROTATION_MASK (0x1)
#define DIR_MASK (0x1)
#define DATA_SHIFT (2)
#define DATA_MASK (0x3E)

// Packet format:
// 7-6: Command
// 5-1: Data
// 0: Direction

AF_DCMotor motor_r(1);
AF_DCMotor motor_l(2);

byte input;
byte data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  motor_l.setSpeed(0);
  motor_r.setSpeed(0);
  motor_l.run(RELEASE);
  motor_r.run(RELEASE);
}

void loop() {
  /*
   *  Commands are received as a single byte, with the 2 msb identifying the
   *  command, and the remaining 6 bits being the command data
   */
  
  switch ((input & COMMAND_MASK) >> CMD_SHIFT) {
    case LINEAR:
      linear(data);
      break;
    case ARC:
      arc(data);
      break;
    case ROTATE:
      rotate(data);
      break;
    case HALT:
      halt(data);
      break;
    };
    //input = 0; 
    //data = 0;
}

void halt(byte data) {
  motor_l.setSpeed(0);
  motor_r.setSpeed(0);
  motor_l.run(RELEASE);
  motor_r.run(RELEASE);
}


byte capture_data(byte data) {
  return (data & DATA_MASK) << DATA_SHIFT;
}

/*
 * Drive the robot forward (0x1) or backward (0x0)
 */
void linear(byte data) {
  int dir;
  switch (data & DIR_MASK) {
    case FW:
      dir = FORWARD;
      break;
    case BW:
      dir = BACKWARD;
      break;
  }
  data = capture_data(data);
  motor_l.setSpeed(data);
  motor_r.setSpeed(data);
  motor_l.run(dir);
  motor_r.run(dir);
}
/*
 * Drive the robot forward or backward in a clockwise/counterclockwise arc
 */
void arc(byte data) {
  byte rotation = data & ROTATION_MASK;
  byte dir = data & 0x02 >> 1;
  byte radius = data >> RADIUS_SHIFT;
  byte outer = 255;
  int inner = ((double)((radius - WHEELBASE) / radius) * outer);
  switch (rotation) {
    case CW:
      motor_l.setSpeed(outer);
      motor_r.setSpeed(inner);
      break;
    case CCW:
      motor_l.setSpeed(inner);
      motor_r.setSpeed(outer);
      break;
  }
  if(dir) {
    motor_l.run(FORWARD);
    motor_r.run(FORWARD);
  }
  else {
    motor_l.run(BACKWARD);
    motor_r.run(BACKWARD);        
  }
}
/*
 * Rotate the robot in place clockwise (0x1) or counter clockwise (0x0)
 */
void rotate(byte data) {
  int dir_l, dir_r;
  switch (data & DIR_MASK) {
    case CW:
      dir_l = FORWARD;
      dir_r = BACKWARD;
      break;
    case CCW:
      dir_l = BACKWARD;
      dir_r = FORWARD;
      break;
  }
  data = capture_data(data);
  
  motor_l.setSpeed(data);
  motor_r.setSpeed(data);
  motor_l.run(dir_l);
  motor_r.run(dir_r);
}


void serialEvent() {
  input = Serial.read();
  data = input & ~COMMAND_MASK;
}

