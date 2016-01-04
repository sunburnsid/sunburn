drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  month text not null,
  day integer not null,
  year integer not null
);