-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema njtransit
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema njtransit
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `njtransit` DEFAULT CHARACTER SET utf8 ;
USE `njtransit` ;

-- -----------------------------------------------------
-- Table `njtransit`.`train_trip`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `njtransit`.`train_trip` ;

CREATE TABLE IF NOT EXISTS `njtransit`.`train_trip` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` CHAR(10) NULL,
  `train_id` VARCHAR(100) NULL,
  `stop_sequence` VARCHAR(100) NULL,
  `from` VARCHAR(255) NULL,
  `from_id` VARCHAR(100) NULL,
  `to` VARCHAR(255) NULL,
  `to_id` VARCHAR(100) NULL,
  `scheduled_time` VARCHAR(100) NULL,
  `actual_time` VARCHAR(100) NULL,
  `delay_minutes` VARCHAR(100) NULL,
  `status` VARCHAR(100) NULL,
  `line` VARCHAR(100) NULL,
  `type` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `njtransit`.`station`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `njtransit`.`station` ;

CREATE TABLE IF NOT EXISTS `njtransit`.`station` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `from` VARCHAR(255) NULL,
  `from_id` VARCHAR(100) NULL,
  `lat` VARCHAR(100) NULL,
  `lng` VARCHAR(100) NULL,
  `formatted_address` VARCHAR(255) NULL,
  `postal_code` CHAR(5) NULL,
  `response` JSON NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `njtransit`.`weather`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `njtransit`.`weather` ;

CREATE TABLE IF NOT EXISTS `njtransit`.`weather` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` CHAR(10) NULL,
  `time` CHAR(4) NULL,
  `postal_code` CHAR(5) NULL,
  `type` CHAR(1) NULL,
  `tempC` VARCHAR(25) NULL,
  `windspeedKmph` VARCHAR(25) NULL,
  `weatherCode` VARCHAR(25) NULL,
  `weatherDesc` VARCHAR(75) NULL,
  `humidity` VARCHAR(25) NULL,
  `HeatIndexC` VARCHAR(25) NULL,
  `DewPointC` VARCHAR(25) NULL,
  `WindChillC` VARCHAR(25) NULL,
  `WindGustKmph` VARCHAR(25) NULL,
  `uvIndex` VARCHAR(25) NULL,
  `response` JSON NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `njtransit`.`eventbrite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `njtransit`.`eventbrite` ;

CREATE TABLE IF NOT EXISTS `njtransit`.`eventbrite` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `station_id` INT NULL,
  `from` VARCHAR(255) NULL,
  `from_id` VARCHAR(100) NULL,
  `name` VARCHAR(255) NULL,
  `start_local` VARCHAR(100) NULL,
  `end_local` VARCHAR(100) NULL,
  `venue_name` VARCHAR(255) NULL,
  `venue_latitude` VARCHAR(100) NULL,
  `venue_longitude` VARCHAR(100) NULL,
  `response` JSON NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
