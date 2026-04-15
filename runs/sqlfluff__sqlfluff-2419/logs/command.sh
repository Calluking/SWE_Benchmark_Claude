#!/usr/bin/env bash
claude -p --dangerously-skip-permissions --strict-mcp-config   --add-dir "/home/luzh22/jiuwenclaw/SWE_clean/runs/sqlfluff__sqlfluff-2419"   --output-format stream-json   --include-partial-messages   --include-hook-events   --verbose   --debug-file /home/luzh22/jiuwenclaw/SWE_clean/runs/sqlfluff__sqlfluff-2419/logs/claude_debug.log   --no-session-persistence   --name "sqlfluff__sqlfluff-2419"   "Read TASK.md in the current directory and complete the SWE-bench Lite task.
Use only built-in Claude Code tools. Work in the repo/ subdirectory.
Keep a careful log in your final response of what you changed and how tests went."
