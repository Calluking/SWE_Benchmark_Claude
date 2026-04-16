Tool Usage & API Time per Run
Run	API Time	Total Calls
marshmallow-code__marshmallow-1343	122.9s	34
marshmallow-code__marshmallow-1359	268.5s	64
pvlib__pvlib-python-1072	157.0s	46
pvlib__pvlib-python-1606	160.1s	47
pvlib__pvlib-python-1707	154.2s	49
pvlib__pvlib-python-1854	233.7s	64
sqlfluff__sqlfluff-1517	677.8s	127
sqlfluff__sqlfluff-1733	952.7s	140
sqlfluff__sqlfluff-1763	367.1s	77
sqlfluff__sqlfluff-2419	185.6s	41
Tool Breakdown Detail
marshmallow-code__marshmallow-1343 (122.9s)

Bash: 20, Read: 9, Edit: 5
marshmallow-code__marshmallow-1359 (268.5s)

Bash: 54, Read: 8, Edit: 2
pvlib__pvlib-python-1072 (157.0s)

Bash: 30, Read: 10, Edit: 6
pvlib__pvlib-python-1606 (160.1s)

Bash: 31, Read: 11, Edit: 4, Monitor: 1
pvlib__pvlib-python-1707 (154.2s)

Bash: 24, Read: 12, Edit: 11, TaskOutput: 2
pvlib__pvlib-python-1854 (233.7s)

Bash: 42, Read: 15, Edit: 7
sqlfluff__sqlfluff-1517 (677.8s)

Bash: 79, Read: 24, Edit: 19, Write: 3, Grep: 1, TaskOutput: 1
sqlfluff__sqlfluff-1733 (952.7s)

Bash: 95, Edit: 26, Read: 17, Write: 1, TaskOutput: 1
sqlfluff__sqlfluff-1763 (367.1s)

Bash: 52, Read: 16, Edit: 5, TodoWrite: 4
sqlfluff__sqlfluff-2419 (185.6s)

Read: 18, Bash: 17, TaskOutput: 4, Write: 1, Edit: 1
Key Observations
Bash dominates in nearly every run (avg ~50% of all tool calls)
sqlfluff__sqlfluff-1733 had the highest API time (952.7s) and most tool calls (140)
sqlfluff__sqlfluff-2419 is unusual — Read outnumbered Bash, suggesting more exploration than execution

Token Usage
Run	Input Tokens	Output Tokens	Cache Read Tokens	Cache Creation Tokens	Cost (USD)
marshmallow-code__marshmallow-1343	282	8,621	1,491,605	87,582	$0.3020
marshmallow-code__marshmallow-1359	522	12,946	3,234,089	69,501	$0.4755
pvlib__pvlib-python-1072	378	13,686	2,420,951	44,858	$0.3670
pvlib__pvlib-python-1606	386	13,275	2,448,656	43,510	$0.3660
pvlib__pvlib-python-1707	402	12,984	2,620,766	56,900	$0.3985
pvlib__pvlib-python-1854	522	17,298	4,545,338	75,513	$0.6359
sqlfluff__sqlfluff-1517	1,026	38,875	9,296,954	88,368	$1.2356
sqlfluff__sqlfluff-1733	1,130	65,512	11,597,123	119,655	$1.6380
sqlfluff__sqlfluff-1763	626	19,899	4,688,472	56,507	$0.6396
sqlfluff__sqlfluff-2419	338	8,342	1,759,021	62,889	$0.2966