CREATE TABLE User (
    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userEmail VARCHAR(80) NOT NULL,
	userPass VARCHAR(200),
	userRole VARCHAR(10),
	userGrade VARCHAR(10),
    schoolName VARCHAR(80),
    schoolCode VARCHAR(80) 
) ENGINE=INNODB;