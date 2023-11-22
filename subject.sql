CREATE TABLE Subject (
    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    subject_id VARCHAR(20) NOT NULL,
	subject_name VARCHAR(20),
    category VARCHAR(20),
	subject_reward VARCHAR(10)
) ENGINE=INNODB;

INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('sat','SAT','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('act','ACT','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('middle-math','Middle Math','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('algebra-1','Algebra 1','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('algebra-2','Algebra 2','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('geometry','Geometry','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('pre-calculus','Pre calculus','Math','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ap-calculus','AP calculus','Math','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ap-statistics','AP statistics','Math','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ib-math','IB math','Math','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('multi-variables','Multi variables','Math','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('biology','Biology','Science','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ap-biology','AP biology','Science','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ib-biology','IB biology','Science','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('chemistry','Chemistry','Science','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ap-chemistry','AP chemistry','Science','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ib-chemistry','IB chemistry','Science','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('physics','Physics','Science','0.25');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ap-physic','AP physics','Science','0.5');
INSERT INTO Subject (subject_id, subject_name, category, subject_reward) values('ib-physics','IB physics','Science','0.5');