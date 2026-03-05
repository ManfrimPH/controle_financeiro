CREATE TABLE financeiro.spent (
	id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
	category varchar NULL,
	payment_method varchar NULL,
	value varchar NULL,
	description varchar NULL,
	"date" timestamp NULL
);