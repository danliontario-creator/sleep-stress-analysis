CREATE DATABASE sleep_data;

CREATE TABLE sleep(
	id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    occupation VARCHAR(100),
    sleep_duration DECIMAL, 
    quality_of_sleep INT,
    Phyiscal_Activity_level INT,
    stress_level INT,
    bmi_category VARCHAR(100),
    blood_pressure VARCHAR(10),
    heart_rate INT,
    daily_Steps INT,
    sleep_disorder VARCHAR(50)
);

LOAD DATA LOCAL INFILE '/Users/danli/Documents/sleep/Sleep_health_and_lifestyle_dataset.csv'
INTO TABLE sleep
CHARACTER SET latin1
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS; 
    
ALTER TABLE sleep
ADD COLUMN systolic_bp INT AFTER blood_pressure,
ADD COLUMN diastolic_bp INT AFTER systolic_bp;


UPDATE sleep
SET 
  systolic_bp = CAST(SUBSTRING_INDEX(blood_pressure, '/', 1) AS UNSIGNED),
  diastolic_bp = CAST(SUBSTRING_INDEX(blood_pressure, '/', -1) AS UNSIGNED);

SELECT id, blood_pressure, systolic_bp, diastolic_bp FROM sleep LIMIT 10;

ALTER TABLE sleep
ADD COLUMN avg_bp INT;

SELECT * 
FROM sleep;



