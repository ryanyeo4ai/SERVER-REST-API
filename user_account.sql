CREATE TABLE Account (
    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userEmail VARCHAR(80) NOT NULL,
    userPoint int(11),
    userPaymentMethod VARCHAR(100),
    userAccountNo VARCHAR(100),
    userRank int(11),
	comments VARCHAR(200)
) ENGINE=INNODB;