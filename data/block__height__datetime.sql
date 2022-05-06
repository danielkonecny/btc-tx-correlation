create table block__height__datetime
(
    block_height serial
        primary key,
    block_time   integer not null
);

alter table block__height__datetime owner to test;
