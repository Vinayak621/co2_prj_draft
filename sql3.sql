create database offset;
use offset;
create table cars_11(

    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    fuel_type VARCHAR(255) NOT NULL,
    fuel_consumption_comb_mpg INT NOT NULL,
    co2_emissions DECIMAL(6,2) NOT NULL
);
select *from cars_11;
show tables;



 SELECT DISTINCT model FROM cars_11 WHERE make = "AUDI" ORDER BY model;