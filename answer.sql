CREATE TABLE Answer (
    answer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    question_id VARCHAR(100),
	author_email VARCHAR(200),
	content VARCHAR(300),
    selected VARCHAR(10),
    created VARCHAR(30),
    updated VARCHAR(30),
    image_url VARCHAR(100),
    recognized_text VARCHAR(300)
) ENGINE=INNODB;