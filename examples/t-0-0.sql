use testing
create table t(idrow int identity(1, 1) primary key,data varchar(50))
insert t(data) values('some % value')
insert t(data) values('some %% value')
SELECT data FROM t
SELECT data FROM t WHERE data = 'some % value'
SELECT data FROM t WHERE data = 'some %% value'
