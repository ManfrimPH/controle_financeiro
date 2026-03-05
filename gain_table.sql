CREATE TABLE financeiro.gain (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	category varchar NULL,
	value varchar NULL,
	description varchar NULL,
	"date" timestamp NULL
);