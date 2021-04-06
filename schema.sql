drop table if exists users;
create table users (
    UserId  INTEGER primary key,
    UserName TEXT not null,
    Tateya TEXT not null,
    KouteiNo INTEGER not null,
    KouteiName TEXT not null
);
INSERT INTO users VALUES 
(1, '山田太郎', 'HQ26', 'P01M001', 'あああああああああ'),
(2, '山田次郎', 'HQ27', 'P01M002', 'いいいいいいいいい');

drop table if exists checklist;
create table checklist (
    Osno TEXT primary key,
    KouteiNo TEXT not null,
    ListRemakeFlag INTEGER not null,
    Result INTEGER default 0 not null,
    ErrMess TEXT,
    TotalCheckNum INTEGER,
    TotalRemainNum INTEGER,
    KouteiCheckNum INTEGER,
    KouteiRemainNum INTEGER,
    MismatchNum INTEGER
);
INSERT INTO checklist VALUES
('1', '0001', 0, 0, null, 11, 13, 15, 17, 21),
('2', '0002', 0, 1, 'error occurred', 21, 23, 25, 27, 21),
('3', '0003', 1, 0, null, 31, 33, 35, 37, 31),
('4', '0004', 1, 1, 'error occurred', 41, 43, 45, 47, 41);
