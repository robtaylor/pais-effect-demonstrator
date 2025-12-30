/*
 * Pais Effect Demonstrator - Data Acquisition
 * 
 * Reads 3× HMC5883L magnetometers via TCA9548A multiplexer
 * Logs to SD card and streams via Serial
 * 
 * Hardware:
 *   - Arduino Due (84 MHz, 12-bit ADC)
 *   - TCA9548A I²C Multiplexer
 *   - 3× HMC5883L Magnetometers
 *   - ADXL345 Accelerometer
 *   - SD Card Module
 * 
 * Wiring:
 *   - SDA (20) -> TCA9548A SDA
 *   - SCL (21) -> TCA9548A SCL
 *   - Pin 4 -> SD Card CS
 *   - Sensors connect to TCA9548A channels 0, 1, 2
 * 
 * License: MIT
 */

#include <Wire.h>
#include <SD.h>
#include <SPI.h>

// ===== CONFIGURATION =====
#define SAMPLE_RATE_HZ    100     // Target sample rate
#define SD_CS_PIN         4       // SD card chip select
#define MUX_ADDRESS       0x70    // TCA9548A I²C address
#define HMC_ADDRESS       0x1E    // HMC5883L I²C address
#define ADXL_ADDRESS      0x53    // ADXL345 I²C address
#define SERIAL_BAUD       115200
#define BUFFER_SIZE       512     // SD write buffer

// ===== GLOBAL VARIABLES =====
File logFile;
char filename[13];
uint32_t sampleCount = 0;
uint32_t lastSampleMicros = 0;
uint32_t sampleIntervalMicros;

// Sensor data structure
struct SensorData {
    uint32_t timestamp_us;
    int16_t mag1_x, mag1_y, mag1_z;
    int16_t mag2_x, mag2_y, mag2_z;
    int16_t mag3_x, mag3_y, mag3_z;
    int16_t acc_x, acc_y, acc_z;
};

SensorData currentData;
char sdBuffer[BUFFER_SIZE];
int bufferPos = 0;

// ===== FUNCTION PROTOTYPES =====
void selectMuxChannel(uint8_t channel);
bool initHMC5883L();
bool initADXL345();
void readHMC5883L(int16_t* x, int16_t* y, int16_t* z);
void readADXL345(int16_t* x, int16_t* y, int16_t* z);
void createNewLogFile();
void writeDataToSD();
void sendDataSerial();

// ===== SETUP =====
void setup() {
    // Initialize serial
    Serial.begin(SERIAL_BAUD);
    while (!Serial && millis() < 3000); // Wait up to 3s for Serial
    
    Serial.println(F("=== Pais Effect Demonstrator DAQ ==="));
    Serial.println(F("Initializing..."));
    
    // Initialize I²C
    Wire.begin();
    Wire.setClock(400000); // 400 kHz I²C
    
    // Calculate sample interval
    sampleIntervalMicros = 1000000 / SAMPLE_RATE_HZ;
    
    // Initialize sensors
    Serial.print(F("Initializing magnetometers... "));
    bool sensorsOK = true;
    
    for (uint8_t ch = 0; ch < 3; ch++) {
        selectMuxChannel(ch);
        delay(10);
        if (!initHMC5883L()) {
            Serial.print(F("FAIL on channel "));
            Serial.println(ch);
            sensorsOK = false;
        }
    }
    
    if (sensorsOK) {
        Serial.println(F("OK"));
    }
    
    // Initialize accelerometer (on main bus or channel 3)
    Serial.print(F("Initializing accelerometer... "));
    selectMuxChannel(7); // Use unused channel to access main bus
    if (initADXL345()) {
        Serial.println(F("OK"));
    } else {
        Serial.println(F("FAIL"));
    }
    
    // Initialize SD card
    Serial.print(F("Initializing SD card... "));
    if (SD.begin(SD_CS_PIN)) {
        Serial.println(F("OK"));
        createNewLogFile();
    } else {
        Serial.println(F("FAIL - continuing without logging"));
    }
    
    Serial.println(F("Initialization complete."));
    Serial.print(F("Sample rate: "));
    Serial.print(SAMPLE_RATE_HZ);
    Serial.println(F(" Hz"));
    Serial.println(F(""));
    Serial.println(F("timestamp_us,m1x,m1y,m1z,m2x,m2y,m2z,m3x,m3y,m3z,ax,ay,az"));
    
    lastSampleMicros = micros();
}

// ===== MAIN LOOP =====
void loop() {
    uint32_t now = micros();
    
    // Check if it's time for next sample
    if (now - lastSampleMicros >= sampleIntervalMicros) {
        lastSampleMicros = now;
        
        // Record timestamp
        currentData.timestamp_us = now;
        
        // Read magnetometer 1
        selectMuxChannel(0);
        readHMC5883L(&currentData.mag1_x, &currentData.mag1_y, &currentData.mag1_z);
        
        // Read magnetometer 2
        selectMuxChannel(1);
        readHMC5883L(&currentData.mag2_x, &currentData.mag2_y, &currentData.mag2_z);
        
        // Read magnetometer 3
        selectMuxChannel(2);
        readHMC5883L(&currentData.mag3_x, &currentData.mag3_y, &currentData.mag3_z);
        
        // Read accelerometer
        readADXL345(&currentData.acc_x, &currentData.acc_y, &currentData.acc_z);
        
        // Output data
        sendDataSerial();
        writeDataToSD();
        
        sampleCount++;
    }
}

// ===== I²C MULTIPLEXER =====
void selectMuxChannel(uint8_t channel) {
    if (channel > 7) return;
    Wire.beginTransmission(MUX_ADDRESS);
    Wire.write(1 << channel);
    Wire.endTransmission();
}

// ===== HMC5883L FUNCTIONS =====
bool initHMC5883L() {
    // Check WHO_AM_I
    Wire.beginTransmission(HMC_ADDRESS);
    Wire.write(0x0A); // ID register A
    Wire.endTransmission();
    Wire.requestFrom(HMC_ADDRESS, 3);
    
    if (Wire.available() < 3) return false;
    
    char id[3];
    id[0] = Wire.read();
    id[1] = Wire.read();
    id[2] = Wire.read();
    
    if (id[0] != 'H' || id[1] != '4' || id[2] != '3') {
        return false;
    }
    
    // Configure: 8 samples averaged, 75 Hz, normal measurement
    Wire.beginTransmission(HMC_ADDRESS);
    Wire.write(0x00); // Config Register A
    Wire.write(0x78); // 8 samples, 75 Hz, normal
    Wire.endTransmission();
    
    // Set gain to ±1.3 Gauss (1090 LSB/Gauss)
    Wire.beginTransmission(HMC_ADDRESS);
    Wire.write(0x01); // Config Register B
    Wire.write(0x20); // Gain = 1
    Wire.endTransmission();
    
    // Continuous measurement mode
    Wire.beginTransmission(HMC_ADDRESS);
    Wire.write(0x02); // Mode Register
    Wire.write(0x00); // Continuous
    Wire.endTransmission();
    
    delay(10);
    return true;
}

void readHMC5883L(int16_t* x, int16_t* y, int16_t* z) {
    Wire.beginTransmission(HMC_ADDRESS);
    Wire.write(0x03); // Start at data register
    Wire.endTransmission();
    
    Wire.requestFrom(HMC_ADDRESS, 6);
    
    if (Wire.available() >= 6) {
        // Data order: X_MSB, X_LSB, Z_MSB, Z_LSB, Y_MSB, Y_LSB
        *x = (Wire.read() << 8) | Wire.read();
        *z = (Wire.read() << 8) | Wire.read();
        *y = (Wire.read() << 8) | Wire.read();
    } else {
        *x = *y = *z = 0;
    }
}

// ===== ADXL345 FUNCTIONS =====
bool initADXL345() {
    // Check device ID
    Wire.beginTransmission(ADXL_ADDRESS);
    Wire.write(0x00); // DEVID register
    Wire.endTransmission();
    Wire.requestFrom(ADXL_ADDRESS, 1);
    
    if (Wire.available() < 1) return false;
    if (Wire.read() != 0xE5) return false;
    
    // Set data format: full resolution, ±16g
    Wire.beginTransmission(ADXL_ADDRESS);
    Wire.write(0x31); // DATA_FORMAT
    Wire.write(0x0B); // Full resolution, ±16g
    Wire.endTransmission();
    
    // Set data rate: 100 Hz
    Wire.beginTransmission(ADXL_ADDRESS);
    Wire.write(0x2C); // BW_RATE
    Wire.write(0x0A); // 100 Hz
    Wire.endTransmission();
    
    // Enable measurement
    Wire.beginTransmission(ADXL_ADDRESS);
    Wire.write(0x2D); // POWER_CTL
    Wire.write(0x08); // Measure bit
    Wire.endTransmission();
    
    delay(10);
    return true;
}

void readADXL345(int16_t* x, int16_t* y, int16_t* z) {
    Wire.beginTransmission(ADXL_ADDRESS);
    Wire.write(0x32); // Start at DATAX0
    Wire.endTransmission();
    
    Wire.requestFrom(ADXL_ADDRESS, 6);
    
    if (Wire.available() >= 6) {
        *x = Wire.read() | (Wire.read() << 8);
        *y = Wire.read() | (Wire.read() << 8);
        *z = Wire.read() | (Wire.read() << 8);
    } else {
        *x = *y = *z = 0;
    }
}

// ===== SD CARD FUNCTIONS =====
void createNewLogFile() {
    // Find next available filename
    for (int i = 0; i < 1000; i++) {
        sprintf(filename, "LOG%03d.CSV", i);
        if (!SD.exists(filename)) {
            break;
        }
    }
    
    logFile = SD.open(filename, FILE_WRITE);
    if (logFile) {
        // Write header
        logFile.println(F("timestamp_us,m1x,m1y,m1z,m2x,m2y,m2z,m3x,m3y,m3z,ax,ay,az"));
        logFile.flush();
        Serial.print(F("Logging to: "));
        Serial.println(filename);
    }
}

void writeDataToSD() {
    if (!logFile) return;
    
    // Format data line
    int len = snprintf(sdBuffer + bufferPos, BUFFER_SIZE - bufferPos,
        "%lu,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
        currentData.timestamp_us,
        currentData.mag1_x, currentData.mag1_y, currentData.mag1_z,
        currentData.mag2_x, currentData.mag2_y, currentData.mag2_z,
        currentData.mag3_x, currentData.mag3_y, currentData.mag3_z,
        currentData.acc_x, currentData.acc_y, currentData.acc_z);
    
    bufferPos += len;
    
    // Write buffer when nearly full
    if (bufferPos > BUFFER_SIZE - 100) {
        logFile.write(sdBuffer, bufferPos);
        logFile.flush();
        bufferPos = 0;
    }
}

// ===== SERIAL OUTPUT =====
void sendDataSerial() {
    Serial.print(currentData.timestamp_us);
    Serial.print(',');
    Serial.print(currentData.mag1_x); Serial.print(',');
    Serial.print(currentData.mag1_y); Serial.print(',');
    Serial.print(currentData.mag1_z); Serial.print(',');
    Serial.print(currentData.mag2_x); Serial.print(',');
    Serial.print(currentData.mag2_y); Serial.print(',');
    Serial.print(currentData.mag2_z); Serial.print(',');
    Serial.print(currentData.mag3_x); Serial.print(',');
    Serial.print(currentData.mag3_y); Serial.print(',');
    Serial.print(currentData.mag3_z); Serial.print(',');
    Serial.print(currentData.acc_x); Serial.print(',');
    Serial.print(currentData.acc_y); Serial.print(',');
    Serial.println(currentData.acc_z);
}
