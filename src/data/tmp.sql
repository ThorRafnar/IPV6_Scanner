select *
from adresses A
join associationtable T
	on A.ID = T.addressID
where exists (
	select *
	from ports P
	where P.ID = T.port
	and P.ID = $port1
)
intersect
select *
from adresses A
join associationtable T
        on A.ID = T.addressID
where exists (
        select *
        from ports P
        where P.ID = T.port
        and P.ID = $port2
);

