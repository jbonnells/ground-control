# Ground Control System

## Instructions to Operate  

Upon initialization, the FSW is in restarting mode and is unable to accept any incoming commands. Once 10 seconds have elapsed, the FSW switches to the ready state and can start processing incoming commands.  

When in the ready state, it is expected to answer all commands as sent by the GCS. After 5 subsequent wrong commands sent by the GCS, the FSW shall switch to safe mode. After 3 more subsequent wrong commands, the system shall switch to BBQ mode.  

Below are the nominal FSW states, and a brief description for each. 

### FSW States
| State | Description | 
| --- | --- |
| RESTARTING | Initialization state while the FSW starts up. |
| READY | FSW is ready to accept commands. |
| SAFE_MODE | 5 subsequent wrong commands sent by the GCS. |
| BBQ_MODE | 3 more subsequent wrong commands after entering SAFE_MODE. |
  
Below are the available commands, how they should work, and when they should work (some commands are disabled when the FSW is in safe mode or BBQ mode, or both). To interact with the FSW, input the desired command, either by ID or name (case sensitive), and hit enter to send it to the running instance.

### Available Commands
| ID | Command | Description |
| -------- | ------- | ------- |
| 1 | SAFE_MODE_ENABLE | Will switch the FSW to safe mode. This command is invalid when in BBQ mode or in safe mode. |
| 2 | SAFE_MODE_DISABLE | Will switch the FSW back to the ready state. This command is always valid. |
| 3 | SHOW_CMDS_RCVD | Will return the total number of valid commands received since startup of the FSW. This command is invalid when in BBQ mode or in safe mode. |
| 4 | SHOW_NUM_SAFES | Will return the number of times the FSW has switched to safe mode since startup. This command is invalid when in BBQ mode. |
| 5 | SHOW_UPTIME | Will return the number of seconds since the FSW was started. This command is invalid when in BBQ mode or in safe mode. |
| 6 | RESET_CMD_CNTR | Will reset the command counter to zero and then return the number of commands received (i.e. zero). This command is invalid when in BBQ mode or in safe mode. |
| 7 | SHUTDOWN | Will return the state of the FSW, close the socket and stop the process. This command is always valid. |