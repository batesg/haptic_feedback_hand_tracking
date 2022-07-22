/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "platform/mbed_thread.h"

#include <cstdio>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <string>

using namespace std;

// Initialise the digital pin LED1 as an output
DigitalOut led(LED1);
int mot_1_pos;
int mot_2_pos;
int mot_1_direction;
int mot_2_direction;

float motor_delay = 1.5;

DigitalOut mot1_pin1(p13);
DigitalOut mot1_pin2(p14);
DigitalOut mot1_pin3(p15);
DigitalOut mot1_pin4(p16);

DigitalOut mot2_pin1(p17);
DigitalOut mot2_pin2(p18);
DigitalOut mot2_pin3(p19);
DigitalOut mot2_pin4(p20);

Serial pc(USBTX, USBRX);

void motor_1_thread_clock();
void motor_1_thread_anticlock();

void motor_2_thread_clock();
void motor_2_thread_anticlock();

void motor_1_thread_clock() {
  mot1_pin1 = 1;
  mot1_pin2 = 0;
  mot1_pin3 = 0;
  mot1_pin4 = 1;
  osDelay(motor_delay);

  mot1_pin1 = 1;
  mot1_pin2 = 0;
  mot1_pin3 = 1;
  mot1_pin4 = 0;
  osDelay(motor_delay);

  mot1_pin1 = 0;
  mot1_pin2 = 1;
  mot1_pin3 = 1;
  mot1_pin4 = 0;
  osDelay(motor_delay);

  mot1_pin1 = 0;
  mot1_pin2 = 1;
  mot1_pin3 = 0;
  mot1_pin4 = 1;
  osDelay(motor_delay);
}

void motor_1_thread_anticlock() {
  mot1_pin1 = 0;
  mot1_pin2 = 1;
  mot1_pin3 = 0;
  mot1_pin4 = 1;
  osDelay(motor_delay);

  mot1_pin1 = 0;
  mot1_pin2 = 1;
  mot1_pin3 = 1;
  mot1_pin4 = 0;
  osDelay(motor_delay);

  mot1_pin1 = 1;
  mot1_pin2 = 0;
  mot1_pin3 = 1;
  mot1_pin4 = 0;
  osDelay(motor_delay);

  mot1_pin1 = 1;
  mot1_pin2 = 0;
  mot1_pin3 = 0;
  mot1_pin4 = 1;
  osDelay(motor_delay);
}

void motor_2_thread_clock() {
  mot2_pin1 = 1;
  mot2_pin2 = 0;
  mot2_pin3 = 0;
  mot2_pin4 = 1;
  osDelay(motor_delay);

  mot2_pin1 = 1;
  mot2_pin2 = 0;
  mot2_pin3 = 1;
  mot2_pin4 = 0;
  osDelay(motor_delay);

  mot2_pin1 = 0;
  mot2_pin2 = 1;
  mot2_pin3 = 1;
  mot2_pin4 = 0;
  osDelay(motor_delay);

  mot2_pin1 = 0;
  mot2_pin2 = 1;
  mot2_pin3 = 0;
  mot2_pin4 = 1;
  osDelay(motor_delay);
}

void motor_2_thread_anticlock() {
  mot2_pin1 = 0;
  mot2_pin2 = 1;
  mot2_pin3 = 0;
  mot2_pin4 = 1;
  osDelay(motor_delay);

  mot2_pin1 = 0;
  mot2_pin2 = 1;
  mot2_pin3 = 1;
  mot2_pin4 = 0;
  osDelay(motor_delay);

  mot2_pin1 = 1;
  mot2_pin2 = 0;
  mot2_pin3 = 1;
  mot2_pin4 = 0;
  osDelay(motor_delay);

  mot2_pin1 = 1;
  mot2_pin2 = 0;
  mot2_pin3 = 0;
  mot2_pin4 = 1;
  osDelay(motor_delay);
}

// if recieve ABC does motor 1 for clockwise, anti clockwise and stop
// if recieve XYZ does motor 2 for clockwise, anti clockwise and stop

char msg;
int main() {

  int cycles = 0;
  while (true) {
    osDelay(1);
    led = !led;
    if (pc.readable()) {

      msg = pc.getc(); // get the data

      // motor 1 go forwards
      if (msg == 'A') {
        mot_1_direction = 1;
      }
      // motor 1 go backwards
      else if (msg == 'B') {
        mot_1_direction = 2;
      }
      // stop motor 1
      else if (msg == 'C') {
        mot_1_direction = 0;
      }
      // reset the position of the motor
      else if (msg == 'D') {
        mot_1_pos = 0;
      }

      // motor 2 go forward
      else if (msg == 'X') {
        mot_2_direction = 1;
      }
      // motor 2 go backwards
      else if (msg == 'Y') {
        mot_2_direction = 2;
      }
      // stop motor 2
      else if (msg == 'Z') {
        mot_2_direction = 0;
      }
      // reset the position of the motor
      else if (msg == 'K') {
        mot_2_pos = 0;
      }
    }

    // control the motor 1 position
    if (mot_1_direction == 1) {
      motor_1_thread_clock();
      mot_1_pos = mot_1_pos + 1;
    } else if (mot_1_direction == 2) {
      motor_1_thread_anticlock();
      mot_1_pos = mot_1_pos - 1;
    } else {
    }

    // control the motor 2 position
    if (mot_2_direction == 1) {
      motor_2_thread_clock();
      mot_2_pos = mot_2_pos + 1;
    } else if (mot_2_direction == 2) {
      motor_2_thread_anticlock();
      mot_2_pos = mot_2_pos - 1;
    } else {
    }
    if (cycles == 10) {
      pc.printf("X, %d, \n", mot_1_pos);
      pc.printf("Y, %d, \n", mot_2_pos);
      cycles = 0;
    } else {
      cycles = cycles + 1;
    }
  }
}
