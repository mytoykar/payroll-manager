CREATE TABLE employees (
	id SERIAL PRIMARY KEY,
	name VARCHAR ( 50 ) NOT NULL,
	birthdate DATE NOT NULL,
	tin VARCHAR ( 50 ) NOT NULL,
	employee_type VARCHAR ( 20 ) NOT NULL,
	basic_rate FLOAT,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	is_deleted BOOL
);