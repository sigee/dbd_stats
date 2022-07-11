create table user
(
	id integer not null constraint user_pk primary key autoincrement,
	username text not null,
	password text not null,
	email text
);

create unique index user_email_uindex on user (email);

create unique index user_id_uindex on user (id);

create unique index user_username_uindex on user (username);

CREATE TABLE `killer` (
	id integer not null constraint killer_pk primary key autoincrement,
	perk1 text not null,
	perk2 text not null,
	perk3 text not null,
	perk4 text not null,
	type text not null
);

create unique index killer_id_uindex on killer (id);

CREATE TABLE `survivor` (
	id integer not null constraint survivor_pk primary key autoincrement,
	escaped text
);

create unique index survivor_id_uindex on survivor (id);

CREATE TABLE `match` (
	id INTEGER not null constraint match_pk primary key autoincrement,
	killer INT not null constraint match_killer_id_fk references killer on update cascade on delete cascade,
	survivor1 INT not null constraint match_survivor1_id_fk references survivor on update cascade on delete cascade,
	survivor2 INT not null constraint match_survivor2_id_fk references survivor on update cascade on delete cascade,
	survivor3 INT not null constraint match_survivor3_id_fk references survivor on update cascade on delete cascade,
	survivor4 INT not null constraint match_survivor4_id_fk references survivor on update cascade on delete cascade
);

create unique index match_id_uindex on match (id);

create unique index match_killer_uindex on match (killer);

create unique index match_survivor1_uindex on match (survivor1);

create unique index match_survivor2_uindex on match (survivor2);

create unique index match_survivor3_uindex on match (survivor3);

create unique index match_survivor4_uindex on match (survivor4);
