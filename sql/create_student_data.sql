-- ************************
-- create_student_data.sql
--
-- Script for student_data table
-- This table holds student data crawled from SIS
--
-- Author: duccuong
--
-- ************************

CREATE TABLE student_data
(
	id INT NOT NULL PRIMARY KEY,
	last_name CHARACTER VARYING(20) NOT NULL,
	middle_name CHARACTER VARYING(30),
	first_name CHARACTER VARYING(20) NOT NULL,
	birth_date DATE NOT NULL,
	class CHARACTER VARYING(50),
	program CHARACTER VARYING(100),
	status SMALLINT NOT NULL,
	cohort SMALLINT NOT NULL
);