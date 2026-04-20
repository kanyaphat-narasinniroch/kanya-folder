set identity_insert LoyaltyProgramHistory on;

insert into LoyaltyProgramHistory(HistoryId, CustomerId, Action, Points, Timestamp)
select HistoryId, CustomerId, Action, Points, Timestamp
from loyalty_program_history
where Action <> 'Current Tier';

set identity_insert LoyaltyProgramHistory off;
