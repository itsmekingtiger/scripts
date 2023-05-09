# Port range

Investigate using port in range.


```ps1
> pr 8000 9000
Protocol LocalPort ProcessName              Id Path                                                                                      State
-------- --------- -----------              -- ----                                                                                      -----
TCP           8888 simplest-oauth-client  5016 C:\Users\██████\AppData\Local\Temp\go-build3774291689\b001\exe\simplest-oauth-client.exe Listen
TCP           8380 StSess                13184 C:\Program Files\AhnLab\Safe Transaction\stsess.exe                                      Listen


> pr 8888

Protocol LocalPort ProcessName             Id Path                                                                                      State
-------- --------- -----------             -- ----                                                                                      -----
TCP           8888 simplest-oauth-client 5016 C:\Users\██████\AppData\Local\Temp\go-build3774291689\b001\exe\simplest-oauth-client.exe Listen
```