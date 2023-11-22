CREATE TABLE Question (
    question_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	author_email VARCHAR(200),
    subject_id VARCHAR(30),
	subject_name VARCHAR(100),
	category VARCHAR(10),
    content VARCHAR(300),
    created VARCHAR(30),
    updated VARCHAR(30),
    image_url VARCHAR(100),
    recognized_text VARCHAR(300),
    has_correct_answer VARCHAR(10) 
) ENGINE=INNODB;