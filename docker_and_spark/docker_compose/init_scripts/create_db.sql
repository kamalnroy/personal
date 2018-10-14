CREATE DATABASE IF NOT EXISTS db_twitter_insights;

USE db_twitter_insights;

CREATE TABLE IF NOT EXISTS tbl_trending_words (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, word VARCHAR(64) NOT NULL, num INT(6));

INSERT INTO tbl_trending_words (word, num) VALUES("Hi", 2);

